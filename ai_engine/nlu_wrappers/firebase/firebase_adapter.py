import pyrebase
import json


class Analytics(object):
    def __init__(self):
        with open('firebase_config.json') as config:
            self.firebase = pyrebase.initialize_app(json.loads(config.read()))
        self.db = self.firebase.database()

    def add_message(self, user_id, msg, intent, messenger):
        data = {"user_id": user_id, "message": msg, "intent": intent}
        self.db.child("messenger/{0}".format(messenger)).push(data)


if __name__ == "__main__":
    analytics = Analytics()
