from telegram import *
from telegram.ext import *
 
updater = Updater(token="1645397769:AAHKOuDWH7YLzP3uPp9wqBrc9wYr2NLLpHs", use_context=True)
dispatcher = updater.dispatcher
 
def send(update:Update, context:CallbackContext):
    update.message.reply_text(update.to_dict())
 
send_handler = MessageHandler(Filters.all, send)
dispatcher.add_handler(send_handler)
 
updater.start_polling()

updater.idle()