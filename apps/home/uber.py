import requests
import json
# import os, uberduck
import requests
from pydub import AudioSegment
from io import BytesIO
import os


DUCK_KEY = os.getenv('DUCK_KEY')
DUCK_SECRET = os.getenv('DUCK_SECRET')
if DUCK_KEY is None:
    try:
        from apps.home.creds import DUCK_KEY, DUCK_SECRET
    except:
        try:
            from creds import DUCK_KEY, DUCK_SECRET
        except:
            print("No creds file")

# WORKING WITH THE UBER DUCK API

url = "https://api.uberduck.ai/reference-audio"


# Replace these with your own values from your creds.py file
api_key = DUCK_KEY
api_secret = DUCK_SECRET


auth=(DUCK_KEY, DUCK_SECRET)



def get_reference_audio(uuid, auth=auth):
    url = f'https://api.uberduck.ai/reference-audio/search?uuid={uuid}'
    response = requests.get(url, auth=auth)
    return response.content

def get_voices(auth=auth):
    url = "https://api.uberduck.ai/voices?mode=tts-all&language=english"
    response = requests.get(url, auth=auth)
    return response.json()

def get_voice_id(voice, auth=auth):
    url = f'https://api.uberduck.ai/voice-data?name={voice}&architecture=tacotron2'
    headers = {
    "accept": "application/json",
    }
    # url = f"https://api.uberduck.ai/voices?mode=tts-all&language=english"
    response = requests.get(url, auth=auth, headers=headers)
    # NEED TO FIND THE RESPONSE THAT HAS THE VOICE NAME
    # voice_object = [x for x in response.json() if x['name'] == voice][0]

    return response.text

# print(get_voice_id('eminem'))
import pydub
def uberduck_audio_segment(speech, voice, auth=auth):
    # auth = (os.getenv('DUCK_KEY'), os.getenv('DUCK_SECRET'))
    # print("AUTH:",auth)

    url = "https://api.uberduck.ai/speak-synchronous"
    headers = {
        "accept": "application/json",
        "authorization": "Basic cHViX3lwdWxvZmtkeGZjYm9lcG5jaTpwa182MDk4NTJjNi02YTQxLTQ3NzYtYjRmYi0zZjljNjRkZDViOWE="
    }
    payload = {
        "speech": speech,
        "voice": voice,
        "model_type":"tacotron2"
        # "pace":12,
        # "duration": [duration]
    }
    response = requests.post(url, json=payload, auth=auth,headers=headers)

    if response.status_code == 200:
        try:
            audio_segment = AudioSegment.from_file(BytesIO(response.content), format="wav")
            return audio_segment
        except pydub.exceptions.CouldntDecodeError:
            print("Could not decode the response content as WAV. Dumping content to file for analysis.")
            with open('response_content.txt', 'wb') as f:
                f.write(response.content)
            return None
    else:
        print(f"Request failed with status code {response.status_code}, message {response.text}.")
        return None

# print(get_voices())


# audio = speak("""I'm feeling way too sentimental,
# Things that used to be so simple,
# Now they're causing me to tremble,
# Growing up is such a mental,
# I wish I could go back to the days,
# When life was just a game we played,
# But now it's real and all the stakes raised,
# Don't know if I'll be able to keep pace.""", 'eminem')
# audio.export("output.wav", format="wav")




# audio_segment = AudioSegment.from_file(BytesIO(reference_audio), format="wav")


# print(get_reference_audio(uuid))
# LIST ALL VOICES
# url = "https://api.uberduck.ai/voices?mode=tts-all&language=english"
# params = {
#     "mode": "tts-",
# }

# headers = {
#     "accept": "application/json",
#     "content-type": "application/json"
# }
# import requests
# import json
# response = requests.get(url, auth=(api_key, api_secret), headers=headers)
# print([voice['name'] for voice in response.json()])
# # save the list in voice-names.txt
# with open('voice-names.txt', 'w') as f:
#     f.write(json.dumps([voice['name'] for voice in response.json()]))

# url = "https://api.uberduck.ai/speak"


# # client = uberduck.UberDuck(os.getenv("DUCK_KEY"), os.getenv("DUCK_SECRET"))


# client = uberduck.UberDuck(DUCK_KEY,DUCK_SECRET)


# voices = uberduck.get_voices(return_only_names = True)

# speech = input('Enter speech: ')
# voice = input('Enter voice or enter "LIST" to see list of voices: ')

# if voice == 'LIST':
#     print('Available voices:\n')
#     for voice in sorted(voices): # sorting the voice list in alphabetical order
#         print(voice)
#     exit()

# # if voice not in voices:
# #     print('Invalid voice')
# #     exit()

# # client.speak(speech, voice, file_path='apps/static/media/voice.mp3', return_bytes=True, play_sound = False)
# # print('Spoke voice')


# # uuid = 'b859b193-eb68-4ec4-907b-ffdff2728357'
# # url = f'https://api.uberduck.ai/reference-audio/search?uuid={uuid}'
# response = requests.get(url, auth=(api_key, api_secret), headers=headers)
# # print(response.text)

# def uberduck_audio_segment(speech, voice, durclient=client):
#     audio_bytes = client.speak(speech, voice, return_bytes=True, check_every=1, play_sound=False)

#     # Convert audio bytes to AudioSegment object
#     AudioSegment.converter = "ffmpeg.exe"
#     audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")

#     return audio_segment

# # Example usage
# voice = 'alan-rickman'  # Replace with a voice from the list of available voices
# voice = 'loser-boy-upbeat'
# speech = 'Hello, world!'
# audio_segment = uberduck_audio_segment(speech, voice, 0)
# print(audio_segment)
# audio_segment = speak(speech, voice)

# print(audio_segment)