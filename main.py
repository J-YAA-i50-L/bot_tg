#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(filename='logging.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
                    )

logger = logging.getLogger(__name__)

TOKEN = "5729933786:AAE4etvixT0i7ZdRbVR5mnsB2RhwpNtnPuk"


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит список команд, когда будет выдана команда /help."""
    await update.message.reply_text('Команды: \n "/catalog" - показывает католог товаров магазина \n')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторите сообщение пользователя."""
    await update.message.reply_text(update.message.text)


async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит список разделов товаров, когда будет выдана команда /help."""
    await update.message.reply_text('Ккуку ёпта')


async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит вырианты связи с магазином, когда будет выдана команда /help."""
    await update.message.reply_text('У нас есть сайт, на котором можно нати много полезной информации. \n'
                                    'Также присоединяйтесь к нам ВКонтакте.\n'
                                    'Вконтакте: https://vk.com/soblaznarzamas \n'
                                    'Сайт: https://soblaznarz.uds.app/c/join?ref=xvvs0921 \n')


def main() -> None:
    """Запустите бота."""
    # Создайте приложение и передайте ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()

    # по разным командам - отвечайте в Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("catalog", catalog_command))
    application.add_handler(CommandHandler("contacts", contacts_command))

    # по некомандному, то есть сообщению - повторить сообщение в Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускайте бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
