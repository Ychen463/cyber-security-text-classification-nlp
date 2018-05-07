import re
from glob import glob
import os


import io
from os import listdir
from os.path import isfile, join

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text



directory = '#Your_PDF_dicrectory'

for file_path in listdir(directory):
    country = str(file_path).split("_", 1)[0]
    fileName = file_path.replace('.pdf', '')
    text = convert_pdf_to_txt(directory + '/' + file_path)  # Convert pdf to txt

    outputfilename = "txt/" + re.sub(r"[^A-Za-z]+", '', fileName) + ".txt"
    with open(outputfilename, 'w', encoding='utf-8') as f:
        f.write(text)
        f.close()

    print(country, fileName)
