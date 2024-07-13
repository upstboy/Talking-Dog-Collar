import cv2
import numpy as np
import base64
from io import BytesIO
import os
import openai

def encode_image_to_base64(frame):
    # Convert the image to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    io_buf = BytesIO(buffer)

    # Encode the image as base64
    return base64.b64encode(io_buf.getvalue()).decode('utf-8')

def get_image_description(image_b64):
    # Set up the OpenAI API client sk-proj-i4ZRIPF2Dj3SsXXXXajLT3BlbkFJXFYT9d8wUDXDtmy484kb
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
    
    return response.choices[0].message.content

def capture_image_on_motion():
    # Initialize the camera
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    # Lower the resolution to avoid issues with memory on the PI-Zero.
    cap.CAP_PROP_FRAME_WIDTH = 320
    cap.CAP_PROP_FRAME_HEIGHT = 240

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Read the first frame
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
                description = get_image_description(image_b64)
                print("Image description:", description)

        gray1 = gray2.copy()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image_on_motion()
