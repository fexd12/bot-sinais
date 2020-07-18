from bot_telegram import Telegram as Operacao
from multiprocessing import Process

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

bot.connect()
bot.change_balance('PRACTICE') # PRACTICE / REAL


if bot.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()



if __name__ == "__main__":

	p1 = Process(target=botInicializa)
	p2 = Process(target=operacaoInicializa)

	p1.start()
	p2.start()