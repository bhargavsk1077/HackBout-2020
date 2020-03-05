# HackBout-2020

HackBout 2020 submission

## Team ID: 16
## Team name: pip install npm
## Track: Open innovation

# Basic Idea

There has been a huge upsurge of vehicles in India, with it comes the problem of people parking irresponsibly on the roads. Also, vehicles are abandoned after being used for illegal activities or sometimes a vehicle breaks down in the middle of a road.

To solve these issues, we have come up with an app to report such vehicles by taking a picture of it. Vehicle detection is performed on the image using Tensorflow-lite on the phone and the user can select which vehicle to report through the interface. After submitting the picture, the cloud server performs number plate detection and OCR on the image to extract the number plate from it. The user can then submit more info about the vehicle such as severity of report, vehicle model, vehicle company, type of report (Abandonment, Illegal Parking or Temporary Breakdown)
