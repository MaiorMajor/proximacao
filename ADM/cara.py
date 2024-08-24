import cv2
import mediapipe as mp
import numpy as np
# Configura as soluções do mp hands e face
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Configura captura de video com webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1024)
cap.set(4, 768)
cap.set(cv2.CAP_PROP_FPS, 30)

# Para a gravação num ficheiro mp4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = None
is_recording = False
fps = 30
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Enquanto captura estiver ativa
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("A ignorar frame vazio.")
        continue
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converter para RGB
    image_rgb.flags.writeable = False
    results_face = face_mesh.process(image_rgb)
    results_hands = hands.process(image_rgb)
    image_rgb.flags.writeable = True
    black_image = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    
    # Desenhar para cada ponto facial com func draw_landmarks 
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                black_image,
                face_landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                None,
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1))
            
    # Desenhar pontos de ref mãos com HAND_CONNECTIONS
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                black_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                None,  # Sem landmark_drawing_spec
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

    if is_recording:
        video_writer.write(black_image)

    cv2.imshow('MediaPipe Detection', black_image)
    
    # Verifica interaçao do utilizador com teclas
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        if is_recording:
            is_recording = False
            video_writer.release()
            print("Gravação parada.")
        else:
            is_recording = True
            video_writer = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))
            print("Gravação iniciada.")
    elif key == 27:
        break
# Termina gravação
if is_recording:
    video_writer.release()
# Liberta recursos e fecha programa
cap.release()
cv2.destroyAllWindows()
hands.close()
face_mesh.close()
