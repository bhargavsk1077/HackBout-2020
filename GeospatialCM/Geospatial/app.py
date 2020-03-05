from flask import Flask, request, jsonify
from location_utils import points_in_radius_wrapper
import pyrebase
from pyfcm import FCMNotification
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

config = {
  "apiKey": os.getenv("apiKey"),
  "authDomain": os.getenv("authDomain"),
  "databaseURL": os.getenv("databaseURL"),
  "storageBucket": os.getenv("storageBucket"),
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

push_service = FCMNotification(api_key=os.getenv("fcm_api_key"))

@app.route("/api/location/pointsInRadius", methods=["POST"])
def pointsInRadius():
    data = request.get_json(silent=False)
    print(data)
    if "lat" not in data or "long" not in data or "point" not in data:
        return 400, "One of lat, long or point values not passed"
    point = data["point"]
    if "lat" not in point or "long" not in point:
        return 400, "Point values are invalid (lat or long not found)"
    if "radius" in data:
        radius = data["radius"]
    else:
        radius = 5000
    neighbours = points_in_radius_wrapper(data["long"], data["lat"], point["long"], point["lat"], radius)
    indexes = [int(i) for i in neighbours.index.values]

    if "showValues" in data and data["showValues"]:
        values = neighbours.geometry
        values = list((i.x, i.y) for i in values)
        return jsonify({
            "indexes": indexes,
            "values": values
        })
    else:
        return jsonify({
            "indexes": indexes
        })

@app.route("/api/location/notifyNearby", methods=["POST"])
def notifyNearby():
    uid_center = request.form["uid"]
    message_title = request.form.get("title", "A vehicle was reported in your area!")
    message_body = request.form.get("body", "There might be traffic issues")
    token_center = ""
    long_center = 0.0
    lat_center = 0.0
    uids = []
    lats = []
    longs = []
    tokens = []
    users = db.child("users").get().val()
    for key, value in users.items():
        # print(key, value)
        if uid_center == key:
            token_center = value["token"]["token"]
            long_center = value["location"]["long"]
            lat_center = value["location"]["lat"]
        else:
            if "location" in value and "token" in value:
                uids.append(key)
                lats.append(float(value["location"]["lat"]))
                longs.append(float(value["location"]["long"]))
                tokens.append(value["token"]["token"])
    # print(uids, lats, longs)
    neighbours = points_in_radius_wrapper(longs, lats, long_center, lat_center, 5000, data={"token": tokens})

    valid_tokens = list(neighbours["token"].values)
    print(valid_tokens)
    result = push_service.notify_multiple_devices(registration_ids=valid_tokens, message_title=message_title, message_body=message_body, timeout=10)
    print(result)
    return "Done"

@app.route("/")
def index():
    return "hello this is api"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

