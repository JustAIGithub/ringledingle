
UD_API_KEY = 'pub_wxradcofrfdsulnxzu'
UD_API_SECRET = 'pk_b4293e8d-e41a-4798-a219-50f7c138a727'
import requests
import time

def speak(text, voice='zwf'):
    # make the API request to generate speech
    response = requests.post('https://api.uberduck.ai/speak',
                            auth=(UD_API_KEY, UD_API_SECRET),
                            json={'speech': text, 'voice': voice})
    uuid = response.json()['uuid']

    # poll the API request to get the status and path to the generated speech file
    while True:
        response = requests.get(f'https://api.uberduck.ai/speak-status?uuid={uuid}',
                                auth=(UD_API_KEY, UD_API_SECRET))
        data = response.json()
        if data['finished_at']:
            print(f"Speech file generated at {data['path']}")
            break
        time.sleep(1)


url = "https://api.uberduck.ai/reference-audio/search?hits_per_page=100&query=h"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers, auth=(UD_API_KEY, UD_API_SECRET))

print(response.text)


# speak('hello world')

