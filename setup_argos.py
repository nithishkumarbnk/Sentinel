# setup_argos.py
import argostranslate.package
import argostranslate.settings
import os

print("--- Starting Argos Translate Setup ---")

# Ensure the directory exists
argos_home = "/usr/local/share/argos-translate"
os.makedirs(argos_home, exist_ok=True)
argostranslate.settings.home_dir = argos_home

print("Updating package index...")
argostranslate.package.update_package_index()

print("Searching for language packages: en -> te")
available_packages = argostranslate.package.get_available_packages()

# Find the package for English to Telugu translation
package_to_install = next(
    filter(
        lambda x: x.from_code == "en" and x.to_code == "te",
        available_packages
    ),
    None
)

if package_to_install:
    print("Found package. Installing...")
    package_to_install.install()
    print("✅ Package installed successfully.")
else:
    print("⚠️ Warning: Could not find the 'en' to 'te' translation package.")

print("--- Argos Translate Setup Complete ---")
