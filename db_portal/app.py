from flask import Flask, render_template, session, redirect, url_for, request
import pyrebase
from dotenv import load_dotenv
load_dotenv()
import os
import subprocess
import time
from map_ import leafletdo
import shutil
import os
from datetime import datetime
config = {
  "apiKey": os.getenv("apiKey"),
  "authDomain": os.getenv("authDomain"),
  "databaseURL": os.getenv("databaseURL"),
  "storageBucket": os.getenv("storageBucket"),
  "serviceAccount": "firebase-adminsdk.json"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
admin_accounts = ["adminboi@pipinstallnpm.com"]

dir_path = os.path.dirname(os.path.realpath(__file__))
print(os.getcwd(), dir_path)
app = Flask(__name__, static_folder=os.path.join(dir_path, "static"))
app.secret_key = 'the random string'

os.makedirs(os.path.join(dir_path, "static", "imgs", "images"), exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("database_access"))
        else:
            return render_template("login.html")
    elif request.method == "POST":
        if "email" in request.form and "password" in request.form:
            email = request.form["email"]
            password = request.form["password"]
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = user
            return redirect(url_for("index"))
        else:
            return render_template("login.html", msg="Email or password not provided")


reports = db.child("reports").get().val()
# for key, value in reports.items():
# print(key)
all_files = storage.child("images/").list_files()

for f in all_files:
    p = os.path.join(dir_path, os.path.join("static", "imgs", f.name + ".jpg"))
    if not os.path.isfile(p):
        try:
            f.download_to_filename(p)
        except Exception as e:
            print('Download Failed', e)
    else:
        print(f"File {p} already exists, not downloaded")
@app.route("/db", methods=["GET", "POST"])
def database_access():
    if request.method == "GET":
        columnNames = ["class", "confidence", "numberPlate", "report", "severity", "vehicleColor", "vehicleCompany", "vehicleModel", "lat", "long", "timestamp"]
        return render_template("index.html", columnNames=columnNames, reports=reports, enumerate=enumerate, str=str, fromtimestamp=datetime.fromtimestamp)
    elif request.method == "POST":
        session.clear()
        return redirect(url_for("index"))

@app.route("/map")
def map():
    try:
        proc = subprocess.Popen(["python", os.path.join(dir_path, "map_.py")])
    except Exception as e:
        proc = subprocess.Popen(["python3", os.path.join(dir_path, "map_.py")])
    proc.communicate()
    time.sleep(1)
    # leafletdo(db)
    # shutil.copy2("../_map.html", "templates/map.html")
    return render_template("map.html")

@app.route("/map2")
def output():
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
    print(uids)
    return render_template("index1.html", uid=uids,lattitude=lats,longitude=longs, vehicleType=vehicle_type,numberPlate=numPlate,
                          vehicleCompany=vehicle_company,vehicleModel=vehicle_model, vehicleColor=vehicle_color, severityScore=severity,reportType=report)


if __name__ == "__main__":
    app.run(port=5005)
