import sqlite3
import telebot
import psycopg2
'''
отсюда в основной файл подкачивается функция, которая вставляет нуные данные из базы данных 
в строку аккаунты
'''

# строка аккаунта
ACCOUNT_STRING = '''
БОТ ТОЛЬКО ДЛЯ ТЕСТА
👤 ACCOUNT INFORMATION
 
👤 User: {user_n}

💰 Balance: {balance}
🤖 Owned machines: {machine}
⚡️ Total Mining Speed: 
         ฿ {min}/min
         ฿ {day}/day
🔐 BTC wallet: {wallet}
✉️ Email: {mail}
📅 Member since: {since}

👥 REFERRAL SYSTEM
Referrals: {ref}
Referral earnings: ฿ {refea}
Referral commission: 20% (On earnings and deposits)
Referral link:{refl}
'''

def toFixed(numObj, digits=0): # эта функция нужна, чтобы когда цифра вывоилась на экран, у нее было 8 знаков после точки
    return f"{numObj:.{digits}f}"

def account_func(user, message):
    global ACCOUNT_STRING
    conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432) # коннект к базе
    curs = conn.cursor()
    curs.execute('''SELECT user_name, balance, btc_wallet, user_email, user_since, how_much_refers, 
    user_referal, referral_link, mining_speed_min, mining_speed_day, owned_machines
    FROM users WHERE user_tg_id = {usr}'''.format(usr=user)) # берет необходимые данные из БД
    from_db = curs.fetchall()
    conn.close()
    from_db = from_db[0]
    from_db = [x for x in from_db]
    for i in from_db: # если у пользователя нет каких либо данных (почта, кошелек), ставится просто пустое место
        if i == None:
            index = from_db.index(i)
            from_db[index] = ' '
    # возвращает строку с вставленными значениями из базы данных
    return ACCOUNT_STRING.format(user_n=from_db[0], balance=toFixed(from_db[1], 8), machine=from_db[10], min=toFixed(from_db[8], 8), day=from_db[9], wallet=from_db[2], mail=from_db[3], since=from_db[4], ref=from_db[5], refea=toFixed(from_db[6], 8), refl=from_db[7])

def support_func(): # возвращает строку саппорта, если пользователь нажимает на кнопку
    SUPPORT_STRING = '''
    БОТ ДЛЯ ТЕСТА
    ❓ SUPPORT/CONTACT

To get support ONLY on important things, like error, problems or paid ads/partnership, please contact us via telegram at: ТУТ БЫЛ БЫ АКК САППОРТА
'''
    return SUPPORT_STRING