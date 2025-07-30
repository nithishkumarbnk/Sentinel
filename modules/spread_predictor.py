# modules/spread_predictor.py
import requests
# You might need to run: pip install textstat
import textstat

OLLAMA_URL = "http://localhost:11434/api/chat"

def predict_virality(text ):
    """Calculates a 'Virality Score' based on text features."""
    print("-> [Predictor] Predicting Spread Potential...")
    
    # Feature 1: Emotional Intensity (via LLM)
    emotion_prompt = f"On a scale from 0 (calm) to 100 (highly emotional), rate the emotional intensity of this text. Respond with only the number. Text: '{text}'"
    emotion_payload = {"model": "llama3", "messages": [{"role": "user", "content": emotion_prompt}], "stream": False}
    try:
        emotion_response = requests.post(OLLAMA_URL, json=emotion_payload).json()['message']['content']
        emotional_score = int(''.join(filter(str.isdigit, emotion_response)))
    except:
        emotional_score = 50 # Default

    # Feature 2: Readability (lower score = harder to read = less viral)
    # Flesch reading ease score (higher is better)
    readability_score = textstat.flesch_reading_ease(text)

    # Combine into a final Virality Score (simple weighted average for demo)
    # We normalize readability (max ~100) and emotion (max 100)
    virality_score = int((emotional_score * 0.6) + (readability_score * 0.4))
    
    return {"virality_score": virality_score, "emotion_score": emotional_score, "readability_score": readability_score}
