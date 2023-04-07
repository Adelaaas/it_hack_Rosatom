import pandas as pd
from data_preprocessing import preprocessing
from lemmatization import lemmatize

import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud

df = pd.read_csv("C:/Users/Аделя/Desktop/hack карьерный клуб/it_hack_Rosatom/distribution of by topics.csv")

topics_df = df[['Count', 'Name', 'words']]

data = topics_df['words'].value_counts().to_dict()
print(data)


# plt.figure()
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()