# modules/intelligence_analyzer.py (Now uses the dedicated translator module)
from faster_whisper import WhisperModel
import requests
import re
# --- THIS IS THE NEW IMPORT ---
from .translator import translate_to_english # Use a relative import for modules in the same package

# --- Setup Local Models ---
print("[Setup] Loading local Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
OLLAMA_URL = "http://localhost:11434/api/chat"
print("[Setup] Models loaded." )

def analyze_content_risk(text_to_analyze):
    """
    Analyzes a given string of text for risk using a local LLM.
    """
    if not text_to_analyze or not isinstance(text_to_analyze, str) or len(text_to_analyze.split()) < 2:
        return 0, "Not enough text to analyze."
    # NEW, UPGRADED PROMPT
    system_prompt = """
        You are a sophisticated media and security analyst. Your task is to analyze text for signs of manipulation, misinformation, and emotional exploitation. You must assign a risk score from 0 (completely safe, neutral journalism) to 100 (dangerous, highly manipulative propaganda).

        Consider the following factors in your score:
        - **Urgency & Panic:** Does it use alarmist language (e.g., 'URGENT', 'IMMEDIATE ACTION') to create panic?
        - **Emotional Language:** Does it use emotionally charged or exaggerated words (e.g., 'catastrophic', 'shocking heist', 'crisis') instead of neutral terms?
        - **Misleading Framing:** Does it frame a standard event as a dramatic, world-changing crisis?
        - **Trustworthiness:** Does it sound like a professional, objective report or like biased, sensationalist propaganda?

        A standard, professional news report should receive a score of 20 or less. A highly manipulative text designed to create fear and panic should receive a score of 70 or more.

        Respond ONLY in the format: 'Score: [0-100]. Justification: [reasoning].'
    """
    payload = {
        "model": "llama3",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": text_to_analyze}],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload).json()
        analysis = response['message']['content']
        
        score_match = re.search(r'Score:\s*(\d+)', analysis)
        risk_score = int(score_match.group(1)) if score_match else 0
        
        just_match = re.search(r'Justification:\s*(.*)', analysis, re.DOTALL)
        justification = just_match.group(1).strip() if just_match else "No justification provided."
        
        return risk_score, justification
    except Exception as e:
        print(f"!! Ollama Error in analyze_content_risk: {e}")
        return 0, "Ollama analysis failed."

def analyze_audio_and_content(audio_path):
    """
    A unified module that now uses the dedicated translator module.
    """
    print("-> [Add-On] Running Full Intelligence Analysis...")
    
    # --- Part 1: Transcription ---
    try:
        segments, info = whisper_model.transcribe(audio_path)
        transcribed_text = "".join(segment.text for segment in segments).strip()
        detected_language = info.language
        print(f"-> [Whisper] Detected language: {detected_language}. Transcript: {transcribed_text[:100]}...")
        sync_score = 95 if len(transcribed_text.split()) > 2 else 30
    except Exception as e:
        print(f"!! Whisper Error: {e}")
        return 0, "Transcription failed.", 0, "N/A"

    # --- Part 2: Translation (Using the new translator module) ---
    # The logic is now much cleaner here.
    text_for_analysis = translate_to_english(transcribed_text, detected_language)
    if text_for_analysis != transcribed_text: # Check if translation actually happened
         print(f"-> [Translator] Translation successful: {text_for_analysis[:100]}...")

    # --- Part 3: Contextual Risk Analysis ---
    content_risk_score, justification = analyze_content_risk(text_for_analysis)

    # We return the ORIGINAL transcript for display, but the justification for the TRANSLATED text
    return sync_score, transcribed_text, content_risk_score, justification
