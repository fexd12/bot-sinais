from bot_telegram import Telegram
from utils import carregaSinais, timestamp_converter
import time
import sys
import logging

logging.disable(level=(logging.DEBUG))


class Operacao(Telegram):
    def __init__(self):
        Telegram.__init__(self)

    def Martingale(self, valor):
        # gale para recuperacao = 1.5 , gale para cobertura = 2.3
        lucro_esperado = float(valor) * 1.5
        # perca = valor

        # while True:
        # 	if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
        # 		return round(valor, 2)
        # 		break
        # 	valor += 0.01
        return float(lucro_esperado)

    def Payout(self, par, timeframe):
        self.subscribe_strike_list(par, timeframe)
        while True:
            d = self.get_digital_current_profit(par, timeframe)
            if d > 0:
                break
            time.sleep(1)
        self.unsubscribe_strike_list(par, timeframe)
        return float(d / 100)

    def entradas(self, par, entrada, direcao, config, opcao, timeframe):
        banca = self.banca()
        if opcao == 'digital':
            status, id = self.buy_digital_spot(
                par, entrada, direcao, timeframe)
            if status:
                # STOP WIN/STP LOSS

                banca_att = banca
                stop_loss = False
                stop_win = False

                if round((banca_att - float(self.config['banca_inicial'])), 2) <= (abs(float(self.config['stop_loss'])) * -1.0):
                    stop_loss = True

                # if round((banca_att - float(config['banca_inicial'])) + (float(entrada) * float(config['payout'])) + float(entrada), 2) >= abs(float(config['stop_win'])):
                # 	stop_win = True
                if round((banca_att - float(self.config['banca_inicial'])), 2) >= abs(float(self.config['stop_win'])):
                    stop_win = True

                while True:
                    status, lucro = self.check_win_digital_v2(id)

                    if status:
                        if lucro > 0:
                            return 'win', round(lucro, 2), stop_win
                        else:
                            return 'loss', 0, stop_loss
                        break
            else:
                return 'error', 0, False

        elif opcao == 'binaria':
            status, id = self.buy(entrada, par, direcao, timeframe)

            if status:
                lucro = self.check_win_v3(id)

                banca_att = banca
                stop_loss = False
                stop_win = False

                if round((banca_att - float(self.config['banca_inicial'])), 2) <= (abs(float(self.config['stop_loss'])) * -1.0):
                    stop_loss = True

                if round((banca_att - float(self.config['banca_inicial'])), 2) >= abs(float(self.config['stop_win'])):
                    stop_win = True

                if lucro:
                    if lucro > 0:
                        return 'win', round(lucro, 2), stop_win
                    else:
                        return 'loss', 0, stop_loss
            else:
                return 'error', 0, False
        else:
            return 'opcao errado', 0, False

    def Timeframe(self, timeframe):

        if timeframe == 'M1':
            return 1

        elif timeframe == 'M5':
            return 5

        elif timeframe == 'M15':
            return 15

        elif timeframe == 'H1':
            return 60
        else:
            return 'erro'

    def checkProfit(self, par, timeframe):
        all_asset = self.get_all_open_time()
        profit = self.get_all_profit()

        digital = 0
        binaria = 0

        if timeframe == 60:
            return 'binaria'

        if all_asset['digital'][par]['open']:
            digital = self.Payout(par, timeframe)
            digital = round(digital, 2)

        if all_asset['turbo'][par]['open']:
            binaria = round(profit[par]["turbo"], 2)

        if binaria < digital:
            return "digital"

        elif digital < binaria:
            return "binaria"

        elif digital == binaria:
            return "digital"

        else:
            "erro"

    def RealizaOperacao(self):
        sinais = carregaSinais()
        for x in sinais:
            timeframe_retorno = self.Timeframe(x.split(';')[0])
            timeframe = 0 if (timeframe_retorno ==
                              'error') else timeframe_retorno
            par = x.split(';')[1].upper()
            minutos_lista = x.split(';')[2]
            direcao = x.split(';')[3].lower().replace('\n', '')
            mensagem_paridade = 'paridade a ser operada: ' + par + ' ' + '/' + ' ' + 'timeframe: ' + \
                str(timeframe) + ' ' + '/' + ' ' + 'horario: ' + \
                str(minutos_lista) + ' ' + '/' + ' ' + 'direcao: ' + direcao
            self.Mensagem(mensagem_paridade)
            # print(par)
            while True:
                # payout = Payout(par,timeframe)
                # config['payout'] = payout
                minutos = timestamp_converter()

                # print(minutos_lista)
                # minutos_lista_parse = time.strptime(minutos_lista,'%H:%M:%S')
                # c = time.strftime('%H:%M:%S', minutos_lista_parse)
                # print(c)
                if minutos_lista < minutos:
                    break

                opcao = self.checkProfit(par, timeframe)

                entrar = True if (minutos_lista == minutos) else False
                # print('Hora de entrar?',entrar,'/ Minutos:',minutos)
                # print('Paridade',par)

                if entrar:
                    bot.Mensagem('\n\nIniciando Operacao')
                    dir = False
                    dir = direcao

                    if dir:
                        mensagem_operacao = 'Paridade: ' + par + ' ' + '/' + ' ' + 'opcao: ' + opcao + ' ' + \
                            '/' + ' ' + 'Horario: ' + \
                            str(minutos_lista) + ' ' + \
                            '/' + ' ' + 'Direção: ' + dir
                        self.Mensagem(mensagem_operacao)
                        valor_entrada = self.valor_entrada_b
                        opcao = 'binaria' if (opcao == 60) else opcao
                        resultado, lucro, stop = self.entradas(
                            par, valor_entrada, dir, config, opcao, timeframe)
                        mensagem_resultado = '   ->  ' + \
                            resultado + ' / ' + str(lucro)
                        self.Mensagem(mensagem_resultado)

                        if resultado == 'error':
                            break

                        if resultado == 'win':
                            break

                        if stop:
                            mensagem_stop = '\n\nStop ' + resultado.upper() + ' batido!'
                            self.Mensagem(mensagem_stop)
                            sys.exit()

                        if resultado == 'loss' and config['martingale'] == 'S':
                            valor_entrada = self.Martingale(
                                float(valor_entrada))
                            for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):

                                mensagem_martingale = '   MARTINGALE NIVEL ' + \
                                    str(i+1) + '..'
                                self.Mensagem(mensagem_martingale)
                                resultado, lucro, stop = self.entradas(
                                    par, valor_entrada, dir, config, opcao, timeframe)
                                mensagem_resultado_martingale = ' ' + \
                                    resultado + ' / ' + str(lucro) + '\n'
                                self.Mensagem(mensagem_resultado_martingale)
                                if stop:
                                    mensagem_stop = '\n\nStop ' + resultado.upper() + ' batido!'
                                    self.Mensagem(mensagem_stop)
                                    sys.exit()

                                if resultado == 'win':
                                    print('\n')
                                    break
                                else:
                                    valor_entrada = self.Martingale(
                                        float(valor_entrada))
                            break
                        else:
                            break
                time.sleep(0.1)
            # break
        self.Mensagem('lista de sinais finalizada')
        sys.exit()
