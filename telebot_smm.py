import json
import time
import schedule
import telebot
import  random
from main import Main
from settings import BOT_TOKEN
from selenium.common.exceptions import TimeoutException

bot = telebot.TeleBot(BOT_TOKEN)


def save_json(id):
    users_id = {}
    users_id[id] = id
    users_id |= open_json()
    print(users_id)
    with open('/Users/macos/Desktop/Обучение/best_price/data.json', 'w') as f:
        json.dump(users_id, f)


def open_json():
    with open('/Users/macos/Desktop/Обучение/best_price/data.json', 'r') as f:
        return json.load(f)


def run_telebot():
    urls = ['vypryamiteli-volos', 'smartfony-android']
    # for url in urls:
    #     try:
    #         Main(url).start()
    #     except TimeoutException:
    #         Main(url).start()
    dt = open_json()
    for _, user in dt.items():
        bot.send_document(user, open(r'/Users/macos/Desktop/Обучение/best_price/price.xlsx', 'rb'))


def run():
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        bot.send_message(1315757744, f"Произошла ошибка: {e}")


schedule.every(15).seconds.do(run_telebot)
# schedule.every().day.at("08:38").do(run_telebot)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Рад тебя видеть в нашем телеграм канале")
    bot.send_message(message.chat.id, "Каждый день сюда будет присылаться файл Exel со всеми категориями, если вашей категории нет, напишите @rvstrizh")
    save_json(str(message.chat.id))


if __name__ == "__main__":
    # 1315757744
    try:
        bot.polling()
        run()
    except Exception as e:
        bot.send_message(1315757744, f"Произошла ошибка: {e}")
