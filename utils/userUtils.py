"""
userUtils.py
Hendrick Ducasse

A Set of utilities for managing discrete user contact info
"""

CONTACT_MODES = {(0, "call"), (1, "text"), (2, "email")}

class User:
    def __init__(self, name, phone, email, preferredMode):
        self.name = name
        self.phone = phone
        self.email = email
        self.preferredMode = preferredMode

    def email_user(self, message):
        print("Emailing Users Is Not Yet Implemented")
        return -1

    def text_user(self, message):
        print("Texting Users is not yet implemented")
        return -1

    def call_user(self, message):
        print("Calling Users is not yet implemented")
        return -1

    def contact_user(self, message): #Contact the user through their preferred contact mode
        if self.preferredMode == "call":
            self.call_user(message)

        elif self.preferredMode == "text":
            self.text_user(message)

        elif self.preferredMode == "email":
            self.email_user(message)

        else:
            print("User does not have a preferred mode of contact. Please use a specific function.")