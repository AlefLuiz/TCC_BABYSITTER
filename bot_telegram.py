import telebot
import threading
from mic_record import MicRecord

bot = telebot.TeleBot("1576597570:AAEWf3F0UmEw4M5b3vL6uxC2Z-66X3c9wCs", parse_mode=None)

monitorar = False
mic_record = MicRecord()
threads = []

def run(message, bot: telebot.TeleBot):
    while monitorar:
        predict_dict = mic_record.chamar_api()
        if predict_dict["baby"] > 80:
            bot.reply_to(message, "Seu bebê está chorando!")

@bot.message_handler(commands=['iniciar_monitoramento'])
def send_welcome(message):
    global monitorar

    bot.reply_to(message, "Estou de prontidão para te avisar qualquer choro!")
    thread = threading.Thread(target=run, args=(message, bot))
    thread.start()
    monitorar = True
    threads.append(thread)

@bot.message_handler(commands=['desligar_monitoramento'])
def send_bye(message):
    global monitorar

    bot.reply_to(message, "Parando IA!")
    monitorar = False
    for thread in threads:
        thread.join()

bot.infinity_polling()