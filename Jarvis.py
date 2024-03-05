import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import elevenlabs

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
api_key = os.getenv("E_API_KEY")
elevenlabs.set_api_key(api_key)
# Configure OpenAI
import openai
openai.api_key = OPENAI_KEY

# Define a function to speak text using pyttsx3
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the speech recognizer
r = sr.Recognizer()

# Define a function to record text from the microphone
def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I am Jarvis, Awaiting your Order Sir")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("I dont understand; {0}".format(e))
        except sr.UnknownValueError:
            print("Well, this looks messed up!!")

# Define a function to send text to ChatGPT and get a response
def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

# Initialize messages with the initial user message
messages = [{"role": "user", "content": "Act like Jarvis from Iron Man, use same voice and behavior, speak little slowly and more deep robotic jarvis voice, Sir is he/him and he is your creator, Your name is Jarvis from Iron Man my personal assistant"}]

# Main loop
while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    
    # Generate Jarvis voice audio using elevenlabs
    audio = elevenlabs.generate(
        text=response,
        voice="bu4OlnABu8CAL4oimVbq"
    )
    # Speak the response
    elevenlabs.play(audio)
    # Print the response
    print(response)

