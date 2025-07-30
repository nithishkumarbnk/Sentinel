# modules/gaze_analyzer_mediapipe.py
import cv2
import mediapipe as mp
import numpy as np

# --- Setup MediaPipe models (this happens once) ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True, # This is key for getting detailed eye landmarks
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# These are the specific landmark indices for the eyes from MediaPipe's documentation
# You can find a diagram here: https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/face_mesh_connections.py
LEFT_EYE_IDXS = [362, 382, 381, 380, 373, 374, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE_IDXS = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

def calculate_ear_mediapipe(landmarks, eye_idxs, frame_shape ):
    """Calculates the Eye Aspect Ratio (EAR) using MediaPipe landmarks."""
    # Get the coordinates of the eye landmarks
    coords = np.array([(landmarks[i].x * frame_shape[1], landmarks[i].y * frame_shape[0]) for i in eye_idxs])
    
    # The MediaPipe indices for vertical and horizontal points are different from dlib's
    # Vertical distances (approximated)
    A = np.linalg.norm(coords[4] - coords[12])  # Top to bottom
    B = np.linalg.norm(coords[2] - coords[14])  # Inner top to inner bottom
    
    # Horizontal distance
    C = np.linalg.norm(coords[0] - coords[8])   # Left corner to right corner
    
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def analyze_gaze_and_blinking_mediapipe(video_path):
    """
    Analyzes a video to detect unnatural blinking patterns using MediaPipe.
    Returns a Gaze Authenticity Score (0-100).
    """
    print("-> [Add-On] Running Gaze & Blinking Analysis (using MediaPipe)...")
    
    EAR_THRESHOLD = 0.20  # Threshold for MediaPipe might be different, requires tuning
    
    blink_count = 0
    frame_count = 0
    is_blinking = False
    
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame_count += 1
        # Convert the BGR image to RGB and process it with MediaPipe Face Mesh.
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Calculate EAR for both eyes
                left_ear = calculate_ear_mediapipe(face_landmarks.landmark, LEFT_EYE_IDXS, frame.shape)
                right_ear = calculate_ear_mediapipe(face_landmarks.landmark, RIGHT_EYE_IDXS, frame.shape)
                ear = (left_ear + right_ear) / 2.0
                
                # Detect a blink
                if ear < EAR_THRESHOLD:
                    if not is_blinking:
                        blink_count += 1
                        is_blinking = True # Mark that a blink has started
                else:
                    is_blinking = False # Reset the blink state

    cap.release()
    
    # Calculate blinks per minute (BPM)
    fps = 30 # Assume 30 FPS, or get it from cap.get(cv2.CAP_PROP_FPS)
    duration_seconds = frame_count / fps if fps > 0 else 0
    if duration_seconds == 0: return 50
    
    blinks_per_minute = (blink_count / duration_seconds) * 60
    
    # Score based on a normal human blinking rate (15-30 BPM)
    if 10 < blinks_per_minute < 35:
        gaze_score = 95
    elif blinks_per_minute <= 5:
        gaze_score = 10 # Unnaturally low, strong deepfake signal
    else:
        gaze_score = 50 # Outside the normal range
        
    print(f"-> [Add-On] Blinks Per Minute: {blinks_per_minute:.2f}. Gaze Score: {gaze_score}/100")
    return gaze_score
