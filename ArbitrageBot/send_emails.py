import smtplib
import pandas as pd
import datetime
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_daily_email(non_empty_arbitrage_tables, file_path): 
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    # SMTP server details for Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # Gmail account credentials
    sender_email = 'footballbettingarbitrage@gmail.com'
    sender_password = 'svpezskzjdheqbzo'
    receiver_email = 'cookieninja78@gmail.com'

    body = 'Hi there, \n \n Here is the daily update on football arbitrage opportunities in EFL League One. We have also attached an excel file of all of the arbitrage opportunities for your convenience. \n \n Thank you! \n'
    msg = MIMEMultipart()

    msg.attach(MIMEText(body, 'plain'))

    for name, match_data in non_empty_arbitrage_tables.items():
        msg.attach(MIMEText(name, 'plain'))
        html_table = match_data.to_html(index=False)
        msg.attach(MIMEText(html_table, 'html'))
    
    with open(file_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        msg.attach(part)

    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'Daily arbitrage opportunity update {current_date}'

    # Connect to the SMTP server and send the email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
    except smtplib.SMTPException as e:
        print(f'Error: Unable to send email. {e}')
    except smtplib.SMTPAuthenticationError:
        print('Error: Authentication failed. Check your email account credentials.')
    finally:
        server.quit()