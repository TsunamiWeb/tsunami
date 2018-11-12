from uvtor.conf import settings
from email import encoders
from email.header import Header
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mimetypes
import re
import smtplib
import aiosmtplib
import logging


async def send_email(mail_subject, mail_content, receiver_list, cc_list=[]):
    sender = settings.EMAIL_USERNAME
    username = settings.EMAIL_USERNAME
    password = settings.EMAIL_PASSWORD
    smtp = aiosmtplib.SMTP(hostname=settings.EMAIL_SMTP_SERVER)
    await smtp.connect()
    await smtp.login(username, password)
    msg = MIMEText(mail_content)
    msg['Subject'] = Header(mail_subject, 'utf-8')
    msg['From'] = username
    msg['To'] = ','.join(receiver_list)
    msg['CC'] = ','.join(cc_list)
    await smtp.send_message(msg)
    logging.debug(f'Email `{mail_subject}` is sent successfully')
    await smtp.quit()
