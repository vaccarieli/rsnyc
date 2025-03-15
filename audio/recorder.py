import soundcard as sc
import numpy as np
import soundfile as sf
import os
import datetime
import warnings
from soundcard import SoundcardRuntimeWarning

warnings.filterwarnings("ignore", category=SoundcardRuntimeWarning)

def record_audio(save_dir, stop_recording, samplerate=48000, blocksize=2048):
    """Record audio from loopback and microphone devices until stop_recording returns True."""
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

    # Create a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    wav_filename = os.path.join(save_dir, f"call_{timestamp}.wav")

    # Save the combined audio to a WAV file
    sf.write(wav_filename, audio, samplerate)
    print(f"Recording saved as {wav_filename}")