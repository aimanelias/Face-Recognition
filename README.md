# Face Recognition Multiple Feed UI v2

A multi-camera face recognition system for MIMOS employees, using ONNX models and a web-based UI.

---

## Project Structure

- **`buffalo_l/`**: Model pack containing face detection and face recognition ONNX models.
- **`db/`**: Images of all MIMOS employees.
- **`failed_faces.txt`**: Lists employee images that failed to convert to embeddings.
- **`selection_log.json`**: Logs face recognition and selection results.
- **`captured_images/`**: Stores images captured from camera feeds.
- **Source code**:  
  - `main.py`  
  - `camera.py`  
  - `face_recognition.py`  
  - `templates/index.html`

---

## Installation

Install dependencies with:

```bash
pip install opencv-python opencv-python-headless insightface fastapi uvicorn jinja2 numpy torch torchvision python-dotenv aiofiles
```

---

## Running the Project

Run the main application:

```bash
python main.py
```

---

## Using with Tablet (IP Webcam)

1. **Connect** the tablet to the `mimoswifi_5g` network.
2. **Open** the IP Webcam app.
3. **Start the server** in the app.
4. **Note** the IP address and port number displayed (in HTTP form).
5. **Convert** to RTSP format:  
   `rtsp://<ip>:<port>/h264_ulaw.sdp`
6. **Edit** `main.py` to add your camera feed:

    ```python
    CAMERA_URLS = {
        "cam1": "rtsp://admin:Mm813669@10.8.11.29/cam/realmonitor?channel=1&subtype=2",
        "cam2": "rtsp://10.1.106.81:8080/h264_ulaw.sdp",
    }
    ```

7. **Access the web UI**:  
   - `http://10.1.39.77:8000/cam1`  
   - `http://10.1.39.77:8000/cam2`
8. **Leave** the IP Webcam app running in the background.
9. **Open** "Fully Kiosk Browser" or Chrome and enter the website URL.

---

## Log File Explanation

- **`selection_log.json`**:
  - `name: None` or `button: None` → No correct face recognized.
  - `name` not None and `button: 1` → Face recognized correctly.
  - `name` not None and `button: 2` or `3` → Face recognized, but not very accurate.
  - `name`: Employee image file name.
  - `button`: Which position's button was clicked.
  - `camera_id`: Location/device of the user click.

---

## Notes

- The main working folder is:  
  `C:\Users\hyper\Documents\Face Recognition Multiple Feed UI v2`
- There is a secondary folder for dynamic file paths:  
  `C:\Users\hyper\Documents\Face Recognition Multiple Feed-build version`  
  (Note: There were issues converting this to `.exe`.)

---

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

--- 