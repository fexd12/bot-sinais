# bot-sinais
<br>
Bot opera apartir de uma lista de sinais(binaria ou digital) <br>
<br>
Exemplo de sinais:<br>
  <p>M1;eurusd;23:19:00;CALL - timeframe de 1 minuto</p>
  <p>M5;gbpusd;03:54:00;CALL - timeframe de 5 minutos</p>
  <p>M15;eurusd;23:30:00;CALL - timeframe de 15 minutos</p>
  <p>H1;eurusd;00:00:00;CALL - timeframe de 1 hora</p>
<br>
Os sinais deve ser inserido em sinais.txt <br>
<br>
Em configuração.txt colocar seu stop_win e stop_loss <br>
<br> 
Instalar as dependencias necessarias:<br>
<p>pip install -r requirements.txt<p>
<br>
Para executar o robo: <br>
<p> python main.py </p>
<br>
Adicionado bot para Telegram , em que envia mensagem do status de cada operação eo seu resultado.

# Iniciar bot

Para seu bot comecar a realizar as operações, em um terminal de comando (CMD) basta digitar python ./main.py

ler Bot_Telegram para poder usar a nova função