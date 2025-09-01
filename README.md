# 🚗 Vehicle Number Plate Recognition System

![Demo](demo.gif)

## 📌 Project Overview
This project implements a **Vehicle number plate detection and recognition system** using:

- **YOLOv10** 🧠 for license plate detection  
- **PaddleOCR** 🔍 for optical character recognition (OCR) of detected plates  
- **SQLite** 💾 for storing recognized license plates in a structured database  
- **JSON logs** 📑 for cumulative and interval-based data storage  

The system processes a video stream, detects license plates, extracts text, and stores the results in both **JSON** files and an **SQL database**.  

---

## ⚙️ How It Works
1. **Detect license plates using YOLOv10**  
   The trained YOLOv10 model detects bounding boxes around license plates in the video.  

2. **Recognize text on the plates using PaddleOCR**  
   PaddleOCR extracts text from the detected license plate region.  

3. **Save results every 20 seconds**  
   All unique license plates detected within a 20-second interval are saved into a **JSON file**.  

4. **Maintain cumulative JSON logs**  
   A new JSON file is generated for each interval while also updating a cumulative JSON file that retains all previous detections without duplication.  

5. **Save results into SQLite database**  
   Each recognized license plate with its start and end timestamps is stored in a lightweight, disk-based **SQLite database**, making it easy to query later.  

---

## ⚡ Features
✅ Real-time license plate detection using YOLOv10  
✅ Text recognition with PaddleOCR  
✅ 20-second interval-based JSON logs  
✅ Cumulative JSON storage of all detections  
✅ Automatic SQLite database storage of results  
✅ Video overlay with bounding boxes and detected text  

## Backend Setup

1. Clone the Repository
    ```bash
    git clone https://github.com/your-username/vehicle-number-plate-detection.git
    cd vehicle-number-plate-detection
    ```

2. Create and activate virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

    ```

3. Install Dependencies

    Make sure you have Python 3.9+ installed.

    ```bash
    pip install -r requirements.txt
    ```

4. Setup Database

    Create the required SQLite table before running:
    ```bash
    python database.py
    ```

5. Run the script with:

    ```bash
    python app.py
    ```

Controls:

- Press 1 → Exit video stream

Outputs:

- JSON files in json/ directory

- Data saved into licensePlatesDatabase.db

### Example JSON Output:
``` bash
{
  "Start Time": "2025-09-01T12:00:00",
  "End Time": "2025-09-01T12:00:20",
  "License Plate": [
    "KL07AB1234",
    "KL55XY9876"
  ]
}

```

## 🚀 Future Improvements:

- Add Flask/FastAPI backend for live API access

- Improve OCR accuracy with character post-processing

- Vehicle tracking across multiple frames and cameras

- Speed tracking of detected vehicles for traffic monitoring and law enforcement

- Deploy as a real-time surveillance system




