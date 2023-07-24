TOKEN = '6394797230:AAFu1TExJBWPVXm3Crc2pisnX7r5WPDA8_Q'
BOT_USERNAME = '@learning_t_bot_bot'

from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters

async def hello_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello world!')

def handle_response(text: str):
    processed = text.lower()
    if 'привет' in processed:
        return 'И тебе привет!'
    else:
        return 'Пока я умею только здороваться'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = handle_response(text)
    await update.message.reply_text(response)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('hello_world', hello_world))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling(poll_interval=3)