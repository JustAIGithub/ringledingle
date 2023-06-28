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


def ai_response(prompt, temperature =.5):
    # OPEN AI CONFIG
    temperature = temperature
  
    # PREPRIME WITH MESSAGES
    # messages = get_conversation(5, 'db','user_responses')

    messages = [{"role": "user", "content": prompt}]
    # NOW RUN THE PROMPT:
    response = openai.ChatCompletion.create( 
    model="gpt-3.5-turbo",
    messages=messages,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=temperature,
        frequency_penalty=1
    )

    message = response["choices"][0]["message"]["content"]
    print(f"Prompt:{prompt}")
    print("AI Response:", message)
    return message.strip()

def ai_response_stream(prompt, temperature=.5):
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
        frequency_penalty=1,
        stream=True
        
    )

    # message = response["choices"][0]["message"]["content"]

    for thing in response:
        if thing["choices"][0]["finish_reason"] == "stop":
            return response

        else:
            try:
                message = thing["choices"][0]["delta"]['content']
                yield f"{message}"
            except:
                print("Error in response, for message ", thing)
    return response


# import time

# def print_word_by_word(text, delay=0.02):
#     words = text.split()
#     for word in words:
#         print(word, end=" ", flush=True)
#         time.sleep(delay)

# prompt = "give me a prompt for an animation in dalle"
# stream = ai_response_stream(prompt)

# for response in stream:
#     print(response.strip(), end=" ", flush=True)
#     final_response = response
# print("FINAL RESPONSE:", stream)




    # print(response, end="")

def generate_image(prompt, size=1):
    
    sizes = {
        1: "256x256",
        2: "512x512",
        3: "1024x1024"
    }
    prompt = prompt
    response = openai.Image.create(
    prompt=prompt,
    n=1,

    size=sizes[size],
    )
    print("Dalle url response:",response['data'][0]['url'])
    return response['data'][0]['url']

# print(generate_image('An illustration of a group of people laughing together in a park or outdoor setting, digital art',3))