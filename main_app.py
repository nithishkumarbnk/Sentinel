import streamlit as st
import os
from moviepy.editor import VideoFileClip
import numpy as np
from groq import Groq  # Use Groq API

# --- MODULES (Simulated for this single-file example) ---
# In your actual project, these would be in separate files.

def analyze_facial_consistency(video_path, sample_rate=30, max_frames_to_check=20):
    # This function remains a placeholder as it doesn't use the LLM.
    st.write("... (Simulating facial consistency check)")
    return 85 # Return a sample score

def analyze_gaze_and_blinking_mediapipe(video_path):
    # This function remains a placeholder as it doesn't use the LLM.
    st.write("... (Simulating gaze and blink analysis)")
    return 92 # Return a sample score

def run_zero_shot_detection(audio_path):
    # This function remains a placeholder as it doesn't use the LLM.
    st.write("... (Simulating zero-shot audio anomaly detection)")
    return 78 # Return a sample score

# --- AI-Powered Modules (Now using Groq) ---

def get_ai_response(client, prompt, model="llama3-8b-8192"):
    """A centralized function to call the Groq API."""
    if not client:
        return "Error: AI client not initialized."
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while contacting the AI service: {e}")
        return f"Error: {e}"

def analyze_content_risk(client, text):
    """Analyzes text for risk using the Groq API."""
    if not text or not text.strip():
        return 0, "No text provided for analysis."
    prompt = f"""
    Analyze the following text and assign a risk score from 0 (safe) to 100 (dangerous).
    Consider factors like panic-inducing language, misinformation, hate speech, or calls to violence.
    Justify your score in one sentence.
    Format your response as: Score: [score], Justification: [justification]
    Text: "{text}"
    """
    response = get_ai_response(client, prompt)
    try:
        score_part = response.split("Score:")[1].split(",")[0].strip()
        justification_part = response.split("Justification:")[1].strip()
        return int(score_part), justification_part
    except (IndexError, ValueError):
        return 50, "Could not parse AI response. The content may be unusual."

def analyze_audio_and_content(client, audio_path, transcribed_text):
    """Analyzes content risk from transcribed text."""
    sync_score = 95  # Placeholder for lip-sync score
    content_risk_score, justification = analyze_content_risk(client, transcribed_text)
    return sync_score, content_risk_score, justification

def run_interrogation(client, text):
    """Generates a threat actor profile using the Groq API."""
    prompt = f"""
    You are a threat intelligence analyst. Based on the following malicious script,
    predict the attacker's intent and methodology.
    Script: "{text}"
    """
    intent_analysis = get_ai_response(client, prompt)
    return {"intent_analysis": intent_analysis}

def predict_virality(client, text):
    """Predicts the virality of a script using the Groq API."""
    prompt = f"""
    Analyze the following text for its potential to go viral.
    Provide a virality score (0-100), an emotion score (0-100), and a readability score (0-100).
    Format as: Virality: [score], Emotion: [score], Readability: [score]
    Text: "{text}"
    """
    response = get_ai_response(client, prompt)
    try:
        virality = int(response.split("Virality:")[1].split(",")[0].strip())
        emotion = int(response.split("Emotion:")[1].split(",")[0].strip())
        readability = int(response.split("Readability:")[1].strip())
        return {"virality_score": virality, "emotion_score": emotion, "readability_score": readability}
    except (IndexError, ValueError):
        return {"virality_score": 50, "emotion_score": 50, "readability_score": 50}

# --- STREAMLIT APP ---

st.set_page_config(page_title="Sentinel: Red vs. Blue", layout="wide")
st.title("🛡️ Sentinel: A Red Team vs. Blue Team Simulation")
st.write("This demo showcases Sentinel's capabilities in a live attack-and-defense scenario.")

# --- Initialize Groq Client ---
# It will automatically use the GROQ_API_KEY from your environment variables
try:
    client = Groq()
except Exception as e:
    st.error("Could not initialize Groq client. Please ensure your `GROQ_API_KEY` is set in your environment variables.")
    client = None

def run_full_analysis(video_path):
    """Main analysis pipeline using all modules."""
    audio_path = "temp_audio.wav"
    transcribed_text = "The new server migration is scheduled for this weekend." # Placeholder transcript

    st.write("✔️ Input Processed. Running All Analysis Modules...")
    
    face_score = analyze_facial_consistency(video_path)
    st.write(f"✔️ Facial Consistency Analysis... Score: {face_score}/100")
    
    zsl_anomaly_score = run_zero_shot_detection(audio_path)
    st.write(f"✔️ Zero-Shot Anomaly Detection... Score: {zsl_anomaly_score}/100")
    
    gaze_score = analyze_gaze_and_blinking_mediapipe(video_path)
    st.write(f"✔️ Gaze & Blink Pattern Analysis... Score: {gaze_score}/100")
    
    sync_score, content_risk_score, justification = analyze_audio_and_content(client, audio_path, transcribed_text)
    st.write(f"✔️ Audio, Content & Sync Analysis... Sync Score: {sync_score}/100, Content Risk: {content_risk_score}/100")

    technical_trust_score = int((face_score + sync_score + zsl_anomaly_score + gaze_score) / 4)
    scores = [face_score / 100, sync_score / 100, zsl_anomaly_score / 100, gaze_score / 100]
    confidence = (1 - np.std(scores)) * 100
    
    return {
        "technical_score": technical_trust_score, "confidence": confidence,
        "content_risk": content_risk_score, "transcribed_text": transcribed_text,
        "risk_justification": justification, "audio_path": audio_path
    }

# --- UI LAYOUT ---

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
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f: f.write(uploaded_file.getbuffer())
        
        with st.status("Blue Team is analyzing the asset...", expanded=True) as status:
            st.session_state['report_data'] = run_full_analysis(video_path)
            status.update(label="✅ Baseline Analysis Complete.", state="complete")
        
        if os.path.exists(video_path): os.remove(video_path)

if st.session_state['report_data']:
    report = st.session_state['report_data']
    st.subheader("Blue Team Full Analysis Report")
    col1, col2 = st.columns(2)
    with col1: st.metric("Final Technical Trust Score", f"{report['technical_score']}/100")
    with col2: st.metric("System Confidence", f"{report['confidence']:.0f}%")
    st.subheader("Content Intelligence Analysis")
    st.text_area("Full Video Transcript (Simulated)", report['transcribed_text'], height=150)
    st.metric("Content Risk Score", f"{report['content_risk']}/100")
    st.info(f"**AI Justification:** {report['risk_justification']}")

st.write("---")
st.header("Act 2: The Attack (Red Team vs. Blue Team)")
st.info("Now, the Red Team will use the transcript from Act 1 and attempt to weaponize it.")

if st.session_state['report_data']:
    initial_text = st.session_state['report_data']['transcribed_text']
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Red Team: Crafting the Attack")
        neutral_text = st.text_area("Start with the video's transcript:", initial_text, height=150)
        
        if st.button("Generate Malicious Script (Red Team Action)"):
            with st.spinner("Red Team AI is weaponizing the text..."):
                prompt = f"You are a disinformation agent. Rewrite the following text to create a sense of extreme urgency and panic, designed to make people act rashly. Text: '{neutral_text}'"
                st.session_state['attack_text'] = get_ai_response(client, prompt)
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
