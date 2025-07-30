# modules/zero_shot_analyzer.py
import numpy as np
from sklearn.ensemble import IsolationForest
import librosa # We need this for audio feature extraction

# --- "Training" our Anomaly Detector ---
# In a real system, you would load audio from many trusted, real videos.
# For this demo, we will simulate a "normal" audio profile.
# This represents the "knowledge" of what real human speech looks like.
print("[Setup] Training Zero-Shot Anomaly Detector...")
# Let's create some dummy "normal" feature vectors.
# These features could be things like pitch, energy, zero-crossing rate, etc.
# A real implementation would have thousands of these from real videos.
X_train_normal = np.random.rand(100, 5) * np.array([0.5, 1.0, 0.2, 0.8, 0.4])
anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
anomaly_detector.fit(X_train_normal)
print("[Setup] Anomaly Detector is ready.")
# -----------------------------------------

def extract_audio_features(audio_path):
    """Extracts a simple feature vector from an audio file."""
    try:
        y, sr = librosa.load(audio_path)
        # Extract a few simple features
        chroma_stft = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
        rmse = np.mean(librosa.feature.rms(y=y))
        spec_cent = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spec_bw = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
        
        return np.array([[chroma_stft, rmse, spec_cent, spec_bw, zero_crossing_rate]])
    except Exception as e:
        print(f"!! Could not extract audio features: {e}")
        return None

def run_zero_shot_detection(audio_path):
    """
    Analyzes audio features to detect anomalies (a form of Zero-Shot Learning).
    Returns an anomaly score (0-100), where a low score is more anomalous.
    """
    print("-> [Add-On] Running Zero-Shot Anomaly Detection...")
    features = extract_audio_features(audio_path)
    if features is None:
        return 50 # Neutral score if feature extraction fails

    # The model returns +1 for inliers (normal) and -1 for outliers (anomalous).
    prediction = anomaly_detector.predict(features)
    # The score_samples gives a raw anomaly score. Lower is more anomalous.
    anomaly_score_raw = anomaly_detector.score_samples(features)

    # Let's convert this to a simple 0-100 score for our dashboard.
    # This is a simplified conversion for the demo.
    if prediction[0] == -1:
        # It's an anomaly, give it a low score
        final_score = 25
    else:
        # It's normal, give it a high score
        final_score = 90
        
    print(f"-> [Add-On] Zero-Shot Anomaly Score: {final_score}/100")
    return final_score
