---
name: whisperx-captions
description: Transkripsi dengan waktu per kata pakai WhisperX, lalu jadikan subtitle dan animasi teks yang menempel pada suara. Dipakai saat caption harus muncul tepat saat kata diucapkan, bukan per kalimat.
license: BSD-2-Clause · m-bain/whisperX · commit b904f02b7e1f
---

# WhisperX — waktu per kata

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/m-bain/whisperX> |
| Bintang saat dicatat | 25.445 |
| Lisensi | BSD-2-Clause |
| Commit yang dibaca | `b904f02b7e1f` |
| Pasang | `pip install whisperx` (butuh torch; GPU sangat disarankan) |

## 1. Kapan dipakai

**Pakai** kalau butuh `word.text`, `word.start`, `word.end` untuk caption beranimasi,
karaoke, atau pemotongan video per frasa.

**Jangan** pakai kalau cukup subtitle per kalimat (SRT biasa dari Whisper sudah cukup), atau
kalau tidak ada GPU dan durasi audio panjang — di CPU bisa berkali-kali waktu audio.

## 2. Alur minimum

```bash
whisperx audio.mp3 --model large-v3 --align --language id \
  --output_format json --output_dir out/
```

```python
import whisperx, json
model = whisperx.load_model("large-v3", device="cpu", compute_type="int8")
audio = whisperx.load_audio("audio.mp3")
hasil = model.transcribe(audio, language="id", batch_size=8)
align, meta = whisperx.load_align_model(language_code="id", device="cpu")
hasil = whisperx.align(hasil["segments"], align, meta, audio, "cpu")
json.dump(hasil, open("out/kata.json", "w"), ensure_ascii=False, indent=1)
```

Diarization (siapa bicara) butuh token Hugging Face dan model tambahan — jangan dipasang
kalau tidak perlu.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Timestamp meleset jauh | audio di-resample/kompresi berat | beri berkas WAV 16 kHz |
| Kata hilang | model terlalu kecil untuk bahasa campur | `large-v3`, atau pisahkan per segmen |
| RAM habis | `batch_size` besar di CPU | turunkan ke 4–8 |
| Caption "melompat" | kalimat digabung | susun ulang per kata dengan jeda > 0,25 s |
| Model diunduh dari internet tiap jalan | cache kosong | simpan di `~/.cache/whisperx`, catat versi model |

## 4. Repo ini

Keluaran `out/kata.json` dipakai dua tempat: subtitle `.srt` dan animasi teks (Remotion
`remotion-captions`, lihat skill `remotion-skills`). Simpan JSON-nya di `data/` supaya
video bisa dirender ulang tanpa menjalankan transkripsi lagi.
