from DocumentParser import TextExtraction
from wand.image import Image
import shutil, os, json, configparser, datetime

config = configparser.RawConfigParser()
config.read('configs.ini')

################## Split the PDF into multiple jpg using pdf2jpg library ###########################

def readPDF(path):
    final_dir = path.split('\\')[-1].split('.')[0]
    output_loc = config.get('paths', 'pdf2img') + "/" + final_dir + "/"

    if not os.path.isdir(output_loc):
        os.mkdir(output_loc)
    if not os.path.isdir(output_loc + 'img/'):
        os.mkdir(output_loc + 'img/')

    with Image(filename=path) as img:
        print('pages = ', len(img.sequence))

        with img.convert('jpg') as converted:
            converted.save(filename=output_loc + 'img/tempImg.jpg')

    billInfo = []
    files = os.listdir(output_loc + 'img/')

    for i in files:
        info = TextExtraction.extractText(output_loc + "img/" + i)
        billInfo.append(info)

    res = {"Result": billInfo}
    print(billInfo)
    res_json = json.dumps(res)
    print(res_json)

###################################################################################################
