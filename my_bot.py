import logging
from telegram import Update, InlineQueryResultVoice
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота (временно добавим сюда напрямую)
TOKEN = '7737449740:AAEw81ud5wsEdzny1HBuyB60kuI_Z91VBX0'

# Данные о голосовых сообщениях (замените на реальные file_id)
voice_messages = [
    {"id": '1', "title": "Розыскадан келиб босишди", "file_id": 'AwACAgIAAxkBAAMDZwV3jnFUDj9JAAHYGL4N9nGbvKI3AAKyXwACSvkoSG-idjIy8r-gNgQ'}, 
    # ошна розыскадан келиб босишди икки кундан бери ашадедим
    {"id": '2', "title": "Силага кайп бўп қоптими а", "file_id": 'AwACAgIAAxkBAAMEZwV3lxqf-KfjfQY537upnNBfyKAAAnNfAALfIwhIuAQ_5KDaT_A2BA'},
    # силага кайп бўп қоптими а қанақадир таблоси узун мошинада ташкенни айланиб юраслар эканда а
    {"id": '3', "title": "Бўлди якшанба саунага чиқамиз", "file_id": 'AwACAgIAAxkBAANgZxamFcZVSUhmW197X6aOWODh0_QAAlY7AAI8rrhK0Ek31X39wN82BA'},
    # бўлди якшанба саунага чиқамиз
    {"id": '4', "title": "Мени аям группалариндан чикееет деган", "file_id": 'AwACAgIAAxkBAAMwZxaiQQ5rw_uXREr6OxDagsStxRgAAnYdAAJxLVlKKKn-81zcPA42BA'},
    # Блин дийиш мениям группалариндан чикип кееет деган яна қўшилволяпман э
    {"id": '5', "title": "Қадан бунақа гап келади калленга сени", "file_id": 'AwACAgIAAxkBAAMyZxaiufBlx775zG0tD_q6Pjihb6sAApNKAAIfGhhJxuKwsppIUcc2BA'},
    # Қадан бунақа гап келади калленга сени
    {"id": '6', "title": "Мениям кўнглим бор", "file_id": 'AwACAgIAAxkBAAM0Zxajap9gJXXI5KVFpJZMbupYnUYAAsAqAAIEN2FJNJbpWU4FlTI2BA'},
    # Насиниэмсин мениям кўнглим бор, мениям кўнглим оғрийди
    {"id": '7', "title": "Хазиллашиб қўйдимда пидараз", "file_id": 'AwACAgIAAxkBAAM2ZxajdBk3OXvrNTQa42njqhI9vxQAAsMqAAIEN2FJw8VJMa3Hn4I2BA'},
    # Хазиллашиб қўйдимда пидараз
    {"id": '8', "title": "Вариант қима менга", "file_id": 'AwACAgIAAxkBAAM4Zxajfcco_tE30MHfqdMFCdM18EsAAs4qAAIEN2FJCliStDmCZD42BA'},
    # Вариант қима менга
    {"id": '9', "title": "Тур йўқале нима деяпсан", "file_id": 'AwACAgIAAxkBAAM6ZxajiK7weU4O96GfT17iuTUjh6QAAh4rAAIEN2FJ3-RxCwo4mgY2BA'},
    # Тур йўқале нима деяпсан
    {"id": '10', "title": "Хее Андрюха нимўляпсан бле", "file_id": 'AwACAgIAAxkBAAM-ZxajoyH94Lx9QdCVx5lg11yfzmYAAisrAAIEN2FJRfO_HMjbxTU2BA'},
    # Хее Андрюха нима бўляпсан блее
    {"id": '11', "title": "Ха вошшем ёрворяпти", "file_id": 'AwACAgIAAxkBAANAZxajrEwvbg0iPlQFf0gL09m_ihMAAjMrAAIEN2FJJKeuHpRdsck2BA'},
    # Ха вошшем ёрворяпти
    {"id": '12', "title": "Кўт бўсенам дўсм бўласан", "file_id": 'AwACAgIAAxkBAANCZxalaZ4RevPuWaQ-_p5JsNidDCYAAo8yAALgBahIfJwiaCSzuE02BA'},
    # Кўт бўсенам дўсм бўласан
    {"id": '13', "title": "Вай жала.. тупойманда бле", "file_id": 'AwACAgIAAxkBAANEZxalcyxGVOLzekLQllZB7-M7aCAAAicvAALgBbBIHKJDq9b7PwM2BA'},
    # Вай жала... Битта харпни ўннига қўйип қўяман деб.. Тупойманда бле
    {"id": '14', "title": "Ёзип туровир минде", "file_id": 'AwACAgIAAxkBAANGZxalfLiluKtlQVjWPfPqPd6XJ0IAArQ6AAL1X2BJk-MbqTFdVIw2BA'},
    # Ха бу йўқ бўп кеттин ёзип туровир уяғ буяғ қилиб
    {"id": '15', "title": "Пашол нахуй дияппан", "file_id": 'AwACAgIAAxkBAANIZxalhfU2mRqH6JT8BrV-jTKsMmUAAh09AAKS6GlJGALjMQSFkh82BA'},
    # Пашол нахуй дияппан
    {"id": '16', "title": "Хааа ха бўпти", "file_id": 'AwACAgIAAxkBAANKZxalkabTnfawl8t3xYYPNNfvgTkAAiU0AAISQcBJZkZs_RKvjVA2BA'},
    # Хааа ха бўпти
    {"id": '17', "title": "Хушёр қайна", "file_id": 'AwACAgIAAxkBAANMZxalpfggO2zb3t88Wt3nQm3KjHIAArs1AAISQcBJLg6y5vWNcXc2BA'},
    # Ашинчун ўзинга эхтият бўлип юровир хушёр қайна
    {"id": '18', "title": "Хааааа", "file_id": 'AwACAgIAAxkBAANOZxalrRAUbL4NYU4y7h7gSVIVWVMAArs3AAJiPhhKHMkiJCvDRTo2BA'},
    # Хааааа
    {"id": '19', "title": "Бўпти хўп чунган бўсен", "file_id": 'AwACAgIAAxkBAANQZxalt10LQep4SD5eBvkU9WmI6UQAAv83AAK-tFBK9nuSUZCP5rw2BA'},
    # Бўпти хўп чунган бўсен
    {"id": '20', "title": "Ха бўпти яхши", "file_id": 'AwACAgIAAxkBAANSZxalxHUtrwo4FzzbI1-5kEH1c7UAAg8-AAKAOClKk-jOQnT8Ycc2BA'},
    # Ха бўпти, яхши
    {"id": '21', "title": "Миям ғалати бўпполди", "file_id": 'AwACAgIAAxkBAANUZxalzERfIgWVo1xFtOsoz4CFqvEAAsVEAALLq6lLs8C59eVXkFU2BA'},
    # Э хози нимўлди чунмадим миям ғалати бўпполди, кимдир бинаса дияпти
    {"id": '22', "title": "Бўпти ошна яхши дам олинг, иссиғроқ кийинволин", "file_id": 'AwACAgIAAxkBAANWZxal2z_fGK06G1JYb54xbVCc1FkAAvlOAAIOkvFIHsZV0QHLMnE2BA'},
    # Бўпти ошна яхши дам олинг тинч бўлинга иссиғроқ кийинволин
    {"id": '23', "title": "Жигарим раҳмат катта боризга шукур", "file_id": 'AwACAgIAAxkBAANYZxal55ETbH2-PeWRPGKnr7yzetkAAkROAAK4lXlJBimPYEdSI3w2BA'},
    # Жигарим раҳмат катта боризга шукур доим бор бўлинг
    {"id": '24', "title": "Орқада турган қизил футболкали қиз", "file_id": 'AwACAgIAAxkBAANaZxal7o-ekXFN2AEDMmE7VMKK6RcAAu5ZAAK4lYlJomozTuCbgH42BA'},
    # Орқадан турган қизил футболкали қиз чиройли қиз эдиканда бети кўринме қопти
    {"id": '25', "title": "Ваалайкум ассалом яхшимисизлар", "file_id": 'AwACAgIAAxkBAANcZxamAVXFhwlpiq2Q7N-22mFGEuAAAqM2AAKH0GFKJ3nWq-1BCQw2BA'},
    # Ваалайкум ассалом яхшимисизлар
    {"id": '26', "title": "Ошна мия кечро ишледими?", "file_id": 'AwACAgIAAxkBAANeZxamCzw5wMxv555hbNk7-LJHwn0AAkczAAL3jWFKaB-8Pbpm2902BA'},
    # Ошна мия кечро ишледими?
    
]

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду /start, отправляет приветственное сообщение пользователю.
    """
    await update.message.reply_text(
        'Используйте инлайн-режим для выбора голосового сообщения. '
        'Введите @имя_бота любой символ или слово.'
    )

# Функция для обработки инлайн-запросов
async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает инлайн-запросы и возвращает список голосовых сообщений по запросу.
    """
    query = update.inline_query.query.strip().lower()

    # Если запрос пустой, возвращаем все голосовые сообщения
    results = []

    # Если запрос не пустой, фильтруем сообщения по названию
    if query:
        logger.info(f"Поисковый запрос: {query}")
        filtered_voices = [voice for voice in voice_messages if query in voice["title"].lower()]
    else:
        # Показываем все голосовые сообщения при любом символе
        filtered_voices = voice_messages

    # Формируем результаты для инлайн-ответа
    for voice in filtered_voices:
        results.append(InlineQueryResultVoice(
            id=voice["id"],
            voice_url=voice["file_id"],
            title=voice["title"]
        ))

    # Отправляем результаты инлайн-запроса
    try:
        await update.inline_query.answer(results)
        logger.info("Инлайн-запрос успешно обработан")
    except Exception as e:
        logger.error(f"Ошибка при обработке инлайн-запроса: {e}")

# Основная функция
def main():
    """
    Запуск бота с обработчиками команд и инлайн-запросов.
    """
    # Создание приложения с токеном
    application = Application.builder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик инлайн-запросов
    application.add_handler(InlineQueryHandler(inline_query_handler))

    # Запуск polling
    try:
        application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()
