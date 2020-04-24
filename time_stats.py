from datetime import datetime
import sqlite3
import time 
import random
import psycopg2

# ФУНКЦИЯ ДЛЯ ОБНОВЛЕНИЯ STATS для количества пользователей 24 ЧАСА 

def time_stats_func():
    while True:
        conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432) # подключение к БД
        curs = conn.cursor()
        curs.execute('SELECT total_deposit, total_withdraw, total_members, active_members, referer FROM stats') # выбирает нужные параметры
        sql_stats = curs.fetchall()
        sql_stats = sql_stats[0]
        sql_stats = [i for i in sql_stats]
        stats_deposit = sql_stats[0] + 0.00111176 # добавляет к общему депозиту такую сумму каждые 24 часа
        stats_withdraw = sql_stats[1] + 0.03111176 # добавляет к общему withdraw , аналогично строке выше
        stats_total = sql_stats[2] + random.randint(3, 30) # добавляет к общему числу пользователей рандомное количество от 3 до 30 каждые 24 часа
        stats_active = sql_stats[3] + random.randint(3, 15) # аналогично строчке выше к активным пользователям
        stats_referral = sql_stats[4] + random.randint(3, 10) # аналогично строчке выше к рефералам
    
        curs.execute('UPDATE stats SET total_deposit = %s, total_withdraw = %s, total_members = %s, active_members = %s, referer = %s WHERE id = 1', (stats_deposit, stats_withdraw, stats_total,stats_active ,stats_referral))
        conn.commit() # засовывает в базу новые значения

        time.sleep(86400) # ждет 24 часа чтобы снова обновить данные

