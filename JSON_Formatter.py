# Name:         Nomura Amraa
# Organization: Infinite Solutions
# File name:    JSON_Formatter.py
# Description:
# Receives 'response' object from 'TextOCR.py'
# and formats the data into fields. 

import json

from Levenshtein import jaro_winkler

# Directory paths for input JSON files and output formatted files
detected_text_folder = 'detected_text_json/'
formatted_text_folder = 'formatted_text/'


detected_json_path = 'detected_text'

# File paths
unemleh_2_path = "unemleh-2"
unemleh_3_path = "unemleh-3"
unemleh_4_path = "unemleh-4"
unemleh_5_path = "unemleh-5"
unemleh_6_path = "unemleh-6"
unemleh_7_path = "unemleh-7"
unemleh_8_path = "unemleh-8"
unemleh_9_path = "unemleh-9"
unemleh_10_path = "unemleh-10"
unemleh_11_path = "unemleh-11"
unemleh_12_path = "unemleh-12"
unemleh_13_path = "unemleh-13"
unemleh_14_path = "unemleh-14"

# Current file to process
current_path = unemleh_3_path

# Load the JSON object
with open(detected_text_folder + current_path + '.json', 'r') as openfile :
    # Loads json object into python dictionary
    json_obj_ocr = json.load(openfile)
    

field_names = [
    "Овог Family name",
    "Эцэг/эх/-ийн нэр Surname",
    "Нэр Given name",
    "Хүйс Sex",
    "Төрсөн он, сар, өдөр Date of birth",
    "Регистрийн дугаар Registration number",
    "Иргэний бүртгэлийн дугаар Civil identification number"
]


# A dictionary to hold extracted field values
# It now currently holds default values
fields = {
    'Овог Family name': 
        {'mn': 'null', 'en': 'null', 'confidence_mn': 0, 'confidence_en': 0},
    'Эцэг/эх/-ийн нэр Surname': 
        {'mn': 'null', 'en': 'null', 'confidence_mn': 0, 'confidence_en': 0},
    'Нэр Given name': 
        {'mn': 'null', 'en': 'null', 'confidence_mn': 0, 'confidence_en': 0},
    'Хүйс Sex': 
        {'mn': 'null', 'en': 'null', 'confidence_mn': 0, 'confidence_en': 0},
    'Төрсөн он, сар, өдөр Date of birth': 
        {'year': 'null', 'month': 'null', 'day': 'null', 'confidence': 0},
    'Регистрийн дугаар Registration number': 
        {'mn': 'null', 'en': 'null', 'confidence_mn': 0, 'confidence_en': 0},
    'Иргэний бүртгэлийн дугаар Civil identification number': 
        {'text': 'null', 'confidence': 0}
}


# List of words that help determine whether data read from
# JSON object is a field name
field_name_words = [
    "овог ",
    "эцэг/эх/",
    "хуйс",
    # "хүйс",
    # "төрсөн он, сар, өдөр",
    # "он, сар",
    # "он, ",
    "регистрийн дугаар",
    "family",
    "surname",
    "given",
    "sex",
    "date of birth",
    "registration",
    "бүртгэлийн дугаар",
    "civil",
    "identification"
]


# List of flag words that help determine whether data read
# is relevant. 'МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ', for example
# is not useful to process.
flag_words = [
    "монгол улсын",
    "иргэний",
    "үнэмлэх",
    "citizen identity",
    "card of mongolia",
]


# Function to find the best matching word between two strings
# based on Jaro-Winkler similarity. Uses module 'Levenshtein'.
# !!! Must be modified to use for ALL cases. Now only works for 'Хүйс Sex' !!!
# This function is used for determining the correct word based
# on read text because sometimes words are read incorrectly.
# For example, if given 'ЭрAгтэй/Mele', it will return 'Эрэгтэй/Male'
def find_match(str1, str2):
    min_similarity = 0.3
    output = []
    results = [[jaro_winkler(x,y) for x in str1.split()] for y in str2.split()]

    # If the function thinks that the given string
    # closely resembles the match word
    # (match word: Эрэгтэй, given string: эрагтай)
    # it gives a similarity score
    
    max_score = 0
    for x in results:
        # If similarity score is above minimum score
        # it returns match word.
        if max(x) >= min_similarity:
            output.append(str1.split()[x.index(max(x))])
        if max(x) > max_score :
            max_score = max(x)

    return output[0], max_score


# Determines whether given text is a field name
# If it's a field name, it returns fieldName
# If not field name, it must be a field value and returns 'False'
# Example:
# text: Овог Family name; returns "Овог Family name"
# text: Баасанхүү; returns 'False'
def is_field_name(text) :
    for word in field_name_words :
        if word in text.lower() :
            for fieldName in field_names :
                if word in fieldName.lower() :
                    return fieldName
    return 'False'


# Determines whether text is valid.
# Also, checks whether text contains flag words.
# There are instances where AWS Rekognition
# reads scratches and spots as text and saves
# it as text. For example:
# "DetectedText": 'II'
def is_valid_text(text) :
    if len(text) < 3 :
        return False
    else :
        for f_word in flag_words :
            if f_word in text :
                return False
    return True


# Used for printing formatted fields and debugging.
def printer(fields) :
    for field in fields :
        print(field)
        for sub in fields[field] :
            print(fields[field][sub])
        print()


# Removes bad characters from text
# Sometimes AWS Rekognition reads spots as characters
# which pollute text. For example:
# Registration number: AB:|123456'78
# Function returns: 'AB12345678'
def filter_text(input_str) :
    legitimate_chars = set("0123456789" \
                           "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                           "abcdefghijklmnopqrstuvwxyz" \
                           "АБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФХЦЧШЩЪЬЫЭЮЯ" \
                           "абвгдеёжзийклмноөпрстуүфхцчшщъьыэюя")

    filtered_word = "".join(c for c in input_str if c in legitimate_chars)
    return filtered_word


# Determines whether character is Cyrillic
# AWS Rekognition sometimes reads text in other languages
# than Mongolian or English like Romanian, Chech, Bulgarian etc.
# which causes errors.
def is_cyrillic(char):
    code_point = ord(char)
    return (
        (0x0400 <= code_point <= 0x04FF) or
        (0x0500 <= code_point <= 0x052F) or
        (0x2DE0 <= code_point <= 0x2DFF) or
        (0xA640 <= code_point <= 0xA69F) or
        (0x1C80 <= code_point <= 0x1C8F) or
        (0x0500 <= code_point <= 0x052F) or
        (0x2DE0 <= code_point <= 0x2DFF) or
        (0xA640 <= code_point <= 0xA69F) or
        (0x1C80 <= code_point <= 0x1C8F) or
        (0x1E030 <= code_point <= 0x1E08F)
    )


# Extracts gender from given text
def extract_gender(text) :
    text_mn = "".join(c for c in text if not c.isascii())
    text_en = "".join(c for c in text if c.isascii())

    # Is used for the case when text_en is not read
    # This part is not finished. Did not finish
    # Must check for the case when text_mn is not read
    if len(text_mn) > 7 :
        male_text_mn, male_score_mn = find_match('Эрэгтэй', text_mn)
        female_text_mn, female_score_mn = find_match('Эмэгтэй', text_mn)
        male_text_en, male_score_en = find_match('Male', text_mn)
        female_text_en, female_score_en = find_match('Female', text_mn)

        if male_text_mn == 'Эрэгтэй' and female_text_mn == 'Эмэгтэй':
            if male_score_mn > female_score_mn :
                text_mn = male_text_mn
            else :
                text_mn = female_text_mn

        if (male_score_en < 0.2 and female_score_en < 0.2) or (text_en == "") :
            if text_mn == "Эрэгтэй" :
                text_en = "Male"
            elif text_mn == "Эмэгтэй" :
                text_en = "Female"

    return text_mn, text_en


# Extracts registration number from filtered text
def extract_id(filtered_word) :
    if filtered_word.isdigit() and len(filtered_word) == 20 :
        change = 10
    else :
        for i in range(len(filtered_word)) :
            # When filtered word is: AB12345678CD987654321
            # checks for when the character changes from num to letter
            if filtered_word[i].isdigit() and filtered_word[i+1].isalpha() :
                change = i + 1
                break

    id_mn = filtered_word[:change]
    id_en = filtered_word[change:]

    return id_mn, id_en


# Finds the confidence of a word from the main JSON object
def confidence_finder(word, obj_input) :
    obj = obj_input
    confidence = -1
    
    lnCtr = 0

    # Finds where WORD index starts in JSON object
    while obj[lnCtr]['Type'] == 'LINE' and lnCtr < 100:
        lnCtr += 1

    # Loops until end of file
    while len(obj) - 1 > lnCtr:
        if word in obj[lnCtr+1]['DetectedText'] :
            confidence = obj[lnCtr+1]['Confidence']
            confidence = round(confidence, 2)
            
            return confidence

        lnCtr += 1


# Finds lines and words that have low confidence scores
def low_confidence_finder(obj) :
    lnCtr = 0
    low_confidence_lines = []
    current_json_ln = {}
    while obj[lnCtr]['Type'] == 'LINE' :
        if obj[lnCtr]['Confidence'] < 90 :
            current_json_ln = {
                'DetectedText': obj[lnCtr]['DetectedText'],
                'Confidence': round(obj[lnCtr]['Confidence'], 2)
            }
            low_confidence_lines.append(current_json_ln)
        lnCtr += 1

    # Finds where WORD index starts in JSON object
    while obj[lnCtr]['Type'] != 'WORD' :
        lnCtr += 1

    low_confidence_words = []
    current_json_wr = {}
    while lnCtr < len(obj):
        if obj[lnCtr]['Confidence'] < 90 :
            current_json_wr = {
                'DetectedText': obj[lnCtr]['DetectedText'],
                'Confidence': round(obj[lnCtr]['Confidence'], 2)
            }
            low_confidence_words.append(current_json_wr)
        lnCtr += 1


    return low_confidence_lines, low_confidence_words


# Main function that gets called by TextOCR.py
def json_formatter(response) :
    # Main loop starts from second line as the first two lines are not relevant
    # 'МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ' and 'CITIZEN IDENTITY CARD OF MONGOLIA'
    lnCtr = 2
    
    # obj = json_obj_ocr['TextDetections']
    obj = response['TextDetections']

    # JSON object that gets returned from json_formatter
    main_json = {
        'Fields': '',
        'LowConfidenceLines': '',
        'LowConfidenceWords': ''
    }

    # Error checking. Did not finish
    error_number = 0
    error_message_en = "Data formatted successfully"
    error_message_mn = "Мэдээллийг амжилттай уншлаа"

    # Loops until 'Type' becomes 'WORD'
    while obj[lnCtr]['Type'] == 'LINE':
        text = obj[lnCtr]['DetectedText']
        
        if is_valid_text(text) == True :
            field_name = is_field_name(text)
            confidence = obj[lnCtr]['Confidence']

            # If text is a field name
            if field_name != 'False' :

                # If field name is one of the first three
                # Reads two lines instead of one
                if any(sub.lower() in field_name.lower() for sub in field_names[:3]) :
                    if is_valid_text(obj[lnCtr+1]['DetectedText']) :
                        if is_field_name(obj[lnCtr+1]['DetectedText']) == 'False' :
                            text_mn = obj[lnCtr+1]['DetectedText']
                            filtered_text = filter_text(text)
                            confidence_mn = obj[lnCtr+1]['Confidence']
                            confidence_mn = round(confidence_mn, 2)
                            fields[field_name]['mn'] = text_mn
                            fields[field_name]['confidence_mn'] = confidence_mn
    
                    if is_valid_text(obj[lnCtr+2]['DetectedText']) :
                        if is_field_name(obj[lnCtr+2]['DetectedText']) == 'False' :
                            text_en = obj[lnCtr+2]['DetectedText']
                            filtered_text = filter_text(text)
                            confidence_en = obj[lnCtr+2]['Confidence']
                            confidence_en = round(confidence_en, 2)

                            # Sets values in dictionary
                            fields[field_name]['en'] = text_en
                            fields[field_name]['confidence_en'] = confidence_en
                    
                    lnCtr += 2
                
    
                if field_name == 'Хүйс Sex':
                    if is_valid_text(obj[lnCtr+1]['DetectedText']) :
                        if is_field_name(obj[lnCtr+1]['DetectedText']) == 'False' :
                            text = obj[lnCtr+1]['DetectedText']
                            filtered_text = filter_text(text)
                            text_mn, text_en = extract_gender(filtered_text)

                            # Sets values in dictionary
                            fields[field_name]['mn'] = text_mn
                            fields[field_name]['en'] = text_en
                            fields[field_name]['confidence_mn'] = confidence_finder(text_mn, obj)
                            fields[field_name]['confidence_en'] = confidence_finder(text_en, obj)
                            


                if field_name == 'Төрсөн он, сар, өдөр Date of birth' :
                    if is_valid_text(obj[lnCtr+1]['DetectedText']) :
                        if is_field_name(obj[lnCtr+1]['DetectedText']) == 'False' :
                            text = obj[lnCtr+1]['DetectedText']

                            text_split = text.split('/')

                            # Filters numbers
                            for word in text_split :
                                word = "".join(c for c in word if c.isdigit())
                                # This    ['198;7', 'a01', '12']
                                # Becomes ['1987', '01', '12']

                            year = text_split[0].strip()
                            month = text_split[1].strip()
                            day = text_split[2].strip()

                            # If somehow the year is not read properly
                            # and is missing its first digit this ensures
                            # that it has its first digit
                            if len(year) < 4 :
                                if int(year[1]) > 0 :
                                    year = '1' + year
                                elif int(year[1]) == 0 :
                                    year = '2' + year
                            
                            confidence = round(obj[lnCtr+1]['Confidence'], 2)
                            fields[field_name]['year'] = year
                            fields[field_name]['month'] = month
                            fields[field_name]['day'] = day
                            fields[field_name]['confidence'] = confidence
    
                
                if field_name == 'Регистрийн дугаар Registration number' :
                    if obj[lnCtr+1]['Type'] == 'LINE' :
                        if is_valid_text(obj[lnCtr+1]['DetectedText']) :
                            if is_field_name(obj[lnCtr+1]['DetectedText']) == 'False' :
                                text = obj[lnCtr+1]['DetectedText']
                                filtered_text = filter_text(text)
                                text_mn, text_en = extract_id(filtered_text)
                                
                                fields[field_name]['mn'] = text_mn
                                fields[field_name]['en'] = text_en
                                fields[field_name]['confidence_mn'] = confidence_finder(text_mn, obj)
                                fields[field_name]['confidence_en'] = confidence_finder(text_en, obj)

                    # If the last line is not read, or in other words
                    # if the registration numbers are not read
                    # saves 'Data not read' into JSON
                    else :
                        error_number = 7
                        error_message_en = "Registration number is not read"
                        fields[field_name]['mn'] = "Data not read"
                        fields[field_name]['en'] = "Data not read"
                        fields[field_name]['confidence_mn'] = "Data not read"
                        fields[field_name]['confidence_en'] = "Data not read"


                if field_name == 'Иргэний бүртгэлийн дугаар Civil identification number' :
                    if obj[lnCtr+1]['Type'] == 'LINE' :
                        if is_valid_text(obj[lnCtr+1]['DetectedText']) :
                            if is_field_name(obj[lnCtr+1]['DetectedText']) == 'False' :
                                text = obj[lnCtr+1]['DetectedText']
                                filtered_text = filter_text(text)
                                confidence = round(obj[lnCtr+1]['Confidence'], 2)

                                fields[field_name]['text'] = text
                                fields[field_name]['confidence'] = confidence

                
                lnCtr += 1

            else :
                lnCtr += 1
        
        else :
            lnCtr += 1

    low_confidence_lines, low_confidence_words = low_confidence_finder(obj)

    # Sets data to main_json
    main_json['Fields'] = fields
    main_json['LowConfidenceLines'] = low_confidence_lines
    main_json['LowConfidenceWords'] = low_confidence_words

    # Prints data. Used for debugging and data verification
    # print(main_json['Fields'])
    # print(main_json['LowConfidenceLines'])
    # print(main_json['LowConfidenceWords'])
            
    return main_json


def main() :
    json_formatter(json_obj_ocr)


if __name__ == "__main__" :
    main()