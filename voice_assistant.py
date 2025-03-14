import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import sys

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.commands = {
            "what is your name": self.respond_name,
            "what time is it": self.respond_time,
            "open youtube": self.open_youtube,
            "open google": self.open_google,
            "tell me a joke": self.tell_joke,
            "play music": self.play_music,
            "stop": self.stop,
        }

    def speak(self, text):
        print("Assistant: " + text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                self.speak("Sorry, my speech service is down.")
                return None

    def execute_command(self, command):
        for key in self.commands.keys():
            if key in command:
                self.commands[key]()
                return
        self.speak("I can only respond to certain commands.")

    def respond_name(self):
        self.speak("I am your voice assistant.")

    def respond_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.speak(f"The current time is {current_time}.")

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        self.speak("Opening YouTube.")

    def open_google(self):
        webbrowser.open("https://www.google.com")
        self.speak("Opening Google.")

    def tell_joke(self):
        jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!",
            "Why don't scientists trust atoms? Because they make up everything!"
        ]
        self.speak(random.choice(jokes))

    def play_music(self):
        music_folder = os.path.join(os.path.expanduser('~'), 'Music')
        songs = os.listdir(music_folder)
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_folder, song))
            self.speak(f"Playing {song}.")
        else:
            self.speak("No music found in your music folder.")

    def stop(self):
        self.speak("Goodbye!")
        sys.exit()

    def run(self):
        self.speak("Hello! How can I assist you today?")
        while True:
            command = self.listen()
            if command:
                self.execute_command(command)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()