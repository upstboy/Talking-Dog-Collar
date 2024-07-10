import cv2
import numpy as np
import base64
import os
import pyaudio
from io import BytesIO
from openai import OpenAI
import time

# Initialize OpenAI and PyAudio clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
p = pyaudio.PyAudio()

difference_threshold = 500000
character_prompt = "I am DogView, a friendly and engaging companion who describes images from a camera mounted on my collar. I respond in a first-person view with brief, simple, and family-friendly descriptions, avoiding complex words and slang. My goal is to provide clear, engaging, and easy-to-understand explanations of what I see through the camera. I use simple words that anybody can understand and talk in a child-friendly manner, avoiding any slang like 'af.' My tone is playful and cheerful, much like Doug from the Pixar movie Up. I make the best guess and keep going without asking for clarification. When provided with an image description, I respond in a playful and engaging manner. For example, if the description is: 'The image shows the top part of a room with a focus on two individuals. One person on the left is looking into the camera and wearing glasses. The person on the right is partially visible, mostly their head and part of their face. The background includes ceiling lights, a ceiling fan, and decor on the walls, including what appears to be some framed artwork. The walls are a mix of beige and reddish-brown colors.' I would respond with: 'Hi there you two! Do you guys want to play with me!'"

def encode_image_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    io_buf = BytesIO(buffer)
    return base64.b64encode(io_buf.getvalue()).decode('utf-8')

def get_image_description(image_b64):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are the eyes of a dog."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
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

def get_latest_frame(cap):
    # Clear the buffer by grabbing several frames quickly
    for _ in range(5):
        cap.grab()

    # Retrieve the latest frame
    ret, latest_frame = cap.retrieve()
    if not ret:
        print("Failed to retrieve the frame.")
        return None
    return latest_frame



def calculate_frame_difference(frame1, frame2):
    # Calculate absolute difference between two frames
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    norm = cv2.norm(diff, cv2.NORM_L1)  # Sum of absolute differences
    return norm

def capture_image_on_motion(message_history):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    initial_buffer_size = 7  # Minimum frames to start processing
    frame_buffer = []
    last_described_frame = None
    processing_time = 0.1  # Initialize with a reasonable guess to avoid division by zero

    while True:
        start_time = time.time()

        # Read the current frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from webcam.")
            continue

        frame_buffer.append(frame)
        dynamic_buffer_size = max(int(cap.get(cv2.CAP_PROP_FPS) * processing_time), initial_buffer_size)

        if len(frame_buffer) > dynamic_buffer_size:
            frame_buffer = frame_buffer[-dynamic_buffer_size:]  # Maintain the buffer size

        # Process frame only if buffer has at least the initial buffer size
        if len(frame_buffer) >= initial_buffer_size:
            current_index = len(frame_buffer) // 2
            current_frame = frame_buffer[current_index]

            if last_described_frame is not None:
                differences = [calculate_frame_difference(current_frame, f) for f in frame_buffer]
                most_different_frame = frame_buffer[np.argmax(differences)]

                if np.max(differences) > difference_threshold:  # Define a suitable threshold

                    # Print that we are processing a frame out of the buffer and print it's size
                    print("Processing frame:", current_index, "Buffer size:", len(frame_buffer))

                    image_b64 = encode_image_to_base64(most_different_frame)
                    description = get_image_description(image_b64)
                    print("Image description:", description)
                    response, message_history = dog_chatbot(description, message_history)
                    print("DogBot:", response)
                    last_described_frame = most_different_frame

                    # Clear the frame buffer after processing
                    frame_buffer.clear()
            else:
                last_described_frame = current_frame  # Initialize the last described frame

        # Update processing time for next iteration
        processing_time = time.time() - start_time

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
    message_history = [{"role": "system", "content": character_prompt}]
    capture_image_on_motion(message_history)
