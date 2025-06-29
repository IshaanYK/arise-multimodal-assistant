import cv2
import mediapipe as mp
import time
from state_manager import is_awake

def detect_hand_wave(trigger_callback):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    print("Camera on... Wave your hand to wake ARISE.")

    wave_count = 0
    wave_triggered = False
    last_wave_time = 0

    while True:
        success, img = cap.read()
        if not success:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            now = time.time()
            if now - last_wave_time > 2:
                wave_count += 1
                print("Hand detected - wave count:", wave_count)
                last_wave_time = now

            if wave_count >= 2 and not wave_triggered:
                print("Hand wave detected! Waking ARISE...")
                wave_triggered = True
                cap.release()
                cv2.destroyAllWindows()
                trigger_callback()
                break

        cv2.imshow("ARISE Hand Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
