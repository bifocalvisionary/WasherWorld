import os

import psycopg2
import logging
import time


class Room:
    def __int__(self, RoomID, RoomName, RoomUser):
        self.RoomID = RoomID
        self.RoomName = RoomName
        self.RoomUser = RoomUser
    def __str__(self):
        return "[", self.RoomID , "," , self.RoomName, "]"


class User:
    def __int__(self, UserName, Phone, Email, PreferredMode):
        self.UserName = UserName
        self.Phone = Phone
        self.Email = Email
        self.PreferredMode = PreferredMode


class Machine:
    def __int__(self, MachineID, Status, Timer, MachineType, RoomID, ActiveUser):
        self.MachineID = MachineID
        self.Status = Status
        self.Timer = Timer
        self.MachineType = MachineType
        self.RoomID = RoomID
        self.ActiveUser = ActiveUser


class Review:
    def __int__(self, ReviewID, Ranking, TimeSubmitted, WrittenReview, MachineID, RoomID):
        self.ReviewID = ReviewID
        self.Ranking = Ranking
        self.TimeSubmitted = TimeSubmitted
        self.WrittenReview = WrittenReview
        self.MachineID = MachineID
        self.RoomID = RoomID


# Examples of stuff
def create_accounts(conn):
    with conn.cursor() as cur:
        #cur.execute("INSERT INTO washerWorld.Room (RoomID, RoomName) VALUES (2, 'Elingson')")
        cur.execute("SELECT * FROM washerworld.Room")
        from_balance = cur.fetchall()
        print(from_balance)
        logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()


# Creates a new room (must have unique id)
def create_room(conn, id, name, user):
    print("Creating room of id", id, "with name", name)
    new_room = Room()
    new_room.RoomID = id
    new_room.RoomName = name
    new_room.RoomUser = user
    cmd = "INSERT INTO washerWorld.Room (RoomID, RoomName, RoomOwner) VALUES (" + str(new_room.RoomID) + ",'" +\
        str(new_room.RoomName) + "','" + str(new_room.RoomUser) + "')"
    print(cmd)
    with conn.cursor() as cur:
        cur.execute(cmd)
    conn.commit()
    return new_room


# Creates a new user (must have unique username)
def create_user(conn, username, phoneNum, email, preference):
    print("Creating user with username", username)
    new_user = User()
    new_user.UserName = username
    new_user.Phone = phoneNum
    new_user.Email = email
    new_user.PreferredMode = preference
    cmd = "INSERT INTO washerWorld.User (UserName, Phone, Email, PreferredMode) VALUES ('" + str(new_user.UserName) + \
          "','" + str(new_user.Phone) + "','" + str(new_user.Email) + "','" + str(new_user.PreferredMode) + "');"
    print(cmd)
    with conn.cursor() as cur:
        cur.execute(cmd)
    conn.commit()
    return new_user


# Creates a new machine (must have unique id)
def create_machine(conn, id, stat, timer, type, roomID):
    print("Creating machine of id", id, "in room", roomID)
    new_machine = Machine()
    new_machine.MachineID = id
    new_machine.Status = stat
    new_machine.Timer = timer
    new_machine.MachineType = type
    new_machine.RoomID = roomID
    cmd = "INSERT INTO washerWorld.Machine (MachineID, Status, Timer, MachineType, RoomID) VALUES (" +\
        str(new_machine.MachineID) + ",'" + str(new_machine.Status) + "'," + str(new_machine.Timer) +\
        ",'" + str(new_machine.MachineType) + "', " + str(new_machine.RoomID) + ");"
    print(cmd)
    with conn.cursor() as cur:
        cur.execute(cmd)
    conn.commit()
    return new_machine


# Creates a new review (must have unique id)
def create_review(conn, id, rank, time, writing, machineID, roomID):
    print("Creating review of machine", machineID, "in room", roomID)
    new_review = Review()
    new_review.ReviewID = id
    new_review.Ranking = rank
    new_review.TimeSubmitted = time
    new_review.WrittenReview = writing
    new_review.MachineID = machineID
    new_review.RoomID = roomID
    cmd = "INSERT INTO washerWorld.Review (ReviewID, Ranking, TimeSubmitted, WrittenReview, MachineID, RoomID) VALUES (" +\
        str(new_review.ReviewID) + "," + str(new_review.Ranking) + "," + str(new_review.TimeSubmitted) +\
        ",'" + str(new_review.WrittenReview) + "'," + str(new_review.MachineID) + "," + str(new_review.RoomID) + ");"
    #print(cmd)
    with conn.cursor() as cur:
        cur.execute(cmd)
    conn.commit()
    return new_review


# get all machines in specified room
def get_machines_in_room(conn, roomID):
    cmd = "SELECT * FROM washerworld.machine WHERE RoomID = " + str(roomID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_room = cur.fetchall()
    conn.commit()
    return the_room


# get room entry from RoomID
def get_entry_room(conn, roomID):
    cmd = "SELECT * FROM washerworld.room WHERE RoomID = " + str(roomID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_room = cur.fetchall()
    conn.commit()
    return the_room


# get user info from UserName
def get_entry_user(conn, name):
    cmd = "SELECT * FROM washerworld.User WHERE UserName = '" + str(name) + "';"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_guy = cur.fetchall()
    conn.commit()
    return the_guy


# get room entry from machineID
def get_entry_machine(conn, machineID):
    cmd = "SELECT * FROM washerworld.machine WHERE MachineID = " + str(machineID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_machine = cur.fetchall()
    conn.commit()
    return the_machine


# get room entry from reviewID
def get_entry_review(conn, reviewID):
    cmd = "SELECT * FROM washerworld.review WHERE ReviewID = " + str(reviewID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_review = cur.fetchall()
    conn.commit()
    return the_review


# get all entries of table room
def list_all_rooms(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM washerworld.room")
        output = cur.fetchall()
    conn.commit()
    return output


# get all entries of table machine
def list_all_machines(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM washerworld.machine")
        output = cur.fetchall()
    conn.commit()
    return output


# get all entries of table review
def list_all_reviews(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM washerworld.review")
        output = cur.fetchall()
    conn.commit()
    return output


# get all entries of table user
def list_all_users(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM washerworld.user")
        output = cur.fetchall()
    conn.commit()
    return output


# Update machine state
def change_state_of_machine(conn, machineID, state):
    cmd = "UPDATE washerworld.machine SET status='" + str(state) + "' WHERE MachineID=" + str(machineID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
    conn.commit()


# Restarts the database with empty tables.
def restart_setup(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE washerWorld.Room (RoomID INT PRIMARY KEY NOT NULL, RoomName STRING, RoomOwner STRING);")
        cur.execute("CREATE TABLE washerWorld.User (UserName STRING PRIMARY KEY NOT NULL, Phone STRING, Email STRING, PreferredMode STRING);")
        cur.execute("CREATE TABLE washerWorld.Machine (MachineID INT PRIMARY KEY NOT NULL, Status STRING, Timer INT, MachineType STRING, RoomID INT REFERENCES washerWorld.Room(RoomID) ON DELETE CASCADE, ActiveUser STRING REFERENCES washerWorld.User(UserName));")
        cur.execute("CREATE TABLE washerWorld.Review (ReviewID INT PRIMARY KEY NOT NULL, Ranking INT, TimeSubmitted TIMESTAMPTZ, WrittenReview STRING, MachineID INT REFERENCES washerWorld.Machine(MachineID) ON DELETE CASCADE, RoomID INT REFERENCES washerWorld.Room(RoomID) ON DELETE CASCADE); ")
    conn.commit()


# Wipes all tables and entries completely by dropping them all.
def wipe_setup(conn):
    with conn.cursor() as cur:
        print("DROPPING PREVIOUS TABLES...")
        cur.execute("DROP TABLE IF EXISTS washerWorld.Room CASCADE")
        cur.execute("DROP TABLE IF EXISTS washerWorld.Machine CASCADE")
        cur.execute("DROP TABLE IF EXISTS washerWorld.Review CASCADE")
        cur.execute("DROP TABLE IF EXISTS washerWorld.User CASCADE")
        time.sleep(5)
        print("Database resetting, please hold...")
        # needs a lot of time to process
        time.sleep(60)
    conn.commit()


def load_database():
    conn = psycopg2.connect(
        database='defaultdb',
        user='cameron',
        password=os.environ["DB_PW"],
        sslmode='verify-full',
        port=26257,
        host='free-tier11.gcp-us-east1.cockroachlabs.cloud',
        options='--cluster=stung-whale-219'
    )
    return conn


# Example of how to use the commands + the connection piece
if __name__ == '__main__':
    conn = psycopg2.connect(
        database='defaultdb',
        user='cameron',
        password=os.environ["DB_PW"],
        sslmode='verify-full',
        port=26257,
        host='free-tier11.gcp-us-east1.cockroachlabs.cloud',
        options='--cluster=stung-whale-219'
    )
    #print(get_machines_in_room(conn, 1))
    #restart_setup(conn)
    #room = create_room(conn, 2, "Sol", "Hendrick")
    #room = create_room(conn, 1, "Elingson", "Cameron")
    #user = create_user(conn, "Cameron", "(555)555-5555", "biff@boff.gorp", "TEXT")
    #user = create_user(conn, "Hendrick", "(123)456-7890", "boof@bop.gorp", "EMAIL")
    #machine = create_machine(conn, 1, "OPEN", 52, "WASHER", 1)
    #review_ex = create_review(conn, 1, 5, "TIMESTAMPTZ '2016-03-26 10:10:10-05:00'", 'pretty cool', 1, 1)
    #machine = create_machine(conn, 2, "USED", 13, "DRYER", 2)
    #review_ex = create_review(conn, 2, 3, "TIMESTAMPTZ '2016-03-26 10:10:10-05:00'", 'pretty cool', 1, 1)
    #print(get_entry_room(conn, 2))
    #print(get_entry_machine(conn,1))
    #print(get_entry_review(conn,1))
    #print(get_entry_user(conn,"Cameron"))
    #print(list_all_rooms(conn))
    #print(list_all_machines(conn))
    #print(list_all_reviews(conn))
    #print(list_all_users(conn))
    #change_state_of_machine(conn, 1, "BROKEN")


