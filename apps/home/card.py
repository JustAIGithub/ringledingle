# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from bson.objectid import ObjectId
from datetime import datetime as dt
import os
# from stt import speech_to_text
from audiobook import make_narration
from prompt import ai_response, generate_image, ai_response_stream
from send import send_email
from html import escape
# from flask_paginate import Pagination, get_page_parameter
from urllib.parse import unquote
import urllib
from store_music import *


def ringledingle(words, voice, singer_name, input_file, email, email_customer=False):

    print("******** LET'S MAKE A GREETING CARD WITH RINGLEDINGLE ********")

    # with datetime, return month, day, year as YYMMDD:
    date = dt.now().strftime("%y%m%d")

    ai_request = "Generate a 3 stanza poem that will be narrated by "+singer_name+". Your poem MUST be in between the deliminiters STARTPOEM and ENDPOEM (respond with poem text ONLY, no 'Verse 1:' labels either).\n Also, the poem title will be between delimiters STARTTITLE and ENDTITLE.\nMake this poem from the following\n"+words


    # ai_payload = ai_response(ai_request)
    ai_payload=    """
    STARTTITLE
    My Love for Charity
    ENDTITLE
    STARTPOEM
    Charity is my gf, she loves me so much,
    She's always there for me, with a gentle touch.
    She'd do anything for me, even take a life,
    But I would never ask her to cause any strife.
    Her heart is pure gold, and her love is true,
    I am the luckiest person to have found you.
    You make my life complete, and I'm grateful each day,
    For your love that shines bright in every way.
    We may not be perfect, but we're perfect together,
    Our love will last forever and ever.
    Thank you for being the one who loves me so much,
    My beautiful Charity, my heart's sweetest touch.
    ENDPOEM
            """

    poem_lyrics = ai_payload[ai_payload.find("STARTPOEM") + len("STARTPOEM"):ai_payload.find("ENDPOEM")].strip()
    title = ai_payload[ai_payload.find("STARTTITLE") + len("STARTTITLE:"):ai_payload.find("ENDTITLE")].strip()
    dalle_request = ai_response(f"Describe in one sentence what a cover photo would be for the poem (i.e. the string will get processed in DALLE for AI image rendering), and put that prompt string in between the delimiters STARTDALLE and ENDDALLE.\n{poem_lyrics}")
    dalle_request = dalle_request[dalle_request.find("STARTDALLE") + len("STARTDALLE:"):dalle_request.find("ENDDALLE")].strip()

    # print(f'Dalle request: {dalle_request}')
    output_file = "output.mp3"
    
    make_narration(f'{input_file}', f'apps/static/media/{output_file}', poem_lyrics,voice=voice)

    if email != "":
        log_info(email)

    if email_customer:
        send_email(to_email=email, attachment=f'apps/static/media/{output_file}', lyrics=poem_lyrics, img_url=img_url, singer_name=singer_name, title=title) 

    # Make text file to upload
    with open('apps/static/media/temp.txt', 'w') as f:
        f.write(f"{title}\n\nIn the style of {singer_name}\n\n{poem_lyrics}\n\nDalle Request: {dalle_request}")

    print("Ringle has been Dingled! Uploading...")
    # Upload Audio 
    audio_url = upload_file(f'apps/static/media/{output_file}', f'cards/{date}/{title}/audio.mp3')   
    # Upload Text
    upload_file('apps/static/media/temp.txt', f'cards/{date}/{title}/text.txt')
    # Upload QR code

    # Get QR code:
    qr_code = generate_qr_code(audio_url)
    upload_file(f'{qr_code}', f'cards/{date}/{title}/qr.png')

    print("Creating image...")
    try:
        KeyError
        img_url = generate_image("A cartoon of "+dalle_request, size=3)
        # Save the image from the url
        urllib.request.urlretrieve(img_url, f'apps/static/media/image.png')
        print("Done, now uploading image...")
        # Upload Image
        upload_file(f'apps/static/media/image.png', f'cards/{date}/{title}/image.png')
    except:
        print("DALLE FAILED - Go back and try generate_image() again")


    emails = collection.find()
    emails = [email_item['email'] for email_item in emails]
    if email not in emails:
        now = datetime.datetime.now()
        log_time = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            ip_address = request.remote_addr
        except:
            ip_address = "unknown"
        collection.insert_one({"email": email, "timestamp": log_time, "ip_address": ip_address})
    else:
        print("Email already in database.")
    
    song_data = {
        "title": title,
        "albumart": img_url,
        "audio": audio_url,
        "json": json_url,
        "author": singer_name,
        "qr": qr_url,
    }

    collection.update_one({"email": cc_email}, {"$push": {"songs": {"$each": [song_data], "$position": 0}}})


    print(f"******** Card Upload Complete! ********\n Go to:\n\n {qr_url} \n\nFor the audio, and \n\nhttps://console.cloud.google.com/storage/browser/ringledingle/cards for the full URL.\n ********Have a Ringly Dingly Day!********")

voice_library = {
        "alan-rickman":"Snape",
        "snoop-dogg":"Snoop Dogg",
        "frenchy":"French Narrator",
        "bugs-bunny-billy-west":"Bugs Bunny",
        "betty-white":"Betty White",
        "eminem-arpa2":"Eminem",
        "shrek":"Shrek",
        "johnny-cash":"Johnny Cash",
        "rizzo-the-rat":"Rizzo the Rat",
        "spongebob-vocodes":"Spongebob",
        "ariel":"Ariel",
        "biggie-smalls":"Notorious B.I.G.",
        "pooh-brock-baker":"Pooh"
    }
tracks = {
    "lullaby": "apps/static/media/lullaby.mp3",
    "magic": "apps/static/media/magic.mp3",
    "motiv": "apps/static/media/motiv.mp3",
    "pensive": "apps/static/media/pensive.mp3",
    "sad": "apps/static/media/sad.mp3"
}


words = "It's mother's day, please describe how wonderful my mom is. her name is Sue. She's raised me for 23 years. She's a nurse. She's a great cook. She's a great mom."
voice = "betty-white"
singer_name = voice_library[voice]
track = tracks["motiv"]

# RUN THE DINGLE FUNCTION
ringledingle(
    words, voice,singer_name,track
    )



# # # IN CASE DALLE FAILS:
# dalle_request = "A cartoon of a mother and daughter hugging"
# title = "Image dump"
# img_url = generate_image("A funny cartoon of "+dalle_request, size=3)
# urllib.request.urlretrieve(img_url, f'apps/static/media/dalle/image.png')
# date = dt.now().strftime("%y%m%d")
# upload_file(f'apps/static/media/dalle/image.png', f'cards/{date}/{title}')


