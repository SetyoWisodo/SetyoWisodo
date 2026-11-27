#!/usr/bin/env python3
"""Terapkan ulang perbaikan atribusi hasil audit sitasi (idempoten).

Semua penggantian berbasis teks unik; yang sudah diganti akan dilaporkan LEWAT,
yang tidak ditemukan dilaporkan TIDAK KETEMU dan membuat exit code 1.
"""
import pathlib
import sys

E = [
    # --- bab 1: 76.000 relawan CPP -> sumber primer + Bangladesh ---
    ("src/en/02-ch01.md",
     "drills that made evacuation routine (@wmo2022).",
     "drills that made evacuation routine [@habibullah2012; @sammonds2021]."),
    ("src/id/02-bab01.md",
     "rutin [@wmo2022].",
     "rutin [@habibullah2012; @sammonds2021]."),
    # --- bab 2: rantai diputus, peringatan lebih murah dari tanggul ---
    ("src/en/03-ch02.md",
     "Strengthening warning systems is cheaper than building embankments (@wmo2022).",
     "Strengthening warning systems is cheaper than building embankments [@sammonds2021; @habibullah2012]."),
    ("src/id/03-bab02.md",
     "Memperkuat sistem peringatan lebih murah daripada membangun tanggul [@wmo2022].",
     "Memperkuat sistem peringatan lebih murah daripada membangun tanggul [@sammonds2021; @habibullah2012]."),
    # --- bab 7: krisis pangan 2007-08 & 2022 ---
    ("src/en/07-ch06.md",
     "import and cannot pay (@fao2022). The 2007–2008 food price crisis followed this pattern",
     "import and cannot pay [@headey2008]. The 2007–2008 food price crisis followed this pattern"),
    ("src/en/07-ch06.md",
     "more than thirty countries, and governments fell in several [@fao2022].",
     "more than thirty countries, and governments fell in several [@headey2008]."),
    ("src/en/07-ch06.md",
     "more reliable predictor of rural poverty than average rainfall (@fao2022).",
     "more reliable predictor of rural poverty than average rainfall [@headey2008; @fao2019]."),
    ("src/en/07-ch06.md",
     "prices. Food prices reached record levels, and the number of people facing acute food insecurity rose\nsharply [@fao2022].",
     "prices. Food prices reached record levels, and the number of people facing acute food insecurity rose\nsharply [@fao2023]."),
    ("src/en/07-ch06.md",
     "**Month 3–4: selling productive assets** [@fao2022].",
     "**Month 3–4: selling productive assets.**"),
    ("src/en/07-ch06.md",
     "roughly a tenth of the global market (@fao2023).",
     "roughly a tenth of the global market [@fao2023beras]."),
    ("src/en/07-ch06.md",
     "reaching a fifteen-year nominal high (@fao2023).",
     "reaching a fifteen-year nominal high [@fao2023beras]."),
    ("src/en/07-ch06.md",
     "traded internationally (@fao2023).",
     "traded internationally [@fao2023beras]."),
    ("src/id/07-bab06.md",
     "negara yang paling menderita adalah yang mengimpor dan tidak mampu membayar [@fao2022].",
     "negara yang paling menderita adalah yang mengimpor dan tidak mampu membayar [@headey2008]."),
    ("src/id/07-bab06.md",
     "Kerusuhan pangan terjadi di lebih dari tiga puluh negara, dan beberapa pemerintah jatuh [@fao2022].",
     "Kerusuhan pangan terjadi di lebih dari tiga puluh negara, dan beberapa pemerintah jatuh [@headey2008]."),
    ("src/id/07-bab06.md",
     "lebih andal memprediksi kemiskinan pedesaan daripada rata-rata curah hujan [@fao2022].",
     "lebih andal memprediksi kemiskinan pedesaan daripada rata-rata curah hujan [@headey2008; @fao2019]."),
    ("src/id/07-bab06.md",
     "jumlah orang yang menghadapi kerawanan pangan akut naik tajam [@fao2022].",
     "jumlah orang yang menghadapi kerawanan pangan akut naik tajam [@fao2023]."),
    ("src/id/07-bab06.md",
     "**Bulan 3–4: menjual aset produktif** [@fao2022].",
     "**Bulan 3–4: menjual aset produktif.**"),
    ("src/id/07-bab06.md",
     "kira-kira sepersepuluh pasar dunia [@fao2023].",
     "kira-kira sepersepuluh pasar dunia [@fao2023beras]."),
    ("src/id/07-bab06.md",
     "mencapai rekor nominal lima belas tahun [@fao2023].",
     "mencapai rekor nominal lima belas tahun [@fao2023beras]."),
    ("src/id/07-bab06.md",
     "diperdagangkan secara internasional [@fao2023].",
     "diperdagangkan secara internasional [@fao2023beras]."),
    # --- bab 10: CPP 76.000 relawan ---
    ("src/en/11-ch10.md",
     "operates with about 76,000 volunteers [@wmo2022].",
     "operates with about 76,000 volunteers [@habibullah2012; @nahar2022]."),
    ("src/id/11-bab10.md",
     "berjalan dengan sekitar 76.000 relawan [@wmo2022].",
     "berjalan dengan sekitar 76.000 relawan [@habibullah2012; @nahar2022]."),
    # --- bab 11: peringatan ---
    ("src/en/12-ch11.md",
     "The tsunami killed an estimated 227,000 people",
     "The tsunami killed an estimated 227,000 people"),
    ("src/en/12-ch11.md",
     "Most investment goes to link one. Most failures occur at links three and four (@wmo2022).",
     "Most investment goes to link one. Most failures occur at links three and four, which is the finding that\nmotivated the shift from warning systems to warning-as-a-service with a named last-mile actor [@sammonds2021; @habibullah2012]."),
    ("src/id/12-bab11.md",
     "Sebagian besar investasi pergi ke mata rantai satu. Sebagian besar kegagalan terjadi pada mata rantai tiga dan empat [@kreienkamp2021; @sammonds2021].",
     "Sebagian besar investasi pergi ke mata rantai satu. Sebagian besar kegagalan terjadi pada mata rantai tiga dan empat, temuan yang mendorong pergeseran dari sistem peringatan ke peringatan sebagai layanan dengan pelaku mil terakhir yang bernama [@sammonds2021; @habibullah2012]."),
    ("src/en/12-ch11.md",
     "with 76,000 volunteers\nwhose job is to be the last mile [@wmo2022].",
     "with 76,000 volunteers\nwhose job is to be the last mile [@habibullah2012; @nahar2022]."),
    ("src/id/12-bab11.md",
     "dengan 76.000 relawan yang pekerjaannya adalah menjadi mil terakhir [@wmo2022].",
     "dengan 76.000 relawan yang pekerjaannya adalah menjadi mil terakhir [@habibullah2012; @nahar2022]."),
    ("src/en/12-ch11.md",
     "including the people who cannot read and the people who will not leave without their livestock (@wmo2022).",
     "including the people who cannot read and the people who will not leave without their livestock [@habibullah2012; @nahar2022]."),
    ("src/en/12-ch11.md",
     "and to use the lower levels for information rather than evacuation [@wmo2022].",
     "and to use the lower levels for information rather than evacuation [@sammonds2021; @habibullah2012]."),
    ("src/id/12-bab11.md",
     "dan memakai tingkat yang lebih rendah untuk informasi dan bukan evakuasi [@wmo2022].",
     "dan memakai tingkat yang lebih rendah untuk informasi dan bukan evakuasi [@sammonds2021; @habibullah2012]."),
    ("src/en/12-ch11.md",
     "produce paralysis or denial rather than evacuation (@wmo2022).",
     "produce paralysis or denial rather than evacuation. The finding is old in risk communication and it is why the best warning messages name the action before the danger [@hsiang2013; @sammonds2021]."),
    ("src/id/12-bab11.md",
     "menghasilkan kelumpuhan atau penyangkalan, bukan evakuasi [@wmo2022].",
     "menghasilkan kelumpuhan atau penyangkalan, bukan evakuasi. Temuan ini sudah lama dalam komunikasi risiko, dan itulah sebabnya pesan peringatan terbaik menyebut tindakannya sebelum bahayanya [@hsiang2013; @sammonds2021]."),
    # --- bab 12: Nansen ---
    ("src/en/13-ch12.md",
     "The Nansen Initiative produced a protection agenda but no obligation (@iom2023).",
     "The Nansen Initiative produced a protection agenda but no obligation, and the Global Compact is a framework without a court [@iom2023; @undrr2022]."),
    ("src/id/13-bab12.md",
     "Nansen Initiative menghasilkan agenda perlindungan tetapi tidak kewajiban [@iom2023].",
     "Nansen Initiative menghasilkan agenda perlindungan tetapi tidak kewajiban, dan Global Compact adalah kerangka tanpa pengadilan [@iom2023; @undrr2022]."),
    # --- bab 15: perilaku, ranking tindakan, persediaan ---
    ("src/en/16-ch15.md",
     "conversation with a trusted person outperforms a leaflet [@wmo2022].",
     "conversation with a trusted person outperforms a leaflet [@aldrich2012; @nahar2022]."),
    ("src/id/16-bab15.md",
     "Bukti tentang perubahan perilaku konsisten menemukan bahwa percakapan dengan orang yang dipercaya mengalahkan selebaran [@wmo2022].",
     "Bukti tentang perubahan perilaku konsisten menemukan bahwa percakapan dengan orang yang dipercaya mengalahkan selebaran [@aldrich2012; @nahar2022]."),
    ("src/en/16-ch15.md",
     "**Knowing the hazard you actually face** [@wmo2022].",
     "**Knowing the hazard you actually face.**"),
    ("src/id/16-bab15.md",
     "**Mengetahui bahaya yang benar-benar Anda hadapi** [@wmo2022].",
     "**Mengetahui bahaya yang benar-benar Anda hadapi.**"),
    ("src/en/16-ch15.md",
     "evaluations, though not by a controlled design in every case [@wmo2022].",
     "evaluations, though not by a controlled design in every case [@hess2018; @bubeck2017]."),
    ("src/id/16-bab15.md",
     "meski tidak dalam desain terkontrol di setiap kasus [@wmo2022].",
     "meski tidak dalam desain terkontrol di setiap kasus [@hess2018; @bubeck2017]."),
    ("src/en/16-ch15.md",
     "better, and that the constraint was not the food but the water [@bccoroners2022].",
     "substantially better, and that the constraint was not the food but the water [@bccoroners2022]."),
    # --- bab 17: ipcc2021 hilang di terjemahan ---
    ("src/id/18-bab17.md",
     "bukan sebagai pengukuran.",
     "bukan sebagai pengukuran [@ipcc2021]."),
]

hitung = {"ok": 0, "lewat": 0, "gagal": 0}
for f, a, b in E:
    p = pathlib.Path(f)
    s = p.read_text(encoding="utf-8")
    if b in s and a not in s:
        hitung["lewat"] += 1
    elif a in s:
        p.write_text(s.replace(a, b, 1), encoding="utf-8")
        hitung["ok"] += 1
    else:
        hitung["gagal"] += 1
        print("TIDAK KETEMU:", f, "|", a[:70])
print(hitung)
sys.exit(1 if hitung["gagal"] else 0)
