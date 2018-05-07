
# coding: utf-8

# In[1]:


import re
from glob import glob
import os
from os import listdir
from os.path import isfile, join
import io


from string import punctuation


# In[2]:


from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

from nltk.tokenize import sent_tokenize

import pandas as pd
import re
import string


# In[3]:


import logging
#logging.root.handlers
logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)


# # PDF into csv with page No.

# transform pdf into csv with page No. Sentence No.

# In[38]:


def convert_pdf_to_txt_csv(path):  
    retstr = io.StringIO()
    codec = 'utf-8'
    
    df = pd.DataFrame()
    
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    #Create DataFrame
    df = pd.DataFrame()
    
    page_list = []
    sent_list = []
    n=0
    for page in doc.get_pages():
        n += 1
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine) :
                t = lt_obj.get_text()
                t = re.sub('\\d+',' ',t)
                t = t.replace('.....',' ')
                t = re.sub('[\s+]', ' ', t)
                t = re.sub(' +',' ',t)
                t = sent_tokenize(t)
                if len(t) > 0:
                    for each in t:
                        sent_list.append(each)
                        page_list.append(n)
                else:
                    t = ''.join(t)
                    page_list.append(n)
                    sent_list.append(t)
                                  

   
    df['Page No.'] = page_list
    df['Sentence']  = sent_list
       
    #Clean dataframe
    df = df[df.Sentence != ' ']
    
    #Filter sentence which len() >
    mask = (df['Sentence'].str.len() > 10)
    df = df.loc[mask]
    

    #Remove duplicate
    df = df.drop_duplicates('Sentence',keep = 'first', inplace=False)
    
    #Set Sentencec No. of Doc
    df['Sentence No. of Doc'] = df.groupby('Page No.').cumcount()+1

    #FileName
    fileName = os.path.basename(path)
    df['Source Document'] = fileName
    
    #Country Name
    Country = fileName.split('_')[0]
    df['Country'] = Country

    fp.close()
    return df


# In[39]:


path = 'C:/Users/gisel/Desktop/UN Project/Official Data/AllPDF\\Afghanistan_2014_National Cybersecurity Strategy of Afghanistan (November2014).pdf'
df = convert_pdf_to_txt_csv(path)
df


# # Read all PDF file

# In[40]:


directory = 'C:/Users/gisel/Desktop/UN Project/Official Data/AllPDF'
pdf_path = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".pdf")]
fileName = [file.replace('.pdf','') for file in os.listdir(directory) if file.endswith(".pdf")]


# # Main Function

# In[43]:


for path in pdf_path:
    try:
        df = convert_pdf_to_txt_csv(path)
        
        #file_Name
        fileName = str(path).split("\\",1)[1]
        df.loc[:,'Source Document'] = fileName
    
    except:
        print(fileName+' Failed!!')

    #write to csv
    outputfilename = "C:/Users/gisel/Desktop/Cyber-master/Analysis Result_UN_Doc/"+ fileName.replace('.pdf',".csv")
    df.to_csv(outputfilename, encoding='utf-8', index=False)
    
    print(fileName.replace('.pdf',".csv"))

