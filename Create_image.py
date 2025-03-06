import cv2
import os
import time
import uuid

# Define the path to save images
IMAGES_PATH = 'images/collectedimages'  # Use relative path for local execution

# Define labels and number of images
labels = ['hello', 'thank you', 'yes', 'no', 'sorry']
number_imgs = 15

# Create directory if not exists
os.makedirs(IMAGES_PATH, exist_ok=True)

for label in labels:
    label_path = os.path.join(IMAGES_PATH, label)
    os.makedirs(label_path, exist_ok=True)  # Create subdirectory for each label
    
    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        print(f"Error: Could not access webcam for '{label}'")
        continue  # Skip to next label if camera fails

    print(f'📸 Collecting images for "{label}"...')
    time.sleep(3)  # Shorter delay before starting

    for imgnum in range(number_imgs):
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Warning: Failed to capture image {imgnum+1} for '{label}'")
            continue

        # Save image with a unique name
        imgname = os.path.join(label_path, f"{label}_{uuid.uuid1()}.jpg")
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(1)  # Short delay between captures

        # Stop capturing if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release camera after each label

cv2.destroyAllWindows()  # Close OpenCV windows
print("✅ Image collection complete!")
