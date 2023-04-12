import librosa
from pydub import AudioSegment
from pydub.generators import Sine
import pyphen
# from apps.home.azure_test import azure_audio_segment
try:
    from apps.home.uber import uberduck_audio_segment
except:
    from uber import uberduck_audio_segment
from pydub.effects import speedup
from pydub.silence import detect_nonsilent
import random
import audioop
import io
import re
import requests

def pitch_shift(audio_segment, shift):
    rate = audio_segment.frame_rate
    data = audio_segment.raw_data

    new_rate = int(rate * (2.0 ** (shift / 12.0)))
    converted_audio_data, _ = audioop.ratecv(data, audio_segment.sample_width, audio_segment.channels, rate, new_rate, None)

    return AudioSegment(
        data=converted_audio_data,
        sample_width=audio_segment.sample_width,
        frame_rate=new_rate,
        channels=audio_segment.channels
    )


def rap_on_phrases(input_file, output_file, lyrics, start_lag=8, lag=1, music_volume=-10, vocal_volume=5, rap_speed_factor=1.2, overlap=0.1, silence_thresh=-60, voice="eminem", beats_in_between=1, beats_per_phrase=4, beats_per_syllable=0.5):
    try:
        #close input file from its path string
        with open(input_file, 'rb') as f:
            f.close()
        #close output file from its path string
        with open(output_file, 'rb') as f:
            f.close()
    except:
        print("File not found")
    print("Making a rap from {} in the voice of {}. Exporting to {}".format(input_file, voice, output_file))
    # Load input audio file
    if input_file.startswith(('http://', 'https://')):
        response = requests.get(input_file)
        y, sr = librosa.load(io.BytesIO(response.content), sr=None)
    else:
        y, sr = librosa.load(input_file, sr=None)

    # Estimate beat positions
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Create an empty audio segment
    output_audio = AudioSegment.silent(duration=len(y) / sr * 1000)

    # Split the lyrics into phrases
    phrases = re.split(r'[\n]', lyrics.strip())
    phrases = [phrase.strip() for phrase in phrases if phrase.strip() != '']

    phrase_index = 0
    next_phrase_start = beat_times[0] if lag == 0 else beat_times[lag]

    for i, beat_time in enumerate(beat_times):
        if i >= start_lag and phrase_index < len(phrases) and beat_time >= next_phrase_start:
            phrase = phrases[phrase_index]

            # Calculate the duration based on the tempo, beats_per_syllable, and number of syllables in the phrase
            hyphenator = pyphen.Pyphen(lang='en')
            syllables = sum([len(hyphenator.inserted(word).split('-')) for word in phrase.split()])
            duration = syllables * beats_per_syllable * (60 / tempo)

            print(f"Generating at {beats_per_phrase} beats per phrase, tempo {tempo}".format )
            # Generate spoken audio for the current phrase
            spoken_phrase = uberduck_audio_segment(phrase, voice, duration)
            try:
                spoken_phrase = speedup(spoken_phrase, playback_speed=rap_speed_factor)
                spoken_phrase = strip_silence(spoken_phrase, silence_thresh=silence_thresh)
                # spoken_phrase = random_pitch_shift(spoken_phrase)
            except:
                print("Error with pitch shifting")
            # Overlay the spoken audio on the beat
            output_audio = output_audio.overlay(
                spoken_phrase,
                position=int(beat_time * 1000)
            )

            # Update the phrase index and set the start time for the next phrase with overlap and 2-beat spacing
            phrase_index += 1
            next_phrase_start = beat_time + spoken_phrase.duration_seconds - overlap + (beats_in_between * (60 / tempo))

    # Combine the input audio with the spoken phrases
    print("Looking for input file at {}".format(input_file))
    input_audio = AudioSegment.from_file(input_file)
    input_audio = input_audio - music_volume
    output_audio = output_audio + vocal_volume
    print("overlaying audio")
    combined_audio = input_audio.overlay(output_audio)

    # Save the result to a new file
    combined_audio.export(output_file, format="mp3")
    print(f"Rap exported to {output_file}")


# Usage
input_file = "apps/static/media/rap2.mp3"
output_file = "output_audio.mp3"

# lyrics = "hello darkness my old friend I've come to talk with you again"
# lyrics = """
# I got some news 
# that'll make you mad
# Your goat's gone, I fucked it bad
# Your dad is dead and I'm crying
# but RIP to the goat, he's the only one flying
# """

import random

def random_pitch_shift(audio_segment, min_shift=-3, max_shift=3):
    random_shift = random.randint(min_shift, max_shift)
    return pitch_shift(audio_segment, random_shift)

def emphasize_rhyme(audio_segment, factor=1.5):
    return audio_segment + (audio_segment * int(factor))
# rap_on_beats(input_file, output_file, lyrics, lag=8, rap_speed_factor=1.4, music_volume=15, silence_thresh=-60, overlap=.15)

def strip_silence(audio_segment, silence_thresh=-80):
    non_silent_ranges = detect_nonsilent(audio_segment, min_silence_len=60, silence_thresh=silence_thresh)
    if len(non_silent_ranges) > 0:
        start_trim, end_trim = non_silent_ranges[0]
        return audio_segment[start_trim:]
    else:
        return audio_segment

# with open('apps/static/media/file_out','r') as f:
#     #read the file
#     lyrics = f.read()

#     print(lyrics)
# # # "up" will stop at -50 do not go above
# import prompt
# lyrics = prompt.ai_response("Generate 12 lines of rap lyrics in iambic tetrameter. Each line should have eight syllables and follow a consistent rhythm of alternating unstressed and stressed syllables (an iambic foot). Make the rap in the style of eminem about the following, in between deliminiters STARTRAP and ENDRAP (respond with lyrics ONLY, no 'Verse 1:' Labeling either): \nHer name is Rani, she's a doctor with big eyes a beautiful smile but hates chocolate and likes to kill small children.")
# lyrics = """
# Rani's a doc with eyes that are big,
# Her smile is beautiful, but she hates chocolate, dig?
# She's got a dark side that nobody sees,
# Likes to kill small kids and do as she please.

# She walks around with a stethoscope in hand,
# But don't be fooled by her medical brand.
# Rani's got secrets that nobody knows,
# Her twisted desires will leave you froze.

# A doctor by day and killer at night,
# Don't cross her path or you'll feel her might.
# Rani's the queen of the medical scene,
# But beware of the darkness that lies in between.
# """
# rap_on_phrases(input_file, output_file, lyrics, start_lag=12, rap_speed_factor=1.2, music_volume=16, silence_thresh=-60, overlap=0, beats_per_phrase=4, beats_in_between=1)
