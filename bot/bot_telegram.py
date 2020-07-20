from telegram import Bot
from utils.utils import configuracao
from iqoptionapi.stable_api import IQ_Option

import time, sys, logging, telegram
import telegram.ext as ext

logging.disable(level=(logging.DEBUG))

class Main():
    def __init__(self):
        self.config                     = configuracao()
        self.token_id                   = self.config['telegram_token']
        self.chat_id                    = self.config['telegram_id']
        self.username                   = self.config['email']
        self.password                   = self.config['password']
        self.bot                        = Bot(token=self.token_id)
        self.usar_bot                   = bool(self.config['usar_bot'])
        self.valor_entrada_b            = float(self.config['valor_entrada'])
        self.balance                    = str(self.config['balance'])
        self.API                        = IQ_Option(self.username,self.password)
        self.conecta()
        self.config['banca_inicial']    = self.banca()
    
    def conecta(self):
        self.API.connect()
        self.API.change_balance(self.balance)

    def banca(self):
        # self.conecta()
        return self.API.get_balance()
        # return 10

    def MonitoraBot(self, dispacher):

        start_handler = ext.CommandHandler('start', self.Start)
        banca_handler = ext.CommandHandler('banca', self.BancaAtual)
        lucro_handler = ext.CommandHandler('lucro', self.Lucro)
        # unknow_handler = ext.MessageHandler([ext.Filters.command],self.Unknown)

        dispacher.add_handler(start_handler)
        dispacher.add_handler(banca_handler)
        dispacher.add_handler(lucro_handler)
        # dispacher.add_handler(unknow_handler)

    # def loginAPI(self):
    #     self.connect()
    #     self.change_balance('PRACTICE') #or REAL
    #     return self.API

    def InicializaBot(self):
        return ext.Updater(token=self.token_id)

    # def login(self):
    #     return self.bot

    def Mensagem(self, mensagem, reply_markup=None,print_msg=True):
        if self.usar_bot:
            self.bot.sendMessage(chat_id=self.chat_id,
                             text=mensagem, reply_markup=reply_markup)
        if print_msg:
            print(mensagem)

    def Start(self, update, context):
        me = update.get_me()

        msg = "Hello!\n"
        # nore do bot
        msg += "I'm {0} and I came here to help you.\n".format(me.first_name)
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
        self.Mensagem(msg, reply_markup=reply_kb_markup,print_msg=False)
        # update.sendMessage(chat_id=context.effective_chat.id,text=msg,reply_markup=reply_kb_markup)

    def BancaAtual(self, update, context):
        msg = "Sua Banca atual é de :" + str(self.banca())

        self.Mensagem(msg,print_msg=False)
        # update.sendMessage(chat_id=context.effective_chat.id,text=msg)

    def Lucro(self, update, context):
        lucro = round(self.banca() - self.config['banca_inicial'],2) if self.banca(
        ) - self.config['banca_inicial'] > 0 else '-' + str(round(self.banca() - self.config['banca_inicial'],2))
        msg = "Seu lucro atual é de: " + str(lucro)

        self.Mensagem(msg,print_msg=False)
