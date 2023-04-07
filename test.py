import pandas as pd
from data_preprocessing import preprocessing
from lemmatization import lemmatize

df = pd.read_excel("C:/Users/Аделя/Desktop/hack карьерный клуб/Массив для хакатона МИФИ.xlsx")
# df.drop(columns=['Unnamed: 0'], inplace=True)
df.columns = ['Answers']

print(df)

df = preprocessing(df)
df = lemmatize(df)

print(df)