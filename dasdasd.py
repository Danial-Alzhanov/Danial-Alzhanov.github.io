import telebot
import schedule
import time
import threading

TOKEN = '7677435555:AAHLTOrBJJEJ4lKO6evvE6XIgVpm-XOIJdc'
bot = telebot.TeleBot(TOKEN)

user_data = {}
RECOMMENDED_WATER = 2000

def send_reminders():
    for user_id in user_data:
        try:
            bot.send_message(user_id, "Не забывай пить воду! Выпей стакан воды.")
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user_id}: {e}")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {'drank': 0}
    bot.reply_to(
        message,
        "Привет! Я помогу тебе не забывать пить воду.\n\n"
        "Команды:\n"
        "/setreminder N — напоминать каждые N часов\n"
        "/drank ML — я выпил ML мл воды\n"
        "/status — покажу, сколько ещё нужно выпить"
    )

@bot.message_handler(commands=['setreminder'])
def setreminder(message):
    user_id = message.chat.id
    try:
        hours = int(message.text.split()[1])
        interval = hours * 60
        schedule.clear(str(user_id))
        schedule.every(interval).minutes.do(send_reminders).tag(str(user_id))
        bot.reply_to(message, f"Напоминание установлено каждые {hours} ч.")
    except:
        bot.reply_to(message, "Пример: /setreminder 2")

@bot.message_handler(commands=['drank'])
def drank(message):
    user_id = message.chat.id
    try:
        amount = int(message.text.split()[1])
        if user_id not in user_data:
            user_data[user_id] = {'drank': 0}
        user_data[user_id]['drank'] += amount
        bot.reply_to(message, f"Принято! Выпито: {user_data[user_id]['drank']} мл")
    except:
        bot.reply_to(message, "Пример: /drank 300")

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.chat.id
    drank = user_data.get(user_id, {}).get('drank', 0)
    remaining = max(RECOMMENDED_WATER - drank, 0)
    bot.reply_to(message, f"Ты выпил {drank} мл. Осталось: {remaining} мл до 2 л.")

def main():
    threading.Thread(target=run_schedule, daemon=True).start()

    print("Бот запущен.")
    bot.polling()

if __name__ == "__main__":
    main()
