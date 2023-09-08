import requests
def send_to_telegram(message):
    
    try:
        apiToken = '6058041177:AAHhrqXPDRa1vghxQu_dTyTXTar1JRgNjCo'
        chatID = '1083941928'
        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)