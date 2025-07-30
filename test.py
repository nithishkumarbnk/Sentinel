# test_deepface.py
from deepface import DeepFace
import cv2
import os

# Suppress verbose TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("--- DeepFace Standalone Test ---")
print("This test will check if the required models can be downloaded and loaded correctly.")
print("The first run might take several minutes as it downloads models. Please be patient.")

# Use a simple, clear image for the test. You can use any jpg/png image of a face.
# If you don't have one, save a clear picture of a face as 'test_face.jpg' in your project folder.
test_image_path = "test_face.jpg" 

# Check if the test image exists
if not os.path.exists(test_image_path):
    print(f"!! ERROR: Test image not found at '{test_image_path}'.")
    print("!! Please save a clear image of a face as 'test_face.jpg' in this directory and run again.")
else:
    try:
        print("\n[Step 1] Attempting to build the VGG-Face model...")
        # This command forces DeepFace to build and cache the model.
        model = DeepFace.build_model('VGG-Face')
        print("✅ VGG-Face model built successfully.")

        print("\n[Step 2] Attempting to run face detection with 'retinaface'...")
        # This will force the download and loading of the retinaface model.
        face_objs = DeepFace.extract_faces(
            img_path=test_image_path,
            detector_backend='retinaface'
        )
        print(f"✅ 'retinaface' detector worked! Found {len(face_objs)} face(s).")
        
        print("\n--- TEST COMPLETE ---")
        print("If you see this message, all models were downloaded and loaded correctly.")
        print("You can now try running your main Streamlit application again.")

    except Exception as e:
        print(f"\n!! AN ERROR OCCURRED DURING THE TEST: {e}")
