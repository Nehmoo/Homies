from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC3421bddca29bf7397de6922301736f65'
auth_token = '50726c76325c684fc1f71d0eee093293'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="bruh button8",
                     from_='+12132931328',
                     to='+16095822880'
                 )

print(message.sid)