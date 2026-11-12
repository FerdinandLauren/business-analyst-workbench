# Panduan Menjalankan Project (Bahasa Indonesia)

## Tujuan

Project ini mengubah catatan bisnis biasa menjadi bahan analisis yang bisa
ditinjau: kandidat kebutuhan, draf BRD, temuan celah proses, dan skenario UAT.

Mesinnya tidak terikat pada contoh pengadaan barang. Tempel catatan tentang
klinik, gudang, tim dukungan, atau proses lain, dan alur yang sama tetap
berjalan. Antarmuka dan dokumen yang dihasilkan tersedia dalam bahasa Inggris
dan Indonesia.

> Ini prototype portfolio. Semua output adalah draf dan wajib diperiksa
> stakeholder. Aplikasi tidak menyetujui permintaan, tidak memindahkan uang, dan
> tidak menggantikan analis.

## Fitur

- **Input bebas.** Tulis satu kalimat untuk setiap masalah atau harapan; mesin
  memecah teks dan mengklasifikasikan tiap kalimat.
- **Berbasis aturan secara default.** Tanpa API key, tanpa jaringan, dan tidak
  ada data yang keluar dari mesin.
- **Tombol bahasa EN / ID** di kanan atas. Tampilan, tabel, BRD, dan UAT
  mengikuti bahasa yang dipilih. Bahasa juga dideteksi otomatis dari input
  sampai kamu memilihnya sendiri.
- **Empat tab terpisah.** Analisis kebutuhan, draf BRD, analisis proses, dan
  generator UAT memiliki input masing-masing.
- **Ekspor.** Kebutuhan dan UAT diunduh sebagai CSV; BRD sebagai Markdown.
- **AI opsional.** Kamu bisa memasukkan API key OpenAI-compatible sendiri di
  sidebar. Kalau panggilan gagal atau key kosong, aplikasi memakai draf lokal.

## Menjalankan di Windows

1. Buka folder project di terminal.
2. Jalankan:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

3. Buka alamat lokal yang muncul di terminal, biasanya
   `http://localhost:8501`.

Gunakan `python -m streamlit`, bukan `streamlit` langsung, jika launcher tidak
ada di PATH. Jika PowerShell memblokir aktivasi environment, pakai Command
Prompt:

```cmd
.venv\Scripts\activate.bat
```

## Menjalankan tes

```bash
python -m unittest discover -s tests -v
```

## Cara mesin memutuskan

Setiap kalimat melewati tiga langkah yang sama, semuanya di folder `src/`:

1. **Deteksi topik.** Kamus memetakan kata ke kategori seperti `scheduling`,
   `payment`, `approval`, `reporting`, dan `integration`. Pencocokan memakai
   batas kata, jadi `WhatsApp` tidak dianggap `sap`.
2. **Deteksi masalah.** Kamus kedua memetakan kata seperti "manual", "bentrok",
   "salah", atau "tidak tahu" ke salah satu dari lima kelompok: consolidation,
   visibility, accuracy, automation, atau none.
3. **Isi template.** Pernyataan menggabungkan kata kerja masalah, kata benda
   kategori, dan hasil yang diharapkan.

Contoh:

```text
Input:  Kasir mencatat pembayaran manual.
Topik:  payment
Masalah: automation
Output: Sistem harus mengotomatiskan pencatatan pembayaran agar pekerjaan
        manual berkurang.
```

Kalimat yang tidak cocok menjadi kebutuhan `unclassified` berstatus
`needs_review` dengan pertanyaan terbuka, supaya celahnya terlihat dan tidak
hilang diam-diam. Area proses tanpa bukti dilaporkan sebagai `unspecified`.

## Struktur modul

```text
app/streamlit_app.py     Tampilan Streamlit, state per tab, tombol bahasa
src/i18n.py              Teks Inggris/Indonesia dan deteksi bahasa
src/text.py              Kamus batas kata dan pemecah kalimat
src/requirements.py      Ekstraksi kebutuhan, prioritas, baris tabel
src/process.py           Perbandingan As-Is / To-Be per area proses
src/uat.py               Skenario UAT sesuai kategori
src/brd.py               BRD Markdown dari input yang sama
src/llm.py               API key opsional, tidak pernah wajib
tests/                   Tes unit dan end-to-end
samples/                 Catatan stakeholder fiktif untuk tes
```

## Catatan penting

- Klasifikasi bersifat heuristik. Sinonim di luar kamus akan menjadi
  `unclassified`; tambahkan istilah di `src/text.py` daripada menebak.
- Satu kalimat menghasilkan paling banyak satu kebutuhan, jadi kalimat majemuk
  sebaiknya dipecah sendiri.
- Prioritas adalah default per kategori, bukan pengganti kesepakatan dengan
  stakeholder.
- Output AI bisa tidak lengkap atau terlalu percaya diri. Aplikasi menandai
  mesin mana yang membuat draf, dan tinjauan manusia tetap wajib.
- Perusahaan dan data contoh bersifat fiktif. Jangan mengirim data rahasia ke
  API pihak ketiga tanpa izin.

## Lisensi

MIT. Lihat [LICENSE](LICENSE).
