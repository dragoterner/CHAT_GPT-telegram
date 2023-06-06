import os
import openai
import telebot
from telebot import types
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
NUMBERS_ROWS = 9
URL = "https://disk.yandex.ru/d/b5nKyNk4NgOohQ"
admins = [5403985984]
channel_id = -1001882163598

openai.api_key = "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"
bot = telebot.TeleBot('5667067959:AAHIZeUoJ_k5zDoMjtJ0Byxyph63zE0TRmQ')

if not os.path.exists("users"):
    os.mkdir("users")
     
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #buttons in menu
    btn0 = types.KeyboardButton("↪️Перезапуск")
    btn1 = types.KeyboardButton("FAQ📗")
    btn2 = types.KeyboardButton("DARK🔦")
    btn3 = types.KeyboardButton("Creator💾")
    markup.add(btn0, btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет👋, {0.first_name}! Я бот CHAT GPT - {1.first_name}\nЗадай мне любой вопрос и я отвечу на него!📝\nНе будь дураком, задавай вопросы правильно ✅ - https://nometa.xyz/ru.html".format(message.from_user, bot.get_me()), reply_markup=markup)

#рассылка
@bot.callback_query_handler(func=lambda call: call.data in ['send_message', 'list_users', 'blacklist', 'exit_admin'])
def admin_panel(call):
    if call.from_user.id not in admins:
        return
    if call.data == 'send_message':
        bot.send_message(chat_id=call.message.chat.id, text='Введите текст рассылки:')
        bot.register_next_step_handler(call.message, bot.send_message_to_all_users)
    elif call.data == 'list_users':
        users = os.listdir('users')
        bot.send_message(chat_id=call.message.chat.id, text=f'Список пользователей:\n\n{len(users)} человек(а)')
    elif call.data == 'blacklist':
        bot.send_message(chat_id=call.message.chat.id, text='Введите id пользователя, которого хотите добавить в чёрный список:')
        bot.register_next_step_handler(call.message, bot.add_user_to_blacklist)
    elif call.data == 'exit_admin':
        keyboard = InlineKeyboardMarkup()
        bot.send_message(chat_id=call.message.chat.id, text='Вы вышли из панели администратора', reply_markup=keyboard)    
    
    
#workkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
@bot.message_handler(content_types=['text']) #создаем команду
def msg(message):
    if f"{message.chat.id}.txt" not in os.listdir('users'):
        with open(f"users/{message.chat.id}.txt", "x") as f:
            f.write('')

    with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as file:
        oldmes = file.read()

    if message.text == '/clear':
        with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return bot.send_message(chat_id=message.chat.id, text='История очищена командой /clear! ')
    
    
    
    #panel inline############################################################################################
    if message.text == 'DARK🔦':
        return bot.send_message(chat_id=message.chat.id, text='Никогда не открывай меня\nhttps://disk.yandex.ru/d/b5nKyNk4NgOohQ\n\n\n❤️Перезапустить бота - /start')
    
    if message.text =="FAQ📗":
        bot.send_message(chat_id=message.chat.id, text="⏳")
        return bot.send_message(message.chat.id, "Милашка мой {0.first_name} тут пока пусто".format(message.from_user, bot.get_me()))
        # return bot.send_message(chat_id=message.chat.id, text="Милашка мой {0.first_name} тут пока пусто :(")
    
    if message.text == "↪️Перезапуск":
        with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return bot.send_message(chat_id=message.chat.id, text='История очищена!✅\nИстория очищается для новой записи данных в бота\n\n❤️Перезапустить бота - /start')
    
    if message.text =="Creator💾":
        return bot.send_message(chat_id=message.chat.id, text='All fixes by @EurozX 🔧\n\n\n❤️Перезапустить бота - /start')
    #fake clear history ###################################################################################
    
    #all links in bot
    if message.text == '/links':
        return bot.send_message(chat_id=message.chat.id, text='https://disk.yandex.ru/d/b5nKyNk4NgOohQ\nhttps://nometa.xyz/ru.html')
        
    try:
        send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        send_message = bot.send_message(chat_id=message.chat.id, text='⏳')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role": "user", "content": oldmes},
                        {"role": "user","content": f'Предыдущие сообщения: {oldmes}; Запрос: {message.text}'}], presence_penalty=0.6)

        bot.edit_message_text(text=completion.choices[0].message["content"], chat_id=message.chat.id, message_id=send_message.message_id)

        with open(f'users/{message.chat.id}.txt', 'a+', encoding='utf-8') as file:
            file.write(message.text.replace('\n', ' ') + '\n' + completion.choices[0].message["content"].replace('\n', ' ') + '\n')


        with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) >= NUMBERS_ROWS +1:
            with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as f:
                f.writelines(lines[2:])

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=e)

               
bot.infinity_polling()