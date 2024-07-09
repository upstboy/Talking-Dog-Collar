import cv2
import base64
from io import BytesIO
import os
import openai

def capture_image():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return None

    # Capture a frame
    ret, frame = cap.read()
    cap.release()  # Release the webcam
    if not ret:
        print("Failed to capture image")
        return None
    
    # Save the image to disk
    cv2.imwrite('captured_image.jpg', frame)


    return frame

def encode_image_to_base64(frame):
    # Convert the image to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    io_buf = BytesIO(buffer)

    # Encode the image as base64
    return base64.b64encode(io_buf.getvalue()).decode('utf-8')

def get_image_description(image_b64):
    # Set up the OpenAI API client
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Send the image to the GPT-4o model
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a highly capable visual assistant."},
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
    
    #return response.choices[0].message['content']
    return response.choices[0].message.content


def main():
    frame = capture_image()
    if frame is not None:
        image_b64 = encode_image_to_base64(frame)
        description = get_image_description(image_b64)
        print("Image description:", description)
    else:
        print("No image to process.")

if __name__ == "__main__":
    main()
