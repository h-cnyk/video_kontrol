#!/usr/bin/env python
# coding: utf-8

# In[10]:


import cv2
import mediapipe as mp
import pyautogui
import math
import time


try:
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_drawing
except ImportError:
    import mediapipe.solutions.hands as mp_hands
    import mediapipe.solutions.drawing_utils as mp_drawing


hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.8, 
    min_tracking_confidence=0.8
)


last_action_time = 0
cooldown = 0.8  

def parmak_say(hand_landmarks):
    tips = [8, 12, 16, 20]
    count = 0
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count

cap = cv2.VideoCapture(0)

print("--- AKILLI VİDEO KONTROL SİSTEMİ AKTİF ---")
print("1. Ses Kontrolü: Sadece İşaret Parmağı Havada")
print("2. Oynat/Durdur: Sadece Baş Parmak Havada (Beğeni İşareti)")
print("3. 10 SN İleri: El Tamamen Açık (5 Parmak)")
print("4. Çıkış: Kamera ekranında 'q' tuşuna basın.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            count = parmak_say(hand_landmarks)
            current_time = time.time()
            
            
            if count == 5:
                if current_time - last_action_time > cooldown:
                    pyautogui.press('l')
                    last_action_time = current_time
                cv2.putText(frame, "VIDEO 10 SN ILERI", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
            
           
            elif count == 1 and hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y:
                if current_time - last_action_time > cooldown:
                    pyautogui.press('space')
                    last_action_time = current_time
                cv2.putText(frame, "VIDEO OYNAT / DURDUR", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
            
            elif count == 1:
                thumb = hand_landmarks.landmark[4]
                index = hand_landmarks.landmark[8]
                x1, y1 = int(thumb.x * w), int(thumb.y * h)
                x2, y2 = int(index.x * w), int(index.y * h)
                distance = math.hypot(x2 - x1, y2 - y1)
                
                
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(frame, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
                
            
                if distance < 80:
                    pyautogui.press('volumedown')
                    cv2.putText(frame, "SES KISILIYOR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
                
                elif distance > 160:
                    pyautogui.press('volumeup')
                    cv2.putText(frame, "SES ACILIYOR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


    cv2.imshow('Final Akilli Kontrol Paneli', frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# In[ ]:


l

