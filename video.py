import cv2
import os
from deepface import DeepFace
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Define image directory and similarity threshold
image_directory = "C:/Users/NHUT HIEU/Downloads/QLNS/hinh"
threshold = 0.6

# Resize dimensions
resize_dim = (128, 128)

# Function to load and resize images from directory
def load_images_from_directory(directory, size):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".png")):
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path)
            if img is not None:
                img_resized = cv2.resize(img, size)
                img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
                images.append(img_rgb)
    return images

# Load and resize images from directory
images = load_images_from_directory(image_directory, resize_dim)
print(f"Loaded {len(images)} images.")

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

frame_rate = 10
prev = 0

while True:
    time_elapsed = time.time() - prev
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break

    if time_elapsed > 1.0 / frame_rate:
        prev = time.time()

        # Resize webcam frame
        frame_resized = cv2.resize(frame, resize_dim)
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        # Process the webcam frame against the loaded images
        for img_rgb in images:
            result = DeepFace.verify(frame_rgb, img_rgb, enforce_detection=False)
            if result["verified"] and result["distance"] >= threshold:
                similarity = result["distance"]
                toado = result["facial_areas"]["img2"]
                x, y, w, h = toado["x"], toado["y"], toado["w"], toado["h"]
                # Adjust coordinates to original frame size
                x = int(x * (frame.shape[1] / resize_dim[0]))
                y = int(y * (frame.shape[0] / resize_dim[1]))
                w = int(w * (frame.shape[1] / resize_dim[0]))
                h = int(h * (frame.shape[0] / resize_dim[1]))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                print(f"Similarity: {similarity}, Coordinates: x={x}, y={y}, w={w}, h={h}")
                print(f"Đúng! Ảnh từ webcam được chấp nhận.")

                # Capture and save the recognized face image
                save_directory = "C:/Users/NHUT HIEU/Downloads/QLNS/hinhchup"
                if not os.path.exists(save_directory):
                    os.makedirs(save_directory)

                save_path = os.path.join(save_directory, f"captured_image_{time.strftime('%Y%m%d_%H%M%S')}.jpg")
                cv2.imwrite(save_path, frame[y:y+h, x:x+w])
                print(f"Ảnh khuôn mặt đã được lưu vào: {save_path}")

        # Process the loaded images against the webcam frame
        for img_rgb in images:
            result = DeepFace.verify(img_rgb, frame_rgb, enforce_detection=False)
            if result["verified"] and result["distance"] >= threshold:
                similarity = result["distance"]
                toado = result["facial_areas"]["img1"]
                x, y, w, h = toado["x"], toado["y"], toado["w"], toado["h"]
                # Adjust coordinates to original frame size
                x = int(x * (frame.shape[1] / resize_dim[0]))
                y = int(y * (frame.shape[0] / resize_dim[1]))
                w = int(w * (frame.shape[1] / resize_dim[0]))
                h = int(h * (frame.shape[0] / resize_dim[1]))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                print(f"Similarity: {similarity}, Coordinates: x={x}, y={y}, w={w}, h={h}")
                print(f"Đúng! Ảnh từ tập dữ liệu được chấp nhận.")

    # Display the original frame with rectangles
    cv2.imshow("Webcam", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()