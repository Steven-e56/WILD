from ultralytics import YOLO
import cv2
import os

# Load your trained model
model = YOLO("C:/Users/m272514/Desktop/roboflow_dataset_v2/runs/detect/train/weights/best.pt")

# Set video source: 0 for webcam or provide video file path
source = 0
cap = cv2.VideoCapture(source)

# Output folder
output_folder = 'saved_frames'
os.makedirs(output_folder, exist_ok=True)

# Track seen person IDs
seen_ids = set()
frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform tracking using DeepSORT
    results = model.track(frame, persist=True, tracker="deep_sort.yaml", verbose=False)

    # Get tracking boxes
    boxes = results[0].boxes
    if boxes.id is not None:
        for i in range(len(boxes.id)):
            track_id = int(boxes.id[i])
            class_id = int(boxes.cls[i])

            # Only save the first frame for each unique person
            if model.names[class_id] == 'person' and track_id not in seen_ids:
                seen_ids.add(track_id)
                save_path = os.path.join(output_folder, f'person_{track_id:06d}.jpeg')
                cv2.imwrite(save_path, frame)
                print(f"Saved frame for person {track_id} at frame {frame_id}")

    frame_id += 1
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
