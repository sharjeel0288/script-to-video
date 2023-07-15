Here are the step-by-step instructions for using the "unsplashvideo.py" script in the mentioned Git repository:

Clone the Repository:

bash
Copy code
git clone git@github.com:sharjeel0288/script-to-video.git

Navigate to the Repository Directory:
cd script-to-video

Install Required Modules:
pip install requests mutagen moviepy gtts pyttsx3 torch transformers


Open the "unsplashvideo.py" File:
nano unsplashvideo.py

Edit the Script:
Replace the placeholder sentences in the sentences list with your own script. Each sentence should be enclosed in quotation marks and separated by a comma.

Save and Exit the File:
Press Ctrl + X, then Y, and finally Enter to save the changes and exit the text editor.

Run the Script:
python unsplashvideo.py
The script will download the necessary images from Unsplash based on the keywords extracted from your script sentences. It will also generate voiceovers and subtitles for each sentence.

Wait for Video Generation:
The script will automatically combine the images, voiceovers, and subtitles to create a final video. The generated video will be saved as "finalvideo.mp4" in the repository directory.

Access the Generated Video:
Once the script finishes executing, you can find the generated video file, "finalvideo.mp4," in the repository directory. You can now view and share the video as desired.

Please note that you will need to have Git and Python (along with pip) installed on your system to successfully execute these steps.
