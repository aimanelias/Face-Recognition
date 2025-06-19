# Face Recognition Multiple Feed UI v2

A multi-camera face recognition system with a web-based UI, supporting both CCTV (RTSP) and mobile/tablet camera feeds. Built with FastAPI, OpenCV, and InsightFace.

---

## Features

- Real-time face detection and recognition from multiple camera sources (CCTV, IP Webcam, etc.)
- Web-based interface for live video and recognition results
- User feedback logging for recognition accuracy
- Performance evaluation tools
- Easy integration of new camera sources

---

## Project Structure

- **`buffalo_l/`**: ONNX models for face detection and recognition (used by InsightFace)
- **`db/`**: Images of enrolled users (used to build the face database)
- **`captured_images/`**: Images saved when a user marks a recognition as incorrect
- **`failed_faces.txt`**: List of images that failed to generate embeddings
- **`recognition_log.json`**: Log of all recognition events
- **`selection_log.json`**: Log of user feedback on recognition results
- **Source code**:
  - `main.py`: FastAPI server, web UI, and API endpoints
  - `camera.py`: Camera stream handling, face detection, and annotation
  - `face_recognition.py`: Face embedding, recognition, and database management
  - `captured.py`: Utilities for saving and retrieving the last captured frame/prediction
  - `eval_performance.py`: Script to evaluate recognition performance from logs
  - `templates/index.html`: Web UI template

---

## Installation

Install dependencies:

```bash
pip install opencv-python opencv-python-headless insightface fastapi uvicorn jinja2 numpy torch torchvision python-dotenv aiofiles
```

---

## Running the Project

Start the FastAPI server:

```bash
python main.py
```

The server will run on `http://0.0.0.0:8000` by default.

---

## Adding Camera Feeds

Edit the `CAMERA_URLS` dictionary in `main.py` to add your camera sources:

```python
CAMERA_URLS = {
    "cam1": "rtsp://admin:password@<ip-address>/cam/realmonitor?channel=1&subtype=2",  # Example CCTV
    "cam2": "rtsp://<ip>:<port>/h264_ulaw.sdp",  # Example IP Webcam
    # Add more cameras as needed
}
```

---

## Using with Tablet (IP Webcam)

1. **Connect** the tablet to your local Wi-Fi network (ensure it is on the same network as the server).
2. **Install and open** the IP Webcam app on the tablet.
3. **Start the server** in the app.
4. **Note** the IP address and port number displayed (in HTTP format).
5. **Convert** to RTSP format:  
   `rtsp://<ip>:<port>/h264_ulaw.sdp`
6. **Edit** `main.py` to add your camera feed as shown above.
7. **Access the web UI**:  
   - `http://<server-ip>:8000/cam1`  
   - `http://<server-ip>:8000/cam2`
8. **Leave** the IP Webcam app running in the background.
9. **Open** your preferred browser and enter the website URL.

---

## Using with CCTV (RTSP Camera)

1. **Set up your CCTV camera** and ensure it is connected to your local network.
2. **Obtain the RTSP stream URL** from your camera's settings or user manual. It usually looks like:
   - `rtsp://<username>:<password>@<camera-ip>:<port>/path`
   - Example: `rtsp://admin:password@192.168.1.100:554/stream1`
3. **Edit the `main.py` file** to add your CCTV RTSP stream(s) to the `CAMERA_URLS` dictionary.
4. **Save the changes** to `main.py`.
5. **Run the application** as above.
6. **Access the web UI** from any device on the same network:
   - `http://<server-ip>:8000/cam1`
   - Replace `<server-ip>` with the IP address of the computer running this project.
7. **View the live CCTV feed and face recognition results** in your browser.

---

## Web Interface

- Visit `http://<server-ip>:8000/` to see the camera selection page.
- Visit `http://<server-ip>:8000/<cam_id>` to view a specific camera feed.
- The UI displays the live video, recognized face, and top predictions.
- Users can provide feedback on recognition accuracy, which is logged for later analysis.

---

## Log Files

- **`recognition_log.json`**: Stores all recognition events with timestamps and confidence scores.
- **`selection_log.json`**: Stores user feedback on recognition results, including:
  - `name`: User image file name or "None"
  - `clicked_position`: Which position's button was clicked
  - `top_prediction`: The top predicted name
  - `correct`: Whether the selection was correct
  - `timestamp`: When the feedback was given
  - `camera_id`: Which camera the feedback was for

---

## Evaluating Performance

Use `eval_performance.py` to analyze recognition accuracy:

```bash
python eval_performance.py --date YYYY-MM-DD
```

- Shows overall and per-camera accuracy for a given date.
- If no date is provided, you can enter one interactively.

---

## Notes

- The face database is built from images in the `db/` folder at startup.
- Failed face detections are listed in `failed_faces.txt`.
- The system uses GPU acceleration if available (CUDA), otherwise falls back to CPU.
- You can add or update user images in `db/` and restart the server to refresh the database.

---
