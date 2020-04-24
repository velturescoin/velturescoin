from blockchain import blockexplorer
import time
import random
import psycopg2

# строка с пруфами, вместо {} вставляются данные с сайта blockchain.com с помощью API
PROOF_STRING = '''
PAYMENT PROOF (Last 10 payouts)

Time: {time0}
User: {name0}
Amount: ฿ {btc0}
{link0}

Time: {time1}
User: {name1}
Amount: ฿ {btc1}
{link1}

Time: {time2}
User: {name2}
Amount: ฿ {btc2}
{link2}

Time: {time3}
User: {name3}
Amount: ฿ {btc3}
{link3}

Time: {time4}
User: {name4}
Amount: ฿ {btc4}
{link4}

Time: {time5}
User: {name5}
Amount: ฿ {btc5}
{link5}

Time: {time6}
User: {name6}
Amount: ฿ {btc6}
{link6}

Time: {time7}
User: {name7}
Amount: ฿ {btc7}
{link7}

Time: {time8}
User: {name8}
Amount: ฿ {btc8}
{link8}

Time: {time9}
User: {name9}
Amount: ฿ {btc9}
{link9}
'''

def proof_func():
    '''
    функция сбора и передачи в строку информации с blockchain.com
    '''
    global PROOF_STRING
    txs = blockexplorer.get_unconfirmed_tx() # парсим все неподтвержденные транзакции

    frst_lnk_prt = 'https://www.blockchain.com/btc/tx/'

    fake_user_names = []
    transactions = []
    template = '{}.{}'

    fake_user_names = ['Dmitry', 'Max', 'Maxim', 'SCARLXRD', 'Ilya', 'Pierre', 'Jacobs', 'Rick', 'OG', 'Lee', 'ROBIN', 'Greenville', 'gixon', 'VNMV', 'Calling', 'Tandura', 'Anthony', 'Turner4', 'Anton', 'Roger', 'Programmer', 'Jack', 'grommok', 'DEAD DIOR', 'wazowski28', 'Alexandr', 'Kon$tantin', 'ROBINHOOD21VEKA', 'Марк', 'Victor Velikiy', 'vi', 'KonanD', 'Carmen Murry', 'Lil', 'Yura', 'Rumbold', 'Abror_G', 'FUCK_THE_POLICE', 'Unknown', 'Nikita', 'Gudini', 'Mammon', 'Misterius', 'Djoni', 'Hewitt', 'Logan', 'Jojo', 'hi i*m', 'Comic', 'Marat Shirimov', 'Crypto Zozo', 'Ali Reza', 'Harry Cooper', 'Mellissa Lemle', 'Roland Frank', 'Mr Bart', 'Madison', 'ferrar', 'Joline Moore']


    for i in txs: # берем только те транзакции, которые удовлетворяют нашим условиям
        if i.inputs[0].value >= 10000000:
            value = str(i.inputs[0].value)
            if len(value) == 8:
                valuable = template.format('0', value)
            elif len(value) > 8:
                valuable = template.format(value[:-8], value[-8:])
            else:
                value = '0.10000000' # вдруг ошибка сервера
            transaction = [str(time.ctime(i.time)),random.choice(fake_user_names), valuable, frst_lnk_prt + i.hash]
            transactions.append(transaction) # добавляем все транзы сумма которых больше 0.10000000 
    transactions = transactions[-10:] # берем последние 10
    # подставляем все в строку и возвращаем ее
    return PROOF_STRING.format(time0=transactions[0][0], name0=transactions[0][1], btc0=transactions[0][2], link0=transactions[0][3], time1=transactions[1][0], name1=transactions[1][1], btc1=transactions[1][2], link1=transactions[1][3], time2=transactions[2][0], name2=transactions[2][1], btc2=transactions[2][2], link2=transactions[2][3], time3=transactions[3][0], name3=transactions[3][1], btc3=transactions[3][2], link3=transactions[3][3], time4=transactions[4][0], name4=transactions[4][1], btc4=transactions[4][2], link4=transactions[4][3], time5=transactions[5][0], name5=transactions[5][1], btc5=transactions[5][2], link5=transactions[5][3], time6=transactions[6][0], name6=transactions[6][1], btc6=transactions[6][2], link6=transactions[6][3], time7=transactions[7][0], name7=transactions[7][1], btc7=transactions[7][2], link7=transactions[7][3], time8=transactions[8][0], name8=transactions[8][1], btc8=transactions[8][2], link8=transactions[8][3], time9=transactions[9][0], name9=transactions[9][1], btc9=transactions[9][2], link9=transactions[9][3])



