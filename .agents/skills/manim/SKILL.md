---
name: manim
description: Animasi diagram dan rumus yang presisi pakai Manim Community — grafik fungsi, transformasi bentuk, persamaan bergerak, dan penjelasan bertahap. Dipakai saat angka dan geometri harus benar secara matematis, bukan digambar dengan mata.
license: MIT · ManimCommunity/manim · commit ab7f9527fa2b
---

# Manim — diagram yang jujur

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/ManimCommunity/manim> |
| Bintang saat dicatat | 42.657 |
| Lisensi | MIT |
| Commit yang dibaca | `ab7f9527fa2b` |
| Pasang | `pip install manim` (butuh ffmpeg + LaTeX untuk rumus) |

## 1. Kapan dipakai

**Pakai** kalau yang bergerak adalah **matematika**: kemiringan kurva ekstraksi, diagram
profil sangrai, grafik harga terhadap berat, skala rasio seduhan.

**Jangan** pakai untuk video produk atau tipografi — itu Remotion/GSAP. Manim lambat
disetel dan hasilnya bergaya "kelas matematika", bukan brand.

## 2. Kerangka minimum

```python
from manim import *

class ProfilSangrai(Scene):
    def construct(self):
        sumbu = Axes(x_range=[0, 12, 2], y_range=[0, 240, 60],
                     axis_config={"include_numbers": True}, tips=False)
        kurva = sumbu.plot(lambda t: 40 + 200 / (1 + np.exp(-(t - 6) * 1.6)), color="#E1542B")
        self.play(Create(sumbu), run_time=1)
        self.play(Create(kurva), run_time=2)
        label = MathTex(r"T_{akhir} = 212^\circ").to_edge(UP)
        self.play(Write(label))
        self.wait(1)
```

Render: `manim -pqh profil.py ProfilSangrai` → `media/videos/.../ProfilSangrai.mp4`.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Gagal render rumus | LaTeX tidak terpasang | `pip install` TeX terpisah, atau hindari `MathTex` |
| Video 4:3 padahal butuh 9:16 | konfigurasi default | `config.frame_width/height` atau `-r 1080,1920` |
| Warna meleset dari brand | hex tanpa `#` atau format RGB | `color="#E1542B"` |
| Render 20 menit | `-ql` untuk uji, `-qh` untuk jadi | uji di `-ql` dulu |
| Font beda tiap mesin | font sistem | `Text(..., font="Inter")` dengan font terpasang/di path |

## 4. Repo ini

Manim untuk **penjelasan** (skala, rasio, profil sangrai), bukan untuk foto produk. Keluaran
mp4 diletakkan di `assets/video/` dan selalu disertai poster `.jpg` untuk pratinjau.
