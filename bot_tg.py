import telebot
from telebot import types
import pandas as pd
import os
import requests
import datetime
from io import BytesIO
from model import model_create_learn, text_generate    
from data_preprocessing import preprocessing
from lemmatization import lemmatize

import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud

import config

token = config.bot_token
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True)
    btn_info = types.KeyboardButton("Посмотреть инструкцию")
    btn_work = types.KeyboardButton("Начать работу")
    btn_alg = types.KeyboardButton("Посмотреть информацию об алгоритме")
    markup.add(btn_info, btn_work, btn_alg)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!\nЯ Бот созданный в рамках хакатона «Шаг в карьеру: ИТ»\nВыбери действие, которое ты хочешь выполнить.".format(message.from_user), reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Посмотреть инструкцию"):
        text = f'Для работы загрузите файл в форме <b>.xlsx</b>.\n\n' \
        f'В файле должна присутсвовать одна колонка:\n\n' \
        f'1. В 0 строке вопрос\n\n' \
        f'2. В остальных строках ответ на этот вопрос от разных участников опроса.'
        bot.send_message(message.chat.id, text=text, parse_mode='HTML')
    
    elif(message.text == "Начать работу"):
        bot.send_message(message.chat.id, "Пришлите файл для обработки")
        bot.register_next_step_handler(message, document_processing)

    elif(message.text == "Посмотреть информацию об алгоритме"):
        text = f'Данный раздел в разработке\n\n' \
        f'Полный исходный код проекта можно посмотреть на <a href="https://github.com/Adelaaas/it_hack_Rosatom">git.</a>'

        bot.send_message(message.chat.id, text=text, parse_mode='HTML')
    
    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован..")

def document_processing(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    path = file_info.file_path # Вот тут-то и полный путь до файла (например: 'documents/file_4.csv')
    fname = os.path.basename(path) # Преобразуем путь в имя файла (например: 'documents/file_4.csv')
    
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path)) 

    with open('data.xlsx', 'wb') as f:
        f.write(doc.content)

    bot.send_message(message.chat.id, text="Please wait this may take some time...")

    """ Тут начинается обработка полученного файла (предобработка, кластеризация и выделение топиков (тем))"""
    df = pd.read_excel('data.xlsx')
    df.columns = ['Answers']

    print("Data preprocessing")
    df = preprocessing(df)
    df = lemmatize(df)

    print("Bulding model")
    df = model_create_learn(df)

    """ Тут идёт визуализация топиков (cloud), сохранение картинки и отправка пользователю """
    data = df['Name'].value_counts().to_dict()

    wordcloud = WordCloud(max_font_size=100,
                    relative_scaling=.5,
                    background_color="white",
                    colormap='viridis_r')    
    
    wordcloud = wordcloud.generate_from_frequencies(data)
    wordcloud.to_file("simple_wordcloud.png")

    text = f'Данное облако сформировано по набору слов для каждого кластера ответов.\n\n' \
        f'Всего модель после обучения сформировала {len(data)} кластеров, объединенные по смыслу\n\n'
    bot.send_message(message.chat.id, text=text, parse_mode='HTML')

    img = open("simple_wordcloud.png", 'rb')
    bot.send_photo(message.chat.id, img)

    """ Генерация осмысленных фраз описывающих кластеры/топики
    И построения облака для этих фраз"""
    # print('ChatGPT meaningful topic phrases generate from words')
    data = df['words'].value_counts().reset_index()
    data.columns = ['words', 'Count']

    data = text_generate(data)

    data['meaningful_topics'] = data['meaningful_topics'].str.replace('\\n\\n','')
    data['meaningful_topics'] = data['meaningful_topics'].str.replace('"','')

    data = data.set_index('meaningful_topics')['Count'].to_dict()

    wordcloud = WordCloud(max_font_size=100,
                    relative_scaling=.5,
                    background_color="white",
                    colormap='viridis_r')    
    
    wordcloud = wordcloud.generate_from_frequencies(data)
    wordcloud.to_file("advantage_wordcloud.png")

    text = f'Данное облако сформировано по осмысленным фразам для каждого кластера ответов.\n\n' \
        f'Осмысленные фразы были сгенерированы по набору слов для кластера с помощью ChatGPT.\n\n' \
        f'Всего модель после обучения сформировала {len(data)} кластеров, объединенные по смыслу\n\n'
    bot.send_message(message.chat.id, text=text, parse_mode='HTML')

    img = open("advantage_wordcloud.png", 'rb')
    bot.send_photo(message.chat.id, img)


    """ Добавление в исходный файл к каждому ответу предсказанный топик и возврат пользвателю """
    print("Dataset and predicted topic to each answer file")
    text = f'В ваш исходный файл добавлена еще одна колонка, в которой.\n\n' \
        f'указана тема для каждого ответа, полученная после обучения\n'
    bot.send_message(message.chat.id, text=text, parse_mode='HTML')

    output_name = f'distribution of by topics.csv'
    df[['Answers', 'words']].to_csv(output_name)
    with open(output_name, 'rb') as doc:
        bot.send_document(message.chat.id, doc)


if __name__ == '__main__':
   bot.polling(none_stop=True, interval=0)