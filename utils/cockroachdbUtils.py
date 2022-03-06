import psycopg2
import logging
import time


class Room:
    def __int__(self, RoomID, RoomName):
        self.RoomID = RoomID
        self.RoomName = RoomName

    def __str__(self):
        return "[", RoomID , "," , RoomName, "]"


class Machine:
    def __int__(self, MachineID, Status, Timer, MachineType, RoomID):
        self.MachineID = MachineID
        self.Status = Status
        self.Timer = Timer
        self.MachineType = MachineType
        self.RoomID = RoomID


class Review:
    def __int__(self, ReviewID, Ranking, TimeSubmitted, WrittenReview, MachineID, RoomID):
        self.ReviewID = ReviewID
        self.Ranking = Ranking
        self.TimeSubmitted = TimeSubmitted
        self.WrittenReview = WrittenReview
        self.MachineID = MachineID
        self.RoomID = RoomID


def create_accounts(conn):
    with conn.cursor() as cur:
        #cur.execute("INSERT INTO washerWorld.Room (RoomID, RoomName) VALUES (2, 'Elingson')")
        cur.execute("SELECT * FROM washerworld.Room")
        from_balance = cur.fetchall()
        print(from_balance)
        logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()


# Creates a new room (must have unique id)
def create_room(conn, id, name):
    print("Creating room of id", id, "with name", name)
    new_room = Room()
    new_room.RoomID = id
    new_room.RoomName = name
    cmd = "INSERT INTO washerWorld.Room (RoomID, RoomName) VALUES (" + str(new_room.RoomID) + ",'" + str(new_room.RoomName) + "')"
    #print(cmd)
    with conn.cursor() as cur:
        cur.execute(cmd)
    conn.commit()
    return new_room


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


# get room entry from RoomID
def get_entry_room(curr, roomID):
    cmd = "SELECT * FROM washerworld.room WHERE RoomID = " + str(roomID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_room = cur.fetchall()
    conn.commit()
    return the_room


# get room entry from RoomID
def get_entry_machine(curr, machineID):
    cmd = "SELECT * FROM washerworld.machine WHERE MachineID = " + str(machineID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_machine = cur.fetchall()
    conn.commit()
    return the_machine


# get room entry from RoomID
def get_entry_review(curr, reviewID):
    cmd = "SELECT * FROM washerworld.review WHERE ReviewID = " + str(reviewID) + ";"
    with conn.cursor() as cur:
        cur.execute(cmd)
        the_review = cur.fetchall()
    conn.commit()
    return the_review


# Completely erases the database and resets it to have no entries.
def restart_setup(conn):
    with conn.cursor() as cur:
        print("DROPPING PREVIOUS TABLES...")
        cur.execute("DROP TABLE IF EXISTS washerWorld.Room CASCADE")
        cur.execute("DROP TABLE IF EXISTS washerWorld.Machine CASCADE")
        cur.execute("DROP TABLE IF EXISTS washerWorld.Review CASCADE")
        time.sleep(5)
        print("Database resetting, please hold...")
        time.sleep(10)
        cur.execute("CREATE TABLE washerWorld.Room (RoomID INT PRIMARY KEY NOT NULL, RoomName STRING);")
        cur.execute("CREATE TABLE washerWorld.Machine (MachineID INT PRIMARY KEY NOT NULL, Status STRING, Timer INT, MachineType STRING, RoomID INT REFERENCES washerWorld.Room(RoomID) ON DELETE CASCADE);")
        cur.execute("CREATE TABLE washerWorld.Review (ReviewID INT PRIMARY KEY NOT NULL, Ranking INT, TimeSubmitted TIMESTAMPTZ, WrittenReview STRING, MachineID INT REFERENCES washerWorld.Machine(MachineID) ON DELETE CASCADE, RoomID INT REFERENCES washerWorld.Room(RoomID) ON DELETE CASCADE); ")
    conn.commit()


if __name__ == '__main__':
    password_thing = input("Enter password:")
    conn = psycopg2.connect(
        database='defaultdb',
        user='cameron',
        password=password_thing,
        sslmode='verify-full',
        port=26257,
        host='free-tier11.gcp-us-east1.cockroachlabs.cloud',
        options='--cluster=stung-whale-219'
    )
    #restart_setup(conn)
    #room = create_room(conn, 2, "Sol")
    #machine = create_machine(conn, 1, "OPEN", 52, "WASHER", 3)
    #review_ex = create_review(conn, 1, 5, "TIMESTAMPTZ '2016-03-26 10:10:10-05:00'", 'pretty cool', 1, 3)
    print(get_entry_room(conn, 2))
    print(get_entry_machine(conn,1))
    print(get_entry_review(conn,1))

