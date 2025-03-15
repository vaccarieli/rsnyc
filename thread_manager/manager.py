from threading import Thread, Event

# Global event to signal stopping
stop_flag = Event()

def main_thread(target):
    return Thread(target=target)

def set_stop_flag():
    """Set the stop flag."""
    stop_flag.set()

def is_stop_flag_set():
    """Return True if the stop flag is set, else False."""
    return stop_flag.is_set()

