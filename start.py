from bot_telegram import Telegram
from utils import configuracao

config = configuracao()

bot = Telegram(config['telegram_token'],config['telegram_id'],config['username'],config['password'])

print('Iniciando Comandos ....')
updater = bot.InicializaBot() #inicialização do bot com os comandos 
dispacher = updater.dispatcher
bot.MonitoraBot(dispacher)
print('Comandos do bot Iniciado.')
updater.start_polling()
# updater.idle()