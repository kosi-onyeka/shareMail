from flask import Flask, request
from twilio.rest import Client
from EmailService import EmailService
import os

app = Flask(__name__)
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)

@app.route('/testAPI', methods=['GET'])
def testAPI():
    mailService = EmailService()
    mailService.getHuluLogin()
    response = mailService.verification_code
    return(response)

@app.route('/sms', methods=['GET'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    
    if message_body.lower() == "hulu".lower():
        mailService = EmailService()
        mailService.getHuluLogin()
        response = mailService.verification_code
    else:
        response = 'Wrong request. Reach out to Kosi :)'

    message = client.messages.create(
        body = response,
        from_='+18556191591',
        to= number
    )
    return str(response)


if __name__ == '__main__':
    app.run(port=5002, debug=True)