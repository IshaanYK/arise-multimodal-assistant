import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import subprocess
import os
import webbrowser
import threading
import time
import dateparser
from arise_memory import handle_memory_query  # Memory brain system
from wake_listener import listen_for_wake_word
from hand_detector import detect_hand_wave
from state_manager import is_awake  # import the awake flag

def run_arise():
    global exit_flag
    is_awake.set()  # ARISE is now awake
    wish_user()
    while True:
        if exit_flag:
            break
        query = take_command()
        if exit_flag:
            break
        if not query:
            continue

        if "time" in query:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {current_time}")

        elif any(word in query for word in ["stop", "exit", "khatam", "band", "hatao", "band kardo", "shutdown"]):
            speak("Goodbye, Eshan. Shutting down ARISE")
            break

        # ... rest of your commands ...

    is_awake.clear()  # ARISE is now sleeping


# Global exit flag
exit_flag = False

# Optional Gemini API integration - Uncomment and configure if you have API key
# import google.generativeai as genai
# genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Local GPT-2 model fallback (comment out if no torch installed)
try:
    from transformers import pipeline
    generator = pipeline('text-generation', model='gpt2')
except ImportError:
    generator = None

# Text-to-Speech setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  # Female voice if available

def speak(text):
    print("ARISE:", text)
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good Morning, Eshan!")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Eshan!")
    else:
        speak("Good Evening, Eshan!")
    speak("I am ARISE, How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you say it again?")
        return ""
    except sr.RequestError as e:
        speak("Sorry, I can't reach the recognition service.")
        print("Speech Recognition Error:", e)
        return ""

def handle_system_commands(query):
    user_path = "C:\\Users\\ISHAAN SEN"
    commands = {
        "open chrome": lambda: os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
        "open vs code": lambda: os.startfile(user_path + "\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"),
        "open notepad": lambda: subprocess.Popen("notepad.exe"),
        "open file explorer": lambda: subprocess.Popen("explorer"),
        "open downloads": lambda: os.startfile(user_path + "\\Downloads"),
        "open documents": lambda: os.startfile(user_path + "\\Documents"),
        "open instagram": lambda: webbrowser.open("https://www.instagram.com"),
        "open facebook": lambda: webbrowser.open("https://www.facebook.com"),
        "open youtube": lambda: webbrowser.open("https://www.youtube.com"),
        "open whatsapp": lambda: webbrowser.open("https://web.whatsapp.com"),
        "open whatsapp web": lambda: webbrowser.open("https://web.whatsapp.com"),
        "shutdown": lambda: print("Shutdown command issued"),
        "restart": lambda: print("Restart command issued")
    }
    for command, action in commands.items():
        if command in query:
            speak(f"{command.replace('open ', '').capitalize()} opening")
            action()
            return True

    if "search google for" in query:
        topic = query.replace("search google for", "").strip()
        speak(f"Searching Google for {topic}")
        webbrowser.open(f"https://www.google.com/search?q={topic}")
        return True

    if "open" in query and "on google" in query:
        search_term = query.replace("open", "").replace("on google", "").strip()
        speak(f"Opening {search_term} on Google")
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        return True

    return False

reminders = []
def add_reminder(text):
    try:
        if " at " in text:
            time_text = text.split(" at ")[-1].strip()
        elif " for " in text:
            time_text = text.split(" for ")[-1].strip()
        else:
            time_text = text
        reminder_time = dateparser.parse(time_text, settings={'PREFER_DATES_FROM': 'future'})
        if not reminder_time:
            speak("Sorry, I couldn't understand the reminder time.")
            return
        reminder_msg = text.split("remind me to")[-1].strip()
        reminders.append((reminder_time, reminder_msg))
        speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}: {reminder_msg}")
    except Exception as e:
        print("Reminder Error:", e)
        speak("Failed to set reminder.")

def reminder_checker():
    while True:
        now = datetime.datetime.now()
        for reminder in reminders[:]:
            time_to_remind, msg = reminder
            if now >= time_to_remind:
                speak(f"Reminder: {msg}")
                reminders.remove(reminder)
        time.sleep(30)

def ask_gpt(prompt):
    if generator:
        try:
            responses = generator(prompt, max_length=100, num_return_sequences=1)
            generated = responses[0]['generated_text']
            if generated.lower().startswith(prompt.lower()):
                generated = generated[len(prompt):].strip()
            return generated
        except Exception as e:
            print("Local GPT Error:", e)
    return "Sorry, I couldn’t get a response."

def exit_listener():
    global exit_flag
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                command = r.recognize_google(audio, language='en-in').lower()
                if any(word in command for word in ["stop", "exit", "band", "shutdown", "close", "quit"]):
                    exit_flag = True
                    speak("Exiting now. Goodbye Ishaan.")
                    os._exit(0)  # immediate exit
            except Exception:
                pass

def run_arise():
    global exit_flag
    wish_user()
    while True:
        if exit_flag:
            break
        query = take_command()
        if exit_flag:  # Check again after taking command
            break
        if not query:
            continue

        if "time" in query:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {current_time}")

        elif any(word in query for word in ["stop", "exit", "khatam", "band", "hatao", "band kardo", "shutdown"]):
            speak("Goodbye, Eshan. Shutting down ARISE")
            break

        elif handle_system_commands(query):
            continue

        elif "remind me" in query:
            add_reminder(query)

        elif "play" in query:
            if "music" in query or query.strip() == "play music":
                song = query.replace("play", "").replace("music", "").strip()
                if song == "":
                    song = "top hits"
                speak(f"Playing music: {song} on YouTube Music")
                webbrowser.open(f"https://music.youtube.com/search?q={song}")
            else:
                video = query.replace("play", "").strip()
                speak(f"Playing {video} on YouTube")
                pywhatkit.playonyt(video)

        elif any(keyword in query for keyword in ["what is", "who is", "explain", "tell me about", "define"]):
            response = ask_gpt(query)
            speak(response)

        else:
            memory_response = handle_memory_query(query)
            if memory_response:
                speak(memory_response)
                continue

            speak("Let me think...")
            response = ask_gpt(query)
            speak(response)

if __name__ == "__main__":
    # Start reminder checker thread
    threading.Thread(target=reminder_checker, daemon=True).start()

    # Start exit listener thread
    threading.Thread(target=exit_listener, daemon=True).start()

    # Start wake word listener in parallel
    threading.Thread(target=listen_for_wake_word, args=(run_arise,), daemon=True).start()

    # Start hand gesture detection
    detect_hand_wave(run_arise)
