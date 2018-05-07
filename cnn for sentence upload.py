import os

import sys

import numpy as np

from keras.preprocessing.text import Tokenizer

from keras.preprocessing.sequence import pad_sequences

from keras.utils import to_categorical

from keras.layers import Dense, Input, GlobalMaxPooling1D

from keras.layers import Conv1D, MaxPooling1D, Embedding

from keras.models import Model

import pickle




BASE_DIR = ''

GLOVE_DIR = os.path.join(BASE_DIR, 'glove.6B')

TEXT_DATA_DIR = os.path.join(BASE_DIR, '20_newsgroup')

MAX_SEQUENCE_LENGTH = 100

MAX_NUM_WORDS = 20000

EMBEDDING_DIM = 100

VALIDATION_SPLIT = 0.2



# first, build index mapping words in the embeddings set

# to their embedding vector



print('Indexing word vectors.')



embeddings_index={}

with open(os.path.join(r'D:\UN cybersecurity material\cnn material\glove', 'glove.6B.100d.txt'),encoding='utf-8') as f:

    for line in f:

        values = line.split()

        word = values[0]

        coefs = np.asarray(values[1:], dtype='float32')

        embeddings_index[word] = coefs



print('Found %s word vectors.' % len(embeddings_index))



#for i in range(10):
#    print(i)

#filepath=r'D:\UN cybersecurity material\Training_clean_tf_wf'
#for i in os.listdir(filepath):
#    with open(os.path.join(filepath,i,'total %s.txt' %(i)),'w',encoding='utf-8') as g:
#        for file in os.listdir(os.path.join(filepath,i)):
#            if 'txt' in file:
#                with open(os.path.join(filepath,i,file),encoding='utf-8') as f:
#                    g.write(f.read()+'\n')


# second, prepare text samples and their labels

# print('Processing text dataset')
#
#
# filepath=r'D:\UN cybersecurity material\Training_clean_tf_wf\CAPACITY BUILDING'
# texts = []  # list of text samples
#
# labels_index = {}  # dictionary mapping label name to numeric id
#
# labels = []  # list of label ids
#
# for name in os.listdir(filepath):
#     if ('total' in name) & ('csv' in name):
#         continue
#
#     path = os.path.join(filepath, name)
#
#     #if os.path.isdir(path):
#
#         label_id = len(labels_index)
#
#         labels_index[name] = label_id
#
#         #for fname in os.listdir(path):
#
#             #fpath = os.path.join(path, 'total %s.txt'%(name))
#
#             #args = {} if sys.version_info < (3,) else {'encoding': 'latin-1'}
#
#             with open(fpath, encoding='utf-8') as f:
#
#                 t = f.read()
#
#                 t=t.split('\n')
#
#                 texts.extend(t)
#
#                 labels = labels + [name] * len(t)
#
#
#
#
#
# print('Found %s texts.' % len(texts))






print('Processing text dataset')


filepath=r'D:\UN cybersecurity material\Training_clean_tf_wf\CAPACITY BUILDING'
texts = []  # list of text samples

labels_index = {}  # dictionary mapping label name to numeric id

labels = []  # list of label ids

for name in os.listdir(filepath):
    if ('total' in name) | ('csv' in name)|('h5' in name):
        continue

    path = os.path.join(filepath, name)

    #if os.path.isdir(path):

    label_id = len(labels_index)

    labels_index[name[:-4]] = label_id

        #for fname in os.listdir(path):

            #fpath = os.path.join(path, 'total %s.txt'%(name))

            #args = {} if sys.version_info < (3,) else {'encoding': 'latin-1'}

    with open(path, 'rb') as f:

        t = f.read()

        t=t.split(b'\n')
        g=[]
        for element in t:
            try:
                g.append(element.decode('utf-8'))
            except:
                continue
        texts.extend(g)

        labels = labels + [name[:-4]] * len(g)





print('Found %s texts.' % len(texts))





# finally, vectorize the text samples into a 2D integer tensor
if os.path.isfile(r'D:\UN cybersecurity material\cnn material\model and tokenizer file\un cnn tokenizer.pickle'):
    with open(r'D:\UN cybersecurity material\cnn material\model and tokenizer file\un cnn tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
else:


    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)

    tokenizer.fit_on_texts(texts)

    with open(r'D:\UN cybersecurity material\cnn material\model and tokenizer file\un cnn tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

sequences = tokenizer.texts_to_sequences(texts)



word_index = tokenizer.word_index

print('Found %s unique tokens.' % len(word_index))



data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)



labels = to_categorical([labels_index[i] for i in labels])


print('Shape of data tensor:', data.shape)

print('Shape of label tensor:', labels.shape)



# split the data into a training set and a validation set

indices = np.arange(data.shape[0])

np.random.shuffle(indices)

data = data[indices]

labels = labels[indices]

num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])



x_train = data[:-num_validation_samples]
y_train = labels[:-num_validation_samples]

x_val = data[-num_validation_samples:]

y_val = labels[-num_validation_samples:]



print('Preparing embedding matrix.')



# prepare embedding matrix

num_words = min(MAX_NUM_WORDS, len(word_index) + 1)

embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))

for word, i in word_index.items():

    if i >= MAX_NUM_WORDS:

        continue

    embedding_vector = embeddings_index.get(word)

    if embedding_vector is not None:

        # words not found in embedding index will be all-zeros.

        embedding_matrix[i] = embedding_vector



# load pre-trained word embeddings into an Embedding layer

# note that we set trainable = False so as to keep the embeddings fixed


embedding_layer = Embedding(num_words,

                            EMBEDDING_DIM,

                            weights=[embedding_matrix],

                            input_length=MAX_SEQUENCE_LENGTH,

                            trainable=True)



print('Training model.')



# train a 1D convnet with global maxpooling

sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')

embedded_sequences = embedding_layer(sequence_input)

x = Conv1D(128, 5, activation='relu',padding='same')(embedded_sequences)

x = MaxPooling1D(5)(x)

x = Conv1D(128, 5, activation='relu',padding='same')(x)

x = MaxPooling1D(5)(x)

x = Conv1D(128, 5, activation='relu',padding='same')(x)

x = GlobalMaxPooling1D()(x)

x = Dense(128, activation='relu')(x)

preds = Dense(len(labels_index), activation='softmax')(x)



model = Model(sequence_input, preds)

model.compile(loss='categorical_crossentropy',

              optimizer='rmsprop',

              metrics=['acc'])



model.fit(data, labels,

          batch_size=128,

          epochs=10,

          validation_data=(x_val, y_val))

model.save(r'D:\UN cybersecurity material\Training_clean_tf_wf\CAPACITY BUILDING\CAPACITY BUILDING subcategory.h5')

print(labels_index)












