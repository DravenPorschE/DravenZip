import os
import urllib.request
import zipfile
import sys

def download_vosk_model():
    # Model URL from Vosk website
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    model_filename = "vosk-model-small-en-us-0.15.zip"
    model_dir = "vosk-model-small-en-us-0.15"
    
    print(f"Downloading Vosk model from: {model_url}")
    
    try:
        # Download the model
        urllib.request.urlretrieve(model_url, model_filename)
        print(f"Downloaded: {model_filename}")
        
        # Extract the zip file
        print(f"Extracting {model_filename}...")
        with zipfile.ZipFile(model_filename, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print(f"Model extracted to: {model_dir}")
        
        # Clean up: remove the zip file
        os.remove(model_filename)
        print(f"Removed zip file: {model_filename}")
        
        print("\nModel downloaded successfully!")
        print(f"Path: ./{model_dir}")
        
        return True
        
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

if __name__ == "__main__":
    download_vosk_model()
