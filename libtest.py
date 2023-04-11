import azure.cognitiveservices.speech as speechsdk
import librosa
from pydub import AudioSegment
from azure import azure_speak_string
import io
import base64
import soundfile as sf
import numpy as np


# Azure Cognitive Services Speech API credentials
SPEECH_KEY = '05fb95209bb34b20abb4cfa5287a3a85'
SPEECH_REGION = 'eastus'

# Path to the audio file of the song
song_path = 'christmas.mp3'

# Load the audio file of the song and extract its pitch
song, sr = librosa.load(song_path)
# song = AudioSegment.from_file(song_path)
pitch = librosa.piptrack(y=song, sr=sr)[0]
mean_song_pitch = pitch.mean()

# Generate the speech output using the Azure Text-to-Speech API

speech_text = "We wish you a merry christmas!"
audio_data_base64 = azure_speak_string(speech_text)
audio_data = base64.b64decode(audio_data_base64)

# Calculate the mean pitch of the speech output
audio_stream = io.BytesIO(audio_data)
speech_audio, sr = librosa.load(audio_stream)
pitch = librosa.piptrack(y=speech_audio, sr=sr)[0]
mean_speech_pitch = pitch.mean()

# Calculate the pitch scaling factor
pitch_scaling_factor = mean_song_pitch / mean_speech_pitch

# Adjust the tempo (speed) of the speech
tempo_scaling_factor = 1.0  # Change this value to adjust the tempo; 1.0 means no change, <1.0 is slower, and >1.0 is faster
speech_audio_time_stretched = librosa.effects.time_stretch(speech_audio, rate=tempo_scaling_factor)

# Adjust the vocal tone (harmonic content) of the speech
speech_audio_harmonic = librosa.effects.harmonic(speech_audio_time_stretched, margin=2.0)  # Change the margin value to adjust the harmonic content; higher values lead to more prominent harmonics



# Convert the speech output to an AudioSegment and adjust its pitch
speech_audio = AudioSegment.from_file(io.BytesIO(audio_data), format='wav')
speech_audio_data = speech_audio.export(format='wav')
speech_audio_data_io = io.BytesIO(speech_audio_data.read())
speech_audio, sr = librosa.load(speech_audio_data_io)
speech_audio_pitch_shifted = librosa.effects.pitch_shift(speech_audio_harmonic, sr=sr, n_steps=pitch_scaling_factor, bins_per_octave=12)

# speech_audio_pitch_shifted = librosa.effects.pitch_shift(speech_audio, sr=sr, n_steps=pitch_scaling_factor, bins_per_octave=12)

# Convert the pitch shifted audio to an AudioSegment
speech_audio_pitch_shifted_bytes = io.BytesIO()
sf.write(speech_audio_pitch_shifted_bytes, speech_audio_pitch_shifted, sr, format='wav')
speech_audio_pitch_shifted_bytes.seek(0)
speech_audio_pitch_shifted = AudioSegment.from_file(speech_audio_pitch_shifted_bytes)

# # Overlay the adjusted speech output on top of the song and export the result
# result_audio = AudioSegment.from_file(song_path)  # Load the song as an AudioSegment
# result_audio = result_audio.overlay(speech_audio_pitch_shifted)
# result_audio.export('temp/result.wav', format='wav')


def detect_beats(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times

def split_speech_to_words(speech_text, speech_audio):
    words = speech_text.split()
    word_boundaries = [i for i, c in enumerate(speech_text) if c == ' ']
    word_timings = [len(speech_audio) * (boundary / len(speech_text)) for boundary in word_boundaries]
    word_timings = [0] + word_timings + [len(speech_audio)]
    
    word_audios = []
    for i in range(len(words)):
        start = int(word_timings[i])
        end = int(word_timings[i + 1])
        word_audio = speech_audio[start:end]
        word_audios.append(word_audio)
    
    return word_audios


import tempfile

def overlay_words_on_beats(song_audio, speech_text, speech_audio):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as song_temp_file, \
         tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as speech_temp_file:

        song_audio.export(song_temp_file.name, format="wav")
        speech_audio.export(speech_temp_file.name, format="wav")

        words = split_speech_to_words(speech_text, speech_audio)
        beats = detect_beats(song_temp_file.name)

        if len(beats) < len(words):
            print("Warning: There are more words than detected beats.")

        overlay_audio = AudioSegment.silent(duration=len(song_audio))
        for i, word_audio in enumerate(words):
            if i >= len(beats):
                break
            overlay_audio = overlay_audio.overlay(word_audio, position=int(beats[i] * 1000))

        return song_audio.overlay(overlay_audio)

speech_audio_pitch_shifted_bytes.seek(0)
speech_audio_pitch_shifted = AudioSegment.from_file(speech_audio_pitch_shifted_bytes)

song_audio = AudioSegment.from_file(song_path)
result_audio = overlay_words_on_beats(song_audio, speech_text, speech_audio_pitch_shifted)
result_audio.export('temp/result.wav', format='wav')
