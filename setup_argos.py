# setup_argos.py
import argostranslate.package
import argostranslate.settings
import os
import requests
import sys

print("--- Starting Robust Argos Translate Setup ---")

# Define the language codes we need
FROM_CODE = "en"
TO_CODE = "te"

try:
    # --- Step 1: Update the package index ---
    print("Updating package index...")
    argostranslate.package.update_package_index()

    # --- Step 2: Find the correct package ---
    print(f"Searching for package to translate from '{FROM_CODE}' to '{TO_CODE}'...")
    available_packages = argostranslate.package.get_available_packages()
    
    package_to_install = next(
        filter(
            lambda x: x.from_code == FROM_CODE and x.to_code == TO_CODE,
            available_packages
        ),
        None
    )

    if not package_to_install:
        print(f"❌ ERROR: Could not find the required language package in the index.", file=sys.stderr)
        sys.exit(1)

    # --- Step 3: Download the package from its official URL ---
    download_url = package_to_install.download_url
    package_path = f"temp_package_{FROM_CODE}_{TO_CODE}.argosmodel"
    
    print(f"Found package. Downloading from official URL: {download_url}")
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(package_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print("Download complete.")

    # --- Step 4: Install the package from the downloaded file ---
    print(f"Installing package from {package_path}...")
    argostranslate.package.install_from_path(package_path)
    print("✅ Package installed successfully.")

except Exception as e:
    print(f"❌ ERROR: An unexpected error occurred during Argos Translate setup: {e}", file=sys.stderr)
    sys.exit(1)

finally:
    # --- Step 5: Clean up the downloaded file ---
    if os.path.exists(package_path):
        os.remove(package_path)
        print(f"Cleaned up temporary file: {package_path}")

print("--- Argos Translate Setup Complete ---")
