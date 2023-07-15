# import subprocess
# from mutagen.mp3 import MP3
# import moviepy.editor as mp
# from gtts import gTTS
# import os
# import requests
# from serpapi import GoogleSearch
#
#
# def download_image(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(filename, 'wb') as f:
#             f.write(response.content)
#             print(f"Downloaded {filename}")
#         return True
#     else:
#         print(f"Failed to download {filename}")
#         return False
#
#
# def download_images_from_sentences(sentences):
#     api_key = "aeb54622bbb059e17c4065cae319d0fa4c50dc36e73b8257acf4541b41836c12"
#
#     for i, sentence in enumerate(sentences):
#         params = {
#             "engine": "google_images",
#             "q": sentence,
#             "api_key": api_key,
#         }
#
#         search = GoogleSearch(params)
#         results = search.get_dict()
#
#         if "images_results" in results:
#             images_results = results["images_results"]
#             for j, image_result in enumerate(images_results):
#                 image_url = image_result["original"]
#                 filename = f"image_{i + 1}.jpg"
#                 if download_image(image_url, filename):
#                     print(f"Downloaded {filename}")
#                     break  # Break out of the inner loop if download succeeds
#             else:
#                 print(f"No image found for sentence {i + 1}")
#         else:
#             print(f"No image results found for sentence {i + 1}")
#
#         print()  # Add a new line for visual separation
#
#
# def generate_voiceover(sentence, filename):
#     tts = gTTS(text=sentence, lang='en')
#     tts.save(filename)
#
#
# def generate_subtitle(sentence, start_time, end_time, filename, i):
#     start_time_str = format_time(start_time)
#     end_time_str = format_time(end_time)
#     subtitle = f"{i}\n{start_time_str} --> {end_time_str}\n{sentence}\n\n"
#     with open(filename, 'a') as f:
#         f.write(subtitle)
#
#
# def format_time(seconds):
#     hours = int(seconds / 3600)
#     minutes = int((seconds % 3600) / 60)
#     seconds = int(seconds % 60)
#     return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
#
#
# def create_video(sentences, image_files, video_filename):
#     video_clips = []
#     audio_clips = []
#     subtitle_filename = 'subtitle.srt'
#     FPS = 24  # Set the desired frames per second for the video
#     subtitle_start_time = 0
#
#     # Generate voiceovers and subtitles for each sentence
#     for i, sentence in enumerate(sentences):
#         image_file = image_files[i]
#         voiceover_filename = f"voiceover_{i+1}.mp3"
#
#         # Generate voiceover
#         generate_voiceover(sentence, voiceover_filename)
#
#         # Load voiceover and get its duration
#         audio_clip = mp.AudioFileClip(voiceover_filename)
#         audio_duration = audio_clip.duration
#
#         # Generate subtitle
#         generate_subtitle(sentence, subtitle_start_time, subtitle_start_time + audio_duration, subtitle_filename, i + 1)
#
#         # Load image and set duration based on voiceover duration
#         image_clip = mp.ImageClip(image_file).set_duration(audio_duration)
#         video_clips.append(image_clip)
#
#         # Append voiceover clip to audio_clips list
#         audio_clips.append(audio_clip)
#
#         # Update the subtitle start time for the next iteration
#         subtitle_start_time += audio_duration
#
#     # Concatenate video and audio clips
#     video = mp.concatenate_videoclips(video_clips, method="compose")
#     audio = mp.concatenate_audioclips(audio_clips)
#
#     # Set audio to match video duration
#     audio = audio.set_duration(video.duration)
#
#     # Add audio to video
#     video = video.set_audio(audio)
#
#     # Add subtitles to the video
#     video = video.set_subtitles(subtitle_filename)
#
#     # Write the final video file
#     video.write_videofile(video_filename, fps=FPS)
#
#     # Remove the subtitle file
#     os.remove(subtitle_filename)
#
#
# # Example usage
# sentences = [
#     'Cricket is believed to have originated in the 16th century in England and is now played in over 100 countries worldwide.',
#     'The longest recorded cricket match lasted for 10 days.',
#     'It took place in 1939 between England and South Africa and ended in a draw.',
#     'The highest individual score in international cricket is 400 runs, scored by Brian Lara from the West Indies against England in 2004.',
#     'The fastest century in international cricket was scored by AB de Villiers from South Africa, who reached the milestone in just 31 balls in 2015.',
#     'The Ashes is a famous cricket series played between England and Australia. It originated in 1882 and is one of the oldest rivalries in sports.'
# ]
#
# image_files = ['image_1.jpg', 'image_2.jpg', 'image_3.jpg', 'image_4.jpg', 'image_5.jpg', 'image_6.jpg']
#
# video_filename = 'cricket_video.mp4'
#
# create_video(sentences, image_files, video_filename)
import random

import gpt_2_simple as gpt2

# Load the pre-trained GPT-2 model
# Download the GPT-2 model files
model_name = "124M"
# gpt2.download_gpt2(model_name=model_name)

# Load the pre-trained GPT-2 model
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, model_name=model_name)

def generate_small_sentences(sentences, model, max_length=20, num_sentences=5, temperature=0.7):
    small_sentences = []

    for _ in range(num_sentences):
        sentence = random.choice(sentences)
        input_text = sentence[:max_length]  # Trim the sentence to the maximum length

        # Generate continuation using the language model
        generated = gpt2.generate(
            sess,
            model_name=model_name,
            length=30,
            temperature=temperature,
            prefix=input_text,
            return_as_list=True
        )[0]
        generated = generated[len(input_text):]

        small_sentences.append(generated.strip())

    return small_sentences

sentences = [
    'Cricket is believed to have originated in the 16th century in England and is now played in over 100 countries worldwide.',
    # 'The longest recorded cricket match lasted for 10 days.',
    # 'It took place in 1939 between England and South Africa and ended in a draw.',
    # 'The highest individual score in international cricket is 400 runs, scored by Brian Lara from the West Indies against England in 2004.',
    # 'The fastest century in international cricket was scored by AB de Villiers from South Africa, who reached the milestone in just 31 balls in 2015.',
    # 'The Ashes is a famous cricket series played between England and Australia. It originated in 1882 and is one of the oldest rivalries in sports.'
]

print(generate_small_sentences(sentences, model_name))