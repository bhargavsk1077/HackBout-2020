import pyrebase
import numpy as np
import matplotlib.pyplot as plt
import mplleaflet
from dotenv import load_dotenv
load_dotenv()
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def leafletdo(db):
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
          
  print(uids)
          
  # plt.figure(figsize=(8,6))
  # fig = plt.figure()
  fig, ax = plt.subplots(figsize = (8,8))
  for i,uid in enumerate(uids):
      x=longs[i]
      y=lats[i]
      ax.scatter(x,y,marker='x',color='red')
      ax.text(x+0.3,y+0.3,uid,fontsize=9)

  #plt.figure(figsize=(8,6))
  #fig = plt.figure()
  #plt.plot(longs, lats, 'ro')

  mplleaflet.save_html(fileobj=os.path.join(dir_path, "templates/map.html"), fig=fig)

if __name__ == "__main__":
    config = {
      "apiKey": os.getenv("apiKey"),
      "authDomain": os.getenv("authDomain"),
      "databaseURL": os.getenv("databaseURL"),
      "storageBucket": os.getenv("storageBucket"),
      "serviceAccount": os.path.join(dir_path, "firebase-adminsdk.json")
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    leafletdo(db)
