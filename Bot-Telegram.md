# bot Telegram

Para habilitar o bot, em config.txt colocar S em usar_bot ou N para nao usar o bot 

Abaixo tutorial de como criar um bot no Telegram

1. Fale com o BotFather em https://telegram.me/botfather
2. Mande uma mensagem `/newbot` pra ele, escolha um nome pro bot
3. Ele irá responder com um token de acesso, um longo texto de números e letras. Salve esse token em um lugar seguro
4. Adicione seu novo bot no Telegram
5. Crie um novo grupo para testes só com você e seu bot
6. Vá em https://web.telegram.org e clique no seu novo grupo
7. No link do seu browser, vai aparecer algo do tipo `https://web.telegram.org/#/im?p=g12345678`
8. Anote esse número no final do link(somente o numero sem o 'g'), ele é o ID desse chat (sendo um chat de grupo, você terá que adicionar um sinal de menos `-` na frente do ID para usá-lo),exemplo -123456789
9. Instale a dependência: `pip install -r requirements.txt`
10. Em config.txt,coloque seu token e ID do chat, obtido anteriormente

Dúvidas? Leia https://github.com/python-telegram-bot/python-telegram-bot

Lembre-se: não compartilhe seu token com ninguém, nem suba ele no GitHub, ou outras pessoas poderão usar seu bot!