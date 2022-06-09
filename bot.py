# -*- coding: utf-8 -*-
import telebot
from main import Worker

bot = telebot.TeleBot('5466647879:AAGE9Ixf1dWXVtRpCCMbZuPxsrQlP73cktE')
worker = Worker()

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, "Let's go")

@bot.message_handler(func=lambda call: True)
def message_handler(message):
    print(message.text)
    result = worker.find_data(message.text)
    for line in result:
        bot.send_message(message.chat.id, line)

if __name__ == '__main__':
    #path = input('Введите путь к файлу базы узлов, включая формат файла xlsx: ')
    path = '//home//kort//usel-bot//Usel_Bot//file.xlsx'
    worker.start(path)
    bot.polling(none_stop=True)
