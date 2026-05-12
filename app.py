import os
import json
import time
import re
from datetime import datetime

from dotenv import load_dotenv
import google.generativeai as genai
from colorama import Fore, Style, init

# ======================================================
# INITIAL SETUP
# ======================================================

init(autoreset=True)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(Fore.RED + "❌ GEMINI_API_KEY not found in .env")
    exit()

genai.configure(api_key=API_KEY)

# ======================================================
# FILES
# ======================================================

CHAT_HISTORY_FILE = "chat_history.json"
MEMORY_FILE = "memory.json"

# ======================================================
# MODEL SETUP
# ======================================================

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    system_instruction="""
You are an advanced AI Study Companion.

Your job:
- Teach students clearly
- Help in exams and revision
- Use simple explanations
- Use examples and analogies
- Improve memory retention
- Encourage understanding instead of rote learning

Rules:
- Keep answers structured
- Keep answers concise unless user asks deeply
- Use clean plain text formatting
- DO NOT use markdown symbols
- DO NOT use:
  #, ##, ###, *, **, backticks
- Use readable spacing instead
- Focus on clarity and exam usefulness
"""
)

# ======================================================
# SAFE JSON FUNCTIONS
# ======================================================

def load_json(filename, default):

    try:

        if not os.path.exists(filename):
            return default

        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except:
        return default


def save_json(filename, data):

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# ======================================================
# SERIALIZE CHAT HISTORY
# ======================================================

def serialize_history(history):

    serialized = []

    try:

        for item in history:

            role = getattr(item, "role", None)
            parts = getattr(item, "parts", [])

            converted_parts = []

            for part in parts:

                text = getattr(part, "text", "")

                converted_parts.append({
                    "text": text
                })

            serialized.append({
                "role": role,
                "parts": converted_parts
            })

    except Exception as e:

        print(Fore.RED + f"Serialization Error: {e}")

    return serialized

# ======================================================
# CLEAN RESPONSE
# ======================================================

def clean_response(text):

    # Remove markdown-like symbols
    text = re.sub(r"[*#`>-]", "", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

# ======================================================
# LOAD MEMORY
# ======================================================

memory = load_json(
    MEMORY_FILE,
    {
        "favorite_topics": [],
        "weak_topics": [],
        "study_sessions": 0,
        "last_studied": ""
    }
)

# ======================================================
# LOAD CHAT HISTORY
# ======================================================

loaded_history = load_json(CHAT_HISTORY_FILE, [])

chat = model.start_chat(history=loaded_history)

# ======================================================
# CURRENT MODE
# ======================================================

mode = "explain"

# ======================================================
# UI
# ======================================================

def banner():

    print(Fore.GREEN + """
=================================================
               AI STUDY COMPANION
             Powered by Gemini Flash
=================================================
""")


def show_help():

    print(Fore.CYAN + """
=================================================
AVAILABLE COMMANDS
=================================================

/help       -> Show commands
/mode       -> Show current mode

/explain    -> Explanation mode
/quiz       -> Quiz mode
/summary    -> Summary mode
/exam       -> Exam preparation mode
/revise     -> Quick revision mode

/timer      -> Start study timer

/memory     -> Show AI memory
/clear      -> Clear history and memory

/exit       -> Exit chatbot

=================================================
""")

# ======================================================
# MEMORY FUNCTIONS
# ======================================================

def update_memory(user_input):

    global memory

    text = user_input.lower()

    topics = [
        "python",
        "java",
        "dbms",
        "os",
        "network",
        "computer networks",
        "cn",
        "dsa",
        "algorithm",
        "ai",
        "ml",
        "math",
        "physics",
        "chemistry"
    ]

    for topic in topics:

        if topic in text:

            if topic not in memory["favorite_topics"]:
                memory["favorite_topics"].append(topic)

    weak_keywords = [
        "difficult",
        "hard",
        "confused",
        "weak",
        "dont understand",
        "don't understand"
    ]

    for keyword in weak_keywords:

        if keyword in text:

            memory["weak_topics"].append(user_input)
            break

    memory["study_sessions"] += 1
    memory["last_studied"] = str(datetime.now())

    # Keep only last 10 weak topics
    memory["weak_topics"] = memory["weak_topics"][-10:]

    save_json(MEMORY_FILE, memory)

# ======================================================
# SHOW MEMORY
# ======================================================

def show_memory():

    print(Fore.MAGENTA + "\n============== MEMORY ==============\n")

    print("Favorite Topics:")

    if memory["favorite_topics"]:

        for topic in memory["favorite_topics"]:
            print("-", topic)

    else:
        print("No favorite topics yet.")

    print("\nWeak Topics:")

    if memory["weak_topics"]:

        for topic in memory["weak_topics"]:
            print("-", topic)

    else:
        print("No weak topics detected.")

    print(f"\nStudy Sessions: {memory['study_sessions']}")
    print(f"Last Studied: {memory['last_studied']}")

    print("\n====================================\n")

# ======================================================
# TIMER
# ======================================================

def start_timer():

    try:

        minutes = int(input("Enter timer duration (minutes): "))

        if minutes <= 0:
            print(Fore.RED + "❌ Enter valid minutes")
            return

        seconds = minutes * 60

        print(
            Fore.GREEN +
            f"\n⏳ Timer started for {minutes} minute(s)\n"
        )

        while seconds > 0:

            mins = seconds // 60
            secs = seconds % 60

            print(
                Fore.YELLOW +
                f"\rTime Left: {mins:02d}:{secs:02d}",
                end=""
            )

            time.sleep(1)

            seconds -= 1

        print(Fore.GREEN + "\n\n✅ Study session completed!\n")

    except ValueError:

        print(Fore.RED + "\n❌ Invalid timer input\n")

# ======================================================
# BUILD PROMPT
# ======================================================

def build_prompt(user_input):

    global mode

    if mode == "quiz":

        return f"""
Create a quiz on:

{user_input}

Requirements:
- 5 MCQs
- 4 options each
- Mention correct answers
- Medium difficulty
"""

    elif mode == "summary":

        return f"""
Summarize the following topic:

{user_input}

Requirements:
- Concise bullet points
- Important concepts only
"""

    elif mode == "exam":

        return f"""
Help student prepare for exams on:

{user_input}

Requirements:
- Important concepts
- Frequently asked questions
- Key points to memorize
- Exam-oriented answers
- Mnemonics if useful
"""

    elif mode == "revise":

        return f"""
Create ultra-short revision notes for:

{user_input}

Requirements:
- Bullet points only
- High retention format
- Last-minute revision style
- Include formulas if needed
"""

    else:

        return f"""
Explain this topic clearly and simply:

{user_input}

Use examples and analogies.
"""

# ======================================================
# COMMAND HANDLER
# ======================================================

def handle_command(user_input):

    global mode
    global chat
    global memory

    cmd = user_input.lower()

    if cmd == "/exit":

        print(Fore.GREEN + "\nGoodbye 👋")
        return False

    elif cmd == "/help":

        show_help()
        return True

    elif cmd == "/mode":

        print(Fore.CYAN + f"\nCurrent Mode: {mode}\n")
        return True

    elif cmd == "/quiz":

        mode = "quiz"
        print(Fore.GREEN + "\n✅ Quiz Mode Activated\n")
        return True

    elif cmd == "/summary":

        mode = "summary"
        print(Fore.GREEN + "\n✅ Summary Mode Activated\n")
        return True

    elif cmd == "/exam":

        mode = "exam"
        print(Fore.GREEN + "\n✅ Exam Mode Activated\n")
        return True

    elif cmd == "/revise":

        mode = "revise"
        print(Fore.GREEN + "\n✅ Revision Mode Activated\n")
        return True

    elif cmd == "/explain":

        mode = "explain"
        print(Fore.GREEN + "\n✅ Explain Mode Activated\n")
        return True

    elif cmd == "/timer":

        start_timer()
        return True

    elif cmd == "/memory":

        show_memory()
        return True

    elif cmd == "/clear":

        save_json(CHAT_HISTORY_FILE, [])

        memory = {
            "favorite_topics": [],
            "weak_topics": [],
            "study_sessions": 0,
            "last_studied": ""
        }

        save_json(MEMORY_FILE, memory)

        chat = model.start_chat(history=[])

        print(Fore.RED + "\n🗑 History and memory cleared\n")

        return True

    return None

# ======================================================
# START APPLICATION
# ======================================================

banner()
show_help()

# ======================================================
# MAIN LOOP
# ======================================================

while True:

    user_input = input(
        Fore.YELLOW + "You: " + Style.RESET_ALL
    ).strip()

    if not user_input:
        continue

    # Handle commands
    result = handle_command(user_input)

    if result is False:
        break

    elif result is True:
        continue

    # Update memory
    update_memory(user_input)

    # Build prompt
    prompt = build_prompt(user_input)

    # Memory context
    memory_context = f"""
Student Memory Context:

Favorite Topics:
{memory['favorite_topics']}

Weak Topics:
{memory['weak_topics']}
"""

    final_prompt = memory_context + "\n\n" + prompt

    try:

        print(Fore.BLUE + "\nThinking...\n")

        response = chat.send_message(final_prompt)

        cleaned_response = clean_response(response.text)

        print(Fore.MAGENTA + "Bot:\n")
        print(Style.BRIGHT + cleaned_response)
        print()

        # Save chat history safely
        serialized_history = serialize_history(chat.history)

        save_json(
            CHAT_HISTORY_FILE,
            serialized_history
        )

    except Exception as e:

        print(Fore.RED + f"\n❌ Error: {e}\n")