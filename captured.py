# captured.py

last_prediction = None
last_frame = None

def set_last_capture(prediction, frame):
    global last_prediction, last_frame
    last_prediction = prediction
    last_frame = frame.copy() if frame is not None else None

def get_last_capture():
    """
    Return a dict with keys:
      - 'name': the last predicted name
      - 'frame': the last captured frame
    """
    return {"name": last_prediction, "frame": last_frame}