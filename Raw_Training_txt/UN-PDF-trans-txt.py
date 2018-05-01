
# coding: utf-8

# In[1]:


import re
from glob import glob
import os
from os import listdir
from os.path import isfile, join


# # PDF to txt

# # Define Function: PDF_to_txt

# In[2]:


import io

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


# In[3]:


directory = r"#your_PDF_directories"
categoryList = os.listdir(directory)
outputTXTdirectory = r"#your_txt_directories"


# In[4]:


categoryList


# In[8]:


category_num = 0
for category in categoryList:
    category_path = glob(directory+"\\" +category)
    subcategories = os.listdir(directory+"\\" +category)
    category_num +=1
    for subcategory in subcategories:
        subcategory_path = glob(directory+"\\" +category +"\\" + subcategory +'\*')
        pdf_num = 0
        for pdf_path in subcategory_path:
            pdfName = os.listdir(directory+"\\" +category + "\\" +subcategory)[pdf_num].replace(".pdf","")
            pdf_num +=1
            print(category_num,pdf_num, pdfName)


# In[9]:


for category in categoryList:
    category_path = glob(directory+"\\" +category)
    subcategories = os.listdir(directory+"\\" +category)
    for subcategory in subcategories:
        subcategory_path = glob(directory+"\\" +category +"\\" + subcategory +'\*')
        pdf_num = 0
        for pdf_path in subcategory_path:
            pdfName = os.listdir(directory+"\\" +category + "\\" +subcategory)[pdf_num].replace(".pdf","")
            try: 
                text = convert_pdf_to_txt(pdf_path)
            except:
                print("error:" , pdf_num, pdfName)
            
            outputfilename = outputTXTdirectory+"\\"+ category + "\\" +subcategory +"\\"+pdfName+ ".txt"
            if not os.path.exists(outputTXTdirectory+"\\"+ category + "\\" +subcategory):
                os.makedirs(outputTXTdirectory+"\\"+ category + "\\" +subcategory)  
            with open(outputfilename, 'w',encoding='utf-8') as f:
                f.write(text)
                f.close()
            pdf_num +=1
            print(pdf_num, pdfName)

