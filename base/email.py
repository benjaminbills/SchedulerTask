from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_reset_password_email(name, reciever, password):
  # Creating message subject and sender
  subject = 'Reset Password.'
  sender = 'oneobaben@gmail.com'
  text_content = render_to_string('email/resetpasswordmail.txt',{"name": name, "password":password})
  html_content = render_to_string('email/resetpasswordmail.html',{"name": name, "password":password})

  msg = EmailMultiAlternatives(subject,text_content,sender,[reciever])
  msg.attach_alternative(html_content,'text/html')
  msg.send()

def send_happy_birthday(name, reciever):
  # Creating message subject and sender
  subject = 'Happy Birthday'
  sender = 'oneobaben@gmail.com'
  text_content = render_to_string('email/happybirthday.txt',{"name": name})
  html_content = render_to_string('email/happybirthday.html',{"name": name})

  msg = EmailMultiAlternatives(subject,text_content,sender,[reciever])
  msg.attach_alternative(html_content,'text/html')
  msg.send()