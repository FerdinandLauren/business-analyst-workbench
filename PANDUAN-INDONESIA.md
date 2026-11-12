# Panduan Menjalankan Project (Bahasa Indonesia)

## Tujuan
Project ini adalah prototype portfolio untuk menunjukkan alur kerja IT Business Analyst: memahami masalah, menyusun kebutuhan, menganalisis proses, membuat BRD, dan menyiapkan UAT dengan bantuan AI.

## Menjalankan di Windows
1. Ekstrak ZIP.
2. Buka folder project di VS Code.
3. Buka terminal pada folder tersebut.
4. Jalankan:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

5. Buka alamat lokal yang muncul di terminal.

Jika PowerShell memblokir aktivasi environment, gunakan Command Prompt:
```cmd
.venv\Scripts\activate.bat
```

## Menjalankan tes
```bash
python -m unittest discover -s tests -v
```

## Catatan penting
- Aplikasi tetap berjalan tanpa API key.
- Mode lokal menggunakan aturan kata kunci sederhana, bukan model AI sungguhan.
- API AI bersifat opsional. Jangan pernah mengunggah data perusahaan yang rahasia.
- Semua output adalah draft dan perlu diperiksa manusia.
- Studi kasus perusahaan dan datanya fiktif.
