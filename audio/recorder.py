import soundcard as sc
import numpy as np
import soundfile as sf
import os
import datetime
import warnings
from soundcard import SoundcardRuntimeWarning
from pathlib import Path
from traceback import print_exc

# Suppress Soundcard warnings
warnings.filterwarnings("ignore", category=SoundcardRuntimeWarning)

# --- Setup the recording directory ---
project_root = Path(__file__).resolve().parent.parent
SAVE_DIR = project_root / "output"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_unique_filename(base_path, filename):
    path = base_path / filename
    counter = 1
    while path.exists():
        name, ext = os.path.splitext(filename)
        path = base_path / f"{name}_{counter}{ext}"
        counter += 1
    return path

def record_audio(root, stop_recording, samplerate=48000, blocksize=2048):

    # List all available devices (including loopback devices)
    mics = sc.all_microphones(include_loopback=True)
    if len(mics) < 2:
        print("Need at least two devices (loopback and microphone) for combined recording!")
        return

    # Assume mics[0] is the system output (loopback) and mics[1] is the microphone
    loopback_device = mics[0]
    mic_device = mics[1]

    frames = []

    # Open both recorders concurrently
    with loopback_device.recorder(samplerate=samplerate, channels=2, blocksize=blocksize) as loopback_recorder, \
         mic_device.recorder(samplerate=samplerate, channels=2, blocksize=blocksize) as mic_recorder:
        
        while not stop_recording():
            # Record a block from both devices
            loopback_data = loopback_recorder.record(numframes=blocksize)
            mic_data = mic_recorder.record(numframes=blocksize)
            
            # Mix the two by averaging their samples
            mixed_data = (loopback_data + mic_data) / 2
            frames.append(mixed_data)

    # Concatenate all recorded blocks
    audio = np.concatenate(frames, axis=0)

    # Create save directory based on client phone number
    try:
        hashed_path_folder = SAVE_DIR / (root.client_data["fullName"].title() + " " + root.client_data["phone"])
        hashed_path_folder.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print_exc()
        return # Skip saving if there's an error
    
    # Create a timestamped filename
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
    base_filename = f"call_{timestamp}.wav"
    wav_filename = get_unique_filename(hashed_path_folder, base_filename)

    # Save the combined audio to a WAV file with metadata and error handling
    try:
        with sf.SoundFile(wav_filename, 'w', samplerate=samplerate, channels=2, subtype='PCM_16') as f:
            f.title = f"Call from {root.client_data['phone']} on {timestamp}"
            f.comment = "Recorded using soundcard and soundfile"
            f.write(audio)
    except Exception as e:
        print(f"Error saving recording: {e}")

