from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests


app = Flask(__name__)


account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')

client = Client(account_sid, auth_token)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("request message",request.values.get('Body',''))
    incoming_msg = request.values.get('Body', '').lower()

    response_from_gemini = send_to_gemini_api(incoming_msg)

    twilio_response = MessagingResponse()

    msg = twilio_response.message()

    msg.body(response_from_gemini)

        
    message_id = send_message("whatsapp:+916290750803",response_from_gemini)

    

    return str(twilio_response)

def send_message(to, body):
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=body,
    to=to
    )
    return message.sid


def send_to_gemini_api(prompt):
    url = "https://api.anthropic.com/v1/chat"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": gemini_api_key
    }
    data = {
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9,
        "n": 1,
        "stream": False,
        "stop": None,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "model": "gpt-3.5-flash"
    }

    response = requests.post(url, headers=headers, json=data)
    response_text = response.json()["choices"][0]["message"]["content"]
    return response_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)