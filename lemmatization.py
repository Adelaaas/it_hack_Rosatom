import pymorphy2
import pandas as pd 


def lemmatize(df):

    def converter(sentence):

        list = []
        words = sentence.split()
        for word in words:
            list.append(morph.parse(word)[0].normal_form)
        return ' '.join(list)

    # train = pd.read_csv("C:/Users/Аделя/Desktop/hack карьерный клуб/prapared_data.csv")
    morph = pymorphy2.MorphAnalyzer()
    # # train = train.iloc[:5,:]
    # print(train)

    df = df[df["Number of Words"] > 2]

    df['cleaned_answers_lemm'] = df['cleaned_answers'].apply(converter)

    # df.to_csv("C:/Users/Аделя/Desktop/hack карьерный клуб/prapared_data_with_lemm.csv", index=False)

    return df