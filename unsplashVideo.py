import random
import string
import urllib.parse
import subprocess
from mutagen.mp3 import MP3
import moviepy.editor as mp
from gtts import gTTS
import os
import requests

UNSPLASH_ACCESS_KEY = "jWFe_MopGmZxO75zXe6JUcz_DsNmbmuHPB2PxvJlpto"

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
        return True
    else:
        print(f"Failed to download {filename}")
        return False


import torch
from transformers import BertTokenizer, BertModel


def create_search_query(sentence, num_keywords=5):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    input_ids = tokenizer.encode(sentence, add_special_tokens=True)
    input_ids = torch.tensor(input_ids).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_ids)
        hidden_states = outputs[0]

    word_lengths = [len(tokenizer.decode([token_id.item()])) for token_id in input_ids.squeeze(0)]
    keywords = []

    for i, length in enumerate(word_lengths):
        if length > max(word_lengths) * 0.6:  # Choose words that are longer than 80% of the maximum word length
            token = tokenizer.decode([input_ids[0][i].item()])
            keywords.append(token)

    query = " ".join(keywords[:num_keywords])  # Use the specified number of extracted keywords as the query

    return urllib.parse.quote(query),keywords[:num_keywords]

import string

def download_images_from_sentences(sentences):
    num = 1
    updated_sentences = []
    for sentence in sentences:
        query, keyword = create_search_query(sentence)
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)
        print(url)
        print(keyword)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                for image_data in data["results"]:
                    image_url = image_data["urls"]["raw"]
                    image_description = image_data["description"]
                    if image_description is not None:
                        # Preprocess string b to remove unwanted characters
                        image_description = image_description.translate(str.maketrans('', '', string.punctuation))
                        print(image_description)

                        intersection = set(keyword).intersection(image_description.lower().split())
                        if len(intersection) >= 0:
                            filename = f'image_{num}.jpg'
                            if download_image(image_url, filename):
                                print(f"Downloaded image for sentence: {sentence}")
                                updated_sentences.append(sentence)
                                num += 1
                                break  # Found a matching image, exit the loop
                            else:
                                print(f"Failed to download the image for sentence: {sentence}")
                        else:
                            print(f"No matching image found for sentence: {sentence}")
                    else:
                        print(f"No image description available for sentence: {sentence}")
            else:
                print(f"No image found for sentence: {sentence}")
        else:
            print("Failed to fetch images from Unsplash.")

    return updated_sentences


import pyttsx3

def generate_voiceover(sentence, filename, speed=1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed * 150)  # Adjust the rate (speed) by scaling the default rate

    # Save the voiceover as an audio file
    engine.save_to_file(sentence, filename)
    engine.runAndWait()

def generate_subtitle(sentence, start_time, end_time, filename, i):
    start_time_str = format_time(start_time)
    end_time_str = format_time(end_time)
    subtitle = f"{i}\n{start_time_str} --> {end_time_str}\n{sentence}\n\n"
    with open(filename, 'a') as f:
        f.write(subtitle)


def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def create_video(sentences, image_files, video_filename):
    video_clips = []
    audio_clips = []
    subtitle_filename = 'subtitle.srt'
    FPS = 24  # Set the desired frames per second for the video
    subtitle_start_time = 0

    # Generate voiceovers and subtitles for each sentence
    for i, sentence in enumerate(sentences):
        image_file = image_files[i]
        voiceover_filename = f"voiceover_{i+1}.mp3"

        # Generate voiceover
        generate_voiceover(sentence, voiceover_filename, speed=1.25)  # Adjust the speed of the voiceover
        # Load voiceover and get its duration
        audio_clip = mp.AudioFileClip(voiceover_filename)
        audio_duration = audio_clip.duration

        # Generate subtitle
        generate_subtitle(sentence, subtitle_start_time, subtitle_start_time + audio_duration, subtitle_filename, i + 1)

        # Load image and set duration based on voiceover duration
        image_clip = mp.ImageClip(image_file).set_duration(audio_duration)
        video_clips.append(image_clip)

        # Append voiceover clip to audio_clips list
        audio_clips.append(audio_clip)

        # Update the subtitle start time for the next iteration
        subtitle_start_time += audio_duration


    # Concatenate video and audio clips
    video = mp.concatenate_videoclips(video_clips, method="compose")
    audio = mp.concatenate_audioclips(audio_clips)

    # Set audio to match video duration
    audio = audio.set_duration(video.duration)

    # Add audio to video
    video = video.set_audio(audio)

    # Write the final video file
    video.write_videofile(video_filename, fps=FPS)

    # Remove temporary files
    os.remove(subtitle_filename)



# Example usage
sentences = [
'Why is popcorn at the movies so expensive?',
' To help keep multiplexes run the show',



'Hey, Are you a movie lover?' ,
'I have an answer to the question for whom we are all curious about why popcorn prices are high in movie cinemas.',
'So, here is the answer to the interesting question.'



]


video_filename = 'finalvideo.mp4'

sentences=download_images_from_sentences(sentences)
image_files = [f"image_{i}.jpg" for i in range(1, len(sentences) + 1)]
create_video(sentences, image_files, video_filename)
