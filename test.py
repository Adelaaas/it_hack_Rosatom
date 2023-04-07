import pandas as pd
from data_preprocessing import preprocessing
from lemmatization import lemmatize

import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud

from model import model_create_learn, text_generate

df = pd.read_csv("C:/Users/Аделя/Desktop/hack карьерный клуб/it_hack_Rosatom/distribution of by topics.csv")

print("HERE")
data = df['words'].value_counts().reset_index()
data.columns = ['words', 'Count']

data = text_generate(data)

data['meaningful_topics'] = data['meaningful_topics'].str.replace('\\n\\n','')
data['meaningful_topics'] = data['meaningful_topics'].str.replace('"','')

print(data)
data = data.set_index('meaningful_topics')['Count'].to_dict()
print(data)