import cv2
from ultralytics import YOLO
import os
from datetime import datetime

# Load YOLOv8 model (you can use 'yolov8n.pt' for a faster, smaller model)
model = YOLO("yolov8n.pt")  # or 'yolov8s.pt', 'yolov8m.pt', etc.

# Set up video source: 0 for webcam or provide a file path or stream URL
video_source = 0  # Change to a filename like 'video.mp4' if needed
cap = cv2.VideoCapture(video_source)

# Output folder for frames containing people
output_dir = "people_frames"
os.makedirs(output_dir, exist_ok=True)

frame_count = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)[0]

    # Filter for 'person' class (class ID 0 in COCO dataset)
    person_detections = [det for det in results.boxes.data if int(det[5]) == 0]

    if person_detections:
        # Save frame if at least one person detected
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(output_dir, f"frame_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1
        print(f"[Saved] {filename}")

    # Optional: Show the frame (with bounding boxes)
    annotated_frame = results.plot()
    cv2.imshow("YOLOv8 Person Detection", annotated_frame)

    # Press 'q' to exit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
print(f"Processed {frame_count} frames. Saved {saved_count} with people.")
