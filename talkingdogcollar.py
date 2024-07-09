import cv2
import numpy as np
import base64
import os
import pyaudio
from io import BytesIO
from openai import OpenAI

# Initialize OpenAI and PyAudio clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
p = pyaudio.PyAudio()

def encode_image_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    io_buf = BytesIO(buffer)
    return base64.b64encode(io_buf.getvalue()).decode('utf-8')

def get_image_description(image_b64):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a highly capable visual assistant."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image? Describe it in first person."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            },
        ]
    )
    return response.choices[0].message.content

def capture_image_on_motion(message_history):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame1 = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        return

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    while True:
        ret, frame2 = cap.read()
        if not ret:
            print("Failed to read from webcam.")
            break

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        delta_frame = cv2.absdiff(gray1, gray2)
        thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                print("Motion detected. Processing image...")
                image_b64 = encode_image_to_base64(frame2)

                # Save the image
                cv2.imwrite('motion_detected.jpg', frame2)

                description = get_image_description(image_b64)
                print("Image description:", description)
                response, message_history = dog_chatbot(description, message_history)
                print("DogBot:", response)

        gray1 = gray2.copy()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def play_stream(data):
    stream = p.open(format=p.get_format_from_width(2), channels=1, rate=22050, output=True)
    stream.write(data)
    stream.stop_stream()
    stream.close()

def dog_chatbot(user_input, message_history):
    message_history.append({"role": "user", "content": user_input})
    chat_completion = client.chat.completions.create(
        messages=message_history,
        model="gpt-3.5-turbo",
        max_tokens=150
    )
    response = chat_completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": response})

    if len(message_history) > 10:
        message_history = message_history[-10:]

    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=response,
        response_format="wav"
    )
    play_stream(audio_response.content)
    return response, message_history

if __name__ == "__main__":
    message_history = [{"role": "system", "content": "You are a family dog named Asher that provides child safe responses based on the intelligence of a dog. You will receive descriptions of images that are visible through the dog's eyes. Reply with you, as the dog, would say. Do not share your thoughts, just reply with what you would say to engage the human."}]
    capture_image_on_motion(message_history)
