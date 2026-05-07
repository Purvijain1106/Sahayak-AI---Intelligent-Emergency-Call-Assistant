import re

INCIDENT_WORDS = {
    "accident": ["accident", "takra", "crash", "takra gaya", "gaadi takra"],
    "fire": ["fire", "aag", "jal raha", "aag lag gayi"],
    "violence": ["attack", "maar", "fight", "maar peet","chor", "thief", "khatra", "danger", "goli", "gunshot"],
    "medical": ["khoon", "blood", "dard", "pain", "saans", "breath", "behosh", "unconscious", "chot"],
}

PANIC_WORDS = ["help", "save", "urgent", "please", "jaldi", "bachao", "madad"]


BOOSTERS= {"bahut", "bohot", "jyada", "zyada", "bilkul", "kafi", "extreme","bhayanak", "sakht", "tezi", "ekdam", "turt", "abhi", "khud"}
EMOTION_SETS = {
    "PANIC": [
        "bachao", "bhago", "bachaoo", "jaldi", "turant", "fauran", "dar", 
        "darr", "ghabrahat", "dhak", "dhak", "chillana", "shor", "bhagdada", 
        "cheekh", "bachaao", "emergency", "urgent", "marr", "marne", "bachna"
    ],

    "DANGER": [
        "khatra", "aag", "chor", "bandook", "goli", "chaku", "hoon", "khoon", 
        "hamla", "piche", "daku", "gunda", "maar", "pitai", "bomb", "dhamaka", 
        "current", "bijli", "zeher", "zahar", "jaan", "dhoka", "kidnap"
    ],

    "DEPRESSED": [
        "akelapan", "dukh", "dard", "pareshan", "himmat", "roney", "rona", 
        "marne", "suicide", "zindagi", "bojh", "udas", "udasi", "akela", 
        "tension", "chinta", "khamosh", "shanti", "bechain", "bechaini"
    ],

    "NORMAL": [
        "pata", "btana", "bolna", "information", "dekhna", "baat", "shayad", 
        "kuch", "idhar", "udhar", "milna", "poochna", "rastay", "theek", 
        "thik", "ok", "acha", "suno", "samajh", "pata"
    ],   
}

LOCATION_WORDS = [
    "near", "station", "road", "market",
    "ke paas", "ke samne", "road pe", "market mein","piche" ,"ke pass"
]

INABILITY_MARKERS = {
    "pata nahi", "nhi pata", "don't know", "dont know", "samajh nahi", 
    "smj nhi", "pata nhi","pta nhi","pta nahi", "confusion", "bhul gaya", "yaad nahi", 
    "nahi maloom", "not sure", "confused"
}

WORD_TO_NUM = {
    "one": "1", "two": "2", "three": "3",
    "ek": "1", "do": "2", "teen": "3"
}

def detect_language(text):
    text = text.lower()

    hinglish_markers = [
            #Grammar & Auxiliary Verbs
        "hai", "hain", "hoon", "tha", "thi", "the", "rha", "raha", "rahi", "rahe", 
        "gaya", "gayi", "gaye", "kar", "kr", "karne", "diya", "liya", "kiya", "ho", 
        "raha", "karke", "hone", "bhaga", "aaya", "baitha", "uthna", "dena", "lena",

        #Pronouns & Conjunctions
        "main", "hum", "tum", "aap", "humein", "mujhe", "mera", "tera", "tumhara", 
        "hamara", "yeh", "woh", "isme", "usme", "aur", "lekin", "magar", "kyunki", 
        "kyu", "kyun", "toh", "bhi", "hi", "ne", "se", "ka", "ki", "ke", "ko",

        #Interrogatives
        "kya", "kab", "kahan", "kaise", "kitna", "kaun", "kiska", "kidhar",

        #Emergency
        "bachao", "bachaoo", "madad", "sahayata", "jaldi", "turant", "abhi", "fauran", 
        "aag", "pani", "chot", "dard", "khoon", "zakhmi", "behosh", "marna", "khatra", 
        "chor", "daku", "gunda", "dhoka", "police", "thana", "ambulance", "hospital", 
        "doctor", "dawai", "goli", "bandook", "chaku", "ladai", "jhagra", "maar",

        #Common Verbs & Negation
        "nahi", "nhi", "mat", "ruko", "jao", "aao", "bhago", "suno", "dekho", 
        "bolo", "samjho", "batao", "chahiye", "pata", "kaam", "log", "baat"
    ]

    count = sum(1 for word in hinglish_markers if word in text)

    if count >= 1:
        return "hinglish"

    return "english"


def detect_emotion(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    input_words = set(text.split())
    
    has_booster = any(word in input_words for word in BOOSTERS)
    
    results = {}
    for emotion, word_list in EMOTION_SETS.items():
        matches = input_words.intersection(word_list)
        if matches:
            score = len(matches)
            if has_booster and emotion != "normal":
                score *= 2
            results[emotion] = score

    if results:
        detected = max(results, key=results.get)
        
        if has_booster and detected in ["danger", "depressed"]:
            return "panic" 
            
        return detected
    
    return "unknown"

def detect_incident(text):
    text = text.lower()

    for incident, words in INCIDENT_WORDS.items():
        if any(word in text for word in words):
            return incident

    return "unknown"

def detect_location(text):
    text_lower = text.lower()
    for word in LOCATION_WORDS:
        if word in text_lower:
            return text 
    return None


def detect_people(text):
    text = text.lower()

    if any(word in text for word in ["nhi", "nahi", "no", "none", "zero", "koi nahi"]):
        return "0"
    for word in text.split():
        if word.isdigit():
            return word

        if word in WORD_TO_NUM:
            return WORD_TO_NUM[word]

    return None


def get_priority(incident, emotion, text):
    text = text.lower()
    input_words = set(text.split())

    if incident in ["accident","fire","violence","medical"]:
        return "HIGH"

    has_booster = any(word in input_words for word in BOOSTERS)
    has_panic_word = any(word in input_words for word in PANIC_WORDS)

    if emotion == "danger" or has_panic_word or has_booster:
        return "HIGH"

    if emotion == "depressed" and any(word in input_words for word in ["suicide", "marne", "maut"]):
        return "HIGH"

    return "MEDIUM"

def next_question(context, last_user_input=""):
    lang = context.get("lang", "english")
    last_user_input = last_user_input.lower().strip()
    
    if "retries" not in context:
        context["retries"] = {"incident": 0, "location": 0, "people": 0}

    is_confused = any(marker in last_user_input for marker in INABILITY_MARKERS)

    if lang == "hinglish":
        # 1. INCIDENT: Ask if unknown and attempts <= 3
        if not context.get("incident") or context.get("incident") == "unknown":
            if context["retries"]["incident"] < 3:
                context["retries"]["incident"] += 1
                if is_confused:
                    return "Theek hai, bas ye batao wahan aag, accident ya koi bimar hai?"
                return "Kya emergency hai?"

        if not context.get("location"):
            if context["retries"]["location"] < 3:
                context["retries"]["location"] += 1
                if is_confused:
                    return "Koi landmark, dukan ya mandir ka naam batao."
                return "Aapka location batao"

        if not context.get("people"):
            if context["retries"]["people"] < 3:
                context["retries"]["people"] += 1
                if is_confused:
                    return "Bas 'Haan' ya 'Nahi' bolo, kya wahan koi injured hai?"
                return "Kitne log injured hai?"


        return "Theek hai, help bhej rahe hain. Line pe bane rahiye."

    else: 
        if not context.get("incident") or context.get("incident") == "unknown":
            if context["retries"]["incident"] < 3:
                context["retries"]["incident"] += 1
                return "What is the emergency?"
        
        if not context.get("location"):
            if context["retries"]["location"] < 3:
                context["retries"]["location"] += 1
                return "Please tell your location."
                
        if not context.get("people"):
            if context["retries"]["people"] < 3:
                context["retries"]["people"] += 1
                return "How many people are injured?"

        return "Help is on the way. Please stay on the line."

def generate_response(context, question):

    lang = context.get("lang", "english")

    if question:
        return question

    incident = context.get("incident")
    location = context.get("location")
    people = context.get("people")

    if lang == "hinglish":
        return f"{incident} detect hua hai. Location: {location}. {people} log affected hai. Help aa rahi hai."

    return f"Emergency detected: {incident}. Location: {location}. {people} people affected. Help is on the way."


def process_text(text, context):

    if "transcript" not in context:
        context["transcript"] = ""
    if "conversation" not in context:
        context["conversation"] = []

    context["conversation"].append({
        "speaker": "caller",
        "text": text
    })

    context["transcript"] += " " + text

    lang = detect_language(text)
    context["lang"] = lang

    emotion = detect_emotion(text)
    incident = detect_incident(text)
    location = detect_location(text)
    people = detect_people(text)

    if incident != "unknown":
        context["incident"] = incident

    if location:
        context["location"] = location

    if people:
        context["people"] = people

    priority = get_priority(context.get("incident"), emotion,text)

    question = next_question(context, text)

    if question:
        context["conversation"].append({
            "speaker": "ai",
            "text": question
        })

    response = generate_response(context, question)

    return {
        "emotion": emotion,
        "priority": priority,
        "incident": context.get("incident"),
        "location": context.get("location"),
        "people": context.get("people"),
        "next_question": question,
        "response": response,
        "transcript": context["transcript"].strip(),
        "conversation": context["conversation"]
    }