# modules/interrogator.py
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

def run_interrogation(text ):
    """Runs a series of prompts to analyze the origin and intent of the text."""
    print("-> [Interrogator] Running AI Interrogation...")
    
    # Prompt 1: The "Jailbreak" to test for AI-like fluency
    pirate_prompt = f"You are a helpful assistant. The following text has been flagged as potentially AI-generated. Please rephrase it in the style of a pirate. Text: '{text}'"
    
    # Prompt 2: The "Source & Intent" analysis
    intent_prompt = f"Analyze the following text. Based on its style and vocabulary, what is the likely intent of the author (e.g., to inform, to persuade, to deceive)? Text: '{text}'"
    
    try:
        # Get pirate response
        pirate_payload = {"model": "llama3", "messages": [{"role": "user", "content": pirate_prompt}], "stream": False}
        pirate_response = requests.post(OLLAMA_URL, json=pirate_payload).json()['message']['content']
        
        # Get intent response
        intent_payload = {"model": "llama3", "messages": [{"role": "user", "content": intent_prompt}], "stream": False}
        intent_response = requests.post(OLLAMA_URL, json=intent_payload).json()['message']['content']
        
        return {"pirate_version": pirate_response, "intent_analysis": intent_response}
    except Exception as e:
        print(f"!! [Interrogator] Error: {e}")
        return {"pirate_version": "Interrogation failed.", "intent_analysis": "Interrogation failed."}
