"""
Credits for this script - 
developed by - Tejas Shathraj
"""

import os
import sys
import epitran
import audioread
import numpy as np
import pandas as pd
import soundfile as sf
from pathlib import Path
import speech_recognition as sr

epi = epitran.Epitran('deu-Latn')

# Generating path for the folders
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = Path(CURR_DIR).parent.absolute()
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(CURR_DIR))

print(f'Current - {CURR_DIR}\nParent - {PARENT_DIR}\nRoot - {PROJECT_ROOT_DIR}')

def read_file(file_path):
    # Read the tsv file
    df = pd.read_csv(file_path, sep='\t')
    
    # Print the first few lines of the data frame
    print(f'{df.head()}\n')

    return df

def convert_media_files(src_file, dest_dir):
    src_dir_audio_file = os.path.join(PROJECT_ROOT_DIR, 'clips')
    dest_dir = os.path.join(PROJECT_ROOT_DIR, 'data', dest_dir, 'clips')
    src_audio_file = f'{src_dir_audio_file}/{src_file}'
    dest_audio_file = f"{dest_dir}/{src_file.split('.')[0]}.wav"

    try:
        with audioread.audio_open(src_audio_file) as clip:
            data = np.hstack([np.frombuffer(chunk, dtype='int16') for chunk in clip])

            sf.write(dest_audio_file, data, clip.samplerate, format='WAV', subtype='PCM_16')
    except Exception as e:
        print(e)

def generate_transcript_ipa(src, folder, file):
    recognizer = sr.Recognizer()

    transcript_file = os.path.join(PROJECT_ROOT_DIR, 'data', folder, 'transcript', file)
    ipa_file = os.path.join(PROJECT_ROOT_DIR, 'data', folder, 'ipa', file)

    with sr.AudioFile(src) as source:
        audio_data = recognizer.record(source)

        try: 
            text = recognizer.recognize_google(audio_data, language='de-DE')
            print(f'Transcript - {text}')

            with open(transcript_file, 'w', encoding='utf-8') as tf:
                tf.write(text)

            ipa_transcription = epi.transliterate(text)
            print(f'IPA - {ipa_transcription}')

            with open(ipa_file, 'w', encoding='utf-8') as ipa:
                ipa.write(ipa_transcription)
        except sr.UnknownValueError:
            print('Audio unrecognised')
            with open('./transcript_log.txt', 'w', encoding='utf-8') as tf:
                tf.write(f"[Audio-Train-Trans] - {file} - Audio not recognised")
            with open('./ipa_log.txt', 'w', encoding='utf-8') as tf:
                tf.write(f"[Audio-Train-IPA] - {file} - Audio not recognised")
        except sr.RequestError as e:
            print('Audio unrecognised')
            with open('./transcript_log.txt', 'w', encoding='utf-8') as tf:
                tf.write(f"[Audio-Train-Trans] - {file} - Error - {e}")
            with open('./ipa_log.txt', 'w', encoding='utf-8') as tf:
                tf.write(f"[Audio-Train-IPA] - {file} - Error - {e}")

def generate_wave_file(src):
    src_files = os.path.join(PROJECT_ROOT_DIR, 'data', src, 'clips')
    op_file = os.path.join(PROJECT_ROOT_DIR, 'data', src, 'wave')

    with open(op_file, 'w') as file:
        for filename in os.listdir(src_files):
            path = os.path.join(src_files, filename)
            if os.path.isfile(path):
                line = f"{filename.split('.')[0]} {os.path.relpath(path)}\n"
                line = line.replace('../', '')
                print(f'LINE - {line}\n')
                file.write(line)
    
    print(f"Lines with filename and path saved to {op_file}")

def generate_text_file(src):
    src_files = os.path.join(PROJECT_ROOT_DIR, 'data', src, 'ipa')
    op_file = os.path.join(PROJECT_ROOT_DIR, 'data', src, 'text1')

    with open(op_file, 'w') as file:
        for filename in os.listdir(src_files):
            if filename:
                path = os.path.join(src_files, filename)

                with open(path, 'r') as f:
                    print(f)
                    f_text = f.read().strip()
                
                new_line = f"{filename} {f_text}\n"

                file.write(new_line)
    
    print(f'Combined text saved to {op_file}')


def main():
    train_media_files = read_file(os.path.join(CURR_DIR, 'train.tsv'))
    validate_media_files = read_file(os.path.join(CURR_DIR, 'validate.tsv'))

    print('Total Files:\n')
    print(f'Total Train Files: {train_media_files.shape[0]}\n')
    print(f'Total Validate Files: {validate_media_files.shape[0]}\n')

    # Convert MP3 to WAV Audio Files
    for i in range(len(train_media_files['clip'])):
        convert_media_files(train_media_files['clip'][i], 'train')
        generate_transcript_ipa(f"{PROJECT_ROOT_DIR}/data/train/clips/{train_media_files['clip'][i].split('.')[0]}.wav", 'train', train_media_files['clip'][i].split('.')[0])
    
    for i in range(len(validate_media_files['clip'])):
        convert_media_files(validate_media_files['clip'][i], 'validate')
        generate_transcript_ipa(f"{PROJECT_ROOT_DIR}/data/validate/clips/{validate_media_files['clip'][i].split('.')[0]}.wav", 'validate', validate_media_files['clip'][i].split('.')[0])
    
    generate_wave_file('train')
    generate_wave_file('validate')

    generate_text_file('train')
    generate_text_file('validate')

# Run the main function
if __name__ == "__main__":
    main()
