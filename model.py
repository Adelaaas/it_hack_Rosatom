# Data processing
import pandas as pd
import numpy as np
# Text preprocessiong
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('omw-1.4')
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()
# Topic model
# from bertopic import BERTopic
from flair.embeddings import TransformerDocumentEmbeddings, TransformerWordEmbeddings, DocumentPoolEmbeddings
# Dimension reduction
# from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
# from bertopic.vectorizers import ClassTfidfTransformer

import re

def test(df):
    print("TEST")
    print(df.shape)

# sentence_model = TransformerWordEmbeddings('cointegrated/rubert-tiny2')
# document_embeddings = DocumentPoolEmbeddings([sentence_model])

# Reduce dimensionality
# umap_model = UMAP(n_neighbors=15, 
#                   n_components=5, 
#                   min_dist=0.0, 
#                   metric='cosine', 
#                   random_state=100)

# Cluster reduced embeddings
# hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

# Tokenize topics
vectorizer_model = CountVectorizer()

# Create topic representation
# ctfidf_model = ClassTfidfTransformer()

# topic_model_v1 = BERTopic(
#     embedding_model = document_embeddings_v1,
#     umap_model = umap_model,
#     hdbscan_model = hdbscan_model,
#     vectorizer_model = vectorizer_model,
#     ctfidf_model = ctfidf_model,
#     n_gram_range=(1,3),
#     calculate_probabilities=True,
#     language="russian"
# )

# topics_v1, probabilities_v1 = topic_model_v1.fit_transform(df['cleaned_answers_lemm'])