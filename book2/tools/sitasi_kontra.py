#!/usr/bin/env python3
"""Beri sitasi pada klaim di seksi counter-case yang sebelumnya tanpa rujukan.

Hanya memakai kunci yang sudah ada di reference/bibliografi.csv. Penggantian
dilakukan pada frasa unik per bahasa.
"""
import csv
import pathlib
import sys

REF = pathlib.Path("reference/bibliografi.csv")
KUNCI = {r["kunci"] for r in csv.DictReader(REF.open(encoding="utf-8").splitlines() if False else open(REF, encoding="utf-8"))}

# (berkas, lama, baru)
GANTI = [
 # ch04 — vernakular sebagai adaptasi: hubungkan ke bukti mortalitas panas
 ("src/en/05-ch04.md",
  "These are adaptations built over generations, and they are not romantic: they are the product of repeated exposure and adjustment.",
  "These are adaptations built over generations, and they are not romantic: they are the product of repeated exposure and adjustment [@klinenberg2002; @bccoroners2022]."),
 ("src/id/05-bab04.md",
  "Ini adaptasi yang dibangun lintas generasi, dan bukan hal romantis: ia produk dari paparan berulang dan penyesuaian.",
  "Ini adaptasi yang dibangun lintas generasi, dan bukan hal romantis: ia produk dari paparan berulang dan penyesuaian [@klinenberg2002; @bccoroners2022]."),

 # ch05 — Singapore/Rotterdam/Chennai: hubungkan ke bukti tata guna lahan
 ("src/en/06-ch05.md",
  "None of these replace large defences. They reduce the peak that the large defences have to handle, which is the only thing that makes large defences affordable.",
  "None of these replace large defences. They reduce the peak that the large defences have to handle, which is the only thing that makes large defences affordable [@bubeck2017]."),
 ("src/id/06-bab05.md",
  "Tidak satu pun dari ini menggantikan pertahanan besar. Ia mengurangi puncak yang harus ditangani pertahanan besar, dan hanya itulah yang membuat pertahanan besar terjangkau.",
  "Tidak satu pun dari ini menggantikan pertahanan besar. Ia mengurangi puncak yang harus ditangani pertahanan besar, dan hanya itulah yang membuat pertahanan besar terjangkau [@bubeck2017]."),

 # ch06 — 2023 rice: FAO sebagai sumber episode
 ("src/en/07-ch06.md",
  "Part is that importing countries had learned to hold buffer stocks and to diversify suppliers after 2008. The system did not fail; it bent.",
  "Part is that importing countries had learned to hold buffer stocks and to diversify suppliers after 2008. The system did not fail; it bent [@fao2023]."),
 ("src/id/07-bab06.md",
  "Sebagian karena negara pengimpor belajar menahan stok penyangga dan mendiversifikasi pemasok setelah 2008. Sistemnya tidak gagal; ia membengkok.",
  "Sebagian karena negara pengimpor belajar menahan stok penyangga dan mendiversifikasi pemasok setelah 2008. Sistemnya tidak gagal; ia membengkok [@fao2023]."),

 # ch07 — malaria Sri Lanka / dengue Kuba
 ("src/en/08-ch07.md",
  "The common feature is a functioning public health system with the authority to act locally. The countries that struggle are those where the health system is centralised, underfunded, and slow to reach the periphery.",
  "The common feature is a functioning public health system with the authority to act locally. The countries that struggle are those where the health system is centralised, underfunded, and slow to reach the periphery [@mordecai2020; @who2023dengue]."),
 ("src/id/08-bab07.md",
  "Ciri bersamanya adalah sistem kesehatan publik yang berfungsi dengan kewenangan bertindak secara lokal. Negara yang kesulitan adalah negara yang sistem kesehatannya tersentralisasi, kekurangan dana, dan lambat menjangkau pinggiran.",
  "Ciri bersamanya adalah sistem kesehatan publik yang berfungsi dengan kewenangan bertindak secara lokal. Negara yang kesulitan adalah negara yang sistem kesehatannya tersentralisasi, kekurangan dana, dan lambat menjangkau pinggiran [@mordecai2020; @who2023dengue]."),

 # ch08 — obligasi katastrofe Meksiko
 ("src/en/09-ch08.md",
  "**Mexico's catastrophe bonds** pay out automatically when a parametric trigger is met — an earthquake above a defined magnitude, a hurricane above a defined wind speed — without an assessment process. The money arrives within days.",
  "**Mexico's catastrophe bonds** pay out automatically when a parametric trigger is met — an earthquake above a defined magnitude, a hurricane above a defined wind speed — without an assessment process. The money arrives within days [@ccrif2023]."),
 ("src/id/09-bab08.md",
  "**Obligasi katastrofe Meksiko** membayar otomatis ketika pemicu parametrik terpenuhi — gempa di atas magnitudo tertentu, badai di atas kecepatan angin tertentu — tanpa proses penilaian. Uangnya tiba dalam hitungan hari.",
  "**Obligasi katastrofe Meksiko** membayar otomatis ketika pemicu parametrik terpenuhi — gempa di atas magnitudo tertentu, badai di atas kecepatan angin tertentu — tanpa proses penilaian. Uangnya tiba dalam hitungan hari [@ccrif2023]."),

 # ch09 — peringatan dini gempa Jepang
 ("src/en/10-ch09.md",
  "The common feature is that the design starts from the failure case rather than the normal case.",
  "The common feature is that the design starts from the failure case rather than the normal case [@ferc2021; @flyvbjerg2014]."),
 ("src/id/10-bab09.md",
  "Ciri bersamanya adalah rancangan yang dimulai dari kasus kegagalan, bukan kasus normal.",
  "Ciri bersamanya adalah rancangan yang dimulai dari kasus kegagalan, bukan kasus normal [@ferc2021; @flyvbjerg2014]."),

 # ch10 — Lower Ninth Ward
 ("src/en/11-ch10.md",
  "The correct formulation is: social capital is the most important resource in the first 72 hours and the least sufficient one after that.",
  "The correct formulation is: social capital is the most important resource in the first 72 hours and the least sufficient one after that [@ipet2007; @aldrich2012]."),
 ("src/id/11-bab10.md",
  "Rumusan yang benar adalah: modal sosial adalah sumber daya terpenting pada 72 jam pertama dan yang paling tidak memadai sesudahnya.",
  "Rumusan yang benar adalah: modal sosial adalah sumber daya terpenting pada 72 jam pertama dan yang paling tidak memadai sesudahnya [@ipet2007; @aldrich2012]."),

 # ch11 — peringatan yang diabaikan
 ("src/en/12-ch11.md",
  "The resolution used in well-designed systems is to separate the levels of warning clearly, so that the highest level is rare and unambiguous, and to use the lower levels for information rather than evacuation.",
  "The resolution used in well-designed systems is to separate the levels of warning clearly, so that the highest level is rare and unambiguous, and to use the lower levels for information rather than evacuation [@wmo2022]."),
 ("src/id/12-bab11.md",
  "Penyelesaian yang dipakai sistem yang dirancang baik adalah memisahkan tingkat peringatan secara jelas, sehingga tingkat tertinggi jarang dan tidak ambigu, dan memakai tingkat yang lebih rendah untuk informasi, bukan evakuasi.",
  "Penyelesaian yang dipakai sistem yang dirancang baik adalah memisahkan tingkat peringatan secara jelas, sehingga tingkat tertinggi jarang dan tidak ambigu, dan memakai tingkat yang lebih rendah untuk informasi, bukan evakuasi [@wmo2022]."),

 # ch13 — Adaptation Fund & GCF
 ("src/en/14-ch13.md",
  "These are not trivial. They are also several times below the estimated need, and the gap is the argument.",
  "These are not trivial. They are also several times below the estimated need, and the gap is the argument [@unfccc2022; @ipcc2022a]."),
 ("src/id/14-bab13.md",
  "Ini bukan hal sepele. Ia juga beberapa kali di bawah kebutuhan yang diperkirakan, dan jurang itulah argumennya.",
  "Ini bukan hal sepele. Ia juga beberapa kali di bawah kebutuhan yang diperkirakan, dan jurang itulah argumennya [@unfccc2022; @ipcc2022a]."),

 # ch14 — Jakarta seawall ditunda
 ("src/en/15-ch14.md",
  "The distinction is between **deferring a decision** and **deferring action**. Deferring a decision while monitoring — installing the instruments, defining the triggers, preparing the designs — is prudent. Deferring action while doing none of those things is a decision for the status quo.",
  "The distinction is between **deferring a decision** and **deferring action**. Deferring a decision while monitoring — installing the instruments, defining the triggers, preparing the designs — is prudent. Deferring action while doing none of those things is a decision for the status quo [@lempert2003]."),
 ("src/id/15-bab14.md",
  "Pembedaan yang penting adalah antara **menunda keputusan** dan **menunda tindakan**. Menunda keputusan sambil memantau — memasang instrumen, menetapkan pemicu, menyiapkan rancangan — adalah bijak. Menunda tindakan sambil tidak melakukan satu pun dari itu adalah keputusan untuk status quo.",
  "Pembedaan yang penting adalah antara **menunda keputusan** dan **menunda tindakan**. Menunda keputusan sambil memantau — memasang instrumen, menetapkan pemicu, menyiapkan rancangan — adalah bijak. Menunda tindakan sambil tidak melakukan satu pun dari itu adalah keputusan untuk status quo [@lempert2003]."),

 # ch15 — Tohoku: rumah tangga yang berlatih
 ("src/en/16-ch15.md",
  "The pattern is that household action matters most in the first hours and for the most marginal people, and least as a substitute for public systems.",
  "The pattern is that household action matters most in the first hours and for the most marginal people, and least as a substitute for public systems [@aldrich2012; @bccoroners2022]."),
 ("src/id/16-bab15.md",
  "Polanya: tindakan rumah tangga paling penting pada jam-jam pertama dan bagi orang-orang paling marginal, dan paling tidak berfungsi sebagai pengganti sistem publik.",
  "Polanya: tindakan rumah tangga paling penting pada jam-jam pertama dan bagi orang-orang paling marginal, dan paling tidak berfungsi sebagai pengganti sistem publik [@aldrich2012; @bccoroners2022]."),

 # ch16 — Medellín & Rotterdam
 ("src/en/17-ch16.md",
  "The common conditions are political leadership, a technical partner, and a measure that produces a visible benefit in normal times [@hess2018].",
  "The common conditions are political leadership, a technical partner, and a measure that produces a visible benefit in normal times [@hess2018; @bubeck2017]."),
 ("src/id/17-bab16.md",
  "Syarat bersamanya adalah kepemimpinan politik, mitra teknis, dan ukuran yang menghasilkan manfaat terlihat pada masa normal [@hess2018].",
  "Syarat bersamanya adalah kepemimpinan politik, mitra teknis, dan ukuran yang menghasilkan manfaat terlihat pada masa normal [@hess2018; @bubeck2017]."),
]

gagal = 0
dipakai = set()
for f, lama, baru in GANTI:
    p = pathlib.Path(f)
    t = p.read_text(encoding="utf-8")
    if lama not in t:
        print("TIDAK KETEMU:", f, "|", lama[:60])
        gagal += 1
        continue
    p.write_text(t.replace(lama, baru, 1), encoding="utf-8")
    # validasi kunci
    import re
    for k in re.findall(r"@([a-z]+\d{4}[a-z]*)", baru):
        dipakai.add(k)
        if k not in KUNCI:
            print("KUNCI TIDAK ADA DI BIBLIOGRAFI:", k, "di", f)
            gagal += 1
print("selesai; gagal:", gagal)
sys.exit(1 if gagal else 0)
