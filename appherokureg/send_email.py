import sendgrid
import os
from sendgrid.helpers.mail import *
import qrcode
import io
import base64
from projherokureg.settings import SENDGRID_KEY


def send_notification(to_email, subject):
    mail = prepare_email(to_email, subject)
    do_it(mail)


def prepare_email(recipient, subject):

    from_email = Email('feliperyan@gmail.com')
    subj = subject
    to_email = Email(recipient)
    content = Content('text/html', '<html><body><h1>yolo</h1></body></html>')

    mail = Mail(from_email, subj, to_email, content)

    img = qrcode.make('some rubbish')
    b = io.BytesIO()
    img.save(b, format='PNG')
    s = b.getvalue()
    result = base64.b64encode(s).decode()

    a = Attachment()
    a.set_content(result)
    a.set_content_id('qr code')
    a.set_disposition('attachment')
    a.set_type('image/png')
    a.set_filename('code.png')

    mail.add_attachment(a)

    return mail


def do_it(the_mail):

    key = SENDGRID_KEY
    sg = sendgrid.SendGridAPIClient(apikey=key)
    res = sg.client.mail.send.post(request_body=the_mail.get())
    print(res.status_code)

