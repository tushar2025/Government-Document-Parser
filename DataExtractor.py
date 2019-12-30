from DocumentParser import TextExtraction
import json
import pandas as pd
import io, re, configparser
from DocumentParser import PDFtoJPEGConverter

config = configparser.RawConfigParser()
config.read('configs.ini')

path = '../pdfs/test.pdf'

PDFtoJPEGConverter.readPDF(path)
