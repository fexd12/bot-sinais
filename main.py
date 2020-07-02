from utils import carregaSinais,configuracao,timestamp_converter
from bot_telegram import Telegram

import time, json, logging,sys

logging.disable(level=(logging.DEBUG))

def Martingale(valor):
	lucro_esperado = float(valor) * 1.5 # gale para recuperacao = 1.5 , gale para cobertura = 2.3
	# perca = valor	
		
	# while True:
	# 	if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
	# 		return round(valor, 2)
	# 		break
	# 	valor += 0.01
	return float(lucro_esperado)

def Payout(par,timeframe):
	API.subscribe_strike_list(par, timeframe)
	while True:
		d = API.get_digital_current_profit(par, timeframe)
		if d > 0:
			break
		time.sleep(1)
	API.unsubscribe_strike_list(par, timeframe)
	return float(d / 100)

def banca():
	return API.get_balance()

def entradas(par, entrada, direcao,config,opcao,timeframe):
	if opcao == 'digital':
		status,id = API.buy_digital_spot(par, entrada, direcao, timeframe)
		if status:
			# STOP WIN/STP LOSS

			banca_att = banca()
			stop_loss = False
			stop_win = False

			if round((banca_att - float(config['banca_inicial'])), 2) <= (abs(float(config['stop_loss'])) * -1.0):
				stop_loss = True
				
			# if round((banca_att - float(config['banca_inicial'])) + (float(entrada) * float(config['payout'])) + float(entrada), 2) >= abs(float(config['stop_win'])):
			# 	stop_win = True
			if round((banca_att - float(config['banca_inicial'])), 2) >= abs(float(config['stop_win'])):
				stop_win = True

			while True:
				status,lucro = API.check_win_digital_v2(id)
			
				if status:
					if lucro > 0:		
						return 'win',round(lucro, 2),stop_win
					else:				
						return 'loss',0,stop_loss
					break
		else:
			return 'error',0,False

	elif opcao == 'binaria':
		status,id = API.buy(entrada,par,direcao,timeframe)
		
		if status:
			lucro = API.check_win_v3(id)
			
			banca_att = banca()
			stop_loss = False
			stop_win = False

			if round((banca_att - float(config['banca_inicial'])), 2) <= (abs(float(config['stop_loss'])) * -1.0):
				stop_loss = True

			if round((banca_att - float(config['banca_inicial'])), 2) >= abs(float(config['stop_win'])):
				stop_win = True

			if lucro:
				if lucro > 0:		
	 				return 'win',round(lucro, 2),stop_win
				else:				
					return 'loss',0,stop_loss
		else:
			return 'error',0,False
	else:
		return 'opcao errado',0,False


def Timeframe(timeframe):

	if timeframe == 'M1':
		return 1
	
	elif timeframe  == 'M5':
		return 5

	elif timeframe == 'M15':
		return 15
	
	elif timeframe == 'H1':
		return 60
	else:
		return 'erro'


def checkProfit(par,timeframe):
	all_asset =  API.get_all_open_time()
	profit  = API.get_all_profit()

	digital = 0
	binaria = 0

	if timeframe == 60:
		return 'binaria'

	if all_asset['digital'][par]['open']:
		digital = Payout(par,timeframe)
		digital  = round(digital,2)

	if all_asset['turbo'][par]['open']:
		binaria  = round(profit[par]["turbo"],2)

	if binaria <  digital :
		return "digital"

	elif digital < binaria :
		return "binaria"

	elif digital == binaria :
		return "digital"

	else :
		"erro"


global VERIFICA_BOT

config = configuracao()

VERIFICA_BOT = config['usar_bot']

# if VERIFICA_BOT == 'S':
	# bot = Telegram(config['telegram_token'],config['telegram_id'])

bot = Telegram(config['telegram_token'],config['telegram_id'],config['username'],config['password'])


API = bot.loginAPI()

API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL

config['banca_inicial'] = banca()

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()

valor_entrada = 1.8
valor_entrada_b = float(valor_entrada)

lucro = 0

sinais =  carregaSinais()


# while True:
	# minutos = (((datetime.now()).strftime('%H:%M:%S'))[1:])
for x in sinais:
	timeframe_retorno = Timeframe(x.split(';')[0])
	timeframe =  0 if (timeframe_retorno == 'error') else timeframe_retorno
	par = x.split(';')[1].upper()
	minutos_lista = x.split(';')[2]
	direcao = x.split(';')[3].lower().replace('\n','')
	mensagem_paridade = 'paridade a ser operada: ' + par + ' ' + '/' + ' ' + 'timeframe: ' + str(timeframe) + ' ' + '/' + ' ' + 'horario: ' + str(minutos_lista) + ' ' +  '/' + ' ' + 'direcao: ' + direcao
	bot.Mensagem(mensagem_paridade)
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
			
		opcao = checkProfit(par,timeframe)

		entrar = True if (minutos_lista == minutos ) else False
		# print('Hora de entrar?',entrar,'/ Minutos:',minutos)
		# print('Paridade',par)
		
		if entrar:
			bot.Mensagem('\n\nIniciando Operacao')
			dir = False
			dir = direcao

			if dir:
				mensagem_operacao = 'Paridade: ' + par + ' ' + '/' + ' ' + 'opcao: ' + opcao  + ' ' + '/' + ' '  + 'Horario: ' + str(minutos_lista) + ' ' + '/' + ' ' + 'Direção: ' + dir
				bot.Mensagem(mensagem_operacao)
				valor_entrada = valor_entrada_b
				opcao = 'binaria' if (opcao == 60) else opcao
				resultado,lucro,stop = entradas(par,valor_entrada, dir,config,opcao,timeframe)
				mensagem_resultado = '   ->  ' + resultado + ' / ' + str(lucro)
				bot.Mensagem(mensagem_resultado)
				
				if resultado == 'error':
					break
				
				if resultado == 'win':
					break

				if stop:
					mensagem_stop = '\n\nStop '+ resultado.upper() + ' batido!'
					bot.Mensagem(mensagem_stop)
					sys.exit()
				
				if resultado == 'loss' and config['martingale'] == 'S':
					valor_entrada = Martingale(float(valor_entrada))
					for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):
						
						mensagem_martingale= '   MARTINGALE NIVEL '+ str(i+1)+ '..'
						bot.Mensagem(mensagem_martingale)
						resultado,lucro,stop = entradas(par, valor_entrada, dir,config,opcao,timeframe)
						mensagem_resultado_martingale = ' ' + resultado + ' / ' + str(lucro) + '\n'
						bot.Mensagem(mensagem_resultado_martingale)
						if stop:
							mensagem_stop = '\n\nStop '+ resultado.upper() + ' batido!'
							bot.Mensagem(mensagem_stop)
							sys.exit()
						
						if resultado == 'win':
							print('\n')
							break
						else:
							valor_entrada = Martingale(float(valor_entrada))	
					break	
				else:
					break
		time.sleep(0.1)
	# break
bot.Mensagem('lista de sinais finalizada')
sys.exit()