from ultralytics import YOLO
import cv2
import os

# Load your trained model
model = YOLO("C:/Users/m272514/Desktop/roboflow_dataset_v2/runs/detect/train/weights/best.pt")

# Set video source (0, 1, etc.)
source = "C:/Users/m272514/Videos/Hacksaw_ridge.mp4"
cap = cv2.VideoCapture(source)

# Output folder
output_folder = 'saved_frames'
os.makedirs(output_folder, exist_ok=True)

# Track seen person IDs
seen_ids = set()
frame_id = 0

# Set labels you want to flag
people_labels = ["Human", "Human feet", "Person", "face", "person", "person dataset - v1 2023-11-16 1-49am"]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Make a copy for drawing boxes on
    display_frame = frame.copy()

    # Perform tracking
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)

    # Get tracking boxes
    boxes = results[0].boxes

    if boxes.id is not None:
        for i in range(len(boxes.id)):
            track_id = int(boxes.id[i])
            class_id = int(boxes.cls[i])

            if model.names[class_id] in people_labels and track_id not in seen_ids:
                seen_ids.add(track_id)
                save_path = os.path.join(output_folder, f'person_{track_id:06d}.jpeg')
                # Save raw frame without bounding boxes
                cv2.imwrite(save_path, frame)
                print(f"Saved frame for person {track_id} at frame {frame_id}")

            # Draw bounding boxes and labels on display frame only
            box = boxes.xyxy[i].cpu().numpy().astype(int)
            x1, y1, x2, y2 = box
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{model.names[class_id]} ID:{track_id}"
            cv2.putText(display_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    frame_id += 1
    cv2.imshow("Tracking with boxes", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
