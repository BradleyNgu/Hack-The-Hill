import cv2
import mediapipe as mp
import time
from math import sqrt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def calculateDistance(landmark1, landmark2):
    return sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2 + (landmark1.z - landmark2.z)**2)


def recognizeGesture(handedness):
    wrist = hand_landmarks.landmark[0]
    thumb1 = hand_landmarks.landmark[1]
    thumb2 = hand_landmarks.landmark[2]
    thumb3 = hand_landmarks.landmark[3]
    thumb4 = hand_landmarks.landmark[4]
    index1 = hand_landmarks.landmark[5]
    index2 = hand_landmarks.landmark[6]
    index3 = hand_landmarks.landmark[7]
    index4 = hand_landmarks.landmark[8]
    middle1 = hand_landmarks.landmark[9]
    middle2 = hand_landmarks.landmark[10]
    middle3 = hand_landmarks.landmark[11]
    middle4 = hand_landmarks.landmark[12]
    ring1 = hand_landmarks.landmark[13]
    ring2 = hand_landmarks.landmark[14]
    ring3 = hand_landmarks.landmark[15]
    ring4 = hand_landmarks.landmark[16]
    pinky1 = hand_landmarks.landmark[17]
    pinky2 = hand_landmarks.landmark[18]
    pinky3 = hand_landmarks.landmark[19]
    pinky4 = hand_landmarks.landmark[20]

    totalFingers = 5

    # Check index, middle, or ring fingers are extended
    for tip in [index4, middle4, ring4]:
        for i in range(21):
            # brute force method
            if i in [8, 12, 16]:
                continue

            if tip.y > hand_landmarks.landmark[i].y:
                totalFingers -= 1
                break

    # Check if pinky extended
    if not (pinky4.y < middle1.y and pinky4.y < pinky3.y):
        totalFingers -= 1

    # Check if thumb extended
    # Right hand

    # print(f"{thumb1.x} vs {thumb2.x} vs {thumb3.x} vs {thumb4.x}")
    # 0.6111839413642883 vs 0.5484028458595276 vs 0.4903261661529541 vs 0.43976545333862305
    
    if handedness == "Right":
        if not(thumb1.x >= thumb4.x*1.3): # may need to adjust number
            totalFingers -= 1

    # Left hand
    else:
        if not(thumb1.x <= thumb4.x*0.65): # may need to adjust number
            totalFingers -= 1

    # print(handedness)
    # print(f"{thumb1.x} vs {thumb2.x} vs {thumb3.x} vs {thumb4.x}")
    print(f"{totalFingers} fingers up")
    return totalFingers


    # for i in range(0, 21):
    #     print(f"Landmark {i}: x={hand_landmarks.landmark[i].x:.4f}, y={hand_landmarks.landmark[i].y:.4f}, z={hand_landmarks.landmark[i].z:.4f}")
        
    


# For webcam input:
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
    stability_duration = 2.0  # Seconds

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
                        elif time.time() - stable_start_time >= stability_duration:
                            print("Hand Landmarks (stable for 2 seconds):")
                            recognizeGesture(handedness)
                            stable_start_time = None  # Reset timer after printing
                    else:
                        stable_start_time = None
                
                last_landmarks = hand_landmarks

        cv2.imshow('MediaPipe Hands', image)

        # quit if user presses "Esc"
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()