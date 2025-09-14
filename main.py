import speech_recognition as sr
import pyttsx3
import os
import platform
import google.generativeai as genai
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment variable
# To get a key, visit https://ai.google.dev/
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("Please set your GOOGLE_API_KEY in the .env file.")
    sys.exit()

genai.configure(api_key=API_KEY)

# --- Initialize Engines ---
# Initialize the text-to-speech engine
engine = pyttsx3.init()
# Get available voices and set a female voice if available
voices = engine.getProperty('voices')
for voice in voices:
    # This check might need adjustment based on the OS and installed voices
    # 'voice.name' or other properties might be more reliable
    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Initialize the speech recognition recognizer
r = sr.Recognizer()

# --- Functions ---
def speak(text):
    """Converts text to speech."""
    print(f"Assistant: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error with text-to-speech engine: {e}")

def listen():
    """Listens for user input and converts speech to text."""
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    
    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def execute_command(command):
    """
    Executes a system command based on user input.
    Note: This is a basic implementation.
    """
    if "open youtube" in command:
        speak("Opening YouTube.")
        subprocess.Popen(["start", "https://www.youtube.com"] if platform.system() == "Windows" else ["open", "https://www.youtube.com"] if platform.system() == "Darwin" else ["xdg-open", "https://www.youtube.com"])
        return True
    elif "open chrome" in command or "open browser" in command:
        speak("Opening Google Chrome.")
        subprocess.Popen(["start", "chrome"] if platform.system() == "Windows" else ["open", "-a", "Google Chrome"] if platform.system() == "Darwin" else ["google-chrome"])
        return True
    elif "open google" in command:
        speak("Opening Google.")
        subprocess.Popen(["start", "https://www.google.com"] if platform.system() == "Windows" else ["open", "https://www.google.com"] if platform.system() == "Darwin" else ["xdg-open", "https://www.google.com"])
        return True
    elif "open gmail" in command:
        speak("Opening Gmail.")
        subprocess.Popen(["start", "https://mail.google.com"] if platform.system() == "Windows" else ["open", "https://mail.google.com"] if platform.system() == "Darwin" else ["xdg-open", "https://mail.google.com"])
        return True
    elif "open spotify" in command:
        speak("Opening Spotify.")
        subprocess.Popen(["start", "spotify"] if platform.system() == "Windows" else ["open", "-a", "Spotify"] if platform.system() == "Darwin" else ["spotify"])
        return True
    return False

def get_gemini_response(prompt):
    """Sends a prompt to the Gemini API and returns the response."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Refined the prompt to provide more context for the AI model
        full_prompt = f"You are a helpful voice assistant. Answer the user's question concisely and accurately: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the Gemini API: {e}"

# --- Main Loop ---
def main():
    speak("Hello, I am your voice assistant. How can I help you today?")
    while True:
        command = listen()
        
        if command:
            if execute_command(command):
                continue
            
            if "stop" in command or "exit" in command or "goodbye" in command:
                speak("Goodbye!")
                break
            
            # If the command is not a system command, send it to the AI model
            response = get_gemini_response(command)
            speak(response)
        else:
            # If nothing was understood, let the user know and continue the loop
            speak("I'm sorry, I didn't catch that. Can you please repeat?")

if __name__ == "__main__":
    main()
