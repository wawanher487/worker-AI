import os
from classifier import classify_face
from sender import send_to_api
from dotenv import load_dotenv
import uuid
import datetime

load_dotenv()

def run_pipeline(payload):
    filename = payload["gambar"]  # sebelumnya "value"
    image_path = f"https://monja-file.pptik.id/v1/view?path=presensi/{filename}"

     # Kirim ke classifier
    klasifikasi = classify_face(image_url)

    result = {
        "guid": payload["guid"],
        "guid_device": payload["guid_device"],
        "datetime": payload["datetime"],
        "timestamp": int(payload["timestamp"]),
        "gambar": filename,
        "process": "done",
        "jam_masuk": "08:00:00",
        "jam_keluar": "17:00:00",
        "jam_masuk_actual": payload["datetime"].split(" ")[1],  # ambil jam saja
        "jam_keluar_actual": payload["datetime"].split(" ")[1],
        "jumlah_telat": 0,
        "total_jam_telat": 0,
        **klasifikasi
    }

    send_to_api(result)


if __name__ == "__main__":
    dummy = {
        "value": "CAM-P020-AbcdEf.jpg",
        "guid": str(uuid.uuid4()),
        "guid_device": "CAM-P020"
    }
    run_pipeline(dummy)
