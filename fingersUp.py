import cv2
import mediapipe as mp
import time
from math import sqrt
import serial



def sendDataToArduino(data):
    arduino.write(bytes(data, 'utf-8'))  # Send data to Arduino as a string
    time.sleep(0.05)  # Delay to avoid overwhelming the serial communication


def calculateDistance(landmark1, landmark2):
    return sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2 + (landmark1.z - landmark2.z)**2)


def recognizeGesture(handedness, hand_landmarks):
    # Unused points are commented out
    # wrist = hand_landmarks.landmark[0]
    # thumb1 = hand_landmarks.landmark[1]
    # thumb2 = hand_landmarks.landmark[2]
    thumb3 = hand_landmarks.landmark[3]
    thumb4 = hand_landmarks.landmark[4]
    # index1 = hand_landmarks.landmark[5]
    # index2 = hand_landmarks.landmark[6]
    index3 = hand_landmarks.landmark[7]
    index4 = hand_landmarks.landmark[8]
    middle1 = hand_landmarks.landmark[9]
    # middle2 = hand_landmarks.landmark[10]
    middle3 = hand_landmarks.landmark[11]
    middle4 = hand_landmarks.landmark[12]
    # ring1 = hand_landmarks.landmark[13]
    # ring2 = hand_landmarks.landmark[14]
    ring3 = hand_landmarks.landmark[15]
    ring4 = hand_landmarks.landmark[16]
    # pinky1 = hand_landmarks.landmark[17]
    # pinky2 = hand_landmarks.landmark[18]
    pinky3 = hand_landmarks.landmark[19]
    pinky4 = hand_landmarks.landmark[20]


    totalFingers = 0

    # Check if index extended
    if index4.y < middle3.y and index4.y < index3.y:
        totalFingers += 1

    # Check if middle extended
    if middle4.y < middle3.y and middle4.y < index4.y and middle4.y < ring4.y:
        totalFingers += 1

    # Check if ring extended
    if ring4.y < middle3.y and ring4.y < ring3.y:
        totalFingers += 1

    # Check if pinky extended
    if pinky4.y < middle1.y and pinky4.y < pinky3.y:
        totalFingers += 1

    # Check if thumb extended
    if handedness == "Right":
        if thumb4.x < thumb3.x:
            totalFingers += 1
    else:  # handedness == "Left"
        if thumb4.x > thumb3.x:
            totalFingers += 1


    print(f"Fingers up == {totalFingers}")
    
    # Send the number of fingers to Arduino
    sendDataToArduino(str(totalFingers))

    return totalFingers


def startMediaPipe():
    # Set up the serial communication (adjust the port and baud rate as needed)
    arduino = serial.Serial(port='/dev/cu.usbmodem101', baudrate=9600, timeout=.1)  # Adjust 'COM3' to your Arduino's port


    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # For webcam input
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        # Variables for tracking hand stability
        last_landmarks = None
        stable_start_time = None
        stability_threshold = 0.01  # Adjust this value to change sensitivity
        stability_duration = 1.5  # In seconds
        read_time = None
        read_delay = 10

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.flip(image, 1)
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                handedness = results.multi_handedness[0].classification[0].label

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    # Check stability
                    if last_landmarks is not None:
                        distance = calculateDistance(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST],
                            last_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                        )

                        if distance < stability_threshold:
                            if stable_start_time is None:
                                stable_start_time = time.time()
                            if (time.time() - stable_start_time >= stability_duration) and (read_time is None or (time.time() - read_time >= read_delay)):
                                read_time = time.time()
                                print(f"Hands stable for {stability_duration} seconds. Please wait {read_delay} seconds for further reads.")
                                recognizeGesture(handedness, hand_landmarks)
                                stable_start_time = None  # Reset timer after gesture is recognized
                        else:
                            stable_start_time = None

                    last_landmarks = hand_landmarks

            cv2.imshow('MediaPipe Hands', image)

            # Quit if user presses "Esc"
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()


def main():
    startMediaPipe()



if __name__ == "__main__":
    main()
