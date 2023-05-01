# Transcription and Summarization with Large Language Models (Aleph Alpha)


## Project Description
This Project show how to transcribe a audio or video using OpenAI Whisper a AI model specialiesed in transcribing 40+ languages. And then the content is summarized using Luminous from Aleph Alpha, a Large Language Model. An example  use case for this project would be to transcribe and summarize a podcast.

## Installation

### Installation as a Docker Container

If you want to use the application as a docker container you need Docker installed.

### Installation directly on your device

I would recommend installing via poetry, but if you do not want to use poetry you have to install the requirements.txt

Installing via Poetry
```
# install poetry
pip install poetry

# poetry installs all the required dependencies and creates a virtual env on your device
poetry install

# spawns a new shell with the newly created virtual env.
poetry shell


```


## How to use

### Docker variant

To start the application start this command.

```
docker-compose up --build -d
```

Then a frontend can be accessed at localhost:8001.
