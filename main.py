from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests
import google.generativeai as genai


app = Flask(__name__)


account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')


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
    
    modified_prompt = f"Provide a detailed explanation about {prompt} in 1200 characters or less."

    response = model.generate_content(modified_prompt)
    response_text = response.text
    print("Response from Gemini API:", response_text)
    return response_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)