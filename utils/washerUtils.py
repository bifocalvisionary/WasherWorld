from userUtils import User
from cockroachdbUtils import *

FREE = 0
FULL = 1
RUNNING = 2
BROKEN = 3
WASHER_STATES = {FREE, FULL, RUNNING, BROKEN}

WASHER = 0
DRYER = 1


class Machine:
    def __init__(self, machineID: int, machineType, rating: int, reviews: list):
        self.state = FREE
        self.user = None
        self.machineType = machineType
        self.machineID = machineID
        self.rating = rating
        self.reviews = reviews

    def contact_user(self, message):
        self.user.contact_user(message)

    def set_user(self, user: User):
        self.user = user

    def set_state(self, state : int):
        if state in WASHER_STATES:
            self.state = state
            return

        raise Exception("Desired State is Invalid(FREE, RUNNING, FULL, BROKEN")


class LaundryRoom:
    def __init__(self, admin, roomID):
        self.admin = admin
        self.roomID = roomID
        self.washers = list()
        self.dryers = list()

    def add_machine(self, machineID, machineType, rating):
        for washer in self.washers:
            if washer.machineID == machineID:
                raise Exception("Machine ID is not unique")

        for dryer in self.dryers:
            if dryer.machineID == machineID:
                raise Exception("Machine ID is not unique")

        if machineType == WASHER:
            self.washers.append(Machine(machineID, WASHER, rating))

        elif machineType == DRYER:
            self.washers.append(Machine(machineID, DRYER, rating))

        else:
            raise Exception("Machine Type is not Valid (WASHER/DRYER)")

    def remove_machine(self, machineID):
        for i in range(len(self.washers)):
            if self.washers[i].machineID == machineID:
                self.washers.remove(i)
                return

        for i in range(len(self.dryers)):
            if self.dryers[i].machineID == machineID:
                self.dryers.remove(i)
                return

        raise Exception("There is no machine with ID " + str(machineID))


def import_rooms_from_database():
    rooms = list()

    # Get All Room Entries From Database
    rawRooms = list_all_rooms()

    # Parse Output as Array of tuples
    roomTuples = exec(rawRooms)

    # Generate Objects From Array Of Tuples
    for roomTuple in roomTuples:
        rooms.append(import_room(roomTuple))

    # Get all Machines from database
    rawMachines = list_all_machines()

    # Parse Output as Array of Tuples
    machineTuples = exec(rawMachines)

    # Using each machine's ID assign them to a room
    for machineTuple in machineTuples:

        #Search for a room with a matching ID
        for room in rooms:
            if room.roomID == machineTuple[4]:
                room.add_machine(machineTuple[0], machineTuple[3], 3)

    # Return an array of rooms
    return -1


def import_room():
    return
