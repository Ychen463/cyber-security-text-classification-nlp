import os

import sys

import numpy as np

from keras.preprocessing.text import Tokenizer

from keras.preprocessing.sequence import pad_sequences

from keras.utils import to_categorical

from keras.layers import Dense, Input, GlobalMaxPooling1D

from keras.layers import Conv1D, MaxPooling1D, Embedding

from keras.models import Model

from keras.models import load_model

import pickle

import pandas as pd

MAX_SEQUENCE_LENGTH = 100

# get category and subcategory, and their trained model
mainmodel=load_model(r'D:\UN cybersecurity material\main category.h5')
catepath=r'D:\UN cybersecurity material\Training_clean_tf_wf'
category={}
for i in os.listdir(catepath):
    subcategory=[]
    subpath=os.path.join(catepath,i)
    if os.path.isdir(subpath):
        globals()[i]=load_model(os.path.join(subpath,'%s subcategory.h5'%(i)))
        for filename in os.listdir(subpath):
            if 'csv' in filename:
                subcategory.append(filename[:-4])

    category[i]=subcategory

# load tokenizer
if os.path.isfile(r'D:\UN cybersecurity material\cnn material\model and tokenizer file\un cnn tokenizer.pickle'):
    with open(r'D:\UN cybersecurity material\cnn material\model and tokenizer file\un cnn tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

def main_cate(df):
    if df.max()>0.6:
        return(df.idxmax(axis=1))
    else:
        return('category unknown')

def sub_cate(df):
    try:
        if df['category']=='category unknown':
            return('category unknown')
        else:
            sequences=globals()['tokenizer'].texts_to_sequences([df['Sentence']])
            data = pad_sequences(sequences, maxlen=globals()['MAX_SEQUENCE_LENGTH'])
            result=globals()[df['category']].predict(data)

            if result[0][result.argmax()]>0:

                return(globals()['category'][df['category']][result.argmax()])
    except:
        print(df)






# read and predict
#filepath=r'D:\UN cybersecurity material\Analysis Result_UN_Doc'
# for i in os.listdir(filepath):
#     if os.path.isfile(os.path.join(filepath,i)):
#         df = pd.read_csv(os.path.join(filepath,i))
df=pd.read_csv(r'C:\Users\luca\Documents\WeChat Files\weiyunjian002\Files\UN_Concatenate.csv')
texts=list(df['Sentence'])
# transform target data
sequences = tokenizer.texts_to_sequences(texts)

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

main_result=mainmodel.predict(data)
main_result_df=pd.DataFrame(main_result,columns=['CAPACITY BUILDING','CHILD ONLINE PROTECTION',
                                      'COOPERATION','LEGAL MEASURES',
                                      'ORGANIZATION MEASURES','TECHNICAL MEASURES'])
df['category']=main_result_df.apply(main_cate, axis=1)
df['sub category']=df.apply(sub_cate,axis=1)
df.to_csv(r'D:\UN cybersecurity material\final UN concatenate.csv',index=False)









