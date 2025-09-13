import speech_recognition as sr
import pyttsx3
import os
import platform
import google.generativeai as genai
import sys
import subprocess

# --- Configuration ---
# You need to set your Gemini API key here or as an environment variable.
# To get a key, visit https://ai.google.dev/
API_KEY = "YOUR_API_KEY"
if not API_KEY or API_KEY == "YOUR_API_KEY":
    print("Please set your Gemini API key in the script or as an environment variable.")
    sys.exit()

genai.configure(api_key=API_KEY)

# --- Initialize Engines ---
# Initialize the text-to-speech engine
engine = pyttsx3.init()
# Get available voices and set a female voice if available
voices = engine.getProperty('voices')
for voice in voices:
    if voice.gender == 'female':
        engine.setProperty('voice', voice.id)
        break

# Initialize the speech recognition recognizer
r = sr.Recognizer()

# --- Functions ---
def speak(text):
    """Converts text to speech."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

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
        # Command varies by OS
        if platform.system() == "Windows":
            subprocess.Popen(["start", "https://www.youtube.com"], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", "https://www.youtube.com"])
        else:  # Linux
            subprocess.Popen(["xdg-open", "https://www.youtube.com"])
        return True
    elif "open chrome" in command:
        speak("Opening Google Chrome.")
        # Command varies by OS
        if platform.system() == "Windows":
            subprocess.Popen(["start", "chrome"])
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Google Chrome"])
        else:  # Linux
            # 'google-chrome' or 'google-chrome-stable' might be the command
            subprocess.Popen(["google-chrome"])
        return True
    return False

def get_gemini_response(prompt):
    """Sends a prompt to the Gemini API and returns the response."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
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
            
            # Send the command to the AI model
            response = get_gemini_response(command)
            speak(response)

if __name__ == "__main__":
    main()
