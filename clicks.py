import numpy as np
import librosa
from pydub import AudioSegment
from pydub.generators import Sine
import pyphen
from azure import azure_audio_segment
from pydub.effects import speedup
from pydub.silence import detect_nonsilent
import random
import audioop
from io import BytesIO
import re

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




def rap_on_phrases(input_file, output_file, lyrics, lag=0, music_volume=-10, vocal_volume=5, rap_speed_factor=1.0, click_volume=10, overlap=0.1, silence_thresh=-60):
    # Load input audio file
    y, sr = librosa.load(input_file, sr=None)

    # Estimate beat positions
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Create an empty audio segment
    output_audio = AudioSegment.silent(duration=len(y) / sr * 1000)

    # Split the lyrics into phrases
    phrases = re.split(r'[\n,]', lyrics.strip())
    phrases = [phrase.strip() for phrase in phrases if phrase.strip() != '']

    phrase_index = 0
    next_phrase_start = beat_times[0] if lag == 0 else beat_times[lag]

    for i, beat_time in enumerate(beat_times):
        if i >= lag and phrase_index < len(phrases) and beat_time >= next_phrase_start:
            phrase = phrases[phrase_index]

            # Generate spoken audio for the current phrase
            spoken_phrase = azure_audio_segment(phrase)
            spoken_phrase = speedup(spoken_phrase, playback_speed=rap_speed_factor)
            spoken_phrase = strip_silence(spoken_phrase, silence_thresh=silence_thresh)

            # Overlay the spoken audio on the beat
            output_audio = output_audio.overlay(
                spoken_phrase,
                position=int(beat_time * 1000)
            )

            # Update the phrase index and set the start time for the next phrase with overlap
            phrase_index += 1
            next_phrase_start = beat_time + spoken_phrase.duration_seconds - overlap

    # Combine the input audio with the spoken phrases
    input_audio = AudioSegment.from_file(input_file)
    input_audio = input_audio - music_volume
    output_audio = output_audio + vocal_volume
    combined_audio = input_audio.overlay(output_audio)

    # Save the result to a new file
    combined_audio.export(output_file, format="mp3")

def rap_on_beats(input_file, output_file, lyrics, lag=0, music_volume=-10, vocal_volume=5, rap_speed_factor=1.0, click_volume=10, overlap=0.1, silence_thresh=-60):
    # Load input audio file
    y, sr = librosa.load(input_file, sr=None)

    # Estimate beat positions
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Create an empty audio segment
    output_audio = AudioSegment.silent(duration=len(y) / sr * 1000)

    # Split the lyrics into lines
    lines = lyrics.strip().split('\n')
    # Split the lyrics into phrases
    phrases = lyrics.strip().split('\n\n')
    words = []
    for phrase in phrases:
        # Split each phrase into lines
        lines = phrase.strip().split('\n')
        for line in lines:
            # Split each line into words
            words_in_line = line.strip().split()
            # Add each word and a pause in between
            for i, word in enumerate(words_in_line):
                words.append(word)
                if i < len(words_in_line) - 1:
                    words.append(' ')
            # Add a rest at the end of each line to fill up the remaining beats
            words.append(' ')
            words.append(' ')

    words_with_pauses = []
    for word in words:
        if ',' in word:
            word_without_comma = word.replace(',', '')
            words_with_pauses.extend([word_without_comma, ','])
        else:
            words_with_pauses.append(word)
    words = words_with_pauses

    word_index = 0
    next_word_start = beat_times[0] if lag == 0 else beat_times[lag]

    for i, beat_time in enumerate(beat_times):
        if i >= lag and word_index < len(words) and beat_time >= next_word_start:
            word = words[word_index]

            if word == '\n':  # Newline, add a 2-beat pause
                next_word_start = beat_time + 4 * (60 / tempo)
                word_index += 1
                continue
            elif ',' in word:  # Comma, add a 1-beat pause
                next_word_start = beat_time + 1 * (60 / tempo)
                word_index += 1
                continue

            # Generate spoken audio for the current word
            if word.strip() != '':
                spoken_word = azure_audio_segment(word)
            else:
                spoken_word = AudioSegment.silent(duration=100)

            # Adjust the rap speed
            spoken_word = speedup(spoken_word, playback_speed=rap_speed_factor)
            # Remove silence from the beginning and end of the spoken word
            spoken_word = strip_silence(spoken_word, silence_thresh=silence_thresh)

            ## Randomize the pitch
            # random_pitch_shift = random.randint(-3, 3)
            # spoken_word = pitch_shift(spoken_word, random_pitch_shift)

            # Overlay the spoken audio on the beat
            output_audio = output_audio.overlay(
                spoken_word,
                position=int(beat_time * 1000)
            )

            # Update the word index and set the start time for the next word with overlap
            word_index += 1
            next_word_start = beat_time + spoken_word.duration_seconds - overlap

    # Combine the click sounds with the original audio
    input_audio = AudioSegment.from_file(input_file)
    input_audio = input_audio - music_volume  # Decrease the music volume
    output_audio = output_audio + vocal_volume  # Increase the vocal volume
    combined_audio = input_audio.overlay(output_audio)

    # Save the result to a new file
    combined_audio.export(output_file, format="mp3")


def strip_silence(audio_segment, silence_thresh=-60):
    non_silent_ranges = detect_nonsilent(audio_segment, min_silence_len=50, silence_thresh=silence_thresh)
    if len(non_silent_ranges) > 0:
        start_trim, end_trim = non_silent_ranges[0]
        return audio_segment[start_trim:end_trim]
    else:
        return audio_segment



# Usage
input_file = "rap.mp3"
output_file = "output_audio_with_clicks.mp3"

# lyrics = "hello darkness my old friend I've come to talk with you again"
# lyrics = """
# I got some news 
# that'll make you mad
# Your goat's gone, I fucked it bad
# Your dad is dead and I'm crying
# but RIP to the goat, he's the only one flying
# """

lyrics = """
I'm spitting rhymes, I'm feeling great
The beats I ride, I navigate
My words are strong, like dynamite
I light it up, I own the night

The microphone, my closest friend
Together, we will never bend
I conquer stages, crowds erupt
My flow's unique, I won't disrupt

I rise above, I break the chains
My verses free, they heal the pains
I'm rapping now, I'm soaring high
A lyricist until I die
"""
import random

def random_pitch_shift(audio_segment, min_shift=-3, max_shift=3):
    random_shift = random.randint(min_shift, max_shift)
    return pitch_shift(audio_segment, random_shift)

def emphasize_rhyme(audio_segment, factor=1.5):
    return audio_segment + (audio_segment * int(factor))
# rap_on_beats(input_file, output_file, lyrics, lag=8, rap_speed_factor=1.4, music_volume=15, silence_thresh=-60, overlap=.15)

def spit_bars(input_file, output_file, lyrics, lag=0, beat_volume=-10, vocal_volume=5, flow_speed=1.0, click_volume=10, overlap=0.1, silence_thresh=-60):
    # Load the beat
    y, sr = librosa.load(input_file, sr=None)
    
    emphasizable_suffixes = ["ate", "ight", "ain", "ing", "one", "yze", "ime", "oke", "ame", "aze","ine", "ive", "ound", "ill", "ash", "ust", "are", "ace", "eep", "oom"]

    # Find the beat positions
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Create an empty audio segment
    output_audio = AudioSegment.silent(duration=len(y) / sr * 1000)

    # Split the lyrics into verses and bars
    verses = lyrics.strip().split('\n\n')
    words = []
    for verse in verses:
        bars = verse.strip().split('\n')
        for bar in bars:
            bar_words = bar.strip().split()
            for i, word in enumerate(bar_words):
                words.append(word)
            words.append(' ')

    words_with_pauses = []
    for word in words:
        if ',' in word:
            word_no_comma = word.replace(',', '')
            words_with_pauses.extend([word_no_comma, ','])
        else:
            words_with_pauses.append(word)
    words = words_with_pauses

    word_index = 0
    next_word_start = beat_times[0] if lag == 0 else beat_times[lag]

    for i, beat_time in enumerate(beat_times):
        if i >= lag and word_index < len(words) and beat_time >= next_word_start:
            word = words[word_index]
            
            # ... existing code ...

            if word.strip() != '' and word.strip() != ',':
            
                spoken_word = azure_audio_segment(word)
                spoken_word = speedup(spoken_word, playback_speed=flow_speed)
                spoken_word = strip_silence(spoken_word, silence_thresh=silence_thresh)
                # except Exception as e:
                #     spoken_word = AudioSegment.silent(duration=1000)

                # Add random pitch variations
                spoken_word = random_pitch_shift(spoken_word)

                # Emphasize rhymes or specific syllables
                if any(word.endswith(suffix) for suffix in emphasizable_suffixes):
                    spoken_word = emphasize_rhyme(spoken_word)

            else:
                spoken_word = AudioSegment.silent(duration=1000)

            output_audio = output_audio.overlay(
                spoken_word,
                position=int(beat_time * 1000)
            )

            word_index += 1
            next_word_start = beat_time + (spoken_word.duration_seconds / 2) - overlap

    input_audio = AudioSegment.from_file(input_file)
    input_audio = input_audio - beat_volume
    output_audio = output_audio + vocal_volume
    combined_audio = input_audio.overlay(output_audio)

    combined_audio.export(output_file, format="mp3")


def strip_silence(audio_segment, silence_thresh=-80):
    non_silent_ranges = detect_nonsilent(audio_segment, min_silence_len=60, silence_thresh=silence_thresh)
    if len(non_silent_ranges) > 0:
        start_trim, end_trim = non_silent_ranges[0]
        return audio_segment[start_trim:end_trim]
    else:
        return audio_segment


# "up" will stop at -50 do not go above
rap_on_phrases(input_file, output_file, lyrics, lag=8, rap_speed_factor=1.2, music_volume=15, silence_thresh=-60, overlap=0)



# spit_bars(input_file, output_file, lyrics, lag=8, flow_speed=1.4, beat_volume=15, silence_thresh=-60, overlap=.05)


# add_click_on_beats(input_file, output_file)