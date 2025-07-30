# ---

---

title: Sentinel-PRO
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false

---

# ---

# 🛡️ Project Sentinel-PRO

**Sentinel-PRO is a sophisticated, multi-modal AI-powered threat intelligence platform...**
(The rest of your README content follows here )

# 🛡️ Project Sentinel-PRO

#myself

**Sentinel-PRO is a sophisticated, multi-modal AI-powered threat intelligence platform designed to detect, analyze, and counteract deepfakes and misinformation in real-time.**

This project moves beyond simple detection by providing a comprehensive, 360-degree analysis of media assets. It examines not only their **technical integrity** (the "how" ) but also their **contextual content** (the "what"). The system is presented as an interactive "Red Team vs. Blue Team" simulation, which demonstrates both its defensive capabilities in analyzing suspicious media and its intelligence capabilities in deconstructing AI-powered propaganda attacks.

---

## ✨ Core Features

- **Multi-Modal Analysis:** Simultaneously analyzes video, audio, and text to form a holistic assessment.
- **Technical Forensics:** Detects deepfakes using facial consistency, gaze/blink patterns, and audio anomalies.
- **Content Intelligence:** Transcribes and analyzes the _meaning_ of the spoken content to assess its risk.
- **Local & Private:** Utilizes a full stack of local AI models (Ollama, Whisper, Argos Translate) to ensure no user data is sent to the cloud.
- **Multilingual:** Capable of transcribing and translating content from multiple languages before analysis.
- **Adversarial Simulation:** Features a unique "Red Team vs. Blue Team" demo to showcase its defensive and analytical capabilities against AI-generated propaganda.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running.
- The `llama3` model pulled via `ollama pull llama3`.
- (For non-English analysis) The required language packs for Argos Translate.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/Sentinel-PRO.git
   cd Sentinel-PRO
   ```

2. **Create and activate a Python virtual environment:**

   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **(First-time setup for Argos Translate )** If you plan to analyze non-English videos, you need to install the language packs. Run this command in your terminal:

   ```bash
   python -c "import argostranslate.package; argostranslate.package.update_package_index(); available_packages = argostranslate.package.get_available_packages(); package_to_install = next(filter(lambda x: x.from_code == 'te' and x.to_code == 'en', available_packages)); package_to_install.install()"
   ```

   _(Note: This example installs the Telugu (`te`) to English (`en`) pack. Change the `from_code` as needed.)_

### Running the Application

Once the installation is complete, launch the Streamlit application:

```bash
streamlit run app.py
```
