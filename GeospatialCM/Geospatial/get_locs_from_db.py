import pyrebase
from dotenv import load_dotenv
load_dotenv()
import os
config = {
  "apiKey": os.getenv("apiKey"),
  "authDomain": os.getenv("authDomain"),
  "databaseURL": os.getenv("databaseURL"),
  "storageBucket": os.getenv("storageBucket"),
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

uids = []
lats = []
longs = []
tokens = []
users = db.child("users").get().val()
for key, value in users.items():
    # print(key, value)
    if "location" in value and "token" in value:
        uids.append(key)
        lats.append(float(value["location"]["lat"]))
        longs.append(float(value["location"]["long"]))
        tokens.append(value["token"]["token"])
