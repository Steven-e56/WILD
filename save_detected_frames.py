from ultralytics import YOLO
import cv2
import os

# Load your trained model
model = YOLO('C:/Users/m272514/Desktop/roboflow_dataset_v2/runs/detect/train/weights/best.pt')

# Set your source: 0 for webcam, or path to video file
source = 0  # or 'your_video.mp4'

# Folder to save frames
output_folder = 'saved_frames'
os.makedirs(output_folder, exist_ok=True)

# Define the target class names you want to save frames for
target_classes = ['Human', 'Human feet', 'Person', 'face', 'person']  # change this list to your classes

# Map class names to class IDs from model.names
class_name_to_id = {name: i for i, name in enumerate(model.names)}
target_class_ids = [class_name_to_id[c] for c in target_classes if c in class_name_to_id]

# Open video capture
cap = cv2.VideoCapture(source)
frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    # Get detected class IDs in this frame
    detected_ids = [int(box.cls[0]) for box in results[0].boxes]

    # Check if any target class is detected
    if any(cls_id in target_class_ids for cls_id in detected_ids):
        # Save frame as image
        frame_path = os.path.join(output_folder, f'frame_{frame_id:06d}.jpeg')
        cv2.imwrite(frame_path, frame)
        print(f"Saved frame {frame_id} containing target objects.")

    frame_id += 1

    # Optional: display the frame live (press 'q' to quit)
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
