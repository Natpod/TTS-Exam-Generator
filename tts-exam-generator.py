import csv
import os
import random
import time
from gtts import gTTS
from pydub import AudioSegment
from pydub import AudioSegment
from pydub.utils import which

import sys

if len(sys.argv) != 3:
    print("Usage: python tts-exam-generator.py <input_csv> <output_mp3>")
    sys.exit(1)

print("Input file:", input_file)
print("Output folder:", output_file)

# =========================
# CONFIGURATION
# =========================
ACCENTS = ["com", "co.uk", "com.au", "ca", "ie", "co.za", "co.in"]


CSV_FILE = sys.argv[1]
SFX_PATH = os.path.abspath("./resources/beep.mp3")
OUTPUT_FOLDER = sys.argv[2]


AudioSegment.converter = $FFMPEG_PATH  # <-- path to ffmpeg.exe


# =========================
# HELPER FUNCTIONS
# =========================

def generate_tts(text, tld="com"):
    """Return AudioSegment object from gTTS"""
    filename = "temp.mp3"
    tts = gTTS(text=text, lang="en", tld=tld)
    tts.save(filename)
    audio = AudioSegment.from_mp3(filename)
    os.remove(filename)
    return audio

def simulate_gender(audio, gender="female"):
    """
    Simulate male/female voice by pitch/speed adjustment
    female: slightly faster, higher pitch
    male: slightly slower, lower pitch
    """
    if gender == "female":
        return audio.speedup(playback_speed=1.1)  # faster
    elif gender == "male":
        return audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * 0.9)  # lower pitch
        }).set_frame_rate(audio.frame_rate)
    else:
        return audio

def format_excerpt(text_type, text):
    """
    Dialogue → split speakers and apply random accent + gender
    Monologue → smooth, default female
    """
    if text_type.lower() == "dialogue" and "-" in text:
        # Intro for dialogue
        intro_text = "Listen to the following dialogue."
        intro_audio = generate_tts(intro_text, tld="com")
        intro_audio = simulate_gender(intro_audio, "female")  # intro always female

        # Split speakers
        speaker_texts = text.split("-")
        audios = []

        # Random accents and genders for each speaker
        accent_list = [random.choice(ACCENTS) for _ in range(2)]
        gender_list = [random.choice(["male", "female"]) for _ in range(2)]

        for idx, sp_text in enumerate(speaker_texts):
            if idx % 2 == 0:  # even question
                accent = accent_list[0]
                gender = gender_list[0]
    
                # Add small silence before each speaker
                sp_audio = AudioSegment.silent(duration=100) + generate_tts(sp_text, tld=accent)
                sp_audio = simulate_gender(sp_audio, gender)
                audios.append(sp_audio)
            else:
                accent = accent_list[1]
                gender = gender_list[1]
    
                # Add small silence before each speaker
                sp_audio = AudioSegment.silent(duration=100) + generate_tts(sp_text, tld=accent)
                sp_audio = simulate_gender(sp_audio, gender)
                audios.append(sp_audio)
                

        # Merge intro + all speaker audios
        return intro_audio + AudioSegment.silent(duration=100) + sum(audios)

    else:
        # Monologue
        intro_text = "Listen to the following speaker. "
        intro_audio = generate_tts(intro_text, tld="com")
        intro_audio = simulate_gender(intro_audio, "female")  # intro always female

        accent = random.choice(ACCENTS)
        gender = random.choice(["male", "female"])

        sp_audio = generate_tts(text, tld=accent)
        sp_audio = simulate_gender(sp_audio, gender)
        return intro_audio + AudioSegment.silent(duration=100) + sp_audio

# =========================
# MERGE EXAM
# =========================

final_audio = AudioSegment.silent(duration=500)

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        q_number = row["QuestionNumber"]
        q_type = row["Type"]
        excerpt = row["Excerpt"]
        question = row["Question"]

        print(f"Processing Question {q_number} ({q_type})...")

        # --- Question number ---
        qnum_audio = generate_tts(f"Question {q_number}.")
        final_audio += AudioSegment.silent(duration=200) + qnum_audio

        # --- Excerpt ---
        excerpt_audio = format_excerpt(q_type, excerpt)
        final_audio += beep + excerpt_audio + beep

        # --- Question ---
        question_audio = generate_tts(question)
        question_audio = simulate_gender(question_audio, "female")
        final_audio += AudioSegment.silent(duration=200) + question_audio + AudioSegment.silent(duration=200)

        # Thinking pause
        final_audio += AudioSegment.silent(duration=8000)

# Export final merged MP3
final_audio.export(FINAL_MP3, format="mp3")
print(f"\nFinal exam MP3 generated: {FINAL_MP3}")