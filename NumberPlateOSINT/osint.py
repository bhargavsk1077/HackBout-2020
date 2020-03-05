import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import os
import  imutils
import sys
import pandas as pd
import numpy as np
import pickle
# import pytesseract
import cv2
from PIL import Image
import io
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()
# client = vision.ImageAnnotatorClient()
def get_text(path):
    # Instantiates a client

    # The name of the image file to annotate
    file_name = os.path.abspath(f"./{path}")

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    text = response.text_annotations
    text1= text[0].description
    return text1.strip()
    # print("Annotation:", text[0].description)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCALSTORAGE_PATH = "localstorages.pkl"

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

browser = "firefox"
if "firefox" in browser.lower():
    driver = webdriver.Firefox(
        executable_path=os.path.join(PROJECT_ROOT, "geckodriver"),options=options)
elif "chrome" in browser.lower():
    driver = webdriver.Chrome(
        executable_path=os.path.join(PROJECT_ROOT, "chromedriver"))


def get_details(regno):
    driver.get('https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml')
    vhno = driver.find_element_by_name("regn_no1_exact")
    vhno.send_keys(regno)
    sleep(1.0)

    import base64
    img_base64 = driver.execute_script("""
        var ele = arguments[0];
        var cnv = document.createElement('canvas');
        cnv.width = 100; cnv.height = 35;
        cnv.getContext('2d').drawImage(ele, 0, 0);
        return cnv.toDataURL('image/jpeg').substring(22);    
        """, driver.find_element_by_class_name("captcha-image"))   #"/html/body/form/div[2]/div[3]/span[3]/div[1]/img"))
    with open(r"image.jpg", 'wb') as f:
        f.write(base64.b64decode(img_base64))

    text = get_text("image.jpg")
    print(text)
    enter_cap = driver.find_element_by_xpath('//*[@id="txt_ALPHA_NUMERIC"]')
    enter_cap.click()
    enter_cap.send_keys(text)

    time.sleep(2)
    button = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[5]/div/button/span')
    button.click()
    time.sleep(2)
    name = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[5]/div[2]').text
    model = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[7]/div[2]').text
    reg_date = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[3]/div[4]').text
    rto = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[2]/div/div').text
    vehicle_class = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[6]/div[2]').text
    fuel = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[6]/div[4]').text
    rc_status = driver.find_element_by_xpath('/html/body/form/div[1]/div[3]/div/div[2]/div/div/div[2]/div[6]/div/div/div/div[10]/div[4]').text
    return name,model,reg_date,rto,vehicle_class,fuel,rc_status

regno='<Enter vehicle registration number here>'
for i in range(0,4):
    try:
        name,model,reg_date,rto,vehicle_class,fuel,rc_status=get_details(regno)
        print(name,model,reg_date,rto,vehicle_class,fuel,rc_status, sep="\n")
        break
    except Exception as e:
        print(f"failed {i} {e}")
        continue
# print(name,model,reg_date,rto,vehicle_class,fuel,rc_status)
driver.close()
