import time
import sqlite3
import random
import psycopg2

'''
В этом файле находится функция, отвечающая за выполнение действий после нажатия кнопки Stats бота
'''

conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432) # коннект к базе данных 
curs = conn.cursor()

# строка, которая возвращается в бота, место {} подставляются значения из базы данных
STATS_STRING = ''' 
БОТ ДЛЯ ТЕСТА
BOT STATS

Total deposit: ฿ {}
Total withdraw: ฿ {}
Total members: {}
Active members: {}
Referral: {}
Online: {}
'''

sql_stats = curs.execute('SELECT total_deposit, total_withdraw, total_members, active_members, referer FROM stats WHERE id = 1;') # достает из базы данных данные статистики
sql_stats = curs.fetchall()
sql_stats = sql_stats[0]
sql_stats = [i for i in sql_stats]


def stats_func():
    '''
    Вставляет в строку данные из базы данных и возвращает в бота 
    '''
    global STATS_STRING
    return STATS_STRING.format(sql_stats[0], sql_stats[1], sql_stats[2], sql_stats[3], sql_stats[4], random.randint(456, 746))


