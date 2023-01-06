# Hand Gesture Recognition ✊✋✌️

The code imports the necessary libraries for image processing (OpenCV) and hand detection (MediaPipe).

It defines a class called **handDetector** for detecting hands in video frames and counting the number of fingers being held up.

The __init__ function initializes the hand detector with several parameters for configuring the hand detection process, including the maximum number of hands to detect, the model complexity, and the detection and tracking confidence thresholds.

The **find_Hands** function processes a frame and uses the MediaPipe Hands solution to detect hands and their landmarks in the frame. It also has an option to draw the detected hand landmarks on the frame.

The **find_Position** function uses the detected landmarks to determine the positions of specific points on the hand. It has an option to draw the positions on the frame.

The **count_Finger** function uses the positions of the hand landmarks to count the number of fingers being held up. It returns a list of binary values indicating which fingers are being held up.

The **frame_rate** function calculates the frame rate at which the webcam is capturing frames.

The main function captures video frames from a webcam and processes each frame using the handDetector class. It displays the resulting frames with hand landmarks and finger count overlaid on the frame, and also displays the frame rate. The loop continues until the user terminates the program.
