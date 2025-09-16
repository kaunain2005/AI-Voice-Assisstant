🤖 AI Voice Assistant
This is a simple AI voice assistant powered by Python libraries for speech recognition, text-to-speech, and Google's Gemini API for conversational responses.

🚀 Getting Started
✅ Prerequisites
You will need Python installed on your system. This project also requires several Python libraries. You can install them by running the following command in your terminal:

pip install SpeechRecognition pyttsx3 google-generativeai python-dotenv

⚙️ Configuration
This project uses an environment variable to securely store your Gemini API key.

Create a file named .env in the same directory as the voice_assistant.py script.

Add your API key to this file in the following format, replacing "your-api-key-here" with your actual key:

GOOGLE_API_KEY="your-api-key-here"

▶️ Usage
To start the voice assistant, simply run the Python script from your terminal:

python voice_assistant.py

The assistant will greet you and begin listening for your commands.

🗣️ System Commands
The assistant has several built-in commands for interacting with your system:

"What is your name" / "What's your name": ❓ The assistant will respond with its current name.

"Update your name": 📝 Prompts you to set a new name for the assistant.

"Open YouTube": ▶️ Opens a web browser to YouTube.

"Open Chrome" / "Open browser": 🌐 Opens Google Chrome.

"Open Google": 🔍 Opens a web browser to Google.

"Open Gmail": ✉️ Opens a web browser to Gmail.

"Open Spotify": 🎶 Opens the Spotify application.

"Stop" / "Exit" / "Goodbye": 🛑 Shuts down the voice assistant.