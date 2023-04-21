import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64
import urllib3


def send_email(to_email='apiispanen1@babson.edu', attachment=None, lyrics='No lyrics found', img_url=None, singer_name=None, title=None):
    email_list = [Bcc('apiispanen@berkeley.edu')]  # always include a Bcc address
    if ',' in to_email:
        # split the comma-separated string into a list of email addresses
        to_email_list = [e.strip() for e in to_email.split(',')]
        email_list.extend(to_email_list)
    else:
        email_list.append(to_email)

    try:
        from apps.home.creds import SENDGRID_KEY
    except:
        try:
            from creds import SENDGRID_KEY
        except:
            SENDGRID_KEY = os.getenv('SENDGRID_KEY')


    # lyrics = lyrics.replace("\n", "<br>")
    message = Mail(
        from_email='drew@ringledingle.com',
        to_emails=email_list,
        subject='Your RingleDingle in this Thingle',
        # html_content=f'<strong>Ringles are great, especially with Dingles. Happy whatever day. Add some Ringle to your Dingle.</strong><br><br><h4>Lyrics</h4><br><br>{lyrics}',
        )

    if attachment:
        with open('apps/static/media/output.mp3', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('ringledingle.mp3'),
            FileType('audio/mpeg'),
            Disposition('attachment'),
            ContentId('ringledingle')
                            )
        message.add_attachment(attachedFile)
    
    if img_url:
        http = urllib3.PoolManager()
        response = http.request('GET', img_url)

        if response.status == 200:
            image_binary = response.data
            # `image_binary` now contains the binary data of the image
        else:
            print('Failed to download image')

        # encode the image
        encoded_file = base64.b64encode(image_binary).decode()
        # img_url = f'data:image/png;base64,{encoded_file}'
        
        attachedFile2 = Attachment(
            FileContent(encoded_file),
            FileName('ringleimage.png'),
            FileType('image/png'),
            Disposition('attachment'),
            ContentId('ringleimage')
        )
        attachedFile2.content_id = 'ringleimage'
        message.add_attachment(attachedFile2)

    message.reply_to = 'apiispanen@berkeley.edu'
    message.template_id = 'd-9f8062ae69344b519ad5bf7da5040e0d'

    message.personalizations[0].dynamic_template_data =     {
        "lyrics": lyrics,
        "img_url": img_url,
        "singer_name": singer_name,
        "title": title

    }

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)




# img_url = 'https://lh6.googleusercontent.com/-qcLTPwh675Y/AAAAAAAAAAI/AAAAAAAACKc/Xgrv1h5ejAw/photo.jpg?sz=64'

# title = "Tony's Birthday Wishes"

# lyrics = """Tony, my dear friend, it's your special day,
# I hope you have a happy birthday in every way.
# Even though your friends may not like you,
# Just know that I'll always be there for you.

# You may be unpopular and alone,
# But with me by your side, you're never on your own.
# So blow out the candles and make a wish,
# I promise to grant it with a hug and a kiss.

# Don't worry about what others say or do,
# Just focus on the love that surrounds you.
# On this day, let all your worries fade away,
# And celebrate another year of being okay.

# Happy birthday Tony, from me to you,
# May all your dreams and wishes come true."""




# send_email(lyrics=lyrics, img_url=img_url, title=title, singer_name='pooh-brock-baker', attachment=True)