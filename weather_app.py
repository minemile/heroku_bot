import os
from telegram.ext import Updater
from telegram.ext import CommandHandler

TOKEN = "391437242:AAG3xkWlG1O4MGKAQu_zWVhUp07TAiRuwfw"
PORT = int(os.environ.get("PORT", "5000"))

class TelegramBot(object):

    def __init__(self, token, port):
        self.updater = Updater(token)
        self.updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
        self.dispatcher = self.updater.dispatcher
        self.add_dispatchers()
        self.updater.bot.set_webhook("https://pure-refuge-87808.herokuapp.com/" + token)
        print("INIT")
        self.updater.idle()
    
    def add_dispatchers(self):
        print("DISPATCHERS")
        self.dispatcher.add_handler(CommandHandler('start', self.start))

    def start(self, bot, update):
        print("START")
        bot.send_message(chat_id=update.message.chat_id, text="What's up?")
        
if __name__ == "__main__":
    bot = TelegramBot(TOKEN, PORT)
