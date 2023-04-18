import requests
import os
import sseclient
import json

API_KEY = os.getenv('API_KEY')


from flask import session
import openai
if API_KEY is None:
    try:
        from apps.home.user import person, google_it
        # from apps.home.database import get_conversation
        from apps.home.creds import *
    except:
        try:
            from creds import *
        except:        
            print("No API Key Found anywhere. Tough luck I guess?")
openai.api_key = API_KEY


def ai_response(prompt, networking = False, temperature =.5):
    import string
    # OPEN AI CONFIG
    temperature = temperature
  
    # PREPRIME WITH MESSAGES
    # messages = get_conversation(5, 'db','user_responses')
    messages = [{"role": "user", "content": prompt}]
    # NOW RUN THE PROMPT:
    response = openai.ChatCompletion.create( 
    model="gpt-3.5-turbo-0301",
    messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=temperature,
        frequency_penalty=1
    )

    message = response["choices"][0]["message"]["content"]
    print(f"Prompt:{prompt}")
    print("AI Response:", message)
    return message.strip()


def generate_image(prompt):
    prompt = "a Cartoon of "+prompt
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256"
    )
    print(response['data'][0]['url'])
    return response['data'][0]['url']

# print(generate_image('a happy dad with a hat'))