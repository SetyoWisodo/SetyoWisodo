"""Sisipkan kalimat penunjuk tabel (dan gambar) ke dalam prosa.

Dipakai sekali saat perbaikan pasca-review; idempoten karena memeriksa
apakah kalimat sudah ada sebelum menambah.
"""
import re

EN = {
    "1.1": "Table 1.1 sets out the three futures that organise the rest of the book, with the temperatures and signature impacts of each.",
    "2.1": "Table 2.1 reduces the three trajectories to numbers at 2050 and 2100 and names the physical consequence attached to each; Figure 2.1 shows the same comparison as bars.",
    "3.1": "Table 3.1 lists the thresholds that matter for decisions, together with the signals that would show one is being approached.",
    "4.1": "Table 4.1 gives the exposure figures city by city, including the wet-bulb values that determine whether cooling can still work, and Figure 4.1 plots the days above 35 \u00b0C that lie behind them.",
    "5.1": "Table 5.1 sets out the same stress basin by basin, with the share of each population at risk and the supply gap implied by current demand; Figure 5.1 plots the people affected against that gap.",
    "6.1": "Table 6.1 compares six coastal cities on subsidence, exposure and adaptation, and Figure 6.1 ranks them by the population exposed to a 1-in-100-year flood.",
    "7.1": "Table 7.1 gives the yield sensitivity of each crop per degree of warming alongside the 2050 projection used here, and Figure 7.1 shows the same sensitivities as a bar chart.",
    "8.1": "Table 8.1 sets out the thresholds of concern for the main ecosystems and what is projected to change at 2 \u00b0C and at 3 \u00b0C; Figure 8.1 shows four of those systems side by side.",
    "9.1": "Table 9.1 summarises the health risks discussed here and marks how the burden changes at 2 \u00b0C and at 3 \u00b0C.",
    "10.1": "Table 10.1 puts the three pathways in money terms, separated into losses that show up in GDP and losses that do not; Figure 10.1 plots the central estimates.",
    "11.1": "Table 11.1 breaks the migration figures down by region of origin, and Figure 11.1 plots the same totals so that the magnitude is visible at a glance.",
    "12.1": "Table 12.1 lists the fragile regions where climate exposure and conflict risk overlap, with the mechanism that connects them.",
    "13.1": "Table 13.1 ranks infrastructure sectors by the resilience gap between current practice and what the record requires.",
    "14.1": "Table 14.1 compares the literacy indicators that can be measured across countries and shows how far the measurement itself is incomplete.",
    "15.1": "Table 15.1 lists the information-environment indicators that distinguish a well-informed public from a misinformed one.",
    "16.1": "Table 16.1 sets out household preparedness hazard by hazard, from what most households have to what the evidence says saves lives.",
    "17.1": "Table 17.1 translates adaptation into health outcomes, with the annual excess heat deaths implied by each level of investment; Figure 17.1 plots the same three paths against a common baseline.",
    "18.1": "Table 18.1 compares governance indicators across the functions that determine whether a response holds.",
    "19.1": "Table 19.1 tracks the clean-energy indicators and shows where the gap is now an integration problem rather than a cost problem.",
    "20.1": "Table 20.1 sets out the mental-health indicators and the service coverage behind each one.",
    "21.1": "Table 21.1 compares the justice indicators and the instruments that move each of them.",
    "22.1": "Table 22.1 places nine disasters side by side on the same five columns, so that the failures can be compared rather than described one at a time; Figure 22.1 plots the death tolls against one another.",
    "23.1": "Table 23.1 does the same for slow-onset crises, where the outcome column records mortality, displacement or epidemic disease as the case allows; Figure 23.1 plots the losses on a logarithmic scale so that crises a thousand times apart can share one chart.",
    "24.1": "Table 24.1 sets out the priorities by horizon, from the actions due before the next event to those due before mid-century.",
}

ID = {
    "1.1": "Tabel 1.1 menyusun tiga masa depan yang menjadi kerangka seluruh buku ini, lengkap dengan suhu dan dampak khas masing-masing.",
    "2.1": "Tabel 2.1 meringkas tiga lintasan itu menjadi angka pada 2050 dan 2100 serta menyebut akibat fisik yang melekat pada masing-masing; Gambar 2.1 menyajikan perbandingan yang sama dalam bentuk batang.",
    "3.1": "Tabel 3.1 mendaftar ambang batas yang penting untuk keputusan, beserta sinyal yang menunjukkan bahwa salah satunya sedang didekati.",
    "4.1": "Tabel 4.1 memberi angka paparan untuk setiap kota, termasuk nilai wet-bulb yang menentukan apakah pendinginan masih mungkin bekerja, dan Gambar 4.1 menggambarkan jumlah hari di atas 35 \u00b0C yang melatarbelakanginya.",
    "5.1": "Tabel 5.1 menyusun tekanan yang sama per cekungan, dengan bagian penduduk yang berisiko dan celah pasokan yang tersirat dari permintaan saat ini; Gambar 5.1 memetakan jumlah orang terhadap celah itu.",
    "6.1": "Tabel 6.1 membandingkan enam kota pesisir pada penurunan tanah, paparan, dan adaptasi, sedangkan Gambar 6.1 mengurutkannya menurut jumlah penduduk yang terpapar banjir 1-dalam-100 tahun.",
    "7.1": "Tabel 7.1 memberi sensitivitas hasil setiap tanaman per derajat pemanasan bersama proyeksi 2050 yang dipakai di sini, dan Gambar 7.1 menampilkan sensitivitas yang sama sebagai diagram batang.",
    "8.1": "Tabel 8.1 menyusun ambang yang mengkhawatirkan bagi ekosistem utama dan apa yang diproyeksikan berubah pada 2 \u00b0C dan 3 \u00b0C; Gambar 8.1 menampilkan empat sistem itu berdampingan.",
    "9.1": "Tabel 9.1 merangkum risiko kesehatan yang dibahas di sini dan menandai bagaimana bebannya berubah pada 2 \u00b0C dan 3 \u00b0C.",
    "10.1": "Tabel 10.1 menerjemahkan tiga jalur itu ke dalam uang, dipisahkan antara kerugian yang tampak di PDB dan yang tidak; Gambar 10.1 menggambarkan estimasi tengahnya.",
    "11.1": "Tabel 11.1 memecah angka migrasi menurut wilayah asal, dan Gambar 11.1 menampilkan total yang sama agar besarnya langsung terlihat.",
    "12.1": "Tabel 12.1 mendaftar wilayah rapuh tempat paparan iklim dan risiko konflik bertumpang tindih, beserta mekanisme yang menghubungkan keduanya.",
    "13.1": "Tabel 13.1 mengurutkan sektor infrastruktur menurut celah ketangguhan antara praktik saat ini dan apa yang dituntut oleh rekam jejak bencana.",
    "14.1": "Tabel 14.1 membandingkan indikator literasi yang dapat diukur lintas negara dan menunjukkan seberapa jauh pengukurannya sendiri masih tidak lengkap.",
    "15.1": "Tabel 15.1 mendaftar indikator lingkungan informasi yang membedakan publik yang terinformasi baik dari publik yang salah informasi.",
    "16.1": "Tabel 16.1 menyusun kesiapsiagaan rumah tangga menurut bahaya, dari yang dimiliki sebagian besar rumah tangga hingga yang menurut bukti menyelamatkan nyawa.",
    "17.1": "Tabel 17.1 menerjemahkan adaptasi menjadi luaran kesehatan, dengan kematian berlebih akibat panas per tahun yang tersirat dari setiap tingkat investasi; Gambar 17.1 menggambarkan ketiga jalur itu terhadap satu basis yang sama.",
    "18.1": "Tabel 18.1 membandingkan indikator tata kelola pada fungsi-fungsi yang menentukan apakah respons bertahan.",
    "19.1": "Tabel 19.1 melacak indikator energi bersih dan menunjukkan bahwa celahnya kini soal integrasi, bukan lagi soal biaya.",
    "20.1": "Tabel 20.1 menyusun indikator kesehatan mental dan cakupan layanan di belakang masing-masing.",
    "21.1": "Tabel 21.1 membandingkan indikator keadilan dan instrumen yang menggerakkan masing-masing.",
    "22.1": "Tabel 22.1 menempatkan sembilan bencana berdampingan pada lima kolom yang sama, sehingga kegagalannya dapat dibandingkan, bukan hanya diceritakan satu per satu; Gambar 22.1 memplot jumlah kematiannya.",
    "23.1": "Tabel 23.1 melakukan hal yang sama untuk krisis yang datang perlahan, dengan kolom dampak yang mencatat kematian, pengungsian, atau wabah sesuai kasusnya; Gambar 23.1 memplot kerugiannya pada skala logaritma agar krisis yang terpaut seribu kali dapat berbagi satu grafik.",
    "24.1": "Tabel 24.1 menetapkan prioritas menurut cakrawala, dari tindakan yang jatuh tempo sebelum peristiwa berikutnya hingga yang jatuh tempo sebelum pertengahan abad.",
}

BAD = ("#", "|", "![")


def apply(path, label, sentences):
    blocks = open(path, encoding="utf-8").read().split("\n\n")
    done, fails = 0, []
    for num, sent in sentences.items():
        marker = "[[TABLE:%s %s " % (label, num)
        idx = [i for i, b in enumerate(blocks) if b.startswith(marker)]
        if len(idx) != 1:
            fails.append((num, "marker", len(idx)))
            continue
        i = idx[0]
        prev = blocks[i - 1].strip()
        if prev.startswith(BAD) or len(prev) < 80:
            fails.append((num, "prev", prev[:40]))
            continue
        if sent in prev:
            continue
        blocks[i - 1] = prev + " " + sent
        done += 1
    open(path, "w", encoding="utf-8").write("\n\n".join(blocks))
    return done, fails


if __name__ == "__main__":
    for path, label, sents in (("book.md", "Table", EN), ("book_id.md", "Tabel", ID)):
        d, f = apply(path, label, sents)
        print(path, "ditambahkan:", d, "gagal:", f)
