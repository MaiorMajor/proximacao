import cv2
import mediapipe as mp

class FaceTracker:
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(0)  # Inicia a captura
        # Define a resolução desejada
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Verifica se a resolução foi aplicada
        actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Resolução definida: {actual_width} x {actual_height}")

        # Inicializa MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False, 
            max_num_faces=1, 
            min_detection_confidence=0.5
        )

    def track_landmark(self):
        success, image = self.cap.read()
        if not success:
            return None  # Falha na captura da imagem
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmark = face_landmarks.landmark[168]  # Obtém o landmark 168
                # Converte coordenadas relativas em coordenadas absolutas da imagem
                h, w, _ = image.shape
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                return x, y
        return None

    def release(self):
        self.cap.release()

# Exemplo de utilização
if __name__ == '__main__':
    tracker = FaceTracker()
    try:
        while True:
            landmark_position = tracker.track_landmark()
            if landmark_position:
                print("Posição do landmark 168:", landmark_position)
            else:
                print("Rosto não detectado.")
    except KeyboardInterrupt:
        print("Interrompido pelo utilizador.")
    finally:
        tracker.release()
