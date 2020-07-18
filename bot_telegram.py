import telegram
from telegram import Bot
import telegram.ext as ext

from iqoptionapi.stable_api import IQ_Option
from utils import configuracao


class ApiConnection(object):
    _ApiConnection_instance = None
    _ApiConnection_connection = None
    _ApiConnection_connection: IQ_Option

    @property
    def connection(self):
        return self._ApiConnection_connection

    @connection.setter  
    def connection(self,value):
        self._ApiConnection_connection = value

    @staticmethod
    def instance():
        if not ApiConnection._ApiConnection_instance:
            ApiConnection._ApiConnection_instance = ApiConnection()
        return ApiConnection._ApiConnection_instance

class Telegram(Bot):

    def __init__(self):
        self.config = configuracao()
        self.token_id = self.config['telegram_token']
        self.chat_id = self.config['telegram_id']
        # self.username = self.config['email']
        self.password = self.config['password']
        self.usar_bot = bool(self.config['usar_bot'])
        self.valor_entrada_b = float(self.config['valor_entrada'])
        self.config['banca_inicial'] = self.banca()
        self.balance = 'PRACTICE'
        self.criaConexao()
        Bot.__init__(self, self.token_id)

    def criaConexao(self):
        apiConn = IQ_Option(self.username,self.password)
        apiConn.connect()
        apiConn.change_balance(self.balance)
        ApiConnection.instance().connection = apiConn

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

    def Mensagem(self, mensagem, reply_markup=None):
        if self.usar_bot:
            self.sendMessage(chat_id=self.chat_id,
                             text=mensagem, reply_markup=reply_markup)
        print(mensagem)

    def banca(self):
        return ApiConnection.instance().connection.get_balance()

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
        self.Mensagem(msg, reply_markup=reply_kb_markup)
        # update.sendMessage(chat_id=context.effective_chat.id,text=msg,reply_markup=reply_kb_markup)

    def BancaAtual(self, update, context):
        msg = "Sua Banca atual é de :" + str(self.banca())

        self.Mensagem(msg)
        # update.sendMessage(chat_id=context.effective_chat.id,text=msg)

    def Lucro(self, update, context):
        lucro = self.banca() - self.config['banca_inicial'] if self.banca(
        ) - self.config['banca_inicial'] > 0 else '-' + str(self.banca() - self.config['banca_inicial'])

        msg = "Seu lucro atual é de: " + str(lucro)

        self.Mensagem(msg)
