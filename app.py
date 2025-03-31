from flask import Flask, request, jsonify
from services import waha
import os


app = Flask(__name__)
waha = waha.Waha()

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

    # Para o "typing" no WhatsApp
    waha.stop_typing(from_user)

    # Envia a mesma resposta para o usuário
    waha.send_message(from_user, message)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
