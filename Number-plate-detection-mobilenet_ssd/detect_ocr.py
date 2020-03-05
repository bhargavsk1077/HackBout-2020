from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import pytesseract
import cv2

import numpy as np
import os
import tensorflow as tf
import pathlib
import time

from PIL import Image

import io

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


def load_model(model_path):

  model_dir = pathlib.Path(model_path)/"saved_model"

  model = tf.compat.v2.saved_model.load(str(model_dir), None)
  model = model.signatures['serving_default']

  return model

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

detection_model = load_model("num_detecion model")

def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]

    # Run inference
    start = time.time()
    output_dict = model(input_tensor)
    end = time.time()
    print(f"Model run took {end - start} seconds")

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy() 
                    for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
    
    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                output_dict['detection_masks'], output_dict['detection_boxes'],
                image.shape[0], image.shape[1])      
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                        tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
        
    return output_dict

def show_inference(model=detection_model, image=None, image_path=None, image_draw=True):
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    if image is not None:
        image_np = image
    elif image_path:
        image_np = np.array(Image.open(image_path))
    else:
        return False
    # Actual detection.
    output_dict = run_inference_for_single_image(model, image_np)
    # Visualization of the results of a detection.
    if image_draw:
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8)
    boxes = output_dict['detection_boxes']
    scores = output_dict['detection_scores']
    min_score_thresh = 0.5
    all_boxes = []
    for i in range(min(boxes.shape[0], boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            all_boxes.append(box)

    return all_boxes, image_np

def crop_img(imagepath, boxes, output_path="cropped_{}.jpeg"):
    count=1
    img = Image.open(imagepath)
    width, height = img.size
    for tple in boxes:
        ymin,xmin,ymax,xmax=tple
        ymin *= height
        ymax *= height
        xmin *= width
        xmax *= width
        img2 = img.crop((xmin, ymin, xmax, ymax))
        img2.save(output_path.format(count))

def image_to_text(im,preprocess):
    # load the example image and convert it to grayscale
    image = cv2.imread(im)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text

def process_image(text):

    state_list = ["AP","AR","AS","BR","CG","GA","GJ","HR","HP","JH","KA","KL","MP","MH","MN","ML","MZ","NL","OD","PB","RJ","SK","TN","TS","TR","UP","UK","WB","AN","CH","DD","DL","JK","LA","LD","PY"]
    indexes = []
    #getting all first occurances
    for substring in state_list:
        index = text.find(substring)
        if(index==-1):
            continue
        indexes.append(index)

    #getting the least first occurance
    if(indexes):
        j=indexes[0]
        for i in indexes:
            if(i<j):
                j=i
        #remove unwanted characters before
        text = text[j:]
    else:
        #if there are no matches
        #print("invalid reg number")
        return "XXXXXXXXXX"
        
    #getting 10 digit number and adding spaces in between
    text = text.replace(" ","")
    if(len(text)>=7):
        if((len(text))>10):
            text=text[:10]

        if(len(text)==9):
            text = text[:6]+"0"+text[6:]
        elif(len(text)==8):
            text = text[:6]+"00"+text[6:]
        elif(len(text)==7):
            text = text[:6]+"000"+text[6:]

        text = text[:2]+" "+text[2:]
        text = text[:5]+" "+text[5:]
        text = text[:8]+" "+text[8:]
        return text.strip()

    else:
        #print("invalid reg number")
        return "XXXXXXXXXX"

        
def text_ocr(path):
    images = []
    files=os.listdir(".")
    for fil in files:
        if fil[:8]=="cropped_":
            images.append(fil)
    texts=[]
    for im in images:
        text=image_to_text(im,"thresh")
        if text=="":
            text=image_to_text(im,"blur")

        if text=="":
            #print("failed to read number from number plate try with a better image ")
            text = "XXXXXXXXXX"
        else:
            text = process_image(text)
        texts.append(text)
    #delete generated images by detection model
    # for im in images:
    #     os.remove(im)
    
    if(texts):
        return texts
    else:
        return ["XXXXXXXXXX"]

client = vision.ImageAnnotatorClient()

def gcloud_ocr(path):
    valid_images = []
    files = os.listdir(path)
    for file_ in files:
        if file_.startswith("cropped_"):
            valid_images.append(file_)
    results = []
    for image in valid_images:
        with io.open(image, 'rb') as image_file:
            content = image_file.read()
        img = types.Image(content=content)
        response = client.text_detection(image=img)
        text = response.text_annotations
        if len(text) > 0:
            results.append(text[0].description)
        os.remove(image)
    return results

def gcloud_ocr_whole_image(path):
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    img = types.Image(content=content)
    response = client.text_detection(image=img)
    text = response.text_annotations
    return text[0].description

if __name__ == "__main__":
    image_path = "imgs/8e1a66ea-8168-4254-b8b0-6e4f9a2c836c.jpg"
    boxes,img = show_inference(model=detection_model, image_path=image_path, image_draw=True)
    img = Image.fromarray(img)
    img.show()
    crop_img(image_path,boxes)
    # texts=text_ocr(os.getcwd())
    texts = gcloud_ocr(os.getcwd())
    text = texts[0]
    text = process_image(text)
    print(text)

