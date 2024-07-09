import cv2
import numpy as np

def capture_image_on_motion():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Read the first frame
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        return
    
    # Convert frame to grayscale and apply Gaussian blur
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    while True:
        # Read the next frame
        ret, frame2 = cap.read()
        if not ret:
            print("Failed to read from webcam.")
            break

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Calculate the difference between each frame
        delta_frame = cv2.absdiff(gray1, gray2)
        # Threshold the delta image to get the regions with significant changes
        thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours of the filtered frame
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Motion detection condition based on the size of the contours
        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                motion_detected = True
                print("Motion detected. Capturing image...")
                cv2.imwrite('motion_detected.jpg', frame2)
                cv2.imshow('Motion Detected', frame2)

        if not motion_detected:
            print("No motion detected.")

        # Update the reference frame
        gray1 = gray2.copy()

        # Show the result in a window
        cv2.imshow('Real Time', frame2)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Check for 'q' to quit
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image_on_motion()
