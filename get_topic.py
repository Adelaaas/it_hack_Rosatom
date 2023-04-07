from munkres import Munkres, DISALLOWED, UnsolvableMatrix
import munkres
import pandas as pd 
import numpy as np
import os

def _get_cost(matrix):
    m = Munkres()
    indices = m.compute(matrix)
    lst = []
    for row, column in indices:
        lst.append(column)
    # return sum([matrix[row][column] for row, column in indices])
    return lst

def get_topics(df):

    try:
        df = df.iloc[np.random.permutation(len(df))]
        df = df.reset_index(drop=True)
        d = {'Очень хотим': 0, 'Не против': 1, 'Все равно': 2, 'Не хотим': 3, 'Не заставите': 4}
        
        try:
            df2 = df.drop(['Группа'], axis=1)
        except:
            err = f'Проверьте, что колонка с номером пары или ФИО студента называется "Группа"'
            return err  

        cols = df2.columns

        if sorted(set(d.keys())) != sorted(pd.unique(df2[cols].values.ravel())):
            err = f'Проверьте, что значения в ячейках именно такие: {set(d.keys())}'
            return err  
        else:
            for i in cols:
                df2[i] = df2[i].map(d).fillna(df2[i])

            matrix = np.array(df2)
            topics = _get_cost(matrix)

            c = df2.columns
            df['topic'] = topics
            df['topic'] += 1    
            df['topics'] = c[topics]

            # df.to_csv('predictiont_pp_students.csv', encoding='utf-8')
            return df
    except:
        err = 'Что-то пошло не так, посмотрите инструкцию и попробуйте еще раз'
        return err

if __name__ == '__main__':

    # df = pd.read_csv("D:\Загрузки\Распределение тем Проектной практики ИИКС (1 курс, весна 2023) (Ответы) - Для Адели.csv")
    # df = pd.read_csv("D:\Загрузки\sample_submission (2).csv")
    # print(get_topics(df))
    dirname = os.path.dirname(__file__)
    print(dirname)
    # pass