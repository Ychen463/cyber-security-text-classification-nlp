
# coding: utf-8

# In[266]:


import csv
import pandas as pd
import numpy as np
import re
import unicodedata

import io
import os
from os import listdir
from os.path import isfile, join
import os.path


# # Read all File

# In[267]:


directory = 'C:/Users/gisel/Desktop/WF'
category_list = [category for category in listdir(directory)]
subcategory_name_list =[]
dic = {}
for category in category_list:
    subcategories = [subcategory for subcategory in listdir(directory+'/'+category)]
    subcategory_name = [s.replace('.csv','') for s in subcategories]
    dic[category] = subcategory_name
    subcategory_name_list.append(subcategory_name)


# In[268]:


def freList(wf_path):
    df_wf = pd.read_csv(wf_path)
    fre_word = [i for i in df_wf.iloc[:,0][0:30]]
    return fre_word


# In[269]:


def tfidfList(tfidf_path, subcategory):
    df_tfidf = pd.read_csv(tfidf_path, encoding = "ISO-8859-1")
    df_tfidf = df_tfidf.sort_values(by=[subcategory],ascending=False)
    
    tfidf_word = [i for i in df_tfidf.loc[:,'word'][0:30]]
    return tfidf_word


# In[270]:


def matchwords(wf_path, tfidf_path, subcategory):
    wf_word = freList(wf_path)
    tfidf_word = tfidfList(tfidf_path, subcategory)
    fre_tf_inter = list(set(wf_word).intersection(tfidf_word))
    return fre_tf_inter


# # Clean RawTrain

# In[271]:


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import sent_tokenize
import nltk


# In[262]:


def Train_sentence_csv(txt_path):
    with open(txt_path, 'r') as RawTrain:
        RawTrain = RawTrain.read()
    
        #split into sentences
        text = unicodedata.normalize("NFKD", RawTrain)
        text = re.sub('\\n',' ',text)
        sentences = sent_tokenize(text)
        df_sent = pd.DataFrame(columns = ['No.','Sentence','StemWords','MatchWords'])
        for n, sent in enumerate(sentences):
            df_sent.loc[n, 'No.'] = n
            df_sent.loc[n, 'Sentence'] = sent
    
        #Split into words
        stop_words = set(stopwords.words('english'))
        #Use Porter Stemmer 
        porter = nltk.PorterStemmer()
    
        stemWordsList = []
        MatchWordsList = []
        for n, sent in enumerate(sentences):
            tokens = word_tokenize(sent)
            words = [w.lower() for w in tokens if w.isalpha() if w.lower()not in stop_words]
            stemwords = [porter.stem(w) for w in words]
            stemWordsList.append(stemwords)

            MatchWords = set(fre_tf_inter).intersection(stemwords)
            MatchWordsList.append(MatchWords)

        df_sent['StemWords']= stemWordsList   
        df_sent['MatchWords']=MatchWordsList
        df_sent['Use'] = np.where(df_sent['MatchWords'] == set(), 'N', 'Y')
        return df_sent
    
    


# # Output File

# In[223]:


def output_sent_csv(txt_path,output_scv_path):
    df_sent = Train_sentence_csv(txt_path)
    df_sent.to_csv(output_scv_path,index=False)


# In[295]:


def ouput_useful_txt(txt_path, output_txt_path):
    df_sent = Train_sentence_csv(txt_path)
    useful_sent = df_sent.loc[df_sent['Use'] == 'Y']['Sentence']
    
    file = open(output_txt_path,'w', encoding = "utf-8") 
    sent = [i for i in useful_sent]
    sent = '\n'.join(sent)
    file.write(sent) 
    file.close() 


# In[296]:


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# # Main Function

# In[297]:


txtpath_list=[]
for n,category in enumerate(category_list):
    for subcategory in dic[category_list[n]]:
        wf_path = "C:/Users/gisel/Desktop/WF/" + category_list[n]+'/'+ subcategory+'.csv'
        tfidf_path = "C:/Users/gisel/Desktop/un crawl raw data/tfidf/"+ category_list[n] + " tfidf.csv"
        
        
        txt_path = "C:/Users/gisel/Desktop/Cyber-master/Raw_Training_txt_combine/"+ category_list[n]+'/'+ subcategory+'.txt'
        txtpath_list.append(txt_path)
        
        output_scv_path = "C:/Users/gisel/Desktop/Cyber-master/Training_clean_tf_wf/"+ category_list[n]+'/'+ subcategory+'.csv'
        output_txt_path = "C:/Users/gisel/Desktop/Cyber-master/Training_clean_tf_wf/"+ category_list[n]+'/'+ subcategory+'.txt'

        directory = os.path.dirname(output_scv_path)

        try:
            os.stat(directory)
        except:
            os.mkdir(directory) 
            
        
        
        
        output_sent_csv(txt_path,output_scv_path)

        
        ouput_useful_txt(txt_path, output_txt_path)
        print(n,category,subcategory)

