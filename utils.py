import configparser
from datetime import datetime
from dateutil import tz


def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')

    return {'password': arquivo.get('GERAL', 'password'), 'email': arquivo.get('GERAL', 'email'), 'stop_win': arquivo.get('GERAL', 'stop_win'), 'stop_loss': arquivo.get('GERAL', 'stop_loss'), 'payout': 0, 'banca_inicial': 0, 'martingale': arquivo.get('GERAL', 'martingale'), 'sorosgale': arquivo.get('GERAL', 'sorosgale'), 'niveis': arquivo.get('GERAL', 'niveis'), 'telegram_token': arquivo.get('telegram', 'telegram_token'), 'telegram_id': arquivo.get('telegram', 'telegram_id'), 'usar_bot': arquivo.get('telegram', 'usar_bot'), 'valor_entrada': arquivo.get('GERAL', 'valor_entrada')}


def carregaSinais():
    x = open('sinais.txt')
    y = []
    for i in x.readlines():
        # print(i)
        y.append(i.replace(':00;', ';'))
    # print (y)
    x.close()
    return y


def timestamp_converter():
    hora = datetime.now()
    tm = tz.gettz('America/Sao Paulo')
    hora_atual = hora.astimezone(tm)
    return hora_atual.strftime('%H:%M')
