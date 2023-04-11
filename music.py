import openai
import os
import random
from midiutil import MIDIFile
from gtts import gTTS
from pydub import AudioSegment
import tempfile
from creds import API_KEY
import time
import uuid


# openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = API_KEY

def generate_song(genre, lyrics):
    prompt = f"Create a {genre} song with the following lyrics:\n\n{lyrics}\n\nSong:\n\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.8,
    )

    generated_text = response.choices[0].text.strip()
    return generated_text

def simple_random_melody_generator(n_notes):
    melody_data = []
    for _ in range(n_notes):
        pitch = random.randint(60, 72)  # Generate random pitches within a range
        duration = random.uniform(0.5, 1.5)  # Generate random durations
        melody_data.append((pitch, duration))
    return melody_data

def create_melody(melody_data, filename):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)

    time = 0
    for pitch, duration in melody_data:
        midi.addNote(0, 0, pitch, time, duration, 100)
        time += duration

    with open(filename, "wb") as f:
        midi.writeFile(f)

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

def mix_audio(melody_file, lyrics_file, output_file):
    with AudioSegment.from_file(melody_file, format="wav") as melody, \
         AudioSegment.from_file(lyrics_file, format="mp3") as lyrics:

        mixed = melody.overlay(lyrics)
        mixed.export(output_file, format="mp3")

def create_song_file(genre, lyrics):
    generated_song = generate_song(genre, lyrics)
    melody_data = simple_random_melody_generator(20)
    lyrics_text = lyrics

    # Create unique names for the temporary files
    timestamp = str(int(time.time()))
    unique_id = str(uuid.uuid4())
    temp_melody_file = f"temp_melody_{timestamp}_{unique_id}.midi"
    temp_lyrics_file = f"temp_lyrics_{timestamp}_{unique_id}.mp3"
    temp_output_file = f"temp_output_{timestamp}_{unique_id}.mp3"

    try:
        create_melody(melody_data, temp_melody_file)
        new_melody_file = temp_melody_file.replace(".midi", ".wav")
        print(temp_melody_file)
        print(new_melody_file)
        midi_to_wav(temp_melody_file, new_melody_file)  # Add this line
        text_to_speech(lyrics_text, temp_lyrics_file)
        mix_audio(temp_melody_file.replace(".midi", ".wav"), temp_lyrics_file, temp_output_file)  # Update this line


        with open(temp_output_file, "rb") as output_file, open("output_song.mp3", "wb") as f:
            f.write(output_file.read())
    finally:
        # Clean up temporary files
        if os.path.exists(temp_melody_file):
            os.remove(temp_melody_file)
        if os.path.exists(temp_lyrics_file):
            os.remove(temp_lyrics_file)
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)
        if os.path.exists(temp_melody_file.replace(".midi", ".wav")):  # Add this line
            os.remove(temp_melody_file.replace(".midi", ".wav"))  # Add this line


from midi2audio import FluidSynth

def midi_to_wav(midi_file, wav_file):
    soundfont_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Lady_Gaga_Square_Lead_V2.sf2")
    fs = FluidSynth(soundfont_path)
    # Change this to the path to your SoundFont file
    fs.midi_to_audio(midi_file, wav_file)

if __name__ == "__main__":
    genre = "rock"
    lyrics = """Verse 1:
    I'm standing on the edge of time
    Waiting for the world to unwind

    Chorus:
    We're breaking through the chains that bind
    Together, we're gonna redefine"""

    create_song_file(genre, lyrics)
    print("Song generated and saved as output_song.mp3")
