import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64
import urllib3


def send_email(to_email='apiispanen1@babson.edu', cc_email="", attachment=None, lyrics='No lyrics found', img_url=None, singer_name=None, title=None, note=""):
    
    if to_email != cc_email and cc_email != "":
        email_list = [Bcc('drew@ringledingle.com'), Cc(cc_email)]  # always include a Bcc address
    else:
        email_list = [Bcc('drew@ringledingle.com')]
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

    lyrics = lyrics.replace("\n", "<br>")
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
        # Now put the encoded file into an audio source string in html:
        # audio_player = f'<audio controls><source src="data:audio/mpeg;base64,{encoded_file}" type="audio/mpeg"></audio>'
        # audio_player = '<audio controls><source src="cid:ringledingle" type="audio/mpeg"/></audio>'
        # audio_player = encoded_file
        
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

        else:
            print('Failed to download image')

      
    # message.reply_to = 'apiispanen@berkeley.edu'
    message.template_id = 'd-9f8062ae69344b519ad5bf7da5040e0d'

    message.personalizations[0].dynamic_template_data =     {
        "lyrics": lyrics,
        "img_url": img_url,
        "singer_name": singer_name,
        "title": title,
        "note":note

    }

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)




# img_url = 'https://www.imagehost.at/images/2023/04/22/johnny-cash.png'

# title = "RingleDingle Blues"
# voice = "Johnny Cash"
# lyrics = """
# Hello, I'd like to tell you a poem I wrote today:
# I appreciate you, my friend,
# For trying out RingleDingle till the end.
# But now I'm hoping for something more,
# Your money, so I can soar.

# My app is great, that much is true,
# And with your help, it'll be worth your due.
# So don't hesitate to invest,
# In RingleDingle's success.

# Thank you for giving it a try,
# Now let's take this app up high.
# With your support and my dream in tow,
# RingleDingle will surely glow.
# """

# # EMAILS:

# emails = [
# "apiispanen1@babson.edu",
# "kl3272@drexel.edu",
# "Dougmac900@gmail.com",
# "adam.piispanen@foreveroceans.com",
# "rani.zierath@gmail.com",
# "5samcasey@gmail.com",
# "dwendling@umass.edu",
# "hannahpiispanen@gmail.com",
# "bnelson6630@gmail.com"
# ]

def send_simple_email(to_email='apiispanen@berkeley.edu',  cc_email = '' ,title = "", note="", link = ""):
    email_list = [Bcc('drew@ringledingle.com')]
    
    if cc_email in to_email or cc_email == None:
        cc_email = ''
    else:
        email_list.append(Cc(cc_email))
    # if to_email != '' and cc_email !='' :
    #     email_list.extend(cc_email)  # always include a Bcc address
    # elif to_email != '':
    #     email_list = [Bcc(bcc_email)]
    # else:
    #     email_list = []
      
    if ',' in to_email:
        # split the comma-separated string into a list of email addresses
        to_email_list = [e.strip() for e in to_email.split(',')]
        email_list.extend(to_email_list)
    else:
        email_list.append(to_email)

    print("email_list", email_list)
    try:
        from apps.home.creds import SENDGRID_KEY
    except:
        try:
            from creds import SENDGRID_KEY
        except:
            SENDGRID_KEY = os.getenv('SENDGRID_KEY')

    message = Mail(
        from_email='drew@ringledingle.com',
        to_emails=email_list
        )

    message.template_id = 'd-f0ed94505a0e4afab3f9418b9f01bb7b'


    if title != "":
        message.personalizations[0].dynamic_template_data = {"title": title, "note":note, "link":link}

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "Success"
    except Exception as e:
        print(e)
        return str(e)

# # send_email(to_email="", lyrics=lyrics, img_url=img_url, title=title, singer_name='Johnny Cash', attachment=True)
# send_simple_email(cc_email='apiispanen@berkeley.edu')

def send_demo_email(to_email,first_name):

    try:
        from apps.home.creds import SENDGRID_KEY
    except:
        try:
            from creds import SENDGRID_KEY
        except:
            SENDGRID_KEY = os.getenv('SENDGRID_KEY')

    message = Mail(
        from_email='apiispanen1@babson.edu',
        to_emails=to_email
        )
    

    message.template_id = 'd-98ed6819d1924c9f87cbbc34c517d112'


    message.personalizations[0].dynamic_template_data =     {
        "first_name": first_name
    }


    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "Success"
    except Exception as e:
        print(e)
        return str(e)



# may5_mailing = [

# ]


# for email in may5_mailing:
#     # print the key and the value as strings
#     email_address = email[0]
#     # get the first name from the [1] index and by splitting the string on the space
#     first_name = email[1].split(" ")[0]
#     print(email_address, first_name)
#     send_demo_email(to_email=email_address, first_name=first_name)