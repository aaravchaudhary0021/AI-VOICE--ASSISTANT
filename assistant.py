import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import datetime
import pyjokes
import threading

# Initialize
listener = sr.Recognizer()

def speak_thread(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def talk(text):
    print("Assistant:", text)
    t = threading.Thread(target=speak_thread, args=(text,))
    t.start()


def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=0.5)
            audio = listener.listen(source)

        command = listener.recognize_google(audio)
        command = command.lower()
        print("You said:", command)

    except:
        print("Didn't catch that")

    return command


def run_ai(command):

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        talk(f"Searching for {search_query}")
        pywhatkit.search(search_query)

    elif 'youtube' in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'instagram' in command:
        talk("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif 'github' in command:
        talk("Opening GitHub")
        webbrowser.open("https://github.com")

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"Current time is {time}")

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'who is' in command or 'what is' in command:
        person = command.replace('who is', '').replace('what is', '').strip()
        talk(f"Searching info about {person}")
        try:
            info = pywhatkit.info(person, 2)
            talk(info)
        except:
            talk("Sorry, I couldn't find information.")

    elif 'send message' in command:
        talk("Sending message")
        pywhatkit.sendwhatmsg_instantly("+917318027513", "Hello from AI assistant!")

    elif 'type' in command:
        text = command.replace('type', '').strip()
        talk("Typing now")
        pywhatkit.typewrite(text, interval=0.05)

    elif 'handwriting' in command:
        text = command.replace('handwriting', '').strip()
        talk("Converting to handwriting")
        pywhatkit.text_to_handwriting(text)

    elif 'exit' in command or 'stop' in command or 'bye' in command:
        talk("Okay bye!")
        return False

    else:
        talk("I didn't understand. Try again.")

    return True


# MAIN LOOP
talk("Say hello assistant to wake me up")

while True:
    wake_command = take_command()

    if 'assistant' in wake_command:
        talk("Yes, I'm listening")

        command = take_command()

        if command != "":
            if not run_ai(command):
                break
