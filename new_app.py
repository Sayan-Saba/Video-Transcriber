import streamlit as st
import os
import io
import moviepy.editor as mp
import assemblyai as aai
import time

# Set your AssemblyAI API key
aai.settings.api_key = "0c92823b2b524f93a5ad80fb3ad8c666"  # Replace with your AssemblyAI API key

# Path to save temporary files
TEMP_DIR = "C:/Users/sayan/Desktop/Youtube_Transcriber/"

# Helper function to convert video to audio
def extract_audio_from_video(uploaded_file):
    temp_file_path = os.path.join(TEMP_DIR, "temp_video.mp4")
    audio_file_path = os.path.join(TEMP_DIR, "temp_audio.wav")

    # Save the uploaded file
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    try:
        # Convert video to audio
        video = mp.VideoFileClip(temp_file_path)
        video.audio.write_audiofile(audio_file_path)
    finally:
        # Ensure the temporary video file is deleted
        attempt = 0
        while attempt < 5:
            try:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                break
            except PermissionError:
                attempt += 1
                time.sleep(1)  # Wait a bit before retrying
            except Exception as e:
                print(f"Error removing file: {e}")
                break
    
    return audio_file_path

# Helper function to transcribe audio using AssemblyAI
def transcribe_audio_assemblyai(audio_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    return transcript.text

# Streamlit app
st.title("Video to Notes")
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mpeg4"])

if uploaded_file:
    st.video(uploaded_file)

    if st.button("Get Notes"):
        # Extract audio from video
        audio_path = extract_audio_from_video(uploaded_file)

        # Transcribe audio
        transcript_text = transcribe_audio_assemblyai(audio_path)
        st.markdown("## Notes: ")
        st.write(transcript_text)

        # Clean up temporary audio file
        attempt = 0
        while attempt < 5:
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                break
            except PermissionError:
                attempt += 1
                time.sleep(1)  # Wait a bit before retrying
            except Exception as e:
                print(f"Error removing file: {e}")
                break
