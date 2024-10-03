import os
from dotenv import load_dotenv
import telebot
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Проверка на наличие токена
if not BOT_TOKEN:
    raise ValueError("Token is missing! Please set the TOKEN environment variable.")

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)




@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    # Создаем новую инлайн-клавиатуру
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_tips = types.InlineKeyboardButton(text="Связаться с создателем🛠️", callback_data="admin")
    button_auction = types.InlineKeyboardButton(text="Мониторинг💻", callback_data="auction")
    button_hist = types.InlineKeyboardButton(text="Актуальные лоты и история продаж📈", callback_data="hist")
    markup.add(button_tips, button_auction, button_hist)
    # Отправляем сообщение с двумя кнопками
    bot.send_message(chat_id, "Хорошо! Что тебя интересует?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "admin")
def handle_admin_callback(call):
    chat_id = call.message.chat.id  # ID чата
    message_id = call.message.message_id  # ID сообщения

    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="https://t.me/mentho1")

from auc import *
from mon import *


@bot.callback_query_handler(func=lambda call: call.data == "hist")
def handle_callback_query_hist(call):
    from auc import user_threads
    chat_id = call.message.chat.id

    # Проверяем, есть ли пользователь в закрытом чате
    try:
        # Используйте метод 'get_chat_member' для проверки
        member = bot.get_chat_member(chat_id=-1002026481923, user_id=call.from_user.id)

        if member.status != 'left':
            # Пользователь в чате, показываем кнопки
            # Проверяем, запущен ли поток мониторинга для этого пользователя
            if chat_id in user_threads:
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                      text="Вы уже мониторите лот❗\nОстановите мониторинг текущего лота, чтобы начать отслеживать новый.\nЧтобы остановить пропишите команду /stop")
                return

            # Создаем новую инлайн-клавиатуру с типами снаряжения
            markup = types.InlineKeyboardMarkup(row_width=1)
            button_harmor = types.InlineKeyboardButton(text="Броня", callback_data="harmor")
            button_hweapon = types.InlineKeyboardButton(text="Оружие", callback_data="hweapon")
            button_hcont = types.InlineKeyboardButton(text="Контейнеры", callback_data="hcont")
            markup.add(button_harmor, button_hweapon, button_hcont)
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text="Хорошо, выбери направление:", reply_markup=markup)
        else:
            # Пользователь не в чате, отправляем сообщение с ссылкой
            bot.send_message(chat_id,
                             'Вы не имеете доступа к этой функции!🚫\nДля получения доступа  необходимо подписаться на телеграмм канал: https://t.me/menthub')
    except Exception as e:
        # Обработка ошибок
        bot.answer_callback_query(callback_query_id=call.id, text="Произошла ошибка. Попробуйте снова.")
        print(f"Ошибка при проверке пользователя в чате: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0, timeout=90)