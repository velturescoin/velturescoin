import telebot
import sqlite3
from datetime import datetime
import bonus
import stats
import account
import proof_blockchain
from flask import Flask, request
import os
import psycopg2
from threading import Thread
from time_stats import *
from time_for_users import *

# главная функция, запускать ее и она подтягивает все, что выше импортировано


TOKEN = '1621919353:AAEPzZFkk7v2PUx6uNSCb-ZEj-qfAjLozgs' # Токен бота

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


KEYBOARD_FOR_ALL = telebot.types.ReplyKeyboardMarkup(True) # клавиатура бота
KEYBOARD_FOR_ALL.row('👤 Account', '✨ Upgrade', '💵 Withdraw')
KEYBOARD_FOR_ALL.row('📊 Stats', '💲 Proof', '🎁 Bonus')

KEYBOARD_ACCOUNT = telebot.types.ReplyKeyboardMarkup(True) # клавиатура бота после нажатия клавиши Account
KEYBOARD_ACCOUNT.row('🔁 Change Your Bitcoin Wallet', '❓ Get Support')
KEYBOARD_ACCOUNT.row('👤 Account', '✨ Upgrade', '💵 Withdraw')
KEYBOARD_ACCOUNT.row('📊 Stats', '💲 Proof', '🎁 Bonus')

KEYBOARD_CANCEL = telebot.types.ReplyKeyboardMarkup(True) # клавиатура для тех кнопок, где есть ввод (например смена адреса биткоин)
KEYBOARD_CANCEL.row('🔙 Cancel')

# строка апгрейда
UPGRADE_STRING = '''
БОТ СУЩЕСТВУЕТ ДЛЯ ОЗНАКОМИТЕЛЬНЫХ ЦЕЛЕЙ

UPGRADE ACCOUNT


🤖 AutoBit One (Owned 0)
➖➖➖
Cost: ฿ 0.0025000
Produces:
  ฿ 0.0000008/min
  ฿ 0.0011520/day


🤖 AutoBit Double (Owned 0)
➖➖➖
Cost: ฿ 0.0050000
Produces:
  ฿ 0.0000020/min
  ฿ 0.0028800/day


🤖 AutoBit Triple (Owned 0)
➖➖➖
Cost: ฿ 0.0225000
Produces:
  ฿ 0.0000100/min
  ฿ 0.0144000/day


🤖 AutoBit Premium (Owned 0)
➖➖➖
Cost: ฿ 0.0500000
Produces:
  ฿ 0.0000250/min
  ฿ 0.0360000/day


🤖 AutoBit Maximal (Owned 0)
➖➖➖
Cost: ฿ 0.1000000
Produces:
  ฿ 0.0000550/min
  ฿ 0.0792000/day

⚠️
After deposit you must send tx id of your transaction to our bot. If you have any questions contact with support @autobitmax

Please send Bitcoin to the address bellow:

ТУТ БЫЛ БЫ БИТКОИН АДРЕС
''' 

# строка кошелька которая идет после апгрейда
MY_WALLET = ''' 
БИТКОИН АДРЕС
''' 

def give_bonus(message): # функция выдачи бонуса
    if message.text == 'BTCBOTFOREVER': # если ввел нужное слово
        conn = psycopg2.connect(dbname='', user='', 
                        password='', 
                        host='',
                        port=5432)
        curs = conn.cursor()
        curs.execute('SELECT bonus FROM users WHERE user_tg_id = {}'.format(message.from_user.id))
        have_bonus = curs.fetchall()
        have_bonus = have_bonus[0][0]
        if have_bonus is None: # проверка чтобы пользователь мог запросить бонус лишь 1 раз
            curs.execute('SELECT balance FROM users WHERE user_tg_id = {}'.format(message.from_user.id))
            balance = curs.fetchall()
            balance = balance[0][0]
            balance += 0.0003 #  добавляем бонус
            curs.execute('UPDATE users SET balance = %s WHERE user_tg_id = %s', (balance, message.from_user.id))
            curs.execute('UPDATE users SET bonus = %s WHERE user_tg_id = %s', (1, message.from_user.id))
            conn.commit()
            conn.close()
            # пишем что бонус успешно добавлен
            bot.send_message(message.chat.id, 'Bonus received successfully', reply_markup=KEYBOARD_FOR_ALL)
        else: # если у него уже был бонус, отправляет сообщение
            bot.send_message(message.chat.id, 'You already have bonus', reply_markup=KEYBOARD_FOR_ALL)
    else: # если неправильно ввел бонусное слово, отправляем сообщение
        bot.send_message(message.chat.id, 'Wrong bonus word', reply_markup=KEYBOARD_FOR_ALL)



def extract_unique_code(text): # эта функция достает код из реферальной ссылки
    return text.split()[1] if len(text.split()) > 1 else None



@bot.message_handler(commands=['start'])
def start_message(message): # функция, которая выполняется после нажатия на старт
    conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432)
    curs = conn.cursor()
    unique_code = extract_unique_code(message.text) # пытается достать код 
    if unique_code: # если юзер перешел по ссылке и эта ссылка рабочая
        curs.execute('SELECT user_tg_id FROM users') # коннект к бд
        for_check_ref = curs.fetchall()
        for_check_ref = [z[0] for z in for_check_ref]
        if message.from_user.id not in for_check_ref: # проверяет, первый ли раз человек заходит по реф. ссылке
            if unique_code in for_check_ref:
                curs.execute('SELECT balance, how_much_refers FROM users WHERE user_tg_id = %s', (unique_code)) # достает баланс человека, который дал реф. ссылку
                balance_from_ref = curs.fetchall()
                how_much_ref = balance_from_ref[0][1]
                balance_from_ref = balance_from_ref[0][0]
                balance_from_ref += 0.001 # добавляет этому человеку 0.001 биткоин
                how_much_ref += 1 # добавляет ему в строку сколько у него реферала + 1
                curs.execute('UPDATE users SET balance= %s, how_much_refers= %s WHERE user_tg_id= %s', (balance_from_ref,how_much_ref ,unique_code)) 
                conn.commit() # заносит эти данные в бд
    ref_link =  't.me/test_crypto_11_bot?start={}'.format(message.from_user.id) # создает реф. ссылку
    curs.execute('SELECT user_tg_id FROM users')
    un_ids = curs.fetchall()
    un_ids = [i[0] for i in un_ids]
    if message.from_user.id not in un_ids: # если юзер первый раз заходит в бота, ему присваиваются значение (нулевой баланс, нулевой реф итд)
        curs.execute("INSERT INTO users(user_name, user_tg_id, balance, how_much_refers, user_referal, referral_link, user_since, owned_machines, mining_speed_min, mining_speed_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (message.from_user.username, message.from_user.id, 0.00000000, 0, 0.00000000, ref_link, datetime.now(), 'AutoBitFree', '0.00000030', '0.00043200'))  #доделать время
        conn.commit() # все заносится и сохраняется в БД
        conn.close()
    # отправляет пользователю приветственное сообщение
    bot.send_message(message.chat.id, 'ЭТО БОТ ТОЛЬКО ДЛЯ ТЕСТОВ\nAutoBit Robot is fully automatic. \
Start earning BTC now. \
AutoBit Robot Free Earning Rate: \
 ฿0.00000040/min \
 ฿0.00057600/day \
Please /upgrade if you want increase mining speed!', reply_markup=KEYBOARD_FOR_ALL)

def change(message): # функция для отработки после нажатия кнопки change btc adress
    if message.text == '🔙 Cancel': # если пользователь жмет cancel он возвращается в обычное меню
        bot.send_message(message.chat.id, 'Operation aborted.', reply_markup=KEYBOARD_FOR_ALL)
    elif ((len(message.text) > 25 and len(message.text) < 36) and (message.text[0] == '1' or message.text[0] == '3')): # если сообщение соответствует параметрам блокчейн адреса
        conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432)
        curs = conn.cursor()
        curs.execute('UPDATE users SET btc_wallet = %s where user_tg_id = %s', (message.text, message.from_user.id))
        conn.commit() # в базу данных заноситься новый адрес
        conn.close()
        # после удачного обновления адреса бот присылает сообщение
        bot.send_message(message.chat.id, 'Your BTC address updated!', reply_markup=KEYBOARD_FOR_ALL)
        user = message.from_user.id
        conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432)
        curs = conn.cursor()
        curs.execute('SELECT btc_wallet, user_email FROM users WHERE user_tg_id = {}'.format(user))
        parametrs = curs.fetchall()
        parametrs = parametrs[0]
    else: # если пользователь вводит недействительный биткоин адрес, бот присылает сообщение
        bot.send_message(message.chat.id, 'Please, give me a valid BTC adress', reply_markup=KEYBOARD_FOR_ALL)

# строка если баланс меньше 0.1 бтц
WITHDRAW_STRING_IF_LOW = '''
WITHDRAW

Sorry! Minimum withdrawal is ฿ 0.1000000!
'''
# строка если баланс больше 0.1 бтц
WITHDRAW_STRING_IF_HIGH = 'You must verify your account by deposit in the amount of 0.01 btc'

def update_email(message): # функция для установки email пользователя
    if message.text == '🔙 Cancel': # если пользователь жмет cancel он возвращается в обычное меню
        bot.send_message(message.chat.id, 'Operation aborted.', reply_markup=KEYBOARD_FOR_ALL)
    elif (('@' in message.text) and ('.' in message.text)): # если пользователь вводит корректный мейл
        conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432)
        curs = conn.cursor()
        curs.execute('UPDATE users SET user_email = %s where user_tg_id = %s', (message.text, message.from_user.id))
        conn.commit() # он обновляется и заносится в БД
        conn.close()
        bot.send_message(message.chat.id, 'Your email address updated!', reply_markup=KEYBOARD_FOR_ALL) # бот пишет сообщение об успешном обновлении
    else: # если пользователь вводит неправильный мейл, бот присылает сообщение
        bot.send_message(message.chat.id, 'Please, give me a valid email', reply_markup=KEYBOARD_FOR_ALL)


@bot.message_handler(content_types=['text'])
def send_text(message):
    # основная функция, отвечает за действия после нажатия кнопок
    if message.text == '👤 Account': # если юзер нажимает на аккаунт
        account_user = message.from_user.id
        needed = account.account_func(account_user, message) # подкачивается функция из файла аккаунт
        bot.send_message(message.chat.id, needed, reply_markup=KEYBOARD_ACCOUNT)
    elif message.text == '❓ Get Support': # если нажимает саппорт, подкачивает из файла аккаунта саппорт
        bot.send_message(message.chat.id, account.support_func(), reply_markup=KEYBOARD_FOR_ALL)
    elif message.text == '🔁 Change Your Bitcoin Wallet': # если нажимает поменять биткоин адрес
        bot.send_message(message.chat.id, 'Update your BTC address:', reply_markup=KEYBOARD_CANCEL)
        bot.register_next_step_handler(message, change) # подкачивает функцию change
    elif message.text == '✨ Upgrade': # если нажимает агрейд, выдает строку апгрейд и номер кошелька
        bot.send_message(message.chat.id, UPGRADE_STRING)
        bot.send_message(message.chat.id, MY_WALLET, reply_markup=KEYBOARD_FOR_ALL)
    elif message.text == '💵 Withdraw': # если нажимает withdraw, начинается проверка
        user = message.from_user.id
        conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432) # коннект к базе
        curs = conn.cursor()
        curs.execute('SELECT btc_wallet, user_email FROM users WHERE user_tg_id = {}'.format(user))
        parametrs = curs.fetchall() # берет поля кошелек и емейл
        parametrs = parametrs[0]
        if parametrs[0] == None: # если кошелек не установлен, просит ввести кошелек и сохраняет его
            bot.send_message(message.chat.id, 'To withdraw give your BTC wallet, please: ', reply_markup=KEYBOARD_CANCEL)
            bot.register_next_step_handler(message, change)
        if (parametrs[1] == None) and (parametrs[0] != None): # если нет почты, просит ее ввести и сохраняет
            bot.send_message(message.chat.id, 'To withdraw give your email, please: ', reply_markup=KEYBOARD_CANCEL)
            bot.register_next_step_handler(message, update_email)
        if (parametrs[0] != None) and (parametrs[1] != None): # если есть все нужные поля
            curs.execute('SELECT balance FROM users WHERE user_tg_id = {}'.format(user))
            curs.fetchall() # смотрит в БД баланс юзера
            user_balance = curs.fetchall()
            try:
                user_balance = user_balance[0][0]
                if user_balance < 0.1000000: # если баланс юзера меньше 0.1 присылает сообщение для низкого баланса
                    bot.send_message(message.chat.id, WITHDRAW_STRING_IF_LOW, reply_markup=KEYBOARD_FOR_ALL) 
                elif user_balance >= 0.1000000: # если баланс больше 0.1, присылает строку с подтверждением акка
                    bot.send_message(message.chat.id, WITHDRAW_STRING_IF_HIGH, reply_markup=KEYBOARD_FOR_ALL) 
            except:
                bot.send_message(message.chat.id, WITHDRAW_STRING_IF_LOW, reply_markup=KEYBOARD_FOR_ALL)
    elif message.text == '📊 Stats': # при нажатии этой кнопки подтягивает функцию из файла статс 
        bot.send_message(message.chat.id, stats.stats_func(), reply_markup=KEYBOARD_FOR_ALL)
    elif message.text == '💲 Proof': # при нажатии этой кнопки подтягивает функцию из файла пруф
        try:
            bot.send_message(message.chat.id, proof_blockchain.proof_func())
        except IndexError:
            bot.send_message(message.chat.id, 'Sorry, Blockchain API is overloaded, try again', reply_markup=KEYBOARD_FOR_ALL)
    elif message.text == '🎁 Bonus': # при нажатии этой кнопки подтягивает функцию из файла бонус
        bot.send_message(message.chat.id, bonus.bonus_func(), reply_markup=KEYBOARD_FOR_ALL)
        bot.register_next_step_handler(message, give_bonus)
    else: # если пользователь вводит что-то иное, бот отправляет сообщение
        bot.send_message(message.chat.id, 'Use buttons, please')


# bot.polling()

@server.route('/'+TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://botfortestonly.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == '__main__':
    # создаю несколько потоков, так как heroku не дает запускать несколько фалов на сервере одновременно
    th1, th2, th3 = Thread(target=server.run, kwargs={'host':"0.0.0.0", 'port':int(os.environ.get('PORT', 5000))}), Thread(target=time_stats_func), Thread(target=time_for_users_func)
    th1.start(), th2.start(), th3.start()
    th1.join(), th2.join(), th3.join()
