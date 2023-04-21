import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64

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
    print(SENDGRID_KEY)
    # lyrics = lyrics.replace("\n", "<br>")
    message = Mail(
        from_email='drew@ringledingle.com',
        to_emails=email_list,
        subject='Your RingleDingle in this Thingle'
        # html_content=f'<strong>Ringles are great, especially with Dingles. Happy whatever day. Add some Ringle to your Dingle.</strong><br><br><h4>Lyrics</h4><br><br>{lyrics}',
        )
    message.reply_to = 'apiispanen@berkeley.edu'
    # message.add_bcc = "apiispanen@berkeley.edu"
    message.template_id = 'd-9f8062ae69344b519ad5bf7da5040e0d'

    message.personalizations[0].dynamic_template_data =     {
        "lyrics": lyrics,
        "img_url": img_url,
        "singer_name": singer_name,
        "title": title

    }

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
    
    # if img_url:
    #     attachedFile = Attachment(
    #         FileContent(img_url),
    #         FileName('ringledingle.png'),
    #         FileType('image/png'),
    #         Disposition('attachment')
    #     )
    #     message.attachment = attachedFile

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)



# img_url = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jNnj47oni5w3Xad1a5a6oVvz/user-FWQEWAK741HhjIuROK9YxBW3/img-eK4RWjWAQOjw1Sa9Tndc3LMq.png?st=2023-04-18T15%3A19%3A59Z&se=2023-04-18T17%3A19%3A59Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-04-18T16%3A02%3A25Z&ske=2023-04-19T16%3A02%3A25Z&sks=b&skv=2021-08-06&sig=atNc8nTkgDRya3ddQJ7tk0IghXUKJSNQ2xGBT/q1mV0%3D'

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




# send_email(second_email='appiispanen@gmail.com', lyrics=lyrics, img_url=img_url, title=title, singer_name='pooh-brock-baker')