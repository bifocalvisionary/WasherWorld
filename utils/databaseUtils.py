from _sha256 import sha256
from bson import ObjectId
#from google.cloud import storage
import pymongo as pymongo
import base64
import gridfs

client = pymongo.MongoClient("mongodb+srv://admin:pass@thecommunityproject-lawyq.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.Users
users = db.users
posts = db.posts
reports = db.reports
fs = gridfs.GridFS(db)

"""
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

    return "https://storage.cloud.google.com/communityproject-images/" + destination_blob_name
"""


# creates a user in the database with a username, password, and post id
def create_user(username, password):
    if get_user_by_name(username) is None:
        user = users.insert_one({
            "username": username,
            "password": hash_password(username, password),
            "postId": []})
        return user.inserted_id
    return None


# gets the username of a user
def get_user_by_name(username):
    return users.find_one({"username": username})


# gets the id of a user
def get_user_by_id(userid):
    return users.find_one({"_id": ObjectId(userid)})


# constructs the value for a password key
def hash_password(username, password):
    return sha256(str(username+password).encode('utf-8')).hexdigest()


# provides the information needed for a user to sign in
def authenticate(username, password):
    user = get_user_by_name(username)
    if user is None:
        return
    if hash_password(username, password) != user["password"]:
        return
    return user["_id"]


# adds a new report to the database
def add_report(report):
    (print(report))
    reports.insert_one({"description": report})


# upgrades a normal user to an admin
def user_admin(userid):
    return None


# returns a picture (image file)
def get_picture(picture):
    return fs.get(picture).read()
