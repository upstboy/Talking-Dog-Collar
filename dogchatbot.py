import openai
import speech_recognition as sr

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def get_audio_input():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def chat_with_gpt(text):
    openai.api_key = 'your-openai-api-key'

    response = openai.Completion.create(
        engine="gpt-4.0-turbo",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    while True:
        text = get_audio_input()
        if text:
            response = chat_with_gpt(text)
            print("ChatGPT:", response)

if __name__ == "__main__":
    main()
