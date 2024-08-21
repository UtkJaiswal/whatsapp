from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)


account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

client = Client(account_sid, auth_token)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("request message",request.values.get('Body',''))
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    
    if 'hello' in incoming_msg:
        msg.body('Hello! How can I help you today?')
    elif 'bye' in incoming_msg:
        msg.body('Goodbye! Have a great day!')
    else:
        msg.body('I am sorry, I didnt understand that. Can you please rephrase?')

    message_id = send_message("whatsapp:+916290750803","Hello")

    print("message id",message_id)

    return str(response)

def send_message(to, body):
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=body,
    to=to
    )
    return message.sid


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)