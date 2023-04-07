# Data processing
import pandas as pd
import numpy as np
# Text preprocessiong
import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('omw-1.4')
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()
# Topic model
# import umap.umap_ as UMAP
from bertopic import BERTopic
from flair.embeddings import TransformerDocumentEmbeddings, TransformerWordEmbeddings, DocumentPoolEmbeddings
# Dimension reduction
from umap import UMAP
# 
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer

import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud

def model_create_learn(df):

    sentence_model = TransformerWordEmbeddings('cointegrated/rubert-tiny2')
    document_embeddings = DocumentPoolEmbeddings([sentence_model])

    # Reduce dimensionality
    umap_model = UMAP(n_neighbors=15, 
                    n_components=5, 
                    min_dist=0.0, 
                    metric='cosine', 
                    random_state=100)

    # Cluster reduced embeddings
    hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

    # Tokenize topics
    vectorizer_model = CountVectorizer()

    # Create topic representation
    ctfidf_model = ClassTfidfTransformer()

    topic_model = BERTopic(
        embedding_model = document_embeddings,
        umap_model = umap_model,
        hdbscan_model = hdbscan_model,
        vectorizer_model = vectorizer_model,
        ctfidf_model = ctfidf_model,
        n_gram_range=(1,3),
        calculate_probabilities=True,
        language="russian"
    )

    topics, probabilities = topic_model.fit_transform(df['cleaned_answers_lemm'])
    df['Topic'] = topics

    topics_df = topic_model.get_topic_info()
    topics_df['words'] = topics_df['Name'].str.split('_').apply(lambda x: x[1:])
    result = df.merge(topics_df, on=['Topic'])

    return result

# def plot_cloud(df):
#     topics_df = df[['Count', 'Name', 'words']]
#     print(topics_df)
#     data = topics_df['words'].value_counts().to_dict()
#     print('dfkdlfk__________________')
#     print(data)

#     wordcloud = WordCloud(max_font_size=100,
#                     relative_scaling=.5,
#                     background_color="white",
#                     colormap='viridis_r')    

#     wordcloud = wordcloud.generate_from_frequencies(data)
#     wordcloud.to_file("simple_wordcloud.png")

if __name__ == '__main__':
    PATH = 'INPUT YOUR PATH TO PREPARED DATASET'
    PATH = 'C:/Users/Аделя/Desktop/hack карьерный клуб/it_hack_Rosatom/distribution of by topics.csv'
    df = pd.read_csv(PATH)

    # result = model_create_learn(df)
    # result = plot_cloud(df)

    print(result)