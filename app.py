import moviepy as mp
import os
import glob
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/convert', methods=['POST'])
def convert_mp4_to_mp3():
    """
    Convert a single MP4 file to MP3 format.

    Args:
        video_file (str): Path to the input MP4 file
        mp3_folder (str): Directory where the MP3 file will be saved

    Returns:
        None
    """
    mp4_path = request.form.get('mp4_path')
    mp3_path = request.form.get('mp3_path')
    message = ""
    try:
        if not os.path.exists(mp4_path) or not os.path.isdir(mp4_path):
            message = f"The MP4 directory {mp4_path} does not exist!"
        elif not os.path.exists(mp3_path) and not os.path.isdir(mp3_path):
            os.makedirs(mp3_path,exist_ok=True)
        
        mp4_files =  glob.glob(os.path.join(mp4_path, "*.mp4"))

        if not mp4_files:
            message = f"No MP4 files found in the provided directory {mp4_path}."

        for mp4_file in mp4_files:

            full_mp4_path = os.path.join(mp4_path, mp4_file)
            # Create video clip object from the input file
            clip = mp.VideoFileClip(mp4_file)

           # Get the base name of the mp4 file (e.g., "video1.mp4")
            base_filename = os.path.basename(full_mp4_path)
                
            # Get the filename without extension (e.g., "video1")
            filename_without_ext = os.path.splitext(base_filename)[0]
            mp3_filename = filename_without_ext + ".mp3"
            full_mp3_path = os.path.join(mp3_path, mp3_filename)
            print("$$$$$$$$$$$$$$$$$"+full_mp3_path)

            # Extract audio from video and save as MP3
            clip.audio.write_audiofile(full_mp3_path)

            # Close the clip to free up system resources
            clip.close()
            
        message = "Files converted successfully!"
            
    except Exception as e:
        message = f"An error occurred: {str(e)}"

    return render_template("index.html", message=message)

   



if __name__ == "__main__":
     app.run(debug=True)
