import telebot
from telebot import types
import pandas as pd
import os
import requests
from get_topic import get_topics
import datetime
from io import BytesIO

token = '6153532423:AAHw9OPg9I5VDX_Vaqare6VZuHB4-wvxHWM'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True)
    btn_info = types.KeyboardButton("Посмотреть инструкцию")
    btn_work = types.KeyboardButton("Начать работу")
    btn_alg = types.KeyboardButton("Посмотреть информацию об алгоритме")
    markup.add(btn_info, btn_work, btn_alg)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!\nЯ Бот созданный для организаторов Проектной практики ИИКС!\nВыбери действие, которое ты хочешь выполнить.".format(message.from_user), reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Посмотреть инструкцию"):
        text = f'Данный бот предназначен для распределения групп/студентов по темам проектной практики ИИКС.\n\n' \
        f'Чтобы все сработало правильно загружаемый файл для распределения должен быть определенного формата:\n\n' \
        f'1. Формат файла должен быть <b>.csv</b>\n\n' \
        f'2. В файле должна быть следующая структура колонок:\n' \
        f'Группа | Тема 1. Название | ... | Тема n. Название\n' \
        f'<i>(Где группа - это номер пары или ФИО студента(ов)</i>\n\n' \
        f'3. Ячейки по желаниям должны быть обязательно заполнены следующими фразами:\n' \
        f'Очень хотим, Не против, Все равно, Не хотим, Не заставите <i>(именно такие названия, с заглавными буквами)</i>\n\n' \
        f'Пример <a href="https://clck.ru/33j7kc">входного файла</a>. \n\n'\
        f'<i>P.s. Из google таблицы файл в формате .csv можно сохранить следующим образом:</i>\n'\
        f'<i>Файл -> Скачать -> Формат CSV (.csv)</i>'
        bot.send_message(message.chat.id, text=text, parse_mode='HTML')
    
    elif(message.text == "Начать работу"):
        bot.send_message(message.chat.id, "Пришлите файл для обработки")
        bot.register_next_step_handler(message, document_processing)

    elif(message.text == "Посмотреть информацию об алгоритме"):
        text = f'Данный бот предназначен для распределения групп/студентов по темам проектной практики ИИКС.\n\n' \
        f'Распределение тем для студентов основано на <a href="https://clck.ru/33j8Mf">Венгерском алгоримте.</a>\n\n' \
        f'Для его реализации используется библиотека <a href="https://pypi.org/project/munkres/">munkres.</a>\n\n'

        bot.send_message(message.chat.id, text=text, parse_mode='HTML')
    
    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммировал..")

def document_processing(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    path = file_info.file_path # Вот тут-то и полный путь до файла (например: 'documents/file_4.csv')
    fname = os.path.basename(path) # Преобразуем путь в имя файла (например: 'documents/file_4.csv')
    
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path)) 

    with open('data.csv', 'wb') as f:
        f.write(doc.content)

    df = pd.read_csv('data.csv')

    df = get_topics(df)

    now = str(datetime.datetime.today()).split()[0]
    output_name = f'distribution of students by topics_{now}.csv'
    df.to_csv(output_name)
    with open(output_name, 'rb') as doc:
        bot.send_document(message.chat.id, doc)


if __name__ == '__main__':
   bot.polling(none_stop=True)