import os
from pathlib import Path
from audio import record_audio  # your recording module function
from thread_manager.manager import main_thread, is_stop_flag_set  # Import the checker
from gui.main_window import main_tk

# --- Setup the recording directory ---
project_root = Path(__file__).resolve().parent
SAVE_DIR = project_root / "output"
LOGO_PATH = project_root / "logo.ico"
os.makedirs(SAVE_DIR, exist_ok=True)

# Create the Tk instance from the GUI module function
root = main_tk(LOGO_PATH)

# Updated stop condition function: returns True if the stop_flag is set.
def stop_recording():
    return is_stop_flag_set()

# --- Recording thread function ---
def recording_thread_function():

    record_audio(root, stop_recording)

# Start the recording thread (non-daemon so we can join later)
recording_thread = main_thread(target=recording_thread_function)
recording_thread.start()

# --- Check periodically if recording has finished ---
def check_recording_thread():
    if not recording_thread.is_alive():
        # Once recording finishes, close the GUI's main loop if it's still running.
        root.quit()
    else:
        # Check again after 100ms
        root.after(100, check_recording_thread)

root.after(100, check_recording_thread)

# Run the GUI event loop in the main thread
root.mainloop()





# Wait for the recording thread to finish before exiting the program
recording_thread.join()
