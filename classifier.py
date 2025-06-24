import random

def classify_face(image_url):
    print("Klasifikasi berdasarkan gambar:", image_url)
    return {
        "nama": "ade",
        "mood": random.choice(["senang", "sedih", "marah"]),
        "keletihan": random.randint(50, 90),
        "userGuid": "27e66e1a-aa5f-4f0b-9418-9a77fcb02810",
        "unit": "karyawan",
        "status_absen": "hadir"
    }
