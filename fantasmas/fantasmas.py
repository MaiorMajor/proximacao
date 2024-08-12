import cv2
import mediapipe as mp
import numpy as np

# Configuração inicial do MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Inicialização da câmera em 720p
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Configurações para exibir em tela cheia
cv2.namedWindow('MediaPipe Faces', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('MediaPipe Faces', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# Função simplificada para desenhar partículas
def draw_particles(image, particles):
    for particle in particles:
        if particle['life'] > 0:
            cv2.circle(image, (particle['x'], particle['y']), 2, (0, 0, 255), -1)
            particle['life'] -= 1
            particle['x'] += np.random.randint(-1, 2)
            particle['y'] += np.random.randint(-1, 2)


particles = []
DETECTION_SKIP_FRAMES = 2
frame_counter = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip horizontal na imagem
    frame = cv2.flip(frame, 1)

    # Cria uma imagem preta com as mesmas dimensões da frame capturada
    black_background = np.zeros_like(frame)

    frame_counter += 1
    if frame_counter % DETECTION_SKIP_FRAMES == 0:
        # Processamento do MediaPipe
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for landmark in results.multi_face_landmarks[0].landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                particles.append({'x': x, 'y': y, 'life': 20})

    draw_particles(black_background, particles)  # Desenha as partículas no fundo preto em vez da frame capturada
    cv2.imshow('MediaPipe Faces', black_background)

    # Limpa partículas antigas
    particles = [p for p in particles if p['life'] > 0]

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
