import json

detected_text_folder = 'detected_text_json/'
formatted_text_folder = 'formatted_text/'
detected_json_path = 'detected_text'
input_path = 'input'
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

current_path = unemleh_3_path

with open(formatted_text_folder + current_path + '-formatted.json', 'r') as openfile :
    json_obj_ocr = json.load(openfile)['Fields']


with open(formatted_text_folder + input_path + '.json', 'r') as inputfile :
    json_obj_input = json.load(inputfile)['Fields']



field_names = [
    "Овог Family name",
    "Эцэг/эх/-ийн нэр Surname",
    "Нэр Given name",
    "Хүйс Sex",
    "Төрсөн он, сар, өдөр Date of birth",
    "Регистрийн дугаар Registration number",
    "Иргэний бүртгэлийн дугаар Civil identification number"
]


def is_input_valid(input_obj, ocr_obj) :
    error_index = 100
    for i in range(len(field_names)) :
        if input_obj[field_names[i]] != ocr_obj[field_names[i]] :
            error_index = i
            return False, error_index
    return True


def input_mismatch_printer(input_valid, error_index) :
    input_valid, error_index = is_input_valid(json_obj_input, json_obj_ocr)
    if input_valid == True :
        print("The input fields match the OCR fields")
    else :
        print(f"Mismatch at: [{error_index}]")
        err_obj_len = len(json_obj_input[field_names[error_index]])
        for field in json_obj_input[field_names[error_index]] :
            field_name = field_names[error_index]
            field_in = str(json_obj_input[field_name][field])
            field_oc = str(json_obj_ocr[field_name][field])
            print(field_name, ":", field_in.ljust(25), field_oc.ljust(25))
            

def main(json_obj_input, json_obj_ocr) :
    input_valid, error_index = is_input_valid(json_obj_input, json_obj_ocr)
    input_mismatch_printer(input_valid, error_index)
        
            


if __name__ == "__main__" :
    main(json_obj_input, json_obj_ocr)