# Name:         Nomura Amraa
# Organization: Infinite Solutions
# File name:    PrinterTXT.py
# Description:
# Prints the text extracted by 'TextOCR.py' in a formatted
# style, and prints the words and lines with low confidence
# scores.


# File paths for detected text files
detected_text_path = '/home/runner/Learning-AWS-Rekognition/detected_text/'
unemleh_nomura_txt_path = "unemleh-nomura.txt"
unemleh_2_txt_path = "unemleh-2.txt"
unemleh_3_txt_path = "unemleh-3.txt"
unemleh_4_txt_path = "unemleh-4.txt"
unemleh_5_txt_path = "unemleh-5.txt"
unemleh_6_txt_path = "unemleh-6.txt"
unemleh_7_txt_path = "unemleh-7.txt"
unemleh_8_txt_path = "unemleh-8.txt"

# Open file for reading
file = open(detected_text_path + unemleh_2_txt_path, 'r')

# Text lines for printing
title = "+----------------------------------------------------------------------+\n\
|  Mongolia            МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ           picture  |\n\
|  Mongolia         CITIZEN IDENTITY CARD OF MONGOLIA         picture  |\n\
+----------------------------------------------------------------------+"
empty_ln = "|                                                                      |"
border_ln = "+----------------------------------------------------------------------+"
pic_plc = "PICTUREPICTURE"
space = "                    "
bar_ver = "[|||||||]"
bar_hor = "[-------]"

# Field names to be used later for form parsing.
# Will be used as key in a key-value pair.
field_names = [
    "Овог / Family Name",
    "Эцэг/эх/-ийн нэр Surname",
    "Нэр Given Name",
    "Хүйс Sex",
    "Төрсөн он, сар, өдөр",
    "Date of birth",
    "Регистрийн дугаар Registration Number"
]

# Flag words that indicate that the line to be printed
# is a field name line.
# It's unneccessary to know how confidently the program
# read unimportant text such as field lines or 
# 'CITIZEN IDENTITY CARD OF MONGOLIA', so these words are
# used to skip such lines.
field_name_words = [
    "монгол улсын",
    "иргэний үнэмлэх",
    "овог",
    "эцэг/эх/",
    "нэр",
    "хүйс",
    "төрсөн он, сар, өдөр",
    "он, сар",
    "регистрийн дугаар",
    "citizen identity",
    "card of mongolia",
    "family name",
    "surname",
    "given name",
    "sex",
    "date of birth",
    "registration number"
]

# Arrays to contain the the extracted lines and their confidence scores
extracted_lines = []
extracted_words = []


# Checks whether a line about to be printed is a field name
# Also checks whether a line is a single character.
def check_for_flagword(dataline) :
    dataline = dataline.lower()
    for flagword in field_name_words :
        if flagword in dataline :
            return True
    if len(dataline) < 3 :
        return True
    return False
            

# Extracts the words into an array
def word_extractor() :
    # Starts reading lines from where line extraction ended
    
    # Saves current line - the line where the cursor is
    # and moves cursor to the next line
    dataline = file.readline()

    # Skips lines in text files to where words start
    while not ("Here are the words:" in dataline) :
        dataline = file.readline()
    dataline = file.readline()

    # Reads lines until the end of file
    while dataline != '' :
        text = dataline.strip()

        # Moves cursor down one line to get confidence score
        dataline = file.readline()
        confidence_line = dataline.strip()
        confidence_num = float(confidence_line[13:18])
        word = {"text": text, "confidence": confidence_num}
        extracted_words.append(word)

        # Moves cursor down two lines
        dataline = file.readline()
        dataline = file.readline()

        """
        # Sample lines from detected_text_file.txt
        МОНГОЛ
        Confidence:  96.71%
        ----------------------------
        УЛСЫН

        Cursor moves down once from the confidence line,
        saves '----' as dataline and moves down one line,
        then saves 'УЛСЫН' as dataline.
        After this, the loop is ready to extract the next word.
        """


# Extracts text with type 'LINE' from text 
def line_extractor() :
    dataline = file.readline()
    
    # Loops until the end of lines and the
    # beginning of words
    while dataline != '\n':
        dataline = dataline.strip()

        # If the line contains a field name,
        # moves cursor down two lines, skipping 
        # the field name line and its confidence score
        if check_for_flagword(dataline) == True :
            file.readline()
            file.readline()
            dataline = file.readline()
        else :
            text = dataline
            dataline = file.readline()
            confidence_line = dataline
            confidence_num = float(confidence_line[13:18])
            line = {"text": text, "confidence": confidence_num}
            extracted_lines.append(line)
            dataline = file.readline()
            dataline = file.readline()

    # After finishing saving the lines into an array
    # saves the words into an array
    word_extractor()


def line_printer_bare() :
    for line in extracted_lines :
        text = line['text']
        conf = str(line['confidence']) + "%"
        print("|    ", text.ljust(48), conf.ljust(15),  "|")


def line_printer_full() :
    for line in extracted_lines :
        text = line['text']
        conf = str(line['confidence']) + "%"
        print("|    ", text.ljust(48), conf.ljust(15), "|")
        

def word_printer() :
    for word in extracted_words :
        text = word['text']
        conf = str(word['confidence'])
        print("|    ", text.ljust(48), conf.ljust(15), "|")


# Prints lines with a confidence score less than 90
def print_low_confidence_lines() :
    print("LOW CONFIDENCE LINES:")
    for line in extracted_lines :
        confidence = line['confidence']
        if confidence < 90 :
            print(line['text'])
            print(confidence)
            print()


# Prints lines with a confidence score less than 90
def print_low_confidence_words() :
    print("LOW CONFIDENCE WORDS:\n")
    for word in extracted_words :
        confidence = word['confidence']
        if confidence < 90 :
            print(word['text'], f"({confidence}%)")


def ultra_printer() :
    print("I AM ULTRA PRINTERRR !!!!")
            

def main():
    print(title)
    print(empty_ln)
    line_extractor()
    line_printer_full()
    print(empty_ln)
    print(border_ln)
    print()

    print(border_ln)
    print_low_confidence_lines()
    print(border_ln)
    print_low_confidence_words()
    print(border_ln)
    
    file.close()


if __name__ == "__main__":
    main()


############     Test Run 1     ############
"""
+----------------------------------------------------------------------+
|  Mongolia            МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ           picture  |
|  Mongolia         CITIZEN IDENTITY CARD OF MONGOLIA         picture  |
+----------------------------------------------------------------------+
|                                                                      |
|     Уран Содном                                      99.15%          |
|     Uran Sodnom                                      98.79%          |
|     Машбаяр                                          98.99%          |
|     Mashbayar                                        98.47%          |
|     САРАНЧУЛУУН                                      84.8%           |
|     SARANCHULUUN                                     97.62%          |
|     Эмэгтэй / Female                                 82.27%          |
|     Терсен OH, cap, едер                             86.27%          |
|     1980/11/03                                       98.05%          |
|     YC80110306 /US80110306                           77.15%          |
|                                                                      |
+----------------------------------------------------------------------+

+----------------------------------------------------------------------+
LOW CONFIDENCE LINES:
САРАНЧУЛУУН
84.8

Эмэгтэй / Female
82.27

Терсен OH, cap, едер
86.27

YC80110306 /US80110306
77.15

+----------------------------------------------------------------------+
LOW CONFIDENCE WORDS:

монгол (81.25%)
ҮНЭМЛЭХ (87.44%)
Эцэг/эх/-ийн (66.28%)
САРАНЧУЛУУН (84.8%)
/ Female (66.76%)
OH, (67.98%)
едер (82.21%)
/US80110306 (59.45%)
+----------------------------------------------------------------------+
"""


############     Test Run 2     ############
"""
+----------------------------------------------------------------------+
|  Mongolia            МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ           picture  |
|  Mongolia         CITIZEN IDENTITY CARD OF MONGOLIA         picture  |
+----------------------------------------------------------------------+
|                                                                      |
|     Шавь                                             99.56%          |
|     Shavi                                            99.66%          |
|     Наваантогмид                                     97.89%          |
|     Navaantogmid                                     99.36%          |
|     БЯМБАЦОГТ                                        64.06%          |
|     BYAMBATSOGT                                      98.96%          |
|     Эрэгтэй /Male                                    90.86%          |
|     Тэрсен он, cap, едер                             64.13%          |
|     1995/07/29                                       99.21%          |
|     H395072914 NE95072914                            72.47%          |
|                                                                      |
+----------------------------------------------------------------------+

+----------------------------------------------------------------------+
LOW CONFIDENCE LINES:
БЯМБАЦОГТ
64.06

Тэрсен он, cap, едер
64.13

H395072914 NE95072914
72.47

+----------------------------------------------------------------------+
LOW CONFIDENCE WORDS:

БЯМБАЦОГТ (64.06%)
/Male (84.92%)
Тэрсен (42.84%)
он, (76.36%)
едер (42.28%)
NE95072914 (47.9%)
+----------------------------------------------------------------------+
"""


############     Test Run 3     ############
"""
+----------------------------------------------------------------------+
|  Mongolia            МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ           picture  |
|  Mongolia         CITIZEN IDENTITY CARD OF MONGOLIA         picture  |
+----------------------------------------------------------------------+
|                                                                      |
|     Боржигон                                         99.35%          |
|     Borjigon                                         99.73%          |
|     Базаррагчаа                                      91.9%           |
|     Bazarragchaa                                     99.03%          |
|     ЦЭЦЭГЖАРГАЛ                                      94.66%          |
|     TSETSEGJARGAL                                    98.34%          |
|     Эмэгтэй / Female                                 48.01%          |
|     1986/11/29                                       98.7%           |
|     ШЖ86112964/ShJ86112964                           24.43%          |
|                                                                      |
+----------------------------------------------------------------------+

+----------------------------------------------------------------------+
LOW CONFIDENCE LINES:
Эмэгтэй / Female
48.01

ШЖ86112964/ShJ86112964
24.43

+----------------------------------------------------------------------+
LOW CONFIDENCE WORDS:

МОНГОЛ (78.68%)
Oeor/Family (31.01%)
Hap/Surname (29.81%)
Хуйс/Sex (64.66%)
Эмэгтэй / Female (48.01%)
Терсен (60.28%)
OH, (73.28%)
exop/Date (19.02%)
Регистрийн (71.78%)
дугаар/Registration (23.61%)
ШЖ86112964/ShJ86112964 (24.43%)
+----------------------------------------------------------------------+
"""


