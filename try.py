from typecast_api import text_to_speech_api
from ai_talk import getSekaiResponse
from get_intent import getSekaiIntent
import json

current_mood = "happy"
message = "How are you today bob?"
#ai_response = getSekaiResponse("Who invented cars?", "angry")


if __name__ == "__main__":
    API_KEY = "__pltMzLwjRtejoHYcjCEi984cBgKa6qMU6EiSkEs2Xne "  # Replace with your actual API key
    
    # Test text
    #test_text = ai_response

    ai_intent = getSekaiIntent(message)

    print(ai_intent)
    data = json.loads(ai_intent)  # Parse JSON string to dictionary
    command_value = data["command"]  # Access the value

    ai_response = getSekaiResponse(message, current_mood)

    # Generate speech
    audio_file = text_to_speech_api(ai_response, API_KEY)
    
    if audio_file and os.path.exists(audio_file):
        print(f"\n🎵 To play the audio on Raspberry Pi:")
        print(f"   aplay {audio_file}")
        
        # Optional: Play it automatically
        import subprocess
        try:
            subprocess.run(['aplay', audio_file], check=True)
        except:
            print("   Could not play audio automatically")