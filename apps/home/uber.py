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
    url = f"https://api.uberduck.ai/voices?mode=tts-all&language=english"
    response = requests.get(url, auth=auth)
    # NEED TO FIND THE RESPONSE THAT HAS THE VOICE NAME
    voice_object = [x for x in response.json() if x['name'] == voice][0]

    return voice_object

# # # print(get_voice('spongebob'))
# print([voice['name'] for voice in get_voices()])
# # put all voice names in C:\Users\appii\Google Drive\Projects\music-player\voice-names.txt:
# with open('voice-names.txt', 'w') as f:
#     for voice in get_voices():
#         f.write(voice['name'] + "\n")



def uberduck_audio_segment(speech, voice, duration):
    auth = (os.getenv('DUCK_KEY'), os.getenv('DUCK_SECRET'))
    # print("AUTH:",auth)

    url = "https://api.uberduck.ai/speak-synchronous"
    payload = {
        "speech": speech,
        "voice": voice,
        "model_type":"tacotron2"
        # "pace":12,
        # "duration": [duration]
    }
    response = requests.post(url, json=payload, auth=auth)
    # AudioSegment.converter = "ffmpeg.exe"
    audio_segment = AudioSegment.from_file(BytesIO(response.content), format="wav")
    return audio_segment

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
# # LIST ALL VOICES
# url = "https://api.uberduck.ai/voices?mode=tts-all&language=english"
# # params = {
# #     "mode": "tts-",
# # }

# headers = {
#     "accept": "application/json",
#     "content-type": "application/json"
# }

# url = "https://api.uberduck.ai/speak"


# # client = uberduck.UberDuck(os.getenv("DUCK_KEY"), os.getenv("DUCK_SECRET"))


# # client = uberduck.UberDuck(DUCK_KEY,DUCK_SECRET)


# # voices = uberduck.get_voices(return_only_names = True)

# # speech = input('Enter speech: ')
# # voice = input('Enter voice or enter "LIST" to see list of voices: ')

# # if voice == 'LIST':
# #     print('Available voices:\n')
# #     for voice in sorted(voices): # sorting the voice list in alphabetical order
# #         print(voice)
# #     exit()

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

# Example usage
# voice = 'spongebob'  # Replace with a voice from the list of available voices
# speech = 'Hello, world!'
# # audio_segment = uberduck_audio_segment(speech, voice)
# audio_segment = speak(speech, voice)

# print(audio_segment)