import smtplib
from numpy import random

from email.message import EmailMessage

gmail_user = 'ambidexter228@gmail.com'
gmail_password = '218591Py@'
sent_from = gmail_user

to = []
subject = 'GlobalLogic Autorization'

def gen_code():
    x=random.randint(9, size=(2, 3))
    a=' '
    for i in x:
        for j in i:
            a+=str(j)
        a+=' '
    return a

def send_code(mail,body):
    subject = 'GlobalLogic Autorization'
    TEXT='Autorization code: {}'.format(body)
    SUBJECT='GlobalLogic Autorization'
    email_text = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, mail, email_text)
        server.close()
    except Exception as ex:
        print("[!] error - {}".format(str(ex)))
        print('Something went wrong...')

# send_code('pavlo.mikush@globallogic.com',gen_code())
