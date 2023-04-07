import pandas as pd
from data_preprocessing import preprocessing
from lemmatization import lemmatize

import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud

df = pd.read_csv("C:/Users/Аделя/Desktop/hack карьерный клуб/it_hack_Rosatom/distribution of by topics.csv")

topics_df = df[['Count', 'Name', 'words']]

print(topics_df)

topics_df = topics_df.drop_duplicates()

print(topics_df)

full_dict = list(zip(topics_df['words'], topics_df['Count']))

wordcloud = WordCloud(max_font_size=100,
                  relative_scaling=.5,
                  background_color="white",
                  colormap='viridis_r')
wordcloud = wordcloud.generate_from_frequencies(dict(full_dict))
wordcloud.to_file("simple_wordcloud.png")
# plt.figure()
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()