# -*- coding: utf-8 -*-
import telebot
from main import Worker

bot = telebot.TeleBot('5466647879:AAGE9Ixf1dWXVtRpCCMbZuPxsrQlP73cktE')
worker = Worker()

@bot.message_handler(commands = ['start'])
def start(message):
    auth = worker.is_auth(message.chat.id)
    if auth:
        bot.send_message(message.chat.id, "Доступ разрешен!\nМожете выполнить запрос")
        bot.register_next_step_handler(message, message_handler)
    else:
        bot.send_message(message.chat.id, "Добро пожаловать!\nДля доступа необходимо ввести логин/пароль.")
        bot.send_message(message.chat.id, "Начнем с логина. Введите логин: ")
        bot.register_next_step_handler(message, check_login)

def check_password(message, name):
    password = message.text
    access = worker.grant_access(name=name, password=password,chat_id=str(message.chat.id))
    if access:
        bot.send_message(message.chat.id, "Доступ разрешен!\nМожете выполнить запрос")
        bot.register_next_step_handler(message, message_handler)
    else:
        bot.send_message(message.chat.id, "Доступ запрещен!\nНеверный логин/пароль.\nПопробуйте снова")
        bot.send_message(message.chat.id, "Начнем с логина. Введите логин: ")
        bot.register_next_step_handler(message, check_login)

def check_login(message):
    name = message.text
    bot.send_message(message.chat.id, "Принято!\nТеперь введите пароль: ")
    bot.register_next_step_handler(message, check_password, name)
    

@bot.message_handler(func=lambda call: True)
def message_handler(message):
    auth = worker.is_auth(message.chat.id)
    if not auth:
        bot.send_message(message.chat.id, 'Вы не авторизованы!')
        bot.send_message(message.chat.id, "Начнем с логина.\nВведите логин: ")
        bot.register_next_step_handler(message, check_login)
    else:
        result = worker.find_data(message.text)
        if result:
            for line in result:
                if line:
                    bot.send_message(message.chat.id, line)
        else:
            bot.send_message(message.chat.id, 'Информация по узлу не найдена!')

if __name__ == '__main__':
    path = ''
    response = input('Задаем путь в ручную?\nВведите путь к файлу базы узлов, включая формат файла xlsx: ')
    if response == 'no':
        #path = '//home//kort//usel-bot//Usel_Bot//file.xlsx'
        path = 'file.xlsx'
    else:
        path = response
    worker.start(path)
    bot.polling(none_stop=True)
