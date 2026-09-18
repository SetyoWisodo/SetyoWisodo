### Hi there 👋

<!--
**SetyoWisodo/SetyoWisodo** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

# Pacdora 3D — Generator & Editor Mockup Kemasan 3D Online

Aplikasi web pembuat mockup kemasan 3D interaktif dan jaring-jaring (*dieline*) profesional layaknya **[Pacdora.com](https://www.pacdora.com)**, dibangun dengan teknologi WebGL, Three.js, React, Tailwind CSS, dan HTML5 Canvas.

![Pacdora 3D Mockup Studio](https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=1200&q=80)

---

## 🌟 Fitur Utama (Features)

### 1. 📦 Katalog Model Kemasan Parametrik (3D Packaging Models)
- **Kotak & Kardus (Boxes)**:
  - **Kotak Mailer (E-Commerce)**: Kardus lipat berengsel dengan lid pengunci depan, animasi buka/tutup lid interaktif (*opening lid slider*).
  - **Kotak Lipat Standar (Tuck Box)**: Straight tuck box serbaguna untuk kosmetik, farmasi, retail, dan botol.
  - **Tas Belanja Kertas (Shopping Bag)**: Paper bag retail dengan lipatan accordion samping dan pegangan tali jinjing (*twisted rope handle*).
- **Botol & Kaleng (Bottles & Cans)**:
  - **Kaleng Minuman Aluminium (Beverage Can)**: Kaleng soda / craft beer dengan lekukan rim atas, pull-tab, dan dasar cekung metalik.
  - **Botol Pipet Serum (Dropper Bottle)**: Botol kaca amber/clear dengan pipet tetes karet dan tutup collar metalik.
  - **Jar Krim Kosmetik (Cream Jar)**: Wadah krim kecantikan dengan tutup ulir metalik/kayu.
- **Pouch & Tube (Pouches & Tubes)**:
  - **Stand-up Pouch (Doypack)**: Kemasan fleksibel bersegel ziplock dan bottom gusset untuk kopi, teh, dan snack.
  - **Gelas Kopi Kertas (Paper Coffee Cup)**: Gelas takeaway kopi dengan tutup lid snap-on dan corong minum.
  - **Tube Kosmetik & Salep (Squeeze Tube)**: Tube fleksibel dengan ujung segel crimped datar dan flip/screw cap.

### 2. 🎨 Editor Grafis & Jaring-jaring 2D Interaktif (Dieline Graphic Editor)
- **Sinkronisasi Real-time 3D**: Setiap perubahan teks, logo, warna, atau posisi elemen pada kanvas 2D langsung terproyeksikan pada model 3D secara instan tanpa lag.
- **Garis CAD Dieline Standar Industri**:
  - Garis potong luar (*Cut Lines* - Merah).
  - Garis lipatan / tekukan (*Crease Lines* - Biru putus-putus).
  - Batas aman (*Bleed Lines* - Hijau).
  - Indikator label sisi: *Front*, *Back*, *Lid*, *Left*, *Right*, *Bottom*, *Tuck Flap*.
- **Alat Desain Lengkap**:
  - **Teks**: Pilihan Google Fonts (Montserrat, Inter, Poppins, Playfair Display, Bebas Neue, Space Grotesk), ukuran font, ketebalan, spasi huruf, perataan (kiri/tengah/kanan), dan warna.
  - **Upload Logo / Gambar**: Unggah file PNG transparan, JPG, atau ilustrasi merek sendiri dengan drag & drop dan resize.
  - **Bentuk (Shapes)**: Persegi, lingkaran, kapsul (*pill*), garis pemisah pembagi informasi.
  - **Generator Barcode Dinamis**: Barcode standar UPC-A / EAN-13 dengan nomor kustom.
  - **Generator QR Code Dinamis**: Ubah tautan website atau nomor seri menjadi QR Code asli yang dapat discan oleh smartphone.
  - **Stempel Sertifikasi Kemasan**: Stempel *100% Recyclable*, *Certified Organic*, *Halal Indonesia*, *Cruelty Free*, *FSC Mix Paper*, dan *Netto Weight*.

### 3. ✨ Material PBR & Efek Khusus Fotorealistik
- Pilihan tekstur permukaan:
  - **Kraft Brown**: Kertas kardus daur ulang berserat kayu organik.
  - **Kraft White**: Kertas kraft putih bersih bertekstur halus.
  - **Matte Coated**: Karton dupleks / ivory laminasi doff premium.
  - **Ultra Gloss**: Lapisan vernis UV kilap tinggi memantulkan studio light.
  - **Metallic Foil**: Foil emas / perak berkilau.
  - **Kaca Transparan & Kaca Amber**: Botol kosmetik tembus cahaya dengan refraksi dan transmitansi akurat.
  - **Frosted Plastic**: Plastik buram matte tembus pandang.
- **Efek Embun Air Dingin (Condensation)**: Tetesan air realistis untuk kaleng soda dingin atau botol bir.
- **Mode Wireframe 3D**: Melihat jaring poligon 3D kemasan.

### 4. 💡 Studio Pencahayaan & Lingkungan (Lighting Rigs)
- Pilihan Preset Cahaya:
  - **Studio Minimal**: Dual softbox netral untuk katalog e-commerce.
  - **Warm Commercial**: Cahaya hangat keemasan ramah konsumen.
  - **Dramatic Rim**: Pencahayaan kontras tinggi ala studio gelap mewah.
  - **Neon Cyberpunk**: Cahaya tepi futuristik cyan & magenta.
  - **Pure Catalog**: Latar putih e-commerce bersih tanpa bayang kasar.
- Kontrol Latar Belakang: Latar transparan (PNG alpha) atau palet warna studio.
- Turntable 360° otomatis dengan slider kecepatan putaran.

### 5. 🚀 Ekspor Lengkap (Export Suite)
1. **Render 4K Ultra HD Snapshot**:
   - Pilihan resolusi: 1080p Full HD, 2K Square (Instagram & Portfolio), 4K Ultra HD.
   - Pilihan latar belakang transparan (PNG) atau solid.
2. **Jaring-jaring Vektor CAD (Dieline SVG & PNG)**:
   - File SVG vector siap buka di Adobe Illustrator / software percetakan kemasan dengan ukuran milimeter presisi.
   - File PNG resolusi tinggi 2048×2048 px.
3. **Rekam Video 360° Turntable**:
   - Rekam putaran 360° kemasan secara otomatis dan download file video `.webm`.
4. **Model 3D (.GLB / glTF)**:
   - Ekspor model 3D lengkap dengan tekstur UV tertanam untuk Blender, Unity, Unreal Engine, atau Figma.

---

## ⌨️ Shortcut Keyboard

- `Ctrl + Z` / `Cmd + Z` : Undo perubahan desain
- `Ctrl + Y` / `Cmd + Shift + Z` : Redo perubahan desain
- `Delete` / `Backspace` : Hapus elemen yang sedang dipilih
- `Klik Kiri Drag` pada 3D : Putar sudut pandang (Orbit)
- `Scroll Mouse` pada 3D : Zoom In / Zoom Out
- `Klik Kanan Drag` pada 3D : Pan kamera

---

## 🛠️ Menjalankan Proyek Secara Lokal

```bash
# Clone repository
git clone https://github.com/SetyoWisodo/SetyoWisodo.git
cd SetyoWisodo

# Install dependencies
npm install

# Jalankan dev server
npm run dev
```

Server akan aktif pada `http://localhost:5173`.
