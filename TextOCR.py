# Name:          Nomura Amraa
# Organisation:  Infinite Solutions
# File name:     TextOCR.py
# Description:
# Takes image of national citizen id as input
# and prints the extracted lines and words along
# with their confidence scores.


import boto3    # AWS SDK for Python
import json     # Used for json
import time     # Used to see program speed

start_time = time.time()

# Function to format AWS response
from JSON_Formatter import json_formatter

# Function to check whether user given input (as JSON)
# matches OCR input
from Validation import is_input_valid
from Validation import input_mismatch_printer


# AWS Rekognition user access key hidden for privacy
import os
my_secret = os.environ['aws_rekognition_key']


# Print boto3 version so that it matches with Amazon's current version
# print(boto3.__version__)

# Setup boto3 session (or in other words, connect)
# with AWS using access keys 
boto3.setup_default_session(
    aws_access_key_id = my_secret,
    aws_secret_access_key = 'd49LRZgv3HaWlwBTUYFusMcvrIz2/pVih4dyLTZC',
    region_name = 'us-east-1'
)


# The parent path of the pictures to be used
files_path = '/home/runner/Learning-AWS-Rekognition/files/'
detected_text_path = '/home/runner/Learning-AWS-Rekognition/detected_text/'
formatted_text_folder = 'formatted_text/'

# The paths of the pictures
# Separated this way so that it's easier to write
# extracted text to text file
pasture_img_path = 'MongoliaPasture.jpg'
unemleh_nomura = 'unemleh-nomura'
unemleh_2 = 'unemleh-2'
unemleh_3 = 'unemleh-3'
unemleh_4 = 'unemleh-4'
unemleh_5 = 'unemleh-5'
unemleh_6 = 'unemleh-6'
unemleh_7 = 'unemleh-7'
unemleh_8 = 'unemleh-8'
unemleh_9 = 'unemleh-9'
unemleh_10 = 'unemleh-10'
unemleh_11 = 'unemleh-11'
unemleh_12 = 'unemleh-12'
unemleh_13 = 'unemleh-13'
unemleh_14 = 'unemleh-14'

# Paths for input that tests validation function
formatted_text_folder = 'formatted_text/'
input_path = 'input'

# The image from which text will be extracted
current_image = unemleh_3

# Opens image file
def get_image_bytes(image_path):
    with open(image_path, 'rb') as file:
        return file.read()

# Image file of the current image
image_bytes = get_image_bytes(files_path + current_image + ".jpg")


# Sends image file to AWS Rekognition
# and gets response JSON file
def detect_text(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_text(Image={'Bytes': image_bytes})
    return response

# Extracted text JSON file
response = detect_text(image_bytes)

# Check whether Rekognition response came through
# print(response['TextDetections'][0])


# Prints the detected text: lines first, words next
# then prints the confidence with which each
# line and word is extracted
# The higher the confidence score, the more likely
# that the extracted text is correct.
# The lower the confidence score, the more likely
# that the extracted text is WRONG.
def print_detected_text(response):
    text_detections = response['TextDetections']
    print("\nDetected text\n----------------------------")

    # Used to separate extracted lines from words
    foundWord = False
    for text in text_detections:

        # When extracting lines end, and extracting words start,
        # prints the message below to console.
        if text['Type'] == 'WORD' and foundWord == False:
            print("\n\nHere are the words:")
            file.write("\n\nHere are the words:\n")
            foundWord = True
        
        print(text['DetectedText'])
        print(f"Confidence:  {text['Confidence']:.2f}%")
        print("----------------------------")


# Saves response to a text file.
# Was used for early debugging.
def save_to_textfile(response) :
    # Create text file to save extracted text
    file = open(detected_text_path + current_image + ".txt", 'w')
    text_detections = response['TextDetections']

    # Used to separate extracted lines from words
    foundWord = False
    for text in text_detections:
        # When extracting lines end, and extracting words start,
        # writes to the text file the message below so
        # that formatting is easier later on.
        if text['Type'] == 'WORD' and foundWord == False:
            file.write("\n\nHere are the words:\n")
            foundWord = True

        # Writes to the text file
        file.write(text['DetectedText'] + '\n')
        file.write(f"Confidence:  {text['Confidence']:.2f}%" + '\n')
        file.write("----------------------------" + '\n')


# Saves response to a JSON file.
# Was used for JSON file debugging.
def save_to_JSONfile(response) :
    json_obj = json.dumps(response, indent=4, ensure_ascii=False)

    with open(f"/home/runner/Learning-AWS-Rekognition/detected_text_json/{current_image}.json", 'w') as outfile :
        outfile.write(json_obj)

# Saves FORMATTED JSON to a file
def save_formatted_json(main_json) :
    with open(formatted_text_folder + current_image + '-formatted.json', 'w') as outfile :
        json_obj_formatted = json.dumps(main_json, indent = 4, ensure_ascii=False)
        outfile.write(json_obj_formatted)


def main():
    save_to_JSONfile(response)
    
    # print_detected_text(response)
    # save_to_textfile(response)
    main_json = json_formatter(response)
    save_formatted_json(main_json)

    # Tests Validation.py
    # with open(formatted_text_folder + input_path + '.json', 'r') as inputfile :
    #     json_obj_input = json.load(inputfile)['Fields']
    #     input_valid, error_index = is_input_valid(json_obj_input, main_json['Fields'])
    #     input_mismatch_printer(input_valid, error_index)
    
    # Prints elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time spent:", round(elapsed_time, 4))

if __name__ == "__main__" :
    main()