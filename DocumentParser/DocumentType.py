import configparser
import difflib

config = configparser.RawConfigParser()
config.read('configs.ini')

aadhaar = config.get('document_keywords', 'aadhaar').split(",")
pan = config.get('document_keywords', 'pan').split(",")
voter_ID = config.get('document_keywords', 'voter_ID').split(",")
driving_licence = config.get('document_keywords', 'driving_licence').split(",")

doc_list = [aadhaar, pan, voter_ID, driving_licence]
doc_names = ['aadhaar', 'pan', 'voter_ID', 'driving_licence']


def getDocumentType(entire_text):
    text = entire_text.lower()
    found = 0

    for i in range(len(doc_list)):
        found = findWhichDoc(doc_list[i], text)
        if found == 1:
            doctype = doc_names[i]
            print("Document Type is", doctype)
            return doctype

    print("not found")
    return "Not Found"


def findWhichDoc(doc, text):
    found = 0
    count = 0
    for j in doc:
        if text.find(j) != -1:
            count += 1
            # change to count >1 or count >2 for stricter check
            if count > 0:
                found = 1
                break

    if found == 0:
        found = getDocFuzzy(doc, text)

    return found


def getDocFuzzy(doc, text):
    text_list = text.replace("\n", " ").split(" ")
    for i in doc:
        j = len(i.split(" "))
        k = 0
        while k < len(text_list):
            words = " ".join(text_list[k:k + j])
            k += int(j / 3) + 1
            if difflib.SequenceMatcher(None, words.lower(), i.lower()).ratio() > 0.7:
                return 1
    return 0


