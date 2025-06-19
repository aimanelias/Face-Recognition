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

1. **Connect** the tablet to your local Wi-Fi network (ensure this device is connected to the same network as the machine running the application).
2. **Install and open** the IP Webcam app on the tablet (make sure the IP Webcam app is installed).
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

## Using with CCTV (RTSP Camera)

To use this system with a CCTV or any RTSP-compatible camera, follow these steps:

1. **Set up your CCTV camera** and ensure it is connected to your local network.
2. **Obtain the RTSP stream URL** from your camera's settings or user manual. It usually looks like:
   - `rtsp://<username>:<password>@<camera-ip>:<port>/path`
   - Example: `rtsp://admin:password@192.168.1.100:554/stream1`
3. **Edit the `main.py` file** to add your CCTV RTSP stream(s) to the `CAMERA_URLS` dictionary:

    ```python
    CAMERA_URLS = {
        "cam1": "rtsp://admin:password@192.168.1.100:554/stream1",
        # Add more cameras as needed
    }
    ```

4. **Save the changes** to `main.py`.
5. **Run the application**:

    ```bash
    python main.py
    ```

6. **Access the web UI** from any device on the same network:
   - `http://<server-ip>:8000/cam1`
   - Replace `<server-ip>` with the IP address of the computer running this project.
7. **View the live CCTV feed and face recognition results** in your browser.

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
