import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    
    # Email credentials and server details
from_address = "api@sourceatlantic.ca"
to_address = "kannana@SourceAtlantic.ca"
smtp_server = "10.37.4.158"
smtp_port = 25
    
def send_error_email(error_message,provider):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Failed to fetch data from "+provider
    
    body = f"We couldn't able to retrive "+provider+" data for particular input [{error_message}]"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print("IT team notified")
    except Exception as e:
        print(f"Failed to send email: {e}")