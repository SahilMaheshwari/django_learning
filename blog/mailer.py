import os
from email.message import EmailMessage
import ssl
import smtplib
import time
import codecs
from email.utils import make_msgid

def sendDaMail(towho, name):

    print('SENDING DA MAIL '+towho)

    email_sender = ''     #email here
    email_password = ''   #password here

    email_reciver = towho

    subject = 'Order placed!'
    body = """<html>
<body>
<p>Dear {name},</p>
<p>An order has been placed :D.</p>
</body>
</html>
    """.format(name)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciver, em.as_string())

    print('DONE')