import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
outbound_number = os.environ['TWILIO_OUTBOUND_PHONE']
client = Client(account_sid, auth_token)


def send_sms_message(recipient_num, message):
    client.messages \
        .create(
            body=message,
            from_=outbound_number,
            to=recipient_num
        )

def receive_sms_message(request):
    return request.values.get('Body', None)

