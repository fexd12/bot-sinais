import telegram
import telegram.ext as ext

from iqoptionapi.stable_api import IQ_Option
from utils import configuracao

class Telegram():
    
    def __init__(self,token,id,username,password):
        self.token_id = token
        self.chat_id = id
        self.username = username
        self.password = password
        self.bot = telegram.Bot(token=self.token_id)
        self.API = IQ_Option(self.username,self.password)
        self.config = configuracao()
        self.config['banca_inicial'] = self.banca()

    def MonitoraBot(self,dispacher):

        start_handler = ext.CommandHandler('start',self.Start)
        banca_handler = ext.CommandHandler('banca',self.BancaAtual)
        lucro_handler = ext.CommandHandler('lucro',self.Lucro)
        # unknow_handler = ext.MessageHandler([ext.Filters.command],self.Unknown)
            
        dispacher.add_handler(start_handler)
        dispacher.add_handler(banca_handler)
        dispacher.add_handler(lucro_handler)
        # dispacher.add_handler(unknow_handler)

    def loginAPI(self):
        return self.API

    def InicializaBot(self):
        return ext.Updater(token=self.token_id)

    def login(self):
        return self.bot

    def Mensagem(self,mensagem,reply_markup=None,send_print=True):
        if send_print:
            print(mensagem)
        self.bot.sendMessage(chat_id = self.chat_id, text = mensagem,reply_markup=reply_markup)

    def banca(self):
        self.API.connect()
        self.API.change_balance('PRACTICE') #or REAL
        return self.API.get_balance()

    def Start(self,update,context):
        me = update.get_me()

        msg = "Hello!\n"
        msg += "I'm {0} and I came here to help you.\n".format(me.first_name) #nore do bot
        msg += "What would you like to do?\n\n"

        msg += "/banca - Verify your money \n"
        msg += "/lucro - check your profit \n\n"
        msg += "/start - if u want to check the commands \n\n\n"

        # Commands menu
        main_menu_keyboard = [[telegram.KeyboardButton('/banca')],
                            [telegram.KeyboardButton('/lucro')]]
        reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                    resize_keyboard=True,
                                                    one_time_keyboard=True)

        # Send the message with menu
        self.Mensagem(msg,reply_markup=reply_kb_markup,send_print=False)
        # update.sendMessage(chat_id=context.effective_chat.id,text=msg,reply_markup=reply_kb_markup)

    def BancaAtual(self,update,context):
        msg= "Sua Banca atual é de :" + str(self.banca())

        self.Mensagem(msg,send_print=False)
        # update.sendMessage(chat_id=context.effective_chat.id,text=msg)
    
    def Lucro(self,update,context):
        lucro =  self.banca() - self.config['banca_inicial'] if self.banca() - self.config['banca_inicial'] > 0 else '-' + str(self.banca() - self.config['banca_inicial'])

        msg = "Seu lucro atual é de: " + str(lucro)

        self.Mensagem(msg,send_print=False)