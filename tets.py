import cv2
import dlib

# Load detector dan shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Baca gambar
image = cv2.imread("image.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Deteksi wajah
faces = detector(gray)
for face in faces:
    landmarks = predictor(gray, face)
    for n in range(0, 68):  # total 68 titik
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

# Tampilkan hasil
cv2.imshow("Landmarks", image)
cv2.waitKey(0)
cv2.destroyAllWindows()