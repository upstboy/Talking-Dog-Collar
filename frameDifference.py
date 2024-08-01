import cv2
import numpy as np

def calculate_frame_difference(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Calculate the absolute difference between the two frames
    diff = cv2.absdiff(gray1, gray2)
    
    # Optionally, apply a threshold to the difference to highlight significant changes
    _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # Calculate the sum of absolute differences
    norm = np.sum(diff)  # Using numpy sum to add up pixel values
    
    return norm

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Read the first frame
    ret, last_frame = cap.read()
    if not ret:
        print("Failed to read the first frame.")
        return

    try:
        while True:
            # Read the next frame
            ret, current_frame = cap.read()
            if not ret:
                print("Failed to read a frame.")
                break

            # Calculate the frame difference
            difference = calculate_frame_difference(last_frame, current_frame)
            print("Frame Difference:", difference)

            # Update last_frame to the current frame for the next iteration
            last_frame = current_frame

            # Display the frame (optional)
            cv2.imshow('Frame', current_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
