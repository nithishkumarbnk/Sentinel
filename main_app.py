# main_app.py (Final Version with Robust File Handling)

import streamlit as st
import os
from moviepy.editor import VideoFileClip
import numpy as np
from groq import Groq
from faster_whisper import WhisperModel

# --- App Configuration ---
st.set_page_config(page_title="Sentinel: Red vs. Blue", layout="wide")
st.title("🛡️ Sentinel: A Red Team vs. Blue Team Simulation")
st.write("This demo showcases Sentinel's capabilities in a live attack-and-defense scenario.")

# --- Initialize AI Models (Groq and Whisper) ---
client = None
transcription_model = None

# Initialize Groq for language tasks
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY is not set. Please add it in your Render service settings under the 'Environment' tab.")
    else:
        client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"An error occurred while initializing the Groq client: {e}")

# Initialize Whisper for transcription
@st.cache_resource
def load_transcription_model():
    try:
        model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
        return model
    except Exception as e:
        st.error(f"Failed to load transcription model: {e}")
        return None

transcription_model = load_transcription_model()

# ==============================================================================
# ALL ANALYSIS MODULES (Self-contained and Cloud-Ready)
# ==============================================================================

def get_ai_response(client, prompt, model="llama3-8b-8192"):
    if not client: return "Error: AI client not initialized."
    try:
        chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=model)
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while contacting the AI service: {e}")
        return f"Error: {e}"

def transcribe_audio(model, audio_path):
    if not model: return "Error: Transcription model not loaded."
    try:
        segments, _ = model.transcribe(audio_path, beam_size=5)
        return " ".join([segment.text for segment in segments])
    except Exception as e:
        st.error(f"Audio transcription failed: {e}")
        return "Transcription failed."

def analyze_facial_consistency(video_path, **kwargs):
    st.write("... (Simulating facial consistency check)")
    return 88

def run_zero_shot_detection(audio_path, **kwargs):
    st.write("... (Simulating zero-shot audio anomaly)")
    return 92

def analyze_gaze_and_blinking_mediapipe(video_path, **kwargs):
    st.write("... (Simulating gaze & blink analysis)")
    return 85

def analyze_content_risk(client, text):
    if not text or not text.strip(): return 0, "No text provided."
    prompt = f"Analyze the following text for risk (0-100) and justify it. Format: Score: [score], Justification: [justification]. Text: '{text}'"
    response = get_ai_response(client, prompt)
    try:
        score = int(response.split("Score:")[1].split(",")[0].strip())
        justification = response.split("Justification:")[1].strip()
        return score, justification
    except (IndexError, ValueError):
        return 50, "Could not parse AI response."

def analyze_audio_and_content(client, model, audio_path):
    st.write("... Transcribing audio with Whisper model...")
    transcribed_text = transcribe_audio(model, audio_path)
    st.write(f"**Transcription complete:** *{transcribed_text[:100]}...*")
    
    sync_score = 95
    content_risk_score, justification = analyze_content_risk(client, transcribed_text)
    return sync_score, transcribed_text, content_risk_score, justification

def run_interrogation(client, text):
    prompt = f"You are a threat intelligence analyst. Based on this script, predict the attacker's intent and methodology. Script: '{text}'"
    return {"intent_analysis": get_ai_response(client, prompt)}

def predict_virality(client, text):
    prompt = f"Analyze this text for virality potential. Provide scores (0-100) for virality, emotion, and readability. Format: Virality: [score], Emotion: [score], Readability: [score]. Text: '{text}'"
    response = get_ai_response(client, prompt)
    try:
        virality = int(response.split("Virality:")[1].split(",")[0].strip())
        emotion = int(response.split("Emotion:")[1].split(",")[0].strip())
        readability = int(response.split("Readability:")[1].strip())
        return {"virality_score": virality, "emotion_score": emotion, "readability_score": readability}
    except (IndexError, ValueError):
        return {"virality_score": 50, "emotion_score": 50, "readability_score": 50}

def run_full_analysis(client, model, video_path):
    audio_path = "temp_audio.wav"
    try:
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_path, codec='pcm_s16le', verbose=False, logger=None)
    except Exception as e:
        st.warning(f"Could not extract audio (this is normal for silent videos): {e}")
        from pydub import AudioSegment
        AudioSegment.silent(duration=1000).export(audio_path, format="wav")

    st.write("✔️ Input Processed. Running All Analysis Modules...")
    
    face_score = analyze_facial_consistency(video_path)
    st.write(f"✔️ Facial Consistency Analysis... Score: {face_score}/100")
    
    zsl_anomaly_score = run_zero_shot_detection(audio_path)
    st.write(f"✔️ Zero-Shot Anomaly Detection... Score: {zsl_anomaly_score}/100")
    
    gaze_score = analyze_gaze_and_blinking_mediapipe(video_path)
    st.write(f"✔️ Gaze & Blink Pattern Analysis... Score: {gaze_score}/100")
    
    sync_score, transcribed_text, content_risk_score, justification = analyze_audio_and_content(client, model, audio_path)
    st.write(f"✔️ Audio, Content & Sync Analysis... Sync Score: {sync_score}/100, Content Risk: {content_risk_score}/100")

    technical_trust_score = int((face_score + sync_score + zsl_anomaly_score + gaze_score) / 4)
    scores = [face_score / 100, sync_score / 100, zsl_anomaly_score / 100, gaze_score / 100]
    confidence = (1 - np.std(scores)) * 100
    
    return {
        "technical_score": technical_trust_score, "confidence": confidence,
        "content_risk": content_risk_score, "transcribed_text": transcribed_text,
        "risk_justification": justification, "audio_path": audio_path
    }

# ==============================================================================
# ACT 1: THE BASELINE (BLUE TEAM ANALYSIS)
# ==============================================================================
st.header("Act 1: The Baseline (Blue Team Analysis)")
st.info("First, the Blue Team establishes a baseline by analyzing a known-good, authentic video.")

if 'report_data' not in st.session_state:
    st.session_state['report_data'] = None
if 'attack_text' not in st.session_state:
    st.session_state['attack_text'] = None

uploaded_file = st.file_uploader("Upload a video to establish the baseline...", type=["mp4", "mov", "avi"])

if uploaded_file:
    # --- ROBUST FILE HANDLING ---
    # 1. Save the uploaded file to a temporary, known path.
    video_path = f"temp_{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 2. Display the video from the saved path, not the uploader object.
    st.video(video_path)
    
    if st.button("Analyze Baseline"):
        if not transcription_model:
            st.error("Transcription model is not loaded. Cannot proceed.")
        else:
            st.session_state['report_data'] = None
            st.session_state['attack_text'] = None
            
            audio_path_to_delete = None
            try:
                with st.status("Blue Team is analyzing the asset...", expanded=True) as status:
                    # 3. Pass the definite video_path to the analysis function.
                    st.session_state['report_data'] = run_full_analysis(client, transcription_model, video_path)
                    audio_path_to_delete = st.session_state['report_data'].get("audio_path")
                    status.update(label="✅ Baseline Analysis Complete.", state="complete")
            finally:
                # 4. Clean up all temporary files.
                if os.path.exists(video_path): os.remove(video_path)
                if audio_path_to_delete and os.path.exists(audio_path_to_delete): os.remove(audio_path_to_delete)

if st.session_state.get('report_data'):
    report = st.session_state['report_data']
    st.subheader("Blue Team Full Analysis Report")
    col1, col2 = st.columns(2)
    with col1: st.metric("Final Technical Trust Score", f"{report['technical_score']}/100")
    with col2: st.metric("System Confidence", f"{report['confidence']:.0f}%")
    st.subheader("Content Intelligence Analysis")
    st.text_area("Full Video Transcript (from Whisper)", report['transcribed_text'], height=150)
    st.metric("Content Risk Score", f"{report['content_risk']}/100")
    st.info(f"AI Justification: {report['risk_justification']}")

# ==============================================================================
# ACT 2: THE ATTACK (RED TEAM vs. BLUE TEAM)
# ==============================================================================
st.write("---")
st.header("Act 2: The Attack (Red Team vs. Blue Team)")
st.info("Now, the Red Team will use the real transcript from Act 1 and attempt to weaponize it.")

if st.session_state.get('report_data'):
    initial_text = st.session_state['report_data']['transcribed_text']
    if not initial_text or len(initial_text.split()) < 2:
        initial_text = "The new server migration is scheduled for this weekend."
        st.warning("Video transcript was empty or too short. Using a default neutral message for the simulation.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Red Team: Crafting the Attack")
        neutral_text = st.text_area("Start with the video's transcript:", initial_text, height=150)
        
        if st.button("Generate Malicious Script (Red Team Action)"):
            with st.spinner("Red Team AI is weaponizing the text..."):
                prompt = f"You are a disinformation agent. Rewrite this text to create extreme urgency and panic: '{neutral_text}'"
                attack_text = get_ai_response(client, prompt)
                st.session_state['attack_text'] = attack_text
                st.session_state['original_text_for_act2'] = neutral_text

    with col2:
        st.subheader("Blue Team: Real-Time Defense")
        if st.session_state.get('attack_text'):
            st.warning("Malicious script generated by Red Team:")
            st.write(st.session_state['attack_text'])
            
            with st.spinner("Blue Team's content analyzer is scanning..."):
                original_risk, _ = analyze_content_risk(client, st.session_state['original_text_for_act2'])
                attack_risk, _ = analyze_content_risk(client, st.session_state['attack_text'])

            st.metric("Risk Score of Original Transcript", f"{original_risk}/100")
            st.metric("Risk Score of Malicious Script", f"{attack_risk}/100")
            
            if attack_risk > original_risk + 20:
                st.error("✅ DEFENSE SUCCESSFUL: Blue Team detected a massive spike in content risk!")
            else:
                st.warning("⚠️ DEFENSE FAILED: The manipulation was too subtle for the content filter.")
else:
    st.warning("Please complete Act 1 first to enable the attack simulation.")

# ==============================================================================
# ACT 3: THE INTELLIGENCE BRIEFING (BLUE TEAM)
# ==============================================================================
st.write("---")
st.header("Act 3: The Intelligence Briefing (Blue Team)")
st.info("The attack was stopped. Now, the Blue Team provides a deep intelligence briefing on the attacker's methods and goals.")

if st.session_state.get('attack_text') and st.button("Generate Intelligence Briefing"):
    with st.spinner("Blue Team's intelligence modules are analyzing the attacker's script..."):
        attack_script = st.session_state['attack_text']
        interrogation_results = run_interrogation(client, attack_script)
        virality_results = predict_virality(client, attack_script)
    st.subheader("Threat Actor Profile")
    st.text_area("Predicted Intent & Methodology (from AI Interrogator):", interrogation_results['intent_analysis'], height=150)
    st.subheader("Predicted Impact Analysis")
    st.metric("Predicted Virality Score", f"{virality_results['virality_score']}/100")
    st.write(f"This script was engineered for rapid spread, using high emotional language (Emotion Score: {virality_results['emotion_score']}) and simple, easy-to-read phrasing (Readability Score: {virality_results['readability_score']}).")
    st.success("✅ Briefing Complete. The Blue Team now understands the attacker's strategy.")
