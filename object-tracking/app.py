import cv2
from ultralytics import YOLO

# Load a pretrained YOLOv8 model (downloads automatically the first time you run this)
model = YOLO("yolov8n.pt")  # "n" = nano, the smallest/fastest version

print("Starting webcam... press 'q' to quit.")

# Open the default webcam (0). Change to 1 if you have multiple cameras.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam.")
    exit()

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to grab frame.")
        break

    # Run detection + tracking on this frame using YOLO's built-in ByteTrack
    results = model.track(frame, persist=True, verbose=False)

    # Draw bounding boxes, labels, and tracking IDs on the frame
    annotated_frame = results[0].plot()

    cv2.imshow("Object Detection and Tracking - Press 'q' to quit", annotated_frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()