import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def warning_mail(h: float, flood: bool) -> None:
    '''
    Sends warning email to me when the path is flooded using mail
    server on Pi
    Inputs:
        h           -   River level
        flood       -   Boolean to say if path is flooded
    '''
    # Get email to send alert to (in enviroment variables
    to_addr = os.environ.get('EMAIL_TO')

    # Get correct message
    if flood:
        # Construct command-line message
        msg = f'The path is currently flooded and the level is at {h:.2f} m'
        subject = 'Flood Warning'
    else:
        msg = f'The path should have cleared - the level is at {h:.2f} m'
        subject = 'Flood Update'

    # Create the email message
    msgRoot = MIMEMultipart('alternative')
    msgRoot['To'] = to_addr
    msgRoot['Subject'] = subject
    text = MIMEText(msg, 'plain', 'utf-8')
    msgRoot.attach(text)

    # Connect to localhost and send using sendmail
    with smtplib.SMTP('localhost') as smtp:
        smtp.sendmail('localhost', to_addr, msgRoot.as_string())
