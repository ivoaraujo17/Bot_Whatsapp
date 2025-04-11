from flask import Flask, request, jsonify
from services import waha
from services import bot
import os
from dotenv import load_dotenv


app = Flask(__name__)
waha = waha.Waha()

load_dotenv()

api_key = os.getenv("API_KEY_MARITAKA_BOT")
bot = bot.PizzaBot()

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    payload = data['payload']

    id_message = payload['id']
    from_user = payload['from']
    message = payload['body']

    print("\nUser ID:", from_user)
    print("Message from user:", message)

    if '@g.us' in from_user or "status@broadcast" in from_user:
        print("Ignoring group message")
        return jsonify({'status': 'success'}), 200

    # envia o "seen" para o WhatsApp
    waha.send_seen(from_user, id_message)

    # Inicia o "typing" no WhatsApp
    waha.start_typing(from_user)

    # Busca a resposta do bot
    resposta = bot.perguntar(message)
    print("Resposta do bot:", resposta)

    # Para o "typing" no WhatsApp
    waha.stop_typing(from_user)

    # Envia a mesma resposta para o usuário
    waha.send_message(from_user, resposta['output'])
    print("Mensagem enviada para o usuário:", resposta['output'])

    return jsonify({'status': 'success'}), 200

@app.route('/', methods=['GET'])
def verify_webhook():
    # Verifica se o webhook está funcionando corretamente
    # retorna uma pagina html simples
    return "<h1>Webhook is working</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
