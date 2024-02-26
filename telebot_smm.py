import time
import schedule
import telebot

from main import Main
from settings import BOT_TOKEN
from telebot import types
from selenium.common.exceptions import TimeoutException

bot = telebot.TeleBot(BOT_TOKEN)


def run_telebot():
    urls = ['vypryamiteli-volos', 'smartfony-android']
    for url in urls:
        try:
            Main(url).start()
        except TimeoutException:
            Main(url).start()
    bot.send_document('1315757744', open(r'/Users/macos/Desktop/Обучение/best_price/price.xlsx', 'rb'))


schedule.every().day.at("08:38").do(run_telebot)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Рад тебя видеть в нашем телеграм канале")
    bot.send_message(message.chat.id, "Каждый день сюда будет присылаться файл Exel со всеми категориями, если вашей категории нет, напишите @rvstrizh")
    while True:
        schedule.run_pending()
        time.sleep(600)


if __name__ == "__main__":
    bot.polling()