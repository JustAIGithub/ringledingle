import os
from pydub import AudioSegment
from google.cloud import texttospeech_v1 as texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google.json"

def synthesize_speech(text, output_file):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

def mix_audio(instrumental_file, speech_file, output_file):
    instrumental = AudioSegment.from_file(instrumental_file, format="mp3")
    speech = AudioSegment.from_file(speech_file, format="mp3")
    mixed = instrumental.overlay(speech)
    mixed.export(output_file, format="mp3")

if __name__ == "__main__":
    lyrics = "My lyrics are nah nah because my dad wants my papa"
    speech_output = "speech_output.mp3"
    synthesize_speech(lyrics, speech_output)

    instrumental_file = "path/to/instrumental.mp3"
    output_file = "output_song_with_custom_lyrics.mp3"
    mix_audio(instrumental_file, speech_output, output_file)
