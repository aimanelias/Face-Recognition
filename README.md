# Face Recognition Multiple Feed UI v2

A multi-camera face recognition system using ONNX models and a web-based UI.

---

## Project Structure

- **`buffalo_l/`**: Model pack containing face detection and face recognition ONNX models.
- **`db/`**: Images of all enrolled users.
- **`failed_faces.txt`**: Lists images that failed to convert to embeddings.
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

1. **Connect** the tablet to your local Wi-Fi network.
2. **Open** the IP Webcam app.
3. **Start the server** in the app.
4. **Note** the IP address and port number displayed (in HTTP form).
5. **Convert** to RTSP format:  
   `rtsp://<ip>:<port>/h264_ulaw.sdp`
6. **Edit** `main.py` to add your camera feed:

    ```python
    CAMERA_URLS = {
        "cam1": "rtsp://admin:password@<ip-address>/cam/realmonitor?channel=1&subtype=2",
        "cam2": "rtsp://<ip>:<port>/h264_ulaw.sdp",
    }
    ```

7. **Access the web UI**:  
   - `http://<server-ip>:8000/cam1`  
   - `http://<server-ip>:8000/cam2`
8. **Leave** the IP Webcam app running in the background.
9. **Open** your preferred browser and enter the website URL.

---

## Log File Explanation

- **`selection_log.json`**:
  - `name: None` or `button: None` → No correct face recognized.
  - `name` not None and `button: 1` → Face recognized correctly.
  - `name` not None and `button: 2` or `3` → Face recognized, but not very accurate.
  - `name`: User image file name.
  - `button`: Which position's button was clicked.
  - `camera_id`: Location/device of the user click.

---

## Notes

- The main working folder is:  
  `<your_project_directory>`
- There is a secondary folder for dynamic file paths (optional):  
  `<your_dynamic_path_folder>`  
  (Note: There were issues converting this to `.exe`.)

---
