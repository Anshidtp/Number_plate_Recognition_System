import cv2
import sqlite3
import time
import numpy as np
from paddleocr import PaddleOCR
from sort.tracker import SortTracker  

# Initialize OCR and SORT
ocr = PaddleOCR(use_angle_cls=True, lang='en')
tracker = SortTracker(max_age=20, min_hits=3, iou_threshold=0.3)

# Connect to SQLite database
conn = sqlite3.connect("vehicle_data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER,
    plate_text TEXT,
    first_seen REAL,
    last_seen REAL,
    avg_speed REAL
)
""")
conn.commit()

# Placeholder YOLO detector (replace with YOLOv10)
def detect_vehicles(frame):
    # TODO: replace with actual YOLOv10 detections
    # return [[x1, y1, x2, y2, confidence, class_id], ...]
    return []

# Speed estimation helper
pixel_to_meter = 0.05  # scaling factor (depends on camera calibration)

vehicle_memory = {}

cap = cv2.VideoCapture("Sample_Data/carLicence1.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_vehicles(frame)
    if len(detections) > 0:
        dets = np.array([[d[0], d[1], d[2], d[3], d[4]] for d in detections])
    else:
        dets = np.empty((0, 5))

    tracked_objects = tracker.update(dets)

    for x1, y1, x2, y2, track_id in tracked_objects:
        x1, y1, x2, y2, track_id = map(int, [x1, y1, x2, y2, track_id])

        # OCR on detected plate region
        plate_crop = frame[y1:y2, x1:x2]
        result = ocr.ocr(plate_crop, cls=True)
        plate_text = ""
        if result and result[0]:
            plate_text = result[0][0][1][0]

        # Speed calculation
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        timestamp = time.time()

        if track_id not in vehicle_memory:
            vehicle_memory[track_id] = {
                "plate": plate_text,
                "positions": [(cx, cy, timestamp)],
                "first_seen": timestamp,
            }
        else:
            vehicle_memory[track_id]["positions"].append((cx, cy, timestamp))
            vehicle_memory[track_id]["plate"] = plate_text or vehicle_memory[track_id]["plate"]

            if len(vehicle_memory[track_id]["positions"]) >= 2:
                (x_prev, y_prev, t_prev), (x_now, y_now, t_now) = vehicle_memory[track_id]["positions"][-2:]
                dist_pixels = np.sqrt((x_now - x_prev) ** 2 + (y_now - y_prev) ** 2)
                dist_meters = dist_pixels * pixel_to_meter
                dt = t_now - t_prev
                if dt > 0:
                    speed_mps = dist_meters / dt
                    speed_kmph = speed_mps * 3.6
                    vehicle_memory[track_id]["speed"] = speed_kmph

        # Draw on frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id} {plate_text}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save/update in DB
        vehicle = vehicle_memory[track_id]
        cursor.execute("""
        INSERT OR REPLACE INTO vehicles (vehicle_id, plate_text, first_seen, last_seen, avg_speed)
        VALUES (?, ?, ?, ?, ?)
        """, (
            track_id,
            vehicle["plate"],
            vehicle["first_seen"],
            timestamp,
            vehicle.get("speed", 0.0),
        )
        )
        conn.commit()

    cv2.imshow("Vehicle Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
