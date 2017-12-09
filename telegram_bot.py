import os
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from ai_engine.nlu_wrappers.dialogflow import DialogFlowClient

TOKEN = "391437242:AAG3xkWlG1O4MGKAQu_zWVhUp07TAiRuwfw"
PORT = int(os.environ.get("PORT", "5000"))

class TelegramBot(object):

    def __init__(self, token, port, url):
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.dialogflow_client = DialogFlowClient()
        self.add_dispatchers()
        self.url = url
        self.port = port

    def start_web_hook(self):
        self.updater.start_webhook(listen="0.0.0.0", port=self.port, url_path="telegram")
        self.dispatcher = self.updater.dispatcher
        self.updater.bot.set_webhook(self.url + "telegram")
        self.updater.idle()

    def add_dispatchers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.conversation))

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="What's up?")

    def conversation(self, bot, update):
        msg = update.message.text
        output = self.dialogflow_client.response(msg, "Telegram", update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id, text=output["msg"])

if __name__ == "__main__":
    bot = TelegramBot(TOKEN, PORT, "https://pure-refuge-87808.herokuapp.com/")
    bot.start_web_hook()
