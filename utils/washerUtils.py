from userUtils import User

FREE = 0
FULL = 1
RUNNING = 2
BROKEN = 3
WASHER_STATES = {FREE, FULL, RUNNING, BROKEN}

WASHER = 0
DRYER = 1


class Machine:
    def __init__(self, machineID: int, machineType, rating: int):
        self.state = FREE
        self.user = None
        self.machineType = machineType
        self.machineID = machineID
        self.rating = rating

    def contact_user(self, message):
        print("This Feature is Not Yet Implemented")
        return -1

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
