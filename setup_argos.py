# setup_argos.py
import argostranslate.package
import argostranslate.settings
import os
import requests
import sys

print("--- Starting Argos Translate Setup ---")

# Define the package URL and the local path to save it
PACKAGE_URL = "https://s3.amazonaws.com/argos-translate/packages/translate-en_te-2_0.argosmodel"
PACKAGE_PATH = "translate-en_te.argosmodel"

try:
    # --- Step 1: Download the package file ---
    print(f"Downloading package from {PACKAGE_URL}..." )
    with requests.get(PACKAGE_URL, stream=True) as r:
        r.raise_for_status()
        with open(PACKAGE_PATH, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print("Download complete.")

    # --- Step 2: Install the package from the downloaded file ---
    print(f"Installing package from {PACKAGE_PATH}...")
    argostranslate.package.install_from_path(PACKAGE_PATH)
    print("✅ Package installed successfully.")

except Exception as e:
    print(f"❌ ERROR: Failed to set up Argos Translate package. Error: {e}", file=sys.stderr)
    sys.exit(1) # Exit with an error code to fail the build if setup fails

finally:
    # --- Step 3: Clean up the downloaded file ---
    if os.path.exists(PACKAGE_PATH):
        os.remove(PACKAGE_PATH)
        print("Cleaned up downloaded package file.")

print("--- Argos Translate Setup Complete ---")
