import sqlite3

'''
Этой программой создается новая база данный, если надо будет сделать новую с теми же полями
'''




import psycopg2
conn = psycopg2.connect(dbname='d6e129ci6qleqc', user='zdiehcudprdhjd', 
                        password='905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf', 
                        host='ec2-54-152-175-141.compute-1.amazonaws.com',
                        port=5432)
curs = conn.cursor()
curs.execute('''CREATE TABLE users(id SERIAL,
user_name VARCHAR(1000), 
balance REAL,
owned_machines VARCHAR(50),
mining_speed_min REAL,
btc_wallet VARCHAR(50), 
user_email VARCHAR(50),
user_since TIMESTAMP,
user_referal REAL,
referral_link VARCHAR(150), 
user_tg_id INT, 
how_much_refers INT, 
mining_speed_day VARCHAR(50),
bonus VARCHAR(50));
''')

curs.execute('''CREATE TABLE stats(id INT PRIMARY KEY NOT NULL,
total_deposit REAL, 
total_withdraw REAL,
total_members INT,
active_members INT,
referer INT);''')

# postgres://zdiehcudprdhjd:905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf@ec2-54-152-175-141.compute-1.amazonaws.com:5432/d6e129ci6qleqc
# username: zdiehcudprdhjd
# password: 905e090c1222572e19d28cc8479ff71c3ac9f8286b32fd1da9dce1584ed97fbf
# host: ec2-54-152-175-141.compute-1.amazonaws.com
# port: 5432
# database: d6e129ci6qleqc 

# local: conn = psycopg2.connect(dbname='cryptobtcbot', user='test_bitcoin', 
#                        password='bitcoin', host='localhost')