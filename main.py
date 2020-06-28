#pip install git+https://github.com/fexd12/iqoptionapi.git --user
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time, json, logging, configparser
from dateutil import tz
import sys

logging.disable(level=(logging.DEBUG))


def stop(lucro, gain, loss):
	print('lucro',lucro)
	if lucro <= float('-' + str(abs(loss))):
		print('Stop Loss batido!')
		sys.exit()
		
	if lucro >= float(abs(gain)):
		print('Stop Gain Batido!')
		sys.exit()

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
	for i in range(0,2):
		d = API.get_digital_current_profit(par, timeframe)
		time.sleep(1)
	API.unsubscribe_strike_list(par, timeframe)
	if d != False:
		return float(d / 100)
	else:
		return 0

def banca():
	return API.get_balance()

def configuracao():
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')	
		
	return {'stop_win': arquivo.get('GERAL', 'stop_win'),'stop_loss': arquivo.get('GERAL', 'stop_loss'), 'payout': 0, 'banca_inicial': banca(), 'martingale': arquivo.get('GERAL', 'martingale'), 'sorosgale': arquivo.get('GERAL', 'sorosgale'), 'niveis': arquivo.get('GERAL', 'niveis')}

def carregaSinais():
	x = open('sinais.txt')
	y=[]
	for i in x.readlines():
		# print(i)
		y.append(i.replace(':00;',';'))
	# print (y)
	x.close
	return y

def entradas(par, entrada, direcao,config,opcao):
	if opcao == 'digital':
		status,id = API.buy_digital_spot(par, entrada, direcao, 5)
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
		status,id = API.buy(entrada,par,direcao,5)
		
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


def timestamp_converter():
	hora = datetime.now()
	tm = tz.gettz('America/Sao Paulo')
	hora_atual = hora.astimezone(tm)
	return hora_atual.strftime('%H:%M')
	# hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%H:%M:%S'), '%H:%M:%S')
	# hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	# return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6] if retorno == 1 else hora.astimezone(tz.gettz('America/Sao Paulo'))

def checkProfit(par,timeframe):
	profit_Binary  = API.get_all_profit()
	profit_Digital = Payout(par, timeframe)

	profit_Binary_Real  = round(profit_Binary[par]["turbo"],2)
	profit_Digital = round(profit_Digital,2)

	if profit_Binary_Real <  profit_Digital :
		return "digital"

	elif profit_Digital < profit_Binary_Real :
		return "binaria"

	elif profit_Digital == profit_Binary_Real :
		return "digital"

	else :
		"erro"

API = IQ_Option('','')
API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

config = configuracao()
config['banca_inicial'] = banca()

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()

valor_entrada = 1.8
valor_entrada_b = float(valor_entrada)

timeframe = 5
lucro = 0

sinais =  carregaSinais()


# while True:
	# minutos = (((datetime.now()).strftime('%H:%M:%S'))[1:])
for x in sinais:
	par = x.split(';')[1].upper()
	minutos_lista = x.split(';')[2]
	direcao = x.split(';')[3].lower().replace('\n','')
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
			
		opcao = checkProfit(par,5)

		entrar = True if (minutos_lista == minutos ) else False
		# print('Hora de entrar?',entrar,'/ Minutos:',minutos)
		# print('Paridade',par)
		
		if entrar:
			print('\n\nIniciando operação!')
			dir = False
			dir = direcao

			if dir:
				print('Paridade',par,'opcao:',opcao,'/','Horario:',minutos_lista,'/','Direção:',dir)
				valor_entrada = valor_entrada_b
				resultado,lucro,stop = entradas(par,valor_entrada, dir,config,opcao)
				print('   -> ',resultado,'/',lucro,'\n\n')
				if resultado == 'error':
					break
				
				if resultado == 'win':
					break

				if stop:
					print('\n\nStop',resultado.upper(),'batido!')
					sys.exit()
				
				if resultado == 'loss' and config['martingale'] == 'S':
					valor_entrada = Martingale(float(valor_entrada))
					for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):
						
						print('   MARTINGALE NIVEL '+str(i+1)+'..', end='')
						resultado,lucro,stop = entradas(par, valor_entrada, dir,config,opcao)
						print(' ',resultado,'/',lucro,'\n')
						if stop:
							print('\n\nStop',resultado.upper(),'batido!')
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
print('lista de sinais finalizada')
sys.exit()