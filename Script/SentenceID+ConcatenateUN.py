
# coding: utf-8

# In[2]:


import os
from os import listdir
from os.path import isfile, join


# In[106]:


import pandas as pd
import csv


# # Read csv file

# In[69]:


directory = 'C:/Users/gisel/Desktop/Cyber-master/Analysis Result_UN_Doc'
csv_path = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".csv")]
AllFileName = [file.replace('.csv','') for file in os.listdir(directory) if file.endswith(".csv")]
BigFrame = pd.DataFrame()
list_ = []


# In[90]:


df_from_each_file = (pd.read_csv(f) for f in csv_path)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
concatenated_df['Doc ID'] = concatenated_df.groupby('Source Document').ngroup()+1
concatenated_df['Page No.'] = ['{:02d}'.format(i) for i in concatenated_df['Page No.']]
concatenated_df['Sentence No. of Doc'] = [str(i).zfill(2) for i in concatenated_df['Sentence No. of Doc']]
concatenated_df['Doc ID'] = [str(i).zfill(2) for i in concatenated_df['Doc ID']]
concatenated_df['Sentence ID'] = concatenated_df['Doc ID'] + concatenated_df['Page No.'] + concatenated_df['Sentence No. of Doc'] 
concatenated_df.applymap(str)


# In[108]:


outputfilename = r'C:\Users\gisel\Desktop\UN Project\Script\UN_Concatenate.csv'
concatenated_df.to_csv(outputfilename, encoding='utf-8', index=False)

