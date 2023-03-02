import os
import whisper
from moviepy.editor import VideoFileClip


def extract_audio(file_name: str) -> str:
    """This method is used to transcribe the Audio File with OpenAI Whisper.

    :param file_name: Name of the Audio or Video File that needs to be processed.
    :type file_name: str
    """

    # extract the audio from the mp4
    video = VideoFileClip(
        f"..data/input/{file_name}"
    )  
    new_file_name = file_name.split(".")[0]

    # Extract the audio
    audio = video.audio

    # Write the audio to a file
    audio.write_audiofile(f"../input/{new_file_name}.mp3")

    # delete the video file
    os.remove(f"../data/input/{file_name}")

    return new_file_name


def transcribe(file_name: str):
    # first check if the input is a video or a audio by checking the ending
    if file_name.split(".")[-1] == "mp4":
        file_name = extract_audio(file_name=file_name)
    model = whisper.load_model("tiny")
    whisper.DecodingOptions(language="de", without_timestamps=False)

    result = model.transcribe(f"{file_name}")  # , task = 'translate'
    return result["text"]
