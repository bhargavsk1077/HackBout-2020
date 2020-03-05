import pyrebase
import numpy as np
import matplotlib.pyplot as plt
import mplleaflet
from dotenv import load_dotenv
load_dotenv()
import os
config = {
  "apiKey": os.getenv("apiKey"),
  "authDomain": os.getenv("authDomain"),
  "databaseURL": os.getenv("databaseURL"),
  "storageBucket": os.getenv("storageBucket"),
  "serviceAccount": "firebase-adminsdk.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

uids = []
lats = []
longs = []
tokens = []
vehicle_type = []
numPlate = []
report = []
severity = []
vehicle_color = []
vehicle_company = []
vehicle_model = []
reports = db.child("reports").get().val()
check = ['lat','long','class','numberPlate','severity', 'uid', 'vehicleColor', 'vehicleCompany', 'vehicleModel']
for key, value in reports.items():
    # if ('lat' and 'long' and 'class' and 'numberPlate' and 'report' and 'severity' and 'vehicleColor' and 'vehicleCompany' and 'vehicleModel') in value.keys():
    keysInValue=value.keys()
    flag=1

    for i in check:
      if i not in keysInValue:
        flag=0

    if flag:
      uids.append(key)
      lats.append(value['lat'])
      longs.append(value['long'])
      vehicle_type.append(value['class'])
      numPlate.append(value['numberPlate'])
      report.append(value['report'])
      severity.append(value['severity'])
      vehicle_color.append(value['vehicleColor'])
      vehicle_company.append(value['vehicleCompany'])
      vehicle_model.append(value['vehicleModel'])


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/output")
def output():
  return render_template("index1.html", uid=uids,lattitude=lats,longitude=longs, vehicleType=vehicle_type,numberPlate=numPlate,
                          vehicleCompany=vehicle_company,vehicleModel=vehicle_model, vehicleColor=vehicle_color, severityScore=severity,reportType=report)

if __name__ == "__main__":
	app.run(debug=True,port="5001")
