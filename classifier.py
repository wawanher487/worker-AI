import dlib
import cv2
import os
import numpy as np
import requests
from io import BytesIO
from PIL import Image

# Path ke model Dlib
MODEL_DIR = os.path.join(os.getcwd(), ".face_recognition")
SHAPE_PREDICTOR_PATH = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
FACE_RECOGNITION_MODEL_PATH = os.path.join(MODEL_DIR, "dlib_face_recognition_resnet_model_v1.dat")

# Inisialisasi model deteksi dan ekstraksi wajah
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
face_rec_model = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)

# Fungsi bantu: membaca gambar dari URL atau lokal
def read_image_from_path_or_url(path_or_url):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        try:
            response = requests.get(path_or_url, timeout=10)
            print("[DEBUG] HTTP Status Code:", response.status_code)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"[ERROR] Gagal unduh gambar dari URL: {e}")
            return None
    else:
        return cv2.imread(path_or_url)

# Load semua gambar dari dataset
DATASET_FOLDER = "dataset"
known_face_encodings = []
known_face_names = []

for filename in os.listdir(DATASET_FOLDER):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        path = os.path.join(DATASET_FOLDER, filename)
        image = cv2.imread(path)
        if image is None:
            print(f"[WARNING] Tidak bisa membaca {filename}")
            continue

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = face_detector(rgb_image)

        if faces:
            shape = shape_predictor(rgb_image, faces[0])
            face_encoding = np.array(face_rec_model.compute_face_descriptor(rgb_image, shape))
            known_face_encodings.append(face_encoding)
            name = os.path.splitext(filename)[0]
            known_face_names.append(name)
        else:
            print(f"[WARNING] Tidak ada wajah terdeteksi di: {filename}")

# Fungsi utama klasifikasi
def run_classification(image_path_or_url):
    print(f"Klasifikasi berdasarkan gambar: {image_path_or_url}")
    try:
        image = read_image_from_path_or_url(image_path_or_url)
        if image is None:
            print("[ERROR] Gagal membaca gambar dari path/URL")
            return {
                "nama": "unknown",
                "mood": "unknown",
                "keletihan": 0,
                "userGuid": "unknown",
                "unit": "tidak diketahui",  # fallback agar tidak kosong
                "status_absen": "tidak dikenali"
            }

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = face_detector(rgb_image)

        for face in faces:
            shape = shape_predictor(rgb_image, face)
            face_encoding = np.array(face_rec_model.compute_face_descriptor(rgb_image, shape))

            distances = [np.linalg.norm(face_encoding - known) for known in known_face_encodings]
            if distances:
                best_match_idx = np.argmin(distances)
                if distances[best_match_idx] < 0.6:
                    nama = known_face_names[best_match_idx]
                    return {
                        "nama": nama,
                        "mood": "senang",
                        "keletihan": np.random.randint(40, 80),
                        "userGuid": f"mock-guid-{nama}",
                        "unit": "karyawan",
                    }

        return {
            "nama": "unknown",
            "mood": "tidak diketahui",
            "keletihan": 0,
            "userGuid": "unknown",
            "unit": "tidak diketahui",  # fallback agar tidak kosong
            "status_absen": "tidak dikenali"
        }

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat klasifikasi: {e}")
        return {
            "nama": "error",
            "mood": "error",
            "keletihan": 0,
            "userGuid": "error",
            "unit": "tidak diketahui",
            "status_absen": "gagal"
        }
