import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

def send_email(to_email='apiispanen@berkeley.edu', attachment=None, lyrics=None):
    try:
        lyrics = lyrics.replace("\n", "<br>")
        from apps.home.creds import SENDGRID_KEY
    except:
        SENDGRID_KEY = os.getenv('SENDGRID_KEY')

    message = Mail(
        from_email='appiispanen@gmail.com',
        to_emails=[to_email, 'apiispanen@berkeley.edu'],
        subject='Your RingleDingle in this Thingle',
        html_content=f'<strong>Ringles are great, especially with Dingles. Happy whatever day. Add some Ringle to your Dingle.</strong><br><br><h4>Lyrics</h4><br><br>{lyrics}')
    
    if attachment:
        with open('apps/static/media/output.mp3', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('ringledingle.mp3'),
            FileType('audio/mpeg'),
            Disposition('attachment')
        )
        message.attachment = attachedFile

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
