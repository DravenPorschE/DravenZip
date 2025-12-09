import json
from rapidfuzz import fuzz

# Load intents JSON once
intents = json.loads(open("intents.json").read())

def get_intent(text, intents_json=intents, threshold=60):
    """
    Returns the predicted intent tag for the given text using fuzzy matching.
    Returns 'none' string if no match is strong enough.
    """
    max_score = 0
    matched_tag = "none"

    text_lower = text.lower()

    for intent in intents_json["intents"]:
        for pattern in intent.get("patterns", []):
            score = fuzz.ratio(text_lower, pattern.lower())
            if score > max_score:
                max_score = score
                matched_tag = intent["tag"]

    if max_score < threshold:
        return "none"

    return matched_tag


# -----------------------------
# WHILE LOOP TO TEST INPUTS
# -----------------------------
# print("Type something to test intent detection (type 'quit' to exit).")
# while True:
#     user_input = input("> ")
#     if user_input.lower() == "quit":
#         break

#     intent_tag = get_intent(user_input)
#     print(intent_tag)  # Will print the intent tag or "none"
