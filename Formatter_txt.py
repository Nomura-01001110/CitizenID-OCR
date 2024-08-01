import re
import json

# Sample text
text = """
МОНГОЛ УЛСЫН ИРГЭНИЙ ҮНЭМЛЭХ
CITIZEN IDENTITY CARD OF MONGOLIA
Овог Family name
Пингүйн
Penguin
Эцэг/эх/-ийн нэр Surname
Смит
Smith
Нэр Given name
Пороро
Pororo
Хуйс Sex
Эрэгтэй /Male
Терсен он, cap, едер
Date of birth
1901/01/3
Регистрийн дугаар Registration number
УЦ01234567 / UTs01234567
"""

# Function to extract information
def extract_information(text) :
    fields = {
        'Овог Family name': {'mn': '', 'en': ''},
        'Эцэг/эх/-ийн нэр Surname': {'mn': '', 'en': ''},
        'Нэр Given name': {'mn': '', 'en': ''},
        'Хуйс Sex': {'mn': '', 'en': ''},
        'Терсен он, cap, едер Date of birth': {'year': '', 'month': '', 'day': ''},
        'Регистрийн дугаар Registration number': {'mn': '', 'en': ''}
    }

    # Extracting using regex
    for field in fields.keys():
        if field == 'Хуйс Sex':
            pattern = f"{field}\n(.*)\n"
            match = re.search(pattern, text)
            if match:
                arr = match.group(1).split('/')
                fields[field]['mn'] = arr[0].strip()
                fields[field]['en'] = arr[1].strip()

        elif field == 'Регистрийн дугаар Registration number':
            pattern = f"{field}\n(.*)\n"
            match = re.search(pattern, text)
            if match:
                arr = match.group(1).split('/')
                fields[field]['mn'] = arr[0].strip()
                fields[field]['en'] = arr[1].strip()
        elif field == 'Терсен он, cap, едер Date of birth':
            pattern_date = "Date of birth\n(.*)\n"
            match_date = re.search(pattern_date, text)
            if match_date:
                date_parts = match_date.group(1).strip().split('/')
                if len(date_parts) == 3:
                    fields[field]['year'] = date_parts[0]
                    fields[field]['month'] = date_parts[1]
                    fields[field]['day'] = date_parts[2]
        else:
            pattern_mn = f"{field}\n(.*)\n"
            pattern_en = f"{field}\n.*\n(.*)\n"
            match_mn = re.search(pattern_mn, text)
            match_en = re.search(pattern_en, text)

            if match_mn:
                fields[field]['mn'] = match_mn.group(1).strip()
            if match_en:
                fields[field]['en'] = match_en.group(1).strip()

    return fields

# Function to create JSON structure
def create_json(fields):
    json_obj = {
        'Fields': [],
        'LowConfidenceLines': [],
        'LowConfidenceWords': []
    }

    for field, values in fields.items():
        if field == 'Терсен он, cap, едер Date of birth':
            field_json = {
                field: {
                    'year': values['year'],
                    'month': values['month'],
                    'day': values['day'],
                    'Confidence': 99
                }
            }
        else:
            field_json = {
                field: {
                    'mn': values['mn'],
                    'Confidence_mn': 99,
                    'en': values['en'],
                    'Confidence_en': 99
                }
            }
        json_obj['Fields'].append(field_json)

    return json_obj

# Extracted information
fields = extract_information(text)

# Creating JSON
json_obj = create_json(fields)

# Save JSON to file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=4)

print("Formatted JSON:\n", json.dumps(json_obj, ensure_ascii=False, indent=4))