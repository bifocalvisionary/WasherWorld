import base64
import os
from datetime import timedelta
from functools import wraps
from random import randint

from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_bootstrap import Bootstrap
from twilio.twiml.messaging_response import MessagingResponse
from werkzeug.urls import url_encode


# from utils import databaseUtils
from utils import cockroachdbUtils, washerUtils
# from utils import databaseUtils, twilioUtils
#from utils import twilioUtils


UPLOAD_FOLDER = "static/"
ROOMS = washerUtils.import_rooms_from_database()
conn = cockroachdbUtils.load_database()


def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to create create a room!")
            return redirect(url_for("login"))
        else:
            return f(*args, **kwargs)

    return inner


app = Flask(__name__)
app.secret_key = os.urandom(16)
Bootstrap(app)


@app.template_global()
def modify_query(origin, **new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(origin, url_encode(args))


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/joinModal', methods=['GET', 'POST'])
def joinModal():
    ID = request.form.get('roomID')
    session['roomID'] = ID
    print(ID)
    print(request.form.keys())
    return redirect("/join_room")


@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    return render_template("join_room.html", roomID=session["roomID"],
                           washers=cockroachdbUtils.get_machines_in_room(conn, session["roomID"]))


@app.route('/useMachine', methods=['GET', 'POST'])
def useMachine():
    ID = request.form.get('washerid')
    session['washerid'] = ID
    cockroachdbUtils.change_state_of_machine(conn, ID, "RUNNING")
    #TODO: TEXT WHEN DONE
    phone_num = request.form.get('phone')
    return redirect("/join_room")


@app.route('/report', methods=['GET', 'POST'])
def report():
    ID = request.form.get('washerid')
    session['washerid'] = ID
    cockroachdbUtils.change_state_of_machine(conn, ID, 'BROKEN')
    return redirect("/join_room")


@app.route('/report_fix', methods=['GET', 'POST'])
def report_fix():
    ID = request.form.get('washerid1')
    session['washerid1'] = ID
    cockroachdbUtils.change_state_of_machine(conn, ID, 'OPEN')
    return redirect("/join_room")


@app.route("/create_room")
@require_login
def create_room():
    return render_template("create_room.html")


@app.route("/report_button", methods=["POST"])
def report_button():
    flash("Thank you for your support!")
    # temp = databaseUtils.add_report(request.form['report'])
    return redirect('/report')


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login'))


@app.route('/sms', methods=["GET", "POST"])
def sms():

	message = twilioUtils.receive_sms_message(request)
	room, machine = message.strip().split(" ")

	if not (room and machine):
		resp = MessagingResponse()
		resp.message("Please Enter your input in the format (Room# Machine#")
		return str(resp)

	room = int(room.strip())
	machine = int(machine.strip())

	resp = MessagingResponse()
	reply = "You have reserved machine " + str(machine) + " in room " + str(room) 

	resp.message(reply)

	return str(resp)

"""
#If Uploading Images Is Required
@app.route("/imgUP", methods=["POST"])
def imgUP():
    print("Uploading")
    data = request.form["url"]
    encoded_data = data.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)
    filename = "imgs/" + str(randint(0, 999999999999)) + ".png"
    print(filename)
    filepath = UPLOAD_FOLDER + filename
    f = open(filepath, "wb")
    f.write(decoded_data)
    f.close()
    url = databaseUtils.upload_blob("communityproject-images", filepath, str(randint(0, 999999999999)))
    session['img_url'] = url
    return redirect(url_for("createpost", img_url=url))
"""

"""
@app.route("/auth", methods=["POST"])
def auth():
    if "submit" not in request.form or "user" not in request.form or "pwd" not in request.form:
        flash("At least one form input was incorrect")
        return redirect(url_for('login'))

    if request.form['submit'] == 'Login':
        user = databaseUtils.authenticate(request.form['user'], request.form['pwd'])
        if user:
            session['user'] = str(user)
            session['username'] = databaseUtils.get_user_by_id(user)['username']
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for('root'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
    else:
        success = databaseUtils.create_user(request.form['user'], request.form['pwd'])
        if (success):
            session['user'] = str(success)
            session['username'] = databaseUtils.get_user_by_id(success)['username']
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for('root'))
        else:
            flash('This username already exists!')
            return redirect(url_for('login'))
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0')
