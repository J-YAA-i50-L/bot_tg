import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    BaseHandler
from for_db import *
from geocod import *
from work_of_xlsx import *

# Enable logging
logging.basicConfig(filename='logging.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
                    )

logger = logging.getLogger(__name__)

TOKEN = "6018046007:AAFLor0c0bG_vXOWDN-a6s5cR-7Bas8gqlA"


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
    print(1)
    await update.message.reply_text('Команды: \n "/catalog" - показывает каталог товаров магазина \n')


async def document_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит xls файл, когда будет выдана команда /document."""
    if is_status(update.effective_user.id):
        get_info_for_base()
        await update.message.reply_document(document='Таблица_Excel_БД.xlsx')
    else:
        await update.message.reply_text('У вас нет прав для данной команды.')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторите сообщение пользователя."""
    await update.message.reply_text(update.message.text)


async def doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ждет файл xlxs т администратора"""
    await update.message.reply_text('Отпавте файл xlsx с изминениями')
    return 0


async def document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторите сообщение пользователя."""
    get_info_for_base()
    await update.message.reply_document('Таблица_Excel_БД.xlsx')


async def statys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Назначает пользователя администратором, когда будет выдана команда /statys [password]."""
    password = update.message.text[8:]
    user = update.effective_user
    if password == '1234':
        remove_status(user.id)
        await update.message.reply_html(rf"{user.mention_html()} назначен администратором!",
                                        reply_markup=ForceReply(selective=True),)
    else:
        await update.message.reply_text('У вас нет прав!!!')


async def check_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Повторите сообщение пользователя."""
    user = update.effective_user
    a = update.message.document
    if not a:
        await update.message.reply_text('не то')
        return ConversationHandler.END

    get_file_of_tg(a.file_id, TOKEN)
    if not check_file_of_tg():
        await update.message.reply_text('pppp')
    else:
        await update.message.reply_text('Полностью ')
        return 1
    return ConversationHandler.END


async def remove_bzd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dow_remove_for_tg(update.message.text)
    await update.message.reply_document('Таблица_Excel_БД.xlsx')


async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит список разделов товаров, когда будет выдана команда /catalog."""
    await update.message.reply_text('Католог товаров у нас большой:\n'
                                    ' 1 -Наборы\n - Детская косметика\n 2 - Лаки, пенки для волос, расчёски\n'
                                    ' 3 - Уход за волосами в домашних условиях\n 4 - Косметика Мирра Люкс\n'
                                    ' 5 - Insight профуход за волосами\n 6 - Крема для лица, тела и рук, очищение\n'
                                    ' 7 - Женские духи\n 8 - Парфюм Niche- духи унисекс\n'
                                    ' 9 - Elements- парфюм унисекс\n'
                                    ' 10 - Продукция с Aloe Vera \n'
                                    'Выбирете интересующий вас раздел(В ведите название или номер)')
    return 0


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
    try:
        maps = maps_global()
        print(maps)
        await update.message.reply_photo(maps)
        await update.message.reply_text('У нас две точки по адресам:'
                                        '\n\t 1. г.Арзамас, просп. Ленина, 121, TЦ «Метро» 3 здание, 1 этаж'
                                        '\n\t 2. г.Арзамас, Парковая ул., 14А, ТЦ «Славянский»,1 этаж, отдел номер 7')
    except RuntimeError as ex:
        await update.message.reply_text('Что то пошло не по плану')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Магазины на карте, когда будет выдана команда /geo."""
    await update.message.reply_text('stop')
    return ConversationHandler.END


async def asortiment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Магазины на карте, когда будет выдана команда /geo."""
    text = update.message.text
    number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    name = ['Наборы', 'Детская косметика', 'Лаки, пенки для волос, расчёски', ' Уход за волосами в домашних условиях',
            'Косметика Мирра Люкс', 'Insight профуход за волосами', 'Крема для лица, тела и рук, очищение',
            'Женские духи', 'Парфюм Niche- духи унисекс', 'Elements- парфюм унисекс', 'Продукция с Aloe Vera']
    if text in number:
        get_assort(int(text))
    else:
        print(text)



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


async def work_schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправит график работы магазинов, когда будет выдана команда /catalog."""
    await update.message.reply_text('У нас два магазина: \n'
                                    ' - Магазин по адресу г.Арзамас, Парковая ул., 14А, ТЦ «Славянский». \n'
                                    'Работает по графику: \n\t пн – пт 9.00-19.00 \n\t сб – вс 9.00-18.00 \n'
                                    ' - Магазин по адресу г.Арзамас, просп. Ленина, 121, TЦ «Метро». \n'
                                    'Работает по графику: \n\t пн – вс 9.00-20.00 \n'
                                    'Будем вас в наших магазинах, '
                                    'их место положение можно узнать с помощью команды /geo')


def main() -> None:
    """Запустите бота."""
    # Создайте приложение и передайте ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()
    script_registration = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('doc_post', doc)],
        # Состояние внутри диалога.
        states={
            0: [MessageHandler(filters.ALL & ~filters.COMMAND, check_file)],
            1: [MessageHandler(filters.ALL & ~filters.COMMAND, remove_bzd)]
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        allow_reentry=False,
        fallbacks=[CommandHandler('stop', stop)]
    )
    script_catalog = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('catalog', catalog_command)],
        # Состояние внутри диалога.
        states={
            0: [MessageHandler(filters.ALL & ~filters.COMMAND, check_file)],
            # 1: [MessageHandler(filters.ALL & ~filters.COMMAND, remove_bzd)]
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        allow_reentry=False,
        fallbacks=[CommandHandler('stop', stop)]
    )
    # по разным командам - отвечайте в Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("statys", statys))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("catalog", catalog_command))
    application.add_handler(CommandHandler("contacts", contacts_command))
    application.add_handler(CommandHandler("administrator", admin_command))
    application.add_handler(CommandHandler("geo", geo_command))
    application.add_handler(CommandHandler("joining_the_club", joining_the_club_command))
    application.add_handler(CommandHandler("club_of_privileges", club_of_privileges_command))
    application.add_handler(CommandHandler("dnt", document))
    application.add_handler(script_registration)
    application.add_handler(script_catalog)
    application.add_handler(CommandHandler("document", document_command))
    application.add_handler(CommandHandler("work_schedule", work_schedule_command))

    # по некомандному, то есть сообщению - повторить сообщение в Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    createBD()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускайте бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
