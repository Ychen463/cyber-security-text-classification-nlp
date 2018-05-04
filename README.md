 Cyber
-------------
We primarily used two methods for sentence classification: One is supervised learning. Another is unsupervied.

-------------
For unsupervised learning we:


1. Preprocess text (tokenizing/remove stopwords/stemming) 2.calculate tf-idf matrix to change raw text into vector space 3.calculate cosine distance between different sentence 4. use k-means to do clustering for text 5. use PCA to visualize data

future update: find the best number of clustering/ use lda to do topic modeling

--------------
For supervised learning we:

1.Crawl the raw data from articles from google based on the categories because we assumed that the google search engine will give us the most related result.

2. Use word frequency and tfidf extract key words for each category. Then use key words to extract traning sentences from crawled data and policy data.

3. Use google translation as a way of sentence paraphrase to double the number of training sentences.

4. Use CNN to classify sentence.
