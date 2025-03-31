import requests

class Waha:
    def __init__(self):
        self.__api_url = 'http://waha:3000'

    def send_message(self, chat_id, message):
        url = f'{self.__api_url}/api/sendText'
        
        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }

        requests.post(url, headers=headers, json=payload)

    def send_seen(self, chat_id, id_message):
        url = f'{self.__api_url}/api/sendSeen'
        
        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            'session': 'default',
            'chatId': chat_id,
            'messageId': id_message,
        }

        requests.post(url, headers=headers, json=payload)
    
    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping'
        
        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        requests.post(url, headers=headers, json=payload)
    
    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping'
        
        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        requests.post(url, headers=headers, json=payload)
    