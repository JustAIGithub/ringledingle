# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.home import blueprint
from flask import render_template, request, session, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
from bson.objectid import ObjectId
from datetime import datetime
import os
# from stt import speech_to_text
from apps.home.audiobook import make_narration
from apps.home.prompt import ai_response, generate_image, ai_response_stream
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
from apps.home.store_music import log_info, upload_file, store_song, get_json_for_user
import requests


@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/music')
def music():
    # get parameter email from url
    user_email = request.args.get('email')
    print("USER EMAIL: ", user_email)
    return render_template('home/music.html', segment='music', user_email=user_email)

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
    return render_template('home/page-500.html')


@blueprint.route('/generate-lyrics', methods=['POST', 'GET'])
def generate_lyrics():
    words = unquote(request.json['words'])
    singer_name = request.json['singer_name']
    email = unquote(request.json['email'])
    
    print("MAKING POEM", words, singer_name)
    lyrics = ai_response(words)
    if "verse" in lyrics.lower():
        lyrics = ai_response(words)
    # lyrics = """STARTTITLE Sound of Silence ENDTITLE \n STARTPOEMHello darkness, my old friend,\n I've come to talk with you again,\n Because a vision softly creeping,\n Left its seeds while I was sleeping.ENDPOEM"""
    poem_lyrics = lyrics[lyrics.find("STARTPOEM") + len("STARTPOEM"):lyrics.find("ENDPOEM")].strip()
    # dalle_request = lyrics[lyrics.find("STARTDALLE") + len("STARTDALLE:"):lyrics.find("ENDDALLE")].strip()
    # print("DALLE REQUEST: ", dalle_request)
    if log_info(email):
        # If new user, send them email:
        # send_email(email, poem_lyrics, singer_name)
        pass
    

    title = lyrics[lyrics.find("STARTTITLE") + len("STARTTITLE:"):lyrics.find("ENDTITLE")].strip()
    return jsonify({  "lyrics":poem_lyrics, "title":title, "singer_name":singer_name})

@blueprint.route('/generate-dingle', methods=['POST', 'GET'])
def generate_dingle():
    words = unquote(request.json['words'])
    voice = request.json['voice']
    title = unquote(request.json['title'])
    email = unquote(request.json['email']).lower()
    singer_name = request.json['singer_name']
    # dalle_request = request.json['dalle_request']
    dalle_request = ai_response(f"Describe in one sentence what a cover photo would be for the poem (i.e. the string will get processed in DALLE for AI image rendering), and put that prompt string in between the delimiters STARTDALLE and ENDDALLE.\n{words}")
    dalle_request = dalle_request[dalle_request.find("STARTDALLE") + len("STARTDALLE:"):dalle_request.find("ENDDALLE")].strip()
    dalle_request = "A funny cartoon of "+dalle_request

    print(f'Dalle request: {dalle_request}')
    input_file = request.json['input_file']
    output_file = "output.mp3"
    # mark the function as called
    session['audio_saved'] = True
    output_path = f'apps/static/temp/{output_file}'
    img_path = f'apps/static/temp/img.png'

    json_lyrics = make_narration(f'apps/static/media/{input_file}', output_path, words,voice=voice)
    # lrc_lyrics =''
    try:
        img_url = generate_image("A funny cartoon of "+dalle_request)
    except Exception as e:
        print(f"Error in generating an image: {e}")
        img_url = "https://ringledingle.com/static/media/ringledingle_na.png"

    # save the img locally to static/temp/img.png:
    with open(img_path, 'wb') as f:
        f.write(requests.get(img_url).content)


    # print(f"title: {title}, lyrics: {rap_lyrics}, img_url: {img_url}, singer_name: {singer_name}")
    
    # save email to a flask session
    session['email'] = email
    store_song(user_email=email, title=title, json_lyrics=json_lyrics, imgsrc=img_path, audiopath=output_path, singer_name=singer_name)
    
    # send_email(to_email=email, attachment=f'apps/static/media/{output_file}', lyrics=words, img_url=img_url, singer_name=singer_name, title=title) 
    # print("Ringle has been Dingled. img_url: ", img_url, "title: ", title)
    # Pass the image url and title to the front end
    return jsonify({  "img_url":img_url, "airesponse":words, "title":title, "json_lyrics":json_lyrics})


import json
@blueprint.route('/get-json', methods=['POST', 'GET'])
def get_json():
    print("GETTING JSON")
    email = session['email']
    # print("ROUTEs.py GETTING JSON FOR USER: ", email)

    # Get the Python dictionary for the user
    
    playlist_dict = get_json_for_user(user_email=email)


    # Replace single quotes with double quotes
    # playlist_dict_fixed = playlist_dict.replace("'", '"')

    # Your current print statements
    print("PLAYLIST_DICT: ", playlist_dict)
    print("PLAYLIST_DICT TYPE", type(playlist_dict))

    # Convert the fixed string to a dictionary
    playlist_dict_obj = json.loads(playlist_dict)

    # Convert the dictionary back to a JSON string
    playlist_json = json.dumps(playlist_dict_obj)

    # Print the JSON string
    print("PLAYLIST_JSON: ", playlist_json)
    print("PLAYLIST_JSON TYPE: ", type(playlist_json))

    return jsonify(playlist_json)


@blueprint.route('/email-share', methods=['POST', 'GET'])
def email_share():
    print("REQUEST",request.json)
    lyrics = unquote(request.json['lyrics'])
    singer_name = request.json['singer_name']
    title = unquote(request.json['title'])
    email = unquote(request.json['email'])
    cc_email = unquote(request.json['cc_email'])

    img_url = request.json['img_url']
    output_file = "output.mp3"
    send_email(to_email=email, attachment=f'apps/static/temp/{output_file}', lyrics=lyrics, img_url=img_url, singer_name=singer_name, title=title) 
    return jsonify({  "success":True})



if __name__ == '__main__':
    app.run()