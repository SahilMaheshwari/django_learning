import os
from email.message import EmailMessage
import ssl
import smtplib
import time
import codecs
from email.utils import make_msgid
from smtplib import SMTPException

# import environ
# env = environ.Env()
# environ.Env.read_env()

#password = env("EMAIL_PASS")
password = os.environ.get("EMAIL_PASS")

def sendDaMail(towho, name, product, quantity):
    global password

    print('SENDING DA MAIL '+towho)

    email_sender = 'sahil7503@gmail.com'
    email_password = password

    email_reciver = towho

    subject = 'Order placed!'
    body = f"""Dear {name},
An order has been placed for {quantity} {product} 
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        try:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_reciver, em.as_string())
        except SMTPException as e:
            print(f"mail wasnt sent to {name} because {e}")

    print('DONE')