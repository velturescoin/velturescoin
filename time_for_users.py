import time
import sqlite3
import psycopg2

'''
В этом файле находится программа, которая каждую минуту начисляет всем пользователям по 0.00000030 BTC
'''

def time_for_users_func():
    while True:
        conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432) # Подключение к БД
        curs = conn.cursor()
        curs.execute('SELECT user_tg_id FROM users') # Берет всех юзеров
        users = curs.fetchall()
        conn.close()
        users = [i[0] for i in users] # Добавляет юзеров в список для удобства
        for x in users:
            conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432)
            curs = conn.cursor()
            curs.execute('SELECT balance FROM users WHERE user_tg_id = {}'.format(x)) # берет баланс каждого юзера
            balance = curs.fetchall()
            balance = balance[0][0]
            balance += 0.00000030 # прибавляет к нему 0.00000030 BTC
            curs.execute('UPDATE users SET balance= %s WHERE user_tg_id= %s', (balance, x)) # засовывает в базу каждому юзеру новый баланс
            conn.commit()
            conn.close()
        time.sleep(60) # ждет минуту и все делает заново 