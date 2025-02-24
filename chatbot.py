import spacy
from transformers import MarianMTModel, MarianTokenizer

# Load Calamancy (NLP for Tagalog)
nlp = spacy.load("tl_calamancy_md")

# Load Helsinki-NLP for English-to-Tagalog translation
model_name = "Helsinki-NLP/opus-mt-en-tl"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Tokenizer function (FSA-based)
def tokenize(text):
    words = []
    curr_word = ""
    for i in text:
        if i.isalpha() or i in "'-":
            curr_word += i
        else:
            if curr_word:
                words.append(curr_word)
                curr_word = ""
    if curr_word:
        words.append(curr_word)
    return words

# English-to-Tagalog Translation
def translate_en_to_tl(text):
    batch = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**batch)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    return translated_text.strip().lower()

# Response Dictionary (Tagalog)
responses = {
    "kamusta": "Ayos lang ako, ikaw?",
    "kumusta": "Ayos lang ako, ikaw?",
    "sino": "Ako si Tagbot, ang chatbot mo!",
    "salamat": "Walang anuman!",
    "paalam": "Paalam! Ingat ka!"
}

# Generate chatbot response
def chatbot_response(user_input):
    # Detect English and translate
    if any(word in user_input.lower() for word in ["hello", "how", "what", "is", "thank", "you"]):
        print("Detected English. Translating to Tagalog...")
        user_input = translate_en_to_tl(user_input)
        print("Translated Text:", user_input)

    # Tokenize translated text
    tokens = tokenize(user_input)

    # Check for a matching response
    for word in tokens:
        if word in responses:
            return responses[word]

    return "Pasensya na, hindi ko naintindihan. Maaari mo bang ipaliwanag?"

# Test chatbot
user_input = "Thank you!"
response = chatbot_response(user_input)
print(f"Bot: {response}")
