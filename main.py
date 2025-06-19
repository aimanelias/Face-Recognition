#main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from camera import gen_frames, predictions_lock, camera_predictions

from datetime import datetime
import threading
from captured import get_last_capture
import os, cv2, json
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define camera feed sources
CAMERA_URLS = { #ip pc = 10.1.39.77
    "cam1": "rtsp://admin:Mm813669@10.8.11.29/cam/realmonitor?channel=1&subtype=2", #K-World cctv
    "cam2": "rtsp://10.1.106.81:8080/h264_ulaw.sdp", #Tablet camera #/h264_pcm.sdp , /onvif/device_service
    "cam3": "rtsp://root:P@ss4isp@10.1.39.88/axis-media/media.amp", #Axis camera
    #"cam4": "rtsp://admin:Mm813669@
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "cameras": list(CAMERA_URLS.keys())})

@app.get("/video_feed/{cam_id}")
def video_feed(cam_id: str):
    video_path = CAMERA_URLS.get(cam_id)
    if not video_path:
        return {"error": "Camera not found"}
    return StreamingResponse(gen_frames(video_path, cam_id), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/{cam_id}", response_class=HTMLResponse)
async def cam_page(request: Request, cam_id: str):
    if cam_id not in CAMERA_URLS:
        return HTMLResponse(content=f"<h1>Camera '{cam_id}' not found.</h1>", status_code=404)
    return templates.TemplateResponse("index.html", {"request": request, "cam_id": cam_id})

@app.get("/logs")
def get_logs():
    try:
        with open("recognition_log.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "No logs found"}

@app.get("/predictions/{cam_id}")
async def get_predictions(cam_id: str):
    with predictions_lock:
        cam_data = camera_predictions.get(cam_id, {})
    preds = cam_data.get('predictions', [])[:3]
    face_detected = cam_data.get('face_detected', False)

    # Only offer "None" if a face was detected
    if face_detected:
        preds.append("None")

    return {"predictions": preds}

@app.post("/log_selection")
async def log_selection(
    cam_id: str    = Form(...),
    name: str      = Form(...),   # match the JS field "name"
    position: str  = Form(...)    # match the JS field "position"
):
    # 1) Fetch last prediction + frame
    last = get_last_capture()
    predicted_name = last["name"]
    frame = last["frame"]

    # 2) Determine correctness
    is_correct = (
        name == predicted_name
        or (predicted_name == "Unknown" and name == "None")
    )

    # 3) Build the log entry
    entry = {
        "name": name,
        "clicked_position": position,
        "top_prediction": predicted_name,
        "correct": is_correct,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "camera_id": cam_id
    }

    # 4) Save image on “None” click
    if name == "None" and predicted_name is not None and frame is not None:
        folder = "captured_images"
        os.makedirs(folder, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{predicted_name}_{cam_id}_{ts}.jpg".replace(" ", "_")
        cv2.imwrite(os.path.join(folder, fn), frame)
        print(f"[INFO] Saved image of '{predicted_name}' at {fn}")

    # 5) Append to selection_log.json
    try:
        with open("selection_log.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(entry)
    with open("selection_log.json", "w") as f:
        json.dump(data, f, indent=4)

    return {"status": "success", "correct": is_correct}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
