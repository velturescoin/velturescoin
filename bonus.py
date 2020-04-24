'''
Из это функции подкачивается нужная строка и функция ее возвращает
'''
# бонусная строка, можешь менять все, что хочешь
BONUS_STRING = BONUS_STRING = '''
БОТ ТОЛЬКО ДЛЯ ТЕСТА
🎁 BONUS 🎁

You can request a bonus of ฿ 0.0003

In order to receive the bonus, please subscribe to all this partner channels: КАНАЛЫ ПАРТНЕРА ДЛЯ БОНУСА

After subscribed enter BTCBOTFOREVER 

⚠️ Be aware, if you unsubscribe from our partners channel your bonus can be removed from your balance.

ℹ️You can request to be our partner (and pay for this in BTC) from the support 'Get Support' button in the Account section
'''

def bonus_func(): # возвращает бонусную строку
    global BONUS_STRING
    return BONUS_STRING