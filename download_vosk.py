import os
import urllib.request
import zipfile
import sys
import shutil

def download_vosk_model():
    # Model URL from Vosk website
    model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
    model_filename = "vosk-model-en-us-0.22-lgraph.zip"
    model_dir = "vosk-model-en-us-0.22-lgraph"
    
    print(f"Downloading Vosk model from: {model_url}")
    
    try:
        # Download the model
        urllib.request.urlretrieve(model_url, model_filename)
        print(f"Downloaded: {model_filename}")
        
        # Extract the model
        print(f"Extracting {model_filename}...")
        with zipfile.ZipFile(model_filename, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print(f"Model extracted to: {model_dir}")
        
        # Clean up: remove the zip file
        os.remove(model_filename)
        print(f"Removed zip file: {model_filename}")
        
        print("\nModel downloaded successfully!")
        print(f"Path: ./{model_dir}")
        
        # Now process the additional zip files
        process_additional_zips()
        
        return True
        
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

def process_additional_zips():
    """Process and delete the additional zip files"""
    zip_files = [
        "angry_results.zip",
        "happy_results.zip", 
        "voices_angry.zip",
        "voices_happy.zip",
        "weather_assets.zip",
        "sekai_faces.zip"  # Added this line
    ]
    
    print("\n" + "="*50)
    print("Processing additional zip files...")
    print("="*50)
    
    for zip_file in zip_files:
        if os.path.exists(zip_file):
            try:
                print(f"\nProcessing: {zip_file}")
                
                # Extract the zip file
                print(f"  Extracting {zip_file}...")
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(".")
                print(f"  ✓ Extracted successfully")
                
                # Remove the zip file
                os.remove(zip_file)
                print(f"  ✓ Removed: {zip_file}")
                
            except Exception as e:
                print(f"  ✗ Error processing {zip_file}: {e}")
        else:
            print(f"\nSkipping: {zip_file} (not found)")
    
    # Verify extracted directories
    print("\n" + "="*50)
    print("Verifying extracted directories...")
    print("="*50)
    
    directories_to_check = [
        "angry_results",
        "happy_results",
        "voices_angry", 
        "voices_happy",
        "weather_assets",
        "sekai_faces"  # Added this line
    ]
    
    for directory in directories_to_check:
        if os.path.exists(directory):
            # Count files in directory
            try:
                files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
                print(f"✓ {directory}: {len(files)} files")
                
                # For sekai_faces, list the files if it's empty or has few files
                if directory == "sekai_faces" and len(files) < 2:
                    print(f"  Warning: sekai_faces should contain at least happy.jpg and angry.jpg")
                    if files:
                        print(f"  Found: {', '.join(files)}")
                    
            except Exception as e:
                print(f"✗ {directory}: Error reading directory - {e}")
        else:
            print(f"✗ {directory}: Directory not found")
    
    print("\n✓ All zip files processed successfully!")

def check_required_directories():
    """Check if all required directories exist and have files"""
    required_dirs = {
        "vosk-model-small-en-us-0.15": "Vosk speech recognition model",
        "angry_results": "Angry result audio files",
        "happy_results": "Happy result audio files",
        "voices_angry": "Angry voice audio files",
        "voices_happy": "Happy voice audio files",
        "weather_assets": "Weather icon images",
        "sekai_faces": "Sekai face images"  # Already included, but keeping for clarity
    }
    
    print("\n" + "="*50)
    print("Checking all required directories...")
    print("="*50)
    
    all_ok = True
    
    for dir_name, description in required_dirs.items():
        if os.path.exists(dir_name):
            # Count files in directory
            try:
                files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]
                if files:
                    print(f"✓ {dir_name}: {len(files)} files ({description})")
                    
                    # Special check for sekai_faces
                    if dir_name == "sekai_faces":
                        # Check for required image files
                        has_happy = any('happy' in f.lower() for f in files)
                        has_angry = any('angry' in f.lower() for f in files)
                        
                        if has_happy and has_angry:
                            print(f"  ✓ sekai_faces has both happy and angry images")
                        else:
                            print(f"  ⚠ sekai_faces missing: ", end="")
                            if not has_happy:
                                print("happy.jpg ", end="")
                            if not has_angry:
                                print("angry.jpg ", end="")
                            print()
                            all_ok = False
                else:
                    print(f"⚠ {dir_name}: Directory exists but is EMPTY ({description})")
                    all_ok = False
            except Exception as e:
                print(f"✗ {dir_name}: Error reading directory - {e}")
                all_ok = False
        else:
            print(f"✗ {dir_name}: NOT FOUND ({description})")
            all_ok = False
    
    return all_ok

def cleanup_empty_zip_files():
    """Remove any remaining zip files to keep the directory clean"""
    print("\n" + "="*50)
    print("Cleaning up any remaining zip files...")
    print("="*50)
    
    # List of zip files we should clean up (including the model zip if it still exists)
    files_removed = 0
    
    # First, check for specific zip files
    specific_zips = [
        "vosk-model-small-en-us-0.15.zip",
        "angry_results.zip",
        "happy_results.zip", 
        "voices_angry.zip",
        "voices_happy.zip",
        "weather_assets.zip",
        "sekai_faces.zip"
    ]
    
    for zip_file in specific_zips:
        if os.path.exists(zip_file):
            try:
                os.remove(zip_file)
                print(f"  Removed: {zip_file}")
                files_removed += 1
            except Exception as e:
                print(f"  Could not remove {zip_file}: {e}")
    
    # Also clean up any other zip files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.lower().endswith('.zip'):
                file_path = os.path.join(root, file)
                # Skip if we already processed it above
                if file not in specific_zips:
                    try:
                        os.remove(file_path)
                        print(f"  Removed: {file}")
                        files_removed += 1
                    except Exception as e:
                        print(f"  Could not remove {file}: {e}")
    
    if files_removed > 0:
        print(f"\n✓ Removed {files_removed} zip file(s)")
    else:
        print("✓ No zip files to remove")

def create_sekai_faces_if_missing():
    """Create a basic sekai_faces directory if it's completely missing"""
    sekai_faces_dir = "sekai_faces"
    
    if not os.path.exists(sekai_faces_dir):
        print(f"\n{sekai_faces_dir} directory not found. Creating basic structure...")
        
        try:
            os.makedirs(sekai_faces_dir, exist_ok=True)
            print(f"✓ Created directory: {sekai_faces_dir}")
            
            # Create a README file explaining what should be there
            readme_content = """# Sekai Faces Directory

This directory should contain images of Sekai's face with different emotions.

Required files:
- happy.jpg or happy.JPG - Sekai's happy face
- angry.jpg or angry.JPG - Sekai's angry face

Optional files:
- Any other emotion images (sad.jpg, surprised.jpg, etc.)

Note: The program will work with these basic colored fallbacks until you add real images.
"""
            
            with open(os.path.join(sekai_faces_dir, "README.txt"), "w") as f:
                f.write(readme_content)
            
            print("✓ Created README.txt with instructions")
            print("\n⚠ Please add happy.jpg and angry.jpg images to this directory.")
            print("  The program will use colored fallbacks until real images are added.")
            
            return True
            
        except Exception as e:
            print(f"✗ Error creating {sekai_faces_dir}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("="*50)
    print("SEKAI PROJECT SETUP SCRIPT")
    print("="*50)
    
    # First, check current directory structure
    print("\nChecking current setup...")
    current_status = check_required_directories()
    
    # Check specifically for sekai_faces and create if missing
    if not os.path.exists("sekai_faces"):
        create_sekai_faces_if_missing()
    
    if not current_status:
        print("\nSome directories are missing or empty. Running setup...")
        
        # Ask for confirmation
        response = input("\nDo you want to download and extract required files? (y/n): ")
        
        if response.lower() == 'y':
            # Download Vosk model and process other zips
            success = download_vosk_model()
            
            if success:
                # Final cleanup
                cleanup_empty_zip_files()
                
                # Final check
                print("\n" + "="*50)
                print("SETUP COMPLETE")
                print("="*50)
                check_required_directories()
                
                # Check sekai_faces again
                if os.path.exists("sekai_faces"):
                    files = [f for f in os.listdir("sekai_faces") if os.path.isfile(os.path.join("sekai_faces", f))]
                    if files:
                        print(f"\n✅ sekai_faces has {len(files)} files:")
                        for file in files[:5]:  # Show first 5 files
                            print(f"  - {file}")
                        if len(files) > 5:
                            print(f"  ... and {len(files)-5} more")
                    else:
                        print("\n⚠ sekai_faces directory is empty. Please add happy.jpg and angry.jpg images.")
                else:
                    create_sekai_faces_if_missing()
                
                print("\n✅ Setup complete!")
                print("You can now run the main Sekai program.")
            else:
                print("\n❌ Setup failed. Please check your internet connection.")
        else:
            print("\nSetup cancelled.")
    else:
        print("\n✅ All required directories are present.")
        print("No setup needed.")
        
        # Still offer to process any zip files that might exist
        zip_files_exist = any(os.path.exists(zip_file) for zip_file in [
            "angry_results.zip",
            "happy_results.zip", 
            "voices_angry.zip",
            "voices_happy.zip",
            "weather_assets.zip",
            "sekai_faces.zip"  # Added this line
        ])
        
        if zip_files_exist:
            response = input("\nFound some zip files. Do you want to extract and remove them? (y/n): ")
            if response.lower() == 'y':
                process_additional_zips()
                cleanup_empty_zip_files()
        
        # Check sekai_faces specifically
        if os.path.exists("sekai_faces"):
            files = [f for f in os.listdir("sekai_faces") if os.path.isfile(os.path.join("sekai_faces", f))]
            happy_files = [f for f in files if 'happy' in f.lower()]
            angry_files = [f for f in files if 'angry' in f.lower()]
            
            if not happy_files:
                print("\n⚠ Warning: No 'happy' image found in sekai_faces directory")
                print("  Please add a file named happy.jpg, happy.JPG, or similar")
            
            if not angry_files:
                print("⚠ Warning: No 'angry' image found in sekai_faces directory")
                print("  Please add a file named angry.jpg, angry.JPG, or similar")
