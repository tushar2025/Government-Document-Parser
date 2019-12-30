from google.cloud import vision
from google.cloud.vision import types
import io, re, configparser
from sympy import Point, Line, Segment
import datetime
from dateutil.parser import parse
from DocumentParser import DocumentType

config = configparser.RawConfigParser()
config.read('configs.ini')

bag_of_words_total = config.get('bag_of_words', 'total').split(",")
bag_of_words_phnum = config.get('bag_of_words', 'phone_number').split(",")


####################################################################################################

def extractText(path):
    print("\nExtracting Text from bill: " + path.split("\\")[-1])

    # Vision API call for text detection
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as path:
        content = path.read()

    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    words = []
    entire_text = ""

    for i in range(len(texts)):
        if i == 0:
            entire_text = texts[i].description

        else:
            words.append([texts[i].description, texts[i].bounding_poly])

    document_type = DocumentType.getDocumentType(entire_text)

    print(document_type)

    temp_dict = {}

    temp_dict['Document_Type'] = document_type

    if document_type == 'aadhaar':
        temp_dict['Name'] = getAadhaarName(entire_text)
        temp_dict['Number'] = getAadhaarNo(entire_text)

    elif document_type == 'pan':
        temp_dict['Name'] = getPanName(entire_text)
        temp_dict['Number'] = getPanNo(entire_text)

    return temp_dict


################################ Convert date to common format #####################################

def getAadhaarNo(entire_text):
    info = entire_text
    print(info)
    num_reg_ex = re.compile(r'\b(\d{4}\s?\d{4}\s?\d{4}\s?)\b')
    info = [x.group() for x in num_reg_ex.finditer(info)]

    if len(info) > 0:
        a_number = info[0].replace("\n", "").replace(" ", "")
        return a_number

    return "Not Found"


def getAadhaarName(entire_text):
    found = 0
    index = -1
    words_to_find = ['जन्म तिथि', ' DOB']

    for i in words_to_find:
        index = entire_text.find(i)
        if index != -1:
            found = 1
            break

    if found == 0:

        date_reg_ex = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')
        info = [x.group() for x in date_reg_ex.finditer(entire_text)]

        if len(info) > 0:
            index = entire_text.find(info[0])

    name_text = entire_text[:index + 1].split('\n')
    print(name_text)
    if len(name_text) > 1:
        name = name_text[-2]
        return name

    return "Not Found"


def getPanNo(entire_text):
    info = entire_text
    num_reg_ex = re.compile(r'\b([A-Za-z]{5}\d{4}[A-Za-z])\b')

    info = [x.group() for x in num_reg_ex.finditer(info)]

    if (len(info) > 0):
        pan_number = info[0].replace("\n", "").replace(" ", "")
        return pan_number

    return "Not Found"


def getPanName(entire_text):
    words_remove = ['भारत सरकार', 'GOVT. OF INDIA']
    string_to_find = "INCOME TAX DEPARTMENT".lower()

    index = entire_text.lower().find(string_to_find)
    entire_text = entire_text[index:].split('\n')

    name_text = [x for x in entire_text if x not in words_remove]

    if len(name_text) > 1:
        return name_text[1]

    return "Not Found"