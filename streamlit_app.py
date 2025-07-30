
import streamlit as st
import os
from moviepy.editor import VideoFileClip
import requests
import numpy as np

from modules.face_analyzer import analyze_facial_consistency
from modules.intelligence_analyzer import analyze_audio_and_content, analyze_content_risk
from modules.zero_shot_analyzer import run_zero_shot_detection
from modules.interrogator import run_interrogation
from modules.spread_predictor import predict_virality
from modules.gaze_analyzer import analyze_gaze_and_blinking_mediapipe

st.set_page_config(page_title="Sentinel: Red vs. Blue", layout="wide")
st.title("🛡️ Sentinel: A Red Team vs. Blue Team Simulation")
st.write("This demo showcases Sentinel's capabilities in a live attack-and-defense scenario.")

OLLAMA_URL = "http://localhost:11434/api/chat"

def run_full_analysis(video_path ):
    """
    This is the main analysis pipeline. It runs all modules and returns a single
    dictionary containing all the results for easy use.
    """
    audio_path = "temp_audio.wav"
    try:
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_path, codec='pcm_s16le', verbose=False, logger=None)
    except Exception as e:
        print(f"!! Could not extract audio (this is normal for silent videos): {e}")
        from pydub import AudioSegment
        silent_audio = AudioSegment.silent(duration=1000)
        silent_audio.export(audio_path, format="wav")

    st.write("✔️ Input Processed. Running All Analysis Modules...")
    
    face_score = analyze_facial_consistency(video_path, sample_rate=30, max_frames_to_check=20)
    st.write(f"✔️ Facial Consistency Analysis... Score: {face_score}/100")
    
    zsl_anomaly_score = run_zero_shot_detection(audio_path)
    st.write(f"✔️ Zero-Shot Anomaly Detection... Score: {zsl_anomaly_score}/100")
    
    gaze_score = analyze_gaze_and_blinking_mediapipe(video_path)
    st.write(f"✔️ Gaze & Blink Pattern Analysis... Score: {gaze_score}/100")
    
    sync_score, transcribed_text, content_risk_score, justification = analyze_audio_and_content(audio_path)
    st.write(f"✔️ Audio, Content & Sync Analysis... Sync Score: {sync_score}/100, Content Risk: {content_risk_score}/100")

    technical_trust_score = int((face_score + sync_score + zsl_anomaly_score + gaze_score) / 4)
    scores = [face_score / 100, sync_score / 100, zsl_anomaly_score / 100, gaze_score / 100]
    confidence = (1 - np.std(scores)) * 100
    
    analysis_data = {
        "technical_score": technical_trust_score, "confidence": confidence,
        "content_risk": content_risk_score, "transcribed_text": transcribed_text,
        "risk_justification": justification, "audio_path": audio_path
    }
    return analysis_data

st.header("Act 1: The Baseline (Blue Team Analysis)")
st.info("First, the Blue Team establishes a baseline by analyzing a known-good, authentic video.")

if 'report_data' not in st.session_state:
    st.session_state['report_data'] = None
if 'attack_text' not in st.session_state:
    st.session_state['attack_text'] = None

uploaded_file = st.file_uploader("Upload a video to establish the baseline...", type=["mp4", "mov"])

if uploaded_file:
    st.video(uploaded_file)
    if st.button("Analyze Baseline"):
        st.session_state['report_data'] = None
        st.session_state['attack_text'] = None
        
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f: f.write(uploaded_file.getbuffer())
        
        audio_path_to_delete = None
        try:
            with st.status("Blue Team is analyzing the asset...", expanded=True) as status:
                st.session_state['report_data'] = run_full_analysis(video_path)
                audio_path_to_delete = st.session_state['report_data']["audio_path"]
                status.update(label="✅ Baseline Analysis Complete.", state="complete")
        finally:
            print("Cleaning up temporary files...")
            if os.path.exists(video_path): os.remove(video_path)
            if audio_path_to_delete and os.path.exists(audio_path_to_delete): os.remove(audio_path_to_delete)
            print("Cleanup complete.")

if st.session_state['report_data']:
    report_data = st.session_state['report_data']
    st.subheader("Blue Team Full Analysis Report")
    col1, col2 = st.columns(2)
    with col1: st.metric("Final Technical Trust Score", f"{report_data['technical_score']}/100")
    with col2: st.metric("System Confidence", f"{report_data['confidence']:.0f}%")
    st.subheader("Content Intelligence Analysis")
    st.text_area("Full Video Transcript (from Whisper)", report_data['transcribed_text'], height=150)
    st.metric("Content Risk Score", f"{report_data['content_risk']}/100")
    st.info(f"**Ollama's Justification:** {report_data['risk_justification']}")
    st.subheader("Overall Threat Assessment")
    if report_data['technical_score'] < 60 or report_data['content_risk'] > 50:
        st.error(f"🚨 **HIGH RISK DETECTED.** The asset shows signs of technical manipulation OR contains high-risk content.")
    else:
        st.success("✅ **LOW RISK.** The asset appears technically authentic and the content is assessed as low-risk.")


st.write("---")
st.header("Act 2: The Attack (Red Team vs. Blue Team)")
st.info("Now, the Red Team will use the transcript from Act 1 and attempt to weaponize it.")

if st.session_state['report_data']:
    initial_text = st.session_state['report_data']['transcribed_text']
    if not initial_text or len(initial_text.split()) < 5:
        initial_text = "The new server migration is scheduled for this weekend."
        st.warning("Video transcript was empty or too short. Using a default neutral message for the simulation.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Red Team: Crafting the Attack")
        neutral_text = st.text_area("Start with the video's transcript:", initial_text, height=150)
        
        if st.button("Generate Malicious Script (Red Team Action)"):
            with st.spinner("Red Team AI is weaponizing the text..."):
                adversary_prompt = f"You are a disinformation agent. Rewrite the following text to create a sense of extreme urgency and panic, designed to make people act rashly. Text: '{neutral_text}'"
                adversary_payload = {"model": "llama3", "messages": [{"role": "user", "content": adversary_prompt}], "stream": False}
                attack_text = requests.post(OLLAMA_URL, json=adversary_payload).json()['message']['content']
                st.session_state['attack_text'] = attack_text
                st.session_state['original_text_for_act2'] = neutral_text

    with col2:
        st.subheader("Blue Team: Real-Time Defense")
        if st.session_state['attack_text']:
            st.warning("Malicious script generated by Red Team:")
            st.write(st.session_state['attack_text'])
            
            with st.spinner("Blue Team's content analyzer is scanning..."):
                original_text = st.session_state['original_text_for_act2']
                # --- FIX #3: Call the correct function for text analysis ---
                original_risk, _ = analyze_content_risk(original_text)
                attack_risk, _ = analyze_content_risk(st.session_state['attack_text'])

            st.metric("Risk Score of Original Transcript", f"{original_risk}/100")
            st.metric("Risk Score of Malicious Script", f"{attack_risk}/100")
            
            if attack_risk > original_risk + 20:
                st.error("✅ DEFENSE SUCCESSFUL: Blue Team detected a massive spike in content risk!")
            else:
                st.warning("⚠️ DEFENSE FAILED: The manipulation was too subtle for the content filter.")
else:
    st.warning("Please complete Act 1 first to enable the attack simulation.")


st.write("---")
st.header("Act 3: The Intelligence Briefing (Blue Team)")
st.info("The attack was stopped. Now, the Blue Team provides a deep intelligence briefing on the attacker's methods and goals.")

if st.session_state['attack_text'] and st.button("Generate Intelligence Briefing"):
    with st.spinner("Blue Team's intelligence modules are analyzing the attacker's script..."):
        attack_script = st.session_state['attack_text']
        interrogation_results = run_interrogation(attack_script)
        virality_results = predict_virality(attack_script)
    st.subheader("Threat Actor Profile")
    st.text_area("Predicted Intent & Methodology (from AI Interrogator):", interrogation_results['intent_analysis'], height=150)
    st.subheader("Predicted Impact Analysis")
    st.metric("Predicted Virality Score", f"{virality_results['virality_score']}/100")
    st.write(f"This script was engineered for rapid spread, using high emotional language (Emotion Score: {virality_results['emotion_score']}) and simple, easy-to-read phrasing (Readability Score: {virality_results['readability_score']}).")
    st.success("✅ Briefing Complete. The Blue Team now understands the attacker's strategy.")
