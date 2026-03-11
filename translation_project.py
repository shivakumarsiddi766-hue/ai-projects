import pyttsx3
import webbrowser
import datetime
import pyautogui
import time
import cv2
import numpy as np
import string
import pywhatkit as kit
import json
import os
import urllib.parse

# -------------------- SPEECH ENGINE --------------------
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------- MEMORY --------------------
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

knowledge = load_memory()

# -------------------- UTILITIES --------------------
def clean_text(text):
    return text.lower().strip().rstrip(string.punctuation)

# -------------------- SMALL CHAT --------------------
def small_chat(command):
    if any(x in command for x in ["hi", "hello", "hey"]):
        return "Hey boss 😄"
    if "how are you" in command:
        return "I'm great! Thanks for asking 😄"
    return None

# -------------------- JOB SEARCH SYSTEM --------------------
def search_job(command):
    speak("Searching for latest jobs")

    cmd = command.lower()

    platform = None
    location = ""
    role = ""

    # Detect platform
    if "linkedin" in cmd:
        platform = "linkedin"
    elif "indeed" in cmd:
        platform = "indeed"

    # Extract role
    words_to_remove = ["find", "search", "job", "jobs", "on", "in", "linkedin", "indeed", "hyd"]
    role_words = cmd.split()
    role = " ".join([w for w in role_words if w not in words_to_remove])

    # Location shortcut
    if "hyd" in cmd:
        location = "Hyderabad"

    # Fresher filter
    fresher_keywords = "fresher OR entry level"

    encoded_role = urllib.parse.quote(role + " " + fresher_keywords)
    encoded_location = urllib.parse.quote(location)

    # Last 24 hours filter
    if platform == "linkedin":
        # f_TPR=r86400 → last 24 hours
        url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_role}&location={encoded_location}&f_TPR=r86400"
        speak("Opening LinkedIn")
        webbrowser.open(url)

    elif platform == "indeed":
        # fromage=1 → last 24 hours
        url = f"https://www.indeed.com/jobs?q={encoded_role}&l={encoded_location}&fromage=1"
        speak("Opening Indeed")
        webbrowser.open(url)

    else:
        speak("Please mention LinkedIn or Indeed")

# -------------------- SCREENSHOT --------------------
def take_screenshot():
    speak("Taking screenshot")
    img = pyautogui.screenshot()
    img.save("screenshot.png")
    speak("Screenshot saved")

# -------------------- SCREEN RECORD --------------------
def record_screen():
    speak("Screen recording started. Press Q to stop")
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("screen_record.avi", fourcc, 20.0, screen_size)

    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    out.release()
    cv2.destroyAllWindows()
    speak("Screen recording saved")

# -------------------- YOUTUBE --------------------
def play_youtube(query):
    speak(f"Playing {query}")
    kit.playonyt(query)

# -------------------- START --------------------
speak("Hello boss, how can I help you")

# -------------------- MAIN LOOP --------------------
while True:
    try:
        command = input("\nEnter command: ").lower().strip()
        cmd = clean_text(command)

        # EXIT
        if cmd in ["exit", "quit", "stop"]:
            speak("Goodbye boss")
            break

        # JOB SEARCH COMMAND
        elif "job" in cmd and ("linkedin" in cmd or "indeed" in cmd):
            search_job(cmd)

        # OPEN YOUTUBE
        elif "youtube" in cmd:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # OPEN GOOGLE
        elif "google" in cmd:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # TIME
        elif cmd == "time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        # SCREENSHOT
        elif "screenshot" in cmd:
            take_screenshot()

        # SCREEN RECORD
        elif "record screen" in cmd:
            record_screen()

        # PLAY MUSIC
        elif cmd.startswith("play "):
            play_youtube(cmd.replace("play ", ""))

        # TEACH MEMORY
        elif cmd.startswith("teach:"):
            try:
                data = command.replace("teach:", "").strip()
                q, a = data.split("=")
                knowledge[clean_text(q)] = a.strip()
                save_memory(knowledge)
                speak("I have learned this permanently")
            except:
                speak("Use format: teach: question = answer")

        elif cmd in knowledge:
            speak(knowledge[cmd])

        else:
            reply = small_chat(cmd)
            if reply:
                speak(reply)
            else:
                speak("I am still learning boss")

    except KeyboardInterrupt:
        speak("Assistant stopped")
        break
