from operacao.services import Operacao
from multiprocessing import Process
import sys

def botInicializa():
	print('Iniciando Comandos ....')
	updater = bot.InicializaBot() #inicialização do bot com os comandos 
	dispacher = updater.dispatcher
	bot.MonitoraBot(dispacher)
	print('Comandos do bot Iniciado.')
	updater.start_polling()
	# updater.idle()

def operacaoInicializa():
	print('Iniciando Operação')
	bot.RealizaOperacao()

bot = Operacao()

if bot.API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	sys.exit()

if __name__ == "__main__":

	p1 = Process(target=botInicializa)
	p2 = Process(target=operacaoInicializa)

	p1.start()
	p2.start()