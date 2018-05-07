# Cyber

Co-authors: Yanlin Chen, Yunjian Wei, Yifan Yu, Wen Xue, Xianya Qin


#Methodology
Supervised Learning

(1) Data Collection

Based on the suggested labels given by the headers in the cyber wellness profiles, we search category keywords in google and use Selenium to crawl the content of top 20 search results, and use this data as training data. Our training goal is to optimize the accuracy of classifying a sentence.

(2) Data Processing

The policy documents were originally in PDF format. We use python with PDFMiner to transform into text file. From the documents of 63 countries,  22053 sentences were extracted at last, which are assigned with different document ID, Sentence ID (unique), Page No. and Sentence No. of the Document.

(3) Text Mining

We use word2vec method to project each word into a 100 dimension and numeric vector so that similar words will be close to each other in the vector space. It makes the model robust to synonym. Then we use cnn to capture the context of a sentence, which means cnn can predict data on the sentence level other than word level. Combining the two methods together makes our model have a strong generalization ability.

#Unsupervised Learning
(1) Data Processing

First we apply a common way to deal with the raw data. Tokenize whole text to words for future tf-idf matrix calculation. Removing some meaningless but high frequent words is very important, in case these words would influence our results.

(2) PCA dimension reduction

Due to high dimension of our matrix, we decide to use principal component analysis to do dimension reduction. PCA can keep the most of the characteristic of the data to present the whole data. In this matrix, we find 200 dimension can explain about 70% of the data. Therefore, we only keep 200 columns to show our whole data.

(3) Hierarchical clustering

Hierarchical clustering is a method of clustering analysis which seeks to build a hierarchical clusters between each point. We use hierarchical clustering to see clusters.

(4) K-means

K-means is another method to do clustering under unsupervised learning. It randomly chooses point as centroid point, and calculate the distance to cluster each point. Then it would recalculate and correct the centroid point until it won’t change. And it is difficult to set the exact number of clusters.

(5) LDA topic extraction

After six overall categories generated, we put these text under different groups in LDA model we build to explore subcategories. We can extract important words under each groups and find the similarities to form sub themes.  

#Sentence search engine

This tool enables users to interact with the data and the classification result we got. Once the user choose a country, the information of categorized sentences will show up as follows, which can give user an overall understanding of the Cyber Security policies of this country. Users can choose different categories and subcategories which they are interested in.
