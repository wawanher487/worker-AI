from classifier import classify_face
from sender import send_to_api

def run_pipeline(data):
    filename = data.get("gambar")

    # 1. Buat URL gambar
    image_url = f"https://monja-file.pptik.id/v1/view?path=presensi/{filename}"

    # 2. Jalankan klasifikasi wajah dari URL
    hasil = classify_face(image_url)

    # 3. Gabungkan hasil klasifikasi dengan metadata dari worker 1
    payload = {
        **hasil,
        "guid": data["guid"],
        "guid_device": data["guid_device"],
        "gambar": filename,
       "timestamp": int(data["timestamp"]),
        "datetime": data["datetime"],
        "process": "done",
        "jam_masuk": "08:00:00",
        "jam_keluar": "17:00:00",
        "jam_masuk_actual": data["datetime"].split(" ")[1],
        "jam_keluar_actual": data["datetime"].split(" ")[1],
        "jumlah_telat": 0,
        "total_jam_telat": 0,
    }

    # 4. Kirim ke API Laravel
    send_to_api(payload)
