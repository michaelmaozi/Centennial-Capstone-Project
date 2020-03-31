from twilio.rest import Client
import json
import  requests

def send_single_sms(account_sid, auth_token, from_twilio_mobile, code, to_mobile):

  client = Client(account_sid, auth_token)

  message = client.messages.create(
    body="Verification Code: {}".format(code),
    from_=from_twilio_mobile,
    to=to_mobile
  )


  # if message.status == "200": 
  #   print("sent sms")
  # else:
  #   print("fail to send sms")
  #   print(message.error_code)
  #   print(message.error_code)

    # print("=====")
    # print(message.values)
  print("=====")
  print(message.status)
  print("=====")
  print(message.feedback)
  print("=====")
  print(message.body)
  print("====")

  # re_json = json.loads(message.sid)
  return message
  
    


if __name__ == "__main__":
    send_single_sms(
      "AC522ed3a7b6e89ed3e51c5c0057f048dd", 
      "a58697d91890e7014aaa3d15682e629a",
      "+12512573354",
      "1111",
      "+16478917886"
    )

