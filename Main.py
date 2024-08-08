import cv2
import numpy as np
import time
import mediapipe as mp
import volume
import math
# Inicialização do Mediapipe com confiança mínima de detecção
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.9)
mpDraw = mp.solutions.drawing_utils

# Configurações da câmera
wCam, hCam = 460, 460
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
PTime = 0
# Definir cores e espessuras personalizadas
landmark_color = (0, 0, 255)  # Verde para pontos (landmarks)
connection_color = (0, 255, 0)  # Azul para conexões
landmark_thickness = 3  # Espessura dos pontos
connection_thickness = 1  # Espessura das conexões

#print(volume.get_volume())
maxVol = 100 #volume.get_volume()
minVol = 0 #volume.get_volume()

while True:
    success, img = cap.read()
    if not success:
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Desenhar marcações das mãos com cores personalizadas
            mpDraw.draw_landmarks(
                img, 
                handLms, 
                mpHands.HAND_CONNECTIONS, 
                mpDraw.DrawingSpec(color=landmark_color, thickness=landmark_thickness, circle_radius=2),
                mpDraw.DrawingSpec(color=connection_color, thickness=connection_thickness)
            )
            
            # Criar lista de posições dos landmarks
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            
            # Imprimir a lista de posições dos landmarks
            if lmList:
                #print(lmList[4], lmList[8])
                
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1+x2) // 2, (y1+y2) // 2
                
                cv2.circle(img, (x1, y1), 14, (255,0,255), cv2.FILLED)  # Corrigido: y1 em vez de y2
                cv2.circle(img, (x2, y2), 14, (255,0,255), cv2.FILLED)
                cv2.line(img, (x1,y1), (x2, y2), (255,0,255), 3)
                cv2.circle(img, (cx, cy), 15, (0,255,255), cv2.FILLED)

                length = math.hypot(x2 - x1, x2 -y1)
                #print(length)

                vol = np.interp(length,[50, 350], [minVol, maxVol])
                valInt = int(vol)
                print(valInt)
                if length <=50:
                    #volume.set_volume(valInt)
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    cTime = time.time()
    fps = 1 / (cTime - PTime)
    PTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Detector de maos", img)
    cv2.waitKey(1)
