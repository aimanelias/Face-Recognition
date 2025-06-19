- buffalo_l is the model pack containing the face detection and face recognition model
- db folder contains the images of all MIMOS employees
- failed_faces.txt lists the employee images that failed being converted to embeddings
- To run the project, run on main.py

selection_log.json:
- if name : None or button : None, means no correct face recognized
- if name not None and button : 1, means face recognized correctly
- if name not None and button: 2 or 3, means the face recognized but not very accurate
- name indicates employee image file name
- button indicates which position's button is clicked
- camera_id indicates the location device that the user clicked on

Source code files:
- camera.py
- face_recognition.py
- main.py
- templates/index.html

Dependencies install:
pip install opencv-python opencv-python-headless insightface fastapi uvicorn jinja2 numpy torch torchvision python-dotenv aiofiles

To run on tablet:
**make sure tablet connected to mimoswifi_5g network
1. Open the ip webcam app
2. Scroll down ip webcam app and click "Start server"
3. Now, you will see the ip address and port number displayed in http form
4. Change to this form rtsp://ip:port number/h264_ulaw.sdp
5. Insert the rtsp into this in main.py
    # Define camera feed sources
    CAMERA_URLS = {
        "cam1": "rtsp://admin:Mm813669@10.8.11.29/cam/realmonitor?channel=1&subtype=2",
        "cam2": "rtsp://10.1.106.81:8080/h264_ulaw.sdp",
    }
    To access website:
    10.1.39.77:8000/cam1
    10.1.39.77:8000/cam2
6. Leave ip webcam app running on background, open "Fully Kiosk Browser" app (can access on Chrome too)
7. Enter the website url in the app and run.

"C:\Users\hyper\Documents\Face Recognition Multiple Feed UI v2"
- this folder is the actual folder you will be working on

"C:\Users\hyper\Documents\Face Recognition Multiple Feed-build version"
- this folder is for dynamic file paths in code, but was facing issue to convert to .exe file

