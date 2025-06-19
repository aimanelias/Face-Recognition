#face_recognition.py
import os, cv2, json
import numpy as np
from datetime import datetime
from insightface.app import FaceAnalysis
import torch

# Device check
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {DEVICE}")

EMPLOYEE_FOLDER = r"C:\Users\hyper\Documents\Face Recognition Multiple Feed UI v2\db"
LOG_FILE = "recognition_log.json"

# Initialize InsightFace
face_app = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider'])
face_app.prepare(ctx_id=0)

def load_employee_images(folder_path):
    db = {}
    failed = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, file)
            name = os.path.splitext(file)[0]
            img = cv2.imread(path)

            faces = face_app.get(img)
            if faces:
                db[name] = (faces[0].normed_embedding, img)
            else:
                failed.append(file)

    print(f"Loaded {len(db)} employees successfully.")
    print(f"Failed to extract faces from {len(failed)} images.")

    if failed:
        with open("failed_faces.txt", "w") as f:
            for file in failed:
                f.write(file + "\n")
        print("Saved failed filenames to failed_faces.txt")

    return db


EMPLOYEE_DB = load_employee_images(EMPLOYEE_FOLDER)
print(f"Loaded {len(EMPLOYEE_DB)} employees from {EMPLOYEE_FOLDER}")

def get_top_predictions(face_embedding, top_n=3):
    matches = []
    for name, (stored_emb, _) in EMPLOYEE_DB.items():
        sim = np.dot(face_embedding, stored_emb)
        matches.append((name, sim))
    
    # Sort by similarity score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    
    # Get matches above threshold
    valid_matches = [match for match in matches if match[1] > 0.4][:top_n]
    return [(name, float(round(conf, 4))) for name, conf in valid_matches]
            
def recognize(face_embedding):
    best_match = "Unknown"
    best_score = 0.4
    for name, (stored_emb, _) in EMPLOYEE_DB.items():
        sim = np.dot(face_embedding, stored_emb)
        if sim > best_score:
            best_score = sim
            best_match = name
    confidence = float(round(best_score, 4))  # Convert to native Python float
    return best_match, EMPLOYEE_DB.get(best_match, (None, None))[1], confidence

def log_recognition(name, confidence):
    entry = {
        "name": name,
        "confidence": confidence,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    if not data or data[-1]["name"] != name:
        data.append(entry)
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=4)

def detect_faces(frame):
    return face_app.get(frame)


