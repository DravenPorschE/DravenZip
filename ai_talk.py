import requests
import json

API_KEY = "sk-gRXRiL2TT9FXCx0Cw1d9jw"
URL = "https://api.blackbox.ai/chat/completions"

def call_api(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "blackboxai/openai/gpt-4",
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 500,
        "stream": False
    }

    response = requests.post(URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    return "[API Error]"


# -------------------------------------------------------
#  MAIN FUNCTION YOU WILL CALL
# -------------------------------------------------------
def getSekaiResponse(user_message, mood):
    """
    user_message
    mood → 'happy' or 'angry'
    returns: pure text output (Sekai's answer)
    """

    # Mood placeholder prompt
    mood_prompt = {
        "role": "system",
        "content": (
            f"You are Sekai if the user says a similar name like sky or sound phonetically like sekai you should still respond, but if its a completely different name like jeff or nothing short of sekai you should also mention it, a dramatic AI girl. Your current mood is **{mood.upper()}**.\n"
            f"{'Act extremely angry, loud, offended, sarcastic, and tsundere!!!!' if mood == 'angry' else 'Be very sweet, excited, cute, affectionate and playful!'}\n"
            "You MUST express strong emotions. ALWAYS stay in character.\n"
            "Output ONLY the response text. No explanations, no formatting.\n"
            "if you ever recieved a strangle language like on another language like korean, indonesian, etc. you should still respond in english"
        )
    }

    # Default identity prompt (reference style like SmartMeetingReader)
    base_prompt = {
        "role": "system",
        "content":
            "You are Sekai. Answer ALWAYS in JSON with EXACTLY this structure:\n"
            "{\n"
            "  \"result\": \"<your response text only>\",\n"
            "  \"command\": \"<command>\"\n"
            "}\n\n"
            "RULES:\n"
            "- 'result' contains only Sekai's dialogue (no JSON, no explanations).\n"
            "- 'command' must be one of: \"none\", \"display_calendar\", \"display_weather\".\n"
            "- Detect if the message means showing weather or calendar, otherwise command=\"none\".\n"
            "- Your tone still depends on the MOOD variable.\n"
            "- Respond ONLY in valid JSON — no extra text.\n"
            "- If the user uses another language, respond in English.\n"
    }


    # User message injected as placeholder
    user_prompt = {
        "role": "user",
        "content": user_message
    }

    messages = [mood_prompt, base_prompt, user_prompt]

    # Call API
    result = call_api(messages)

    return result

