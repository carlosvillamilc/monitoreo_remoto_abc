
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import create_engine

import smtplib
import sys
import traceback


def send_email(message, to_address):
    # message
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['Subject'] = 'Notificaciones X'
    msg['From'] = cfg.app_email
    msg['To'] = to_address
    msg.attach(MIMEText(message.encode('utf-8'), 'html', 'UTF-8'))
    # server connection
    with smtplib.SMTP(cfg.smtp_host, cfg.smtp_port) as server:
        server.send_message(msg)