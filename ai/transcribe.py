from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource
)
import os
from dotenv import load_dotenv

load_dotenv()
DEEPGRAM_KEY = os.getenv("DEEPGRAM_KEY")

def transcribe_audio(audio_file, language="en-US"):
    try:
        deepgram = DeepgramClient(DEEPGRAM_KEY)
        
        # Remove 'tier' and use current model name
        options = PrerecordedOptions(
            model="nova-2",  # or "nova" if 403 persists
            punctuate=True,
            language=language
        )
        
        with open(audio_file, "rb") as file:
            buffer_data = file.read()
        
        payload: FileSource = {"buffer": buffer_data}
        
        # Use non-deprecated endpoint
        response = deepgram.listen.rest.v("1").transcribe_file(
            payload, options
        )
        return response.results.channels[0].alternatives[0].transcript

    except Exception as e:
        print(f"Exception: {e}")
