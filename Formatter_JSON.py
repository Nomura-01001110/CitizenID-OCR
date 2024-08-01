import re
import json

# Function to extract information
def extract_information(text_detections):
    fields = {
        'Овог Family name': 
            {'mn': '', 'en': '', 'confidence_mn': '', 'confidence_en': ''},
        'Эцэг/эх/-ийн нэр Surname': 
            {'mn': '', 'en': '', 'confidence_mn': '', 'confidence_en': ''},
        'Нэр Given name': 
            {'mn': '', 'en': '', 'confidence_mn': '', 'confidence_en': ''},
        'Хуйс Sex': 
            {'mn': '', 'en': '', 'confidence_mn': '', 'confidence_en': ''},
        'Терсен он, cap, едер Date of birth': 
            {'year': '', 'month': '', 'day': '', 'confidence_mn': '', 'confidence_en': ''},
        'Регистрийн дугаар Registration number': 
            {'mn': '', 'en': '', 'confidence_mn': '', 'confidence_en': ''}
    }

    """
        Go through dummy json
        Match cases: find family name for example
        When case found, save the id
            The id will be used to extract text: will extract text until next field index
        
    """

    text_map = {item['Id']: item for item in text_detections}

    # Extracting using regex
    for field in fields.keys():
        if field == 'Хуйс Sex':
            text = text_map[12]['DetectedText']
            arr = text.split('/')
            fields[field]['mn'] = arr[0].strip()
            fields[field]['en'] = arr[1].strip()
        elif field == 'Регистрийн дугаар Registration number':
            text = text_map[18]['DetectedText']
            arr = text.split('/')
            fields[field]['mn'] = arr[0].strip()
            fields[field]['en'] = arr[1].strip()
        elif field == 'Терсен он, cap, едер Date of birth':
            text = text_map[16]['DetectedText']
            text = text.strip().split('/')
            if len(text) == 3:
                fields[field]['year'] = text[0]
                fields[field]['month'] = text[1]
                fields[field]['day'] = text[2]
        else:
            # Get corresponding values for each field
            for item in text_detections:
                if item['DetectedText'].startswith(field):
                    field_id = item['Id']
                    fields[field]['mn'] = text_map[field_id + 1]['DetectedText']
                    fields[field]['en'] = text_map[field_id + 2]['DetectedText']
                    break

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



def main() :
    # Load data from dummy.json
    with open('dummy.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extracted information
    fields = extract_information(data['TextDetections'])
    
    # Creating JSON
    json_obj = create_json(fields)
    
    # Save JSON to file
    with open('output_1.json', 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)
    
    print("Formatted JSON:\n", json.dumps(json_obj, ensure_ascii=False, indent=4))


if __name__ == "__main__" :
    main()
    