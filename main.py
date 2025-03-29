import os
from pathlib import Path
from audio import record_audio
from thread_manager.manager import main_thread, is_stop_flag_set
from gui.main_window import main_tk
from dotenv import load_dotenv
from handle_data.data import write_json_file
from ai.transcribe import transcribe_audio
from datetime import datetime  # Added for date handling

# Load environment variables
load_dotenv()
RECORD_CALL = os.getenv("RECORD_CALL", "False").lower() == "true"  # Convert to boolean

# Setup the recording directory
project_root = Path(__file__).resolve().parent
SAVE_DIR = project_root / "output"
LOGO_PATH = project_root / "logo.ico"
CLIENT_DATA_PATH = project_root / "data/clients.json"

os.makedirs(SAVE_DIR, exist_ok=True)

# Create the Tkinter GUI instance
root = main_tk(LOGO_PATH)

# Define stop condition for recording
def stop_recording():
    """Return True if the stop flag is set, signaling recording to stop."""
    return is_stop_flag_set()

# Define the recording thread's target function
def recording_thread_function():
    """Execute the audio recording process with the GUI root and stop condition."""
    record_audio(root, stop_recording)

# Define the function to monitor recording thread completion
def check_if_recording_finished(thread):
    """Check if the recording thread has finished; quit GUI if done, else recheck."""
    if not thread.is_alive():
        root.quit()
    else:
        root.after(100, lambda: check_if_recording_finished(thread))

# Function to append transcription to today's comment
def append_transcription_to_today(client_data, transcription):
    """Append a transcription to the 'transcribed call' list for today's date."""
    today = datetime.now().strftime("%m-%d-%Y")  # Format: MM-DD-YYYY
    comments = client_data.get("comments", [])  # Safely get comments, default to empty list
    # Find existing comment for today
    comment_today = next((comment for comment in comments if comment["date"] == today), None)
    if comment_today is None:
        # Create new comment entry for today if none exists
        comment_today = {
            "date": today,
            "comment": "",  # Empty by default; could be modified to accept user input
            "transcribed call": []
        }
        comments.append(comment_today)
    # Ensure 'transcribed call' key exists
    if "transcribed call" not in comment_today:
        comment_today["transcribed call"] = []
    # Append the transcription
    comment_today["transcribed call"].append(transcription)

# Start recording if enabled
if RECORD_CALL:
    # Initialize and start the recording thread
    recording_thread = main_thread(target=recording_thread_function)
    recording_thread.start()
    
    # Schedule periodic check for thread completion
    root.after(100, lambda: check_if_recording_finished(recording_thread))

# Run the GUI event loop
root.mainloop()

# Ensure recording thread completes before program exit
if RECORD_CALL:
    recording_thread.join()
    
    if root.language == "English":
        transcribed_audio_text = transcribe_audio(root.wav_filename)
    else:
        transcribed_audio_text = transcribe_audio(root.wav_filename, "es-ES")  # Spanish transcription

    # Access client data
    client_data = root.main_data[root.full_phone_number][0]
    # Append transcription to today's comment
    append_transcription_to_today(client_data, transcribed_audio_text)
    # Save updated data to JSON file
    write_json_file(CLIENT_DATA_PATH, root.main_data)