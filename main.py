import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from for_db import *

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
    cont.add_user(user.id, f"{user.first_name} {user.last_name}", user.username)
    await update.message.reply_html(rf"Hi {user.mention_html()}!", reply_markup=ForceReply(selective=True),)


async def statys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит список команд, когда будет выдана команда /help."""
    await update.message.reply_text('Команды: \n "/catalog" - показывает каталог товаров магазина \n')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторите сообщение пользователя."""
    await update.message.reply_text(update.message.text)


async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит список разделов товаров, когда будет выдана команда /catalog."""
    await update.message.reply_text('Ккуку ёпта')


async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит вырианты связи с магазином, когда будет выдана команда /contacts."""
    await update.message.reply_text('У нас есть сайт, на котором можно найти много полезной информации. \n'
                                    'Также присоединяйтесь к нам ВКонтакте.\n'
                                    'Вконтакте: https://vk.com/soblaznarzamas \n'
                                    'Сайт: https://soblaznarz.uds.app/c/join?ref=xvvs0921 \n')


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Связь с админимтратором, когда будет выдана команда /admin."""
    await update.message.reply_text('Администратор ответит на все интересующие вас вопросы. '
                                    'С ним можно связаться по телефону: +79202980333')


async def geo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Магазины на карте, когда будет выдана команда /geo."""
    await update.message.reply_text('я карта. я карта')


async def joining_the_club_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """вступления в Клуб Привилегий, когда будет выдана команда /joining_the_club."""
    await update.message.reply_text('Хочешь получать крутые преимущества? \n'
                                    'Вступай в Клуб Привилегий. Что бы вступить нужно сделать некоторые действия: \n'
                                    ' - Зайти в PlayMarket или AppStore и скачать приложение "UDS APP" \n'
                                    ' - Зарегистрироваться и перейти по ссылке: '
                                    'https://soblaznarz.uds.app/c/join?ref=dwac1210 \n'
                                    ' - Получите первые 100 баллов на бонусный счет! (1 балл = 1 рубль) \n'
                                    'Для того что бы ознокомиться с примуществами команда: /club_of_privileges')


async def club_of_privileges_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Преимущества Клуба Привилегий, когда будет выдана команда /club_of_privileges."""
    await update.message.reply_text('У нас есть Клуба Привилегий, участникам он даёт некоторые примущества:\n'
                                    ' - Получают скидку на первую покупку \n'
                                    ' - Получают персональные уведомления о новинках и акциях \n '
                                    ' - Копят баллы с каждой покупки и забирают товар БЕСПЛАТНО \n'
                                    ' - Рекомендуют нас друзьям и получают баллы с их покупок \n'
                                    'Что бы ознокомится с инструкцией вступления команда: /joining_the_club')


def main() -> None:
    """Запустите бота."""
    # Создайте приложение и передайте ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()

    # по разным командам - отвечайте в Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("catalog", catalog_command))
    application.add_handler(CommandHandler("contacts", contacts_command))
    application.add_handler(CommandHandler("administrator", admin_command))
    application.add_handler(CommandHandler("geo", geo_command))
    application.add_handler(CommandHandler("joining_the_club", joining_the_club_command))
    application.add_handler(CommandHandler("club_of_privileges", club_of_privileges_command))

    # по некомандному, то есть сообщению - повторить сообщение в Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускайте бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
