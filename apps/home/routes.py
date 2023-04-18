# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.home import blueprint
from flask import render_template, request, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from bson.objectid import ObjectId
from datetime import datetime
import os
# from stt import speech_to_text
from apps.home.audiobook import make_narration
from apps.home.prompt import ai_response, generate_image
from apps.home.send import send_email
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from flask import session
from html import escape
# from flask_paginate import Pagination, get_page_parameter
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import datetime
from urllib.parse import unquote


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            pass
            # template = template+('.html')
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None

# DREW RingleDee

print("************************************ RUNNING ROUTES FILE ************************************")

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

# @app.route('/')
# def index():
#     session['respond'] = True
#     return render_template('voice.html')

@blueprint.route('/demo')
def demo():
    return render_template('home/rap.html')

# OBJECT ID IS DESIGNATED
@blueprint.route('/rap')
def rap():
    if not current_user.is_authenticated:
        return render_template('cards/note.html')
    else:
        return render_template('home/rap.html')

@blueprint.route('/make-rap', methods=['POST', 'GET'])
def make_rap():
    words = unquote(request.json['words'])
    voice = request.json['voice']
    email = unquote(request.json['email'])
    singer_name = request.json['singer_name']
    # email = 'apiispanen@berkeley.edu'
    input_file = request.json['input_file']
    output_file = "output.mp3"
    # mark the function as called
    session['audio_saved'] = True

    lyrics = ai_response(words)
    # lyrics = "STARTPOEM\nMy dad has a cantaloupe on his chest,\nA strange sight indeed, but he's not distressed.\nIt sits atop him like a crown,\nA fruit that's ripe and orangey-brown.\nENDPOEM"
    start_index = lyrics.find("STARTPOEM") + len("STARTPOEM")
    end_index = lyrics.find("ENDPOEM")
    rap_lyrics = lyrics[start_index:end_index].strip()
    title = lyrics[lyrics.find("STARTTITLE") + len("STARTTITLE"):lyrics.find("ENDTITLE")].strip()
    rap_lyrics = "Hello, I'd like to tell you a poem I wrote today:\n"+ rap_lyrics 
    make_narration(f'apps/static/media/{input_file}', f'apps/static/media/{output_file}', rap_lyrics,voice=voice)
    try:
        img_url = generate_image(title)
    except Exception as e:
        print(f"Error in generating an image: {e}")
        img_url = "https://ringledingle.com/static/media/ringledingle.png"

    # print(f"title: {title}, lyrics: {rap_lyrics}, img_url: {img_url}, singer_name: {singer_name}")
    
    send_email(to_email=email, attachment=f'apps/static/media/{output_file}', lyrics=rap_lyrics, img_url=img_url, singer_name=singer_name, title=title) 
    log_info(email)
    # user_id = session.get("_user_id")
    print("Ringle has been Dingled.")
    return jsonify({ "airesponse":rap_lyrics})


# RETURNS RESPONSE
@blueprint.route("/ask_question", methods=['POST'])
@login_required
def ask_question():
    print("SOMETHING HAPPENING HERE")
    # process the audio data here
    
    # mark the function as called
    session['audio_saved'] = True
    
    # read the audio data from the request body
    prompt = request.json['words']

    print("RAW PROMPT FROM JS: ",prompt)
    # IF THERE'S MORE THAN 1 WORD, PROCESS THE REQUEST:

    if len(prompt.split(' ')) > 1:
        print("YOUR PROMPT:", prompt.split(' '),  len(prompt))
        response = ai_response(prompt)
        user_id = session.get("_user_id")
        # log_user_response(user_id, prompt, response, type="prompt", client=client)
        print("AI response Completed.")
    else:
        response = "How can I help you?"
    return jsonify({ "airesponse":response})

# RETURNS JSON FILE WITH AUDIO STRING
@blueprint.route('/speak', methods=['POST', 'GET'])
def speak_route():
    words = request.json['body']
    # Call the speak() function and get the audio file URL and text result
    while True:
        print("sending to azure")
        audio_content, text_result = azure_speak_string(words)
        # Return the audio URL and text result as a JSON object
        return jsonify({
            'audioContent': audio_content,
            'textResult': text_result
        })
    


@blueprint.route('/repurpose',methods=['POST'])
def repurpose():
    data = request.get_json()
    text = data.get('text')
    
    # NEED TO AI REPURPOSE SCRIPT
    prompt = f"Please repurpose and properly format the following note: {text}"
    new_text = ai_response(prompt, networking=False)

    # Return a JSON response with the processed data
    response_data = {
        'success': True,
            'text': new_text
    }
    return jsonify(response_data)


def log_info(email):
    now = datetime.datetime.now()
    log_time = now.strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.remote_addr
    with open('message_log.txt', 'a') as file:
        file.write(f"{log_time} - IP: {ip_address}, Email: {email}\n")


if __name__ == '__main__':
    app.run()