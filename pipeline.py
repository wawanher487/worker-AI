from classifier import run_classification
from datetime import datetime, time, timedelta
from sender import send_to_api

def run_pipeline(data):
    filename = data.get("gambar")

    # 1. Buat URL gambar
    image_url = f"https://monja-file.pptik.id/v1/view?path=presensi/{filename}"

    # 2. Jalankan klasifikasi wajah dari URL
    hasil = run_classification(image_url)

    #cek status absensi
    #Konversi waktu string ke datetime
    try:
        waktu_absen = datetime.strptime(data["datetime"], "%d-%m-%Y %H:%M:%S")
    except ValueError as e:
        print(f"[ERROR] Format datetime salah: {data.get('datetime')}")
        return

    jam_normal = datetime.combine(waktu_absen.date(), time(8, 0, 0)) # Jam masuk normal
    jam_pulang = datetime.combine(waktu_absen.date(), time(17, 0, 0)) # Jam pulang normal

    if waktu_absen <= jam_pulang:
        # Kehadiran (bisa tepat waktu atau terlambat)
        if waktu_absen > jam_normal:
            status_absen = "terlambat"
            selisih = waktu_absen - jam_normal
            total_jam_telat = round(selisih.total_seconds() / 3600, 2)  # Jam desimal
        else:
            status_absen = "hadir"
            total_jam_telat = 0

        jam_masuk_actual = waktu_absen.strftime("%H:%M:%S")
        jam_keluar_actual = "-"
    else:
        # Pulang
        status_absen = "pulang"
        jam_masuk_actual = "-"
        jam_keluar_actual = waktu_absen.strftime("%H:%M:%S")
        total_jam_telat = 0


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
        "jam_masuk_actual": jam_masuk_actual,
        "jam_keluar_actual":  jam_keluar_actual,
        "status_absen": status_absen,
        "jumlah_telat": 0,
        "total_jam_telat": total_jam_telat,
    }

    # 4. Kirim ke API Laravel
    send_to_api(payload)
