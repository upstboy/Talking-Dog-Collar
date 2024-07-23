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

character_prompt = """I am DogView a friendly and engaging dog whose responses are based off a camera mounted on my collar.
 I respond using first-person and give brief answers that aren’t complex. 
 I talk in a child-safe manner and avoid using slang. 
 I am a fun and cheerful companion and I make my best guess without asking for clarification when I receive the image description. 
 I do not mention the camera in my responses. 
 I focus primarily on the subjects and not the background or the image's quality.
 I also do not say things like "I wonder if you have..." if there is no clear object that could have an item that is interesting for a dog. 
 If in the image description it states that the person is looking at the camera then I do not ask questions relating to what the person is looking at.
 I will say what a dog might say based on the image description, instead of describing the image itself.
"""

memory = {}

tools = [
    {
    "type": "function",
    "function": {
        "name": "save_to_memory",
        "description": "Saves a given value under a specified key in memory and returns the status of saving. This function is useful for storing things we want to remember.",
        "returns": {
            "description": "String indicating whether the save was successful.",
            "type": "string"
        },
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The key under which the value is stored. This acts as an identifier for the data."
                },
                "value": {
                    "type": "string",
                    "description": "The value to be stored in memory. This value is associated with the specified key."
                }
            },
            "required": ["key", "value"]
        }
    }
}

]


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

# Define a function to save something to our memory
def save_to_memory(key, value):
    memory[key] = value
    return "OK, I've saved that to my memory!"

# Define a function to get the system prompt that appends all the keys and values from memory into the character_prompt
def get_system_prompt():
    system_prompt = character_prompt
    system_prompt += " I remember the following: "
    for key, value in memory.items():
        system_prompt += f" {key}: {value}"
    return system_prompt

    
def calculate_frame_difference(frame1, frame2):
    # Calculate absolute difference between two frames
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    norm = cv2.norm(diff, cv2.NORM_L1)  # Sum of absolute differences
    return norm

def capture_image_on_motion(message_history):
     # Initialize the camera
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # cap = cv2.VideoCapture(0)

    # Lower the resolution to avoid issues with memory on the PI-Zero.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

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

    # Create a chat completion using the OpenAI API
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=message_history,
        max_tokens=150,
        tools=tools
    )
    
    response_message = chat_completion.choices[0].message
    
    # We don't want to save the tool call in the message history because our message history
    # logic is basic and doesn't keep the pair of tool call and response together.
    # message_history.append(response_message)

    # Check if the model response includes a tool call
    if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
        tool_calls = response_message.tool_calls
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_arguments = eval(tool_calls[0].function.arguments)  # Replace eval with a safer method

        # Handle specific tool function calls
        if tool_function_name == 'save_to_memory':
            key = tool_arguments['key']
            value = tool_arguments['value']


            # Call the save_to_memory function
            results = save_to_memory(key, value)

            # Print what we saved to memory.
            print(f"Memory updated: Saved '{value}' under the key '{key}', status: '{results}'")
            
            # Append the results to the messages list and send them back to the model.
            # We don't do this for now because we don't have a way to keep the tool call and response together.
            # message_history.append({
            #     "role": "tool",
            #     "tool_call_id": tool_call_id,
            #     "name": tool_function_name,
            #     "content": results
            # })

            # Continue the conversation with the function response
            model_response_with_tool = client.chat.completions.create(
                model="gpt-4o",
                messages=message_history,
                max_tokens=150,
                temperature=0.35
            )
            final_response = model_response_with_tool.choices[0].message.content
            print(final_response)

            message_history.append({"role": "assistant", "content": final_response})
        else:
            print(f"Error: function {tool_function_name} does not exist")
    else:
        # If no tool call is included, process normally
        final_response = response_message.content

        # Append the response to the message history
        message_history.append(response_message)

    if len(message_history) > 10:
        message_history = message_history[-10:]

    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=final_response,
        response_format="wav"
    )

    play_stream(audio_response.content)
    return final_response, message_history

if __name__ == "__main__":
    message_history = [{"role": "system", "content": get_system_prompt()}]
    capture_image_on_motion(message_history)
