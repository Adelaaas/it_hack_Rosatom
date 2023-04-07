import pymorphy2
import pandas as pd 

def lemmatize(df):

    def converter(sentence):

        list = []
        words = sentence.split()
        for word in words:
            list.append(morph.parse(word)[0].normal_form)
        return ' '.join(list)

    morph = pymorphy2.MorphAnalyzer()

    df = df[df["Number of Words"] > 2]

    df['cleaned_answers_lemm'] = df['cleaned_answers'].apply(converter)

    return df

if __name__ == '__main__':
    PATH = 'INPUT YOUR PATH TO FILE'
    df = pd.read_csv(PATH)

    df = lemmatize(df)

    print(df)