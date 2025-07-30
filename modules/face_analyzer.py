# modules/face_analyzer.py (ULTRA OPTIMIZED - "One-Pass" Method)
import cv2
from deepface import DeepFace
import os
import time
import numpy as np
from scipy.spatial.distance import cosine

# Suppress verbose TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def analyze_facial_consistency(video_path, sample_rate=30, max_frames_to_check=30):
    """
    ULTRA-OPTIMIZED version. It makes a single pass over the video to collect all face
    embeddings, then analyzes them in memory. This is dramatically faster.
    """
    print(f"-> [Video Specialist] Running ULTRA-FAST Facial Consistency Analysis...")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("!! Error opening video file")
        return 0

    total_frames_checked = 0
    all_embeddings = [] # We will store all found embeddings here

    frame_id = 0
    start_time = time.time()

    print("--- [Pass 1/2] Extracting face embeddings from video... ---")
    while total_frames_checked < max_frames_to_check:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % sample_rate == 0:
            total_frames_checked += 1
            try:
                # This is the ONLY expensive call we make in the loop
                embedding_objs = DeepFace.represent(
                    img_path=frame,
                    model_name='VGG-Face',
                    enforce_detection=True,
                    detector_backend='retinaface'
                )
                all_embeddings.append(embedding_objs[0]['embedding'])
                print(f"  - Frame {frame_id}: Face found.")
            except ValueError:
                print(f"  - Frame {frame_id}: No face detected.")
                pass
        
        frame_id += 1

    cap.release()
    pass1_time = time.time() - start_time
    print(f"--- [Pass 1/2] Complete. Found {len(all_embeddings)} faces in {pass1_time:.2f} seconds. ---")

    # --- Pass 2: Analyze the collected embeddings (this is extremely fast) ---
    print("--- [Pass 2/2] Analyzing embedding consistency... ---")
    
    if len(all_embeddings) < 2:
        # If we found 0 or 1 face, we can't determine consistency.
        print("-> Not enough faces found to determine consistency.")
        return 75 # Return a neutral score

    first_face_embedding = all_embeddings[0]
    matching_faces = 0
    threshold = 0.4  # Cosine distance threshold for VGG-Face

    for embedding in all_embeddings:
        distance = cosine(embedding, first_face_embedding)
        if distance < threshold:
            matching_faces += 1
            
    consistency_score = int((matching_faces / len(all_embeddings)) * 100)
    
    print(f"-> [Video Specialist] Analysis complete. Consistency: {consistency_score}%")
    return consistency_score
