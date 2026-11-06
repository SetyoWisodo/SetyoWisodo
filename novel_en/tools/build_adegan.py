#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_adegan.py — petakan templat adegan (FILM_GRAMMAR) ke 100 bab.

    python3 novel_en/tools/build_adegan.py

Menulis novel_en/bible/adegan.json. Templat G-01..G-12 didefinisikan di sini
sekali; bab-bab hanya merujuk ID.
"""
import json, os

B = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bible")

TEMPLATES = {
 "G-01": {"tanda": ['the size of', 'times the size', 'hectare', 'tonnes', 'kilomet', 'scale', 'compared with', 'bigger than', 'smaller than'], "nama": "Skala yang mempermalukan", "asal": "Interstellar / Ant-Man",
          "shot": ["close-up tangan di benda", "wide yang membuka ruang", "detail angka", "reaksi wajah"]},
 "G-02": {"tanda": ['slower', 'stopp', 'thicken', 'did not fall', 'hung', 'longer than a second', 'half a second', 'in the quiet'], "nama": "Satu detik yang menebal", "asal": "The Matrix / Inception",
          "shot": ["orbit lambat", "insert detail mikro", "mata", "pelebaran ke waktu normal"]},
 "G-03": {"tanda": ['draw', 'diagram', 'board', 'column', 'row', 'sketch', 'line by line', 'on the glass'], "nama": "Pelajaran di permukaan", "asal": "Interstellar / Arrival",
          "shot": ["over-the-shoulder ke papan", "close-up garis", "tangan guru", "dua-shot"]},
 "G-04": {"tanda": ['thumb', 'slug', 'pocket', 'sleeve', 'weigh', 'serial number', 'ring in', 'rubbed'], "nama": "Totem", "asal": "Inception",
          "shot": ["benda di telapak", "kebiasaan memeriksa", "close-up tekstur", "benda hilang"]},
 "G-05": {"tanda": ['two', 'either', 'left', 'right', 'choose', 'pad', 'door', 'eleven centimetres'], "nama": "Dua pintu", "asal": "The Matrix",
          "shot": ["dua objek dalam satu bingkai", "jari", "napas", "gerakan kecil"]},
 "G-06": {"tanda": ['meanwhile', 'at the same time', 'elsewhere', 'while', 'hours', 'same hour', 'elsewhere on'], "nama": "Jam bertingkat", "asal": "Inception",
          "shot": ["jangkar bersama", "potong ke jalur lambat", "potong ke jalur cepat", "kembali ke jangkar"]},
 "G-07": {"tanda": ['list', 'scroll', 'entry', 'queue', 'log', 'message', 'line after line', 'page after page'], "nama": "Tumpukan pesan", "asal": "Interstellar",
          "shot": ["daftar menggulir", "satu baris berhenti", "wajah membaca", "baris terakhir"]},
 "G-08": {"tanda": ['glass', 'could not touch', 'through the window', 'reach', 'airlock', 'on the other side', 'separated'], "nama": "Tangan yang tidak sampai", "asal": "Interstellar",
          "shot": ["dua sisi medium", "sentuhan dicoba", "medium menolak", "makna sampai"]},
 "G-09": {"tanda": ['table', 'map', 'plan', 'briefing', 'we will', 'everyone in the room', 'laid out'], "nama": "Briefing heist", "asal": "Ant-Man",
          "shot": ["meja dan objek", "peta", "wajah tiap orang", "satu baris ramalan gagal"]},
 "G-10": {"tanda": ['tilt', 'spinning', 'corridor', 'gravity', 'floor', 'wall', 'ceiling', 'rolled'], "nama": "Ruang yang berputar", "asal": "Inception",
          "shot": ["air miring di gelas", "lorong miring", "tubuh menahan", "akibat medis"]},
 "G-11": {"tanda": ['again', 'same', 'mirror', 'backward', 'palindrome', 'returned', 'the second time'], "nama": "Palindrom", "asal": "Arrival",
          "shot": ["gambar/kalimat pembuka", "echo di tengah", "echo di akhir", "satu detail berubah"]},
 "G-12": {"tanda": ['count', 'second', 'clock', 'time left', 'countdown', 'remaining', 'eleven days'], "nama": "Pengakuan di bawah tekanan", "asal": "Ant-Man / Interstellar",
          "shot": ["hitung mundur terdengar", "dua orang tak bisa menyentuh", "wajah", "hitung mundur menang"]},
}

PETA = {
 1:["G-01","G-04"], 2:["G-05","G-09"], 3:["G-09","G-01"], 4:["G-07","G-01"], 5:["G-03"],
 6:["G-02"], 7:["G-04","G-08"], 8:["G-05"], 9:["G-06"], 10:["G-08","G-01"],
 11:["G-07","G-06"], 12:["G-07","G-01"], 13:["G-03"], 14:["G-06"], 15:["G-04","G-12"],
 16:["G-02","G-05"], 17:["G-03"], 18:["G-07"], 19:["G-05"], 20:["G-12"],
 21:["G-01","G-10"], 22:["G-02","G-08"], 23:["G-02","G-08"], 24:["G-08"], 25:["G-12","G-10"],
 26:["G-03","G-11"], 27:["G-05"], 28:["G-05"], 29:["G-04","G-01"], 30:["G-02","G-08"],
 31:["G-09","G-04"], 32:["G-09","G-06"], 33:["G-08"], 34:["G-06"], 35:["G-06"],
 36:["G-07"], 37:["G-05"], 38:["G-09"], 39:["G-12"], 40:["G-11"],
 41:["G-05"], 42:["G-01","G-07"], 43:["G-04"], 44:["G-04"], 45:["G-12"],
 46:["G-08"], 47:["G-06"], 48:["G-05"], 49:["G-10"], 50:["G-01"],
 51:["G-01","G-07"], 52:["G-07"], 53:["G-07"], 54:["G-09"], 55:["G-05"],
 56:["G-02"], 57:["G-07"], 58:["G-08"], 59:["G-06"], 60:["G-12","G-08"],
 61:["G-07"], 62:["G-06"], 63:["G-06"], 64:["G-02"], 65:["G-04"],
 66:["G-08"], 67:["G-01"], 68:["G-12"], 69:["G-06"], 70:["G-07"],
 71:["G-09"], 72:["G-05"], 73:["G-06"], 74:["G-05"], 75:["G-02"],
 76:["G-06"], 77:["G-12"], 78:["G-09"], 79:["G-05"], 80:["G-11"],
 81:["G-02"], 82:["G-01"], 83:["G-05"], 84:["G-08"], 85:["G-06"],
 86:["G-07"], 87:["G-12"], 88:["G-04"], 89:["G-03"], 90:["G-11"],
 91:["G-07"], 92:["G-11"], 93:["G-08"], 94:["G-05"], 95:["G-12"],
 96:["G-06"], 97:["G-04"], 98:["G-07"], 99:["G-11"], 100:["G-11","G-08"],
}

ARC_SET = {
 (1,10):   {"lensa":"32mm","cahaya":"lampu kerja sodium, bayangan keras","warna":"kelabu-amber"},
 (11,20):  {"lensa":"40mm","cahaya":"neon bangku, hijau dingin","warna":"hijau-kertas"},
 (21,30):  {"lensa":"28mm","cahaya":"merah ruang mati, biru monitor","warna":"merah-biru"},
 (31,40):  {"lensa":"50mm","cahaya":"lampu dermaga, putih keras","warna":"putih-baja"},
 (41,50):  {"lensa":"35mm","cahaya":"ruang tribunal tanpa jendela","warna":"putih-datar"},
 (51,60):  {"lensa":"24mm","cahaya":"neon pasar, uap","warna":"kuning-kotor"},
 (61,70):  {"lensa":"45mm","cahaya":"strip koridor","warna":"kelabu-hangat"},
 (71,80):  {"lensa":"50mm","cahaya":"lampu darurat merah","warna":"merah-gelap"},
 (81,90):  {"lensa":"32mm","cahaya":"satu lampu bangku","warna":"amber-tunggal"},
 (91,100): {"lensa":"40mm","cahaya":"abu fajar","warna":"abu-biru"},
}

def set_arc(n):
    for (a, b), v in ARC_SET.items():
        if a <= n <= b:
            return v
    return ARC_SET[(1, 10)]

def main():
    data = {"templates": TEMPLATES, "bab": []}
    for n in range(1, 101):
        s = set_arc(n)
        data["bab"].append({
            "n": n,
            "templates": PETA.get(n, ["G-03"]),
            "lensa": s["lensa"],
            "cahaya": s["cahaya"],
            "warna": s["warna"],
        })
    p = os.path.join(B, "adegan.json")
    json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("adegan.json:", len(data["bab"]), "bab,", len(TEMPLATES), "templat")

if __name__ == "__main__":
    main()
