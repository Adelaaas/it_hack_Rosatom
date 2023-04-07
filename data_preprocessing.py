import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re

# data preprocessing
def remove_punct(text):
    # удаление пунктуации в тексте
    table = {33: ' ', 34: ' ', 35: ' ', 36: ' ', 37: ' ', 38: ' ', 39: ' ', 40: ' ', 41: ' ', 42: ' ', 43: ' ', 44: ' ', 45: ' ', 46: ' ', 47: ' ', 58: ' ', 59: ' ', 60: ' ', 61: ' ', 62: ' ', 63: ' ', 64: ' ', 91: ' ', 92: ' ', 93: ' ', 94: ' ', 95: ' ', 96: ' ', 123: ' ', 124: ' ', 125: ' ', 126: ' '}
    return text.translate(table)

def data_prep(df):
    # count words
    russian_stopwords = stopwords.words("russian")
    
    df["Number of Words"] = df["Answers"].apply(lambda n: len(str(n).split()))

    # remove stopwors
    df['answers_without_stopwords'] = df['Answers'].apply(
        lambda x: ' '.join([word for word in str(x).split()if word not in (russian_stopwords)]))

    # remove puntuation
    df['cleaned_answers'] = df['answers_without_stopwords'].map(lambda x: remove_punct(x))

    # low case of text
    df['cleaned_answers'] = df['cleaned_answers'].str.lower()

    # remove digits
    for index, row in df.iterrows():
        df.loc[index, 'cleaned_answers'] = re.sub(r"\d+", "", row['cleaned_answers'])

    return df


def preprocessing(df):
    # url = 'https://raw.githubusercontent.com/Adelaaas/it_hack_Rosatom/main/%D0%9C%D0%B0%D1%81%D1%81%D0%B8%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D1%85%D0%B0%D0%BA%D0%B0%D1%82%D0%BE%D0%BD%D0%B0%20%D0%9C%D0%98%D0%A4%D0%98.csv'

    # df = pd.read_csv(url)
    # df.drop(columns=['Unnamed: 0'], inplace=True)
    # df.columns = ['Answers']

    df = data_prep(df)
    # df.to_csv('C:/Users/Аделя/Desktop/hack карьерный клуб/prapared_data.csv')

    return df