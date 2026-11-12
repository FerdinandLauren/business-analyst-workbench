# Design — Workbench v2: generic, bilingual, deterministic

Status: awaiting approval
Tanggal: 2026-11-12

## 1. Intent / why

Aplikasi sekarang hanya benar untuk skenario procurement bawaan. Requirement
diambil apa adanya dari kalimat keluhan, BRD punya bagian hardcoded (approval
matrix, ERP, supplier), UAT selalu template yang sama, dan proses analisis hanya
mengecek 5 kata kunci. Untuk dipublikasikan sebagai portfolio, aplikasi harus
menerima problem statement apa pun dan menghasilkan draft yang layak dibaca.

Pemilik project memilih: **rule-based saja (tanpa API key wajib)**, dengan slot
API key opsional yang bisa diisi pengguna sendiri, output **EN/ID** yang bisa
dipilih di kanan atas, dan publikasi GitHub dengan commit bertahap.

## 2. Goals

- Input apa pun (bukan procurement) menghasilkan requirement yang terbaca
  sebagai requirement, bukan tempelan kalimat keluhan.
- BRD, process analysis, dan UAT mengikuti isi input. Tidak ada sisa istilah
  yang tidak relevan.
- Toggle bahasa EN/ID di kanan atas; label UI dan dokumen yang dihasilkan ikut.
- Deterministik: input sama → output sama, bisa diuji otomatis.
- API key opsional dari UI (hanya di memori sesi), fallback otomatis ke engine
  rule-based kalau kosong/gagal.
- Unit test untuk engine + i18n, plus CI GitHub Actions.
- Repo git bersih dengan commit bertahap (bukan satu commit raksasa).

## 3. Non-goals

- Tidak mengganti engine rule-based dengan LLM sebagai default.
- Tidak menyimpan API key ke disk, `.env`, atau commit.
- Tidak menghapus skenario procurement; tetap jadi contoh default.
- Tidak menambah dependency baru (kecuali opsional `openai` yang sudah ada).

## 4. Anti-goals (dianggap gagal walau kode jalan)

- Output generik yang sama untuk semua input, mis. "The system shall support the
  business need described by the stakeholder."
- Istilah procurement muncul saat input tentang klinik/HR/logistik.
- Toggle bahasa yang hanya mengubah label UI tapi dokumen tetap satu bahasa.
- Commit awal berisi seluruh perubahan sekaligus.

## 5. Arsitektur

```
src/
  i18n.py          STRINGS[lang] untuk UI + template dokumen, detect_language()
  text.py          split_sentences(), normalize(), keyword match word-boundary,
                   detect_categories(), detect_pain_signals(), detect_entities()
  requirements.py  extract_requirements(text, lang) -> list[Requirement]
  process.py       analyze_process(as_is, to_be, lang) -> rows + severity + summary
  uat.py           make_uat_cases(reqs, lang) -> steps per kategori, priority turunan
  brd.py           brd_markdown(...) -> semua bagian diturunkan dari input
  llm.py           optional: OpenAI pakai key dari UI/env/secrets, prompt dari
                   ai/prompts/*.md, return None saat gagal
app/streamlit_app.py
tests/             unittest (stdlib, tanpa dependency baru)
.github/workflows/tests.yml
```

Modul dipisah supaya tiap bagian bisa diuji tanpa Streamlit. Fungsi engine murni
(tidak menyentuh `st.session_state`).

## 6. Aturan generate requirement (deterministik)

1. Pecah kalimat (regex `[.!?;\n]`), buang kalimat < 10 karakter dan sapaan
   (`halo`, `hai`, `terima kasih`, dan sejenisnya).
2. Deteksi kategori bisnis dari kamus ID+EN dengan pencocokan kata utuh
   (word boundary), bukan substring: `scheduling, intake, approval, payment,
   reporting, tracking, notification, validation, integration, audit, search,
   access, inventory, support`.
3. Deteksi sinyal masalah: `manual, sering salah, bentrok, tidak tahu, lambat,
   hilang, dobel, tidak konsisten, tidak ada, susah, ribet`.
4. Statement disusun dari template kategori + sinyal masalah + entitas yang
   terdeteksi, mis. "Jadwal sering bentrok karena dicatat di buku" →
   "Sistem harus menyediakan satu jadwal terpusat yang mencegah bentrok."
5. Kategori tidak dikenali → `Needs analyst review`, statement netral, plus satu
   pertanyaan klarifikasi yang spesifik terhadap kalimat itu.
6. NFR: keamanan, performa, ketersediaan, kepatuhan, usability, maintainability
   → type `Non-functional` dengan subkategori. Kategori fungsional menang lebih
   dulu; sinyal NFR hanya dipakai kalau tidak ada kategori fungsional yang
   cocok. Kategori `audit` juga ber-type `Non-functional` (aturan lama).
7. Percobaan pencocokan "WhatsApp" tidak boleh lagi memicu kategori
   `integration` (bug `sap` substring).

## 7. Dokumen yang dihasilkan

- **BRD**: executive summary, problem, objectives (dari input + pain dominan),
  stakeholders, scope, requirement table, traceability req→UAT (dibuat dengan
  memanggil `make_uat_cases` di dalam builder), assumptions (hanya yang relevan
  dengan kategori terdeteksi), open questions (dari item `Needs analyst review`
  + area proses yang kosong di To-Be, lewat parameter `process` opsional).
- **Process analysis**: 5 area tetap, tiap baris punya evidence kutipan +
  severity (`Improve / Clarify / Potential regression / Unspecified`) + ringkasan
  jumlah langkah manual dan handoff yang terdeteksi.
- **UAT**: langkah berbeda per kategori (mis. approval vs payment vs reporting),
  priority dari tipe/kategori requirement, preconditions mengikuti kategori.

## 8. UI

- Toggle `EN | ID` di kanan atas (kolom terakhir header, segmented control).
  Default mengikuti bahasa input saat pertama kali analisis.
- Sidebar: expander "AI (optional)" → password input API key + nama model +
  checkbox "pakai key saya untuk draft BRD". Key hanya di `st.session_state`.
  Tanpa key → rule-based, dengan caption jelas.
- Perbaikan state: requirement dihitung dari teks tab yang sedang dipakai
  (cache per hash teks), tidak lagi meminjam state tab lain.
- `use_container_width` diganti `width="stretch"` (deprecated di Streamlit 1.67).
- Download CSV/Markdown tetap ada, ditambah tombol copy-friendly text area.

## 9. Testing

`unittest` (stdlib). Kasus minimal:

- Klinik gigi (ID): kategori jadwal/pembayaran/laporan terdeteksi, bukan
  procurement.
- Procurement (EN): perilaku lama tetap benar.
- Input kosong / 1 kalimat / teks tanpa kategori.
- False positive `WhatsApp` → bukan `integration`.
- NFR: audit log, response time, enkripsi.
- BRD untuk input klinik tidak memuat `ERP`, `supplier`, `approval matrix`.
- UAT steps berbeda antara requirement approval dan reporting.
- i18n: semua key ada di EN dan ID; tidak ada key yang hanya di satu bahasa.

CI: GitHub Actions, `python -m unittest discover -s tests -v` di Python
3.11/3.12/3.13.

## 10. Rencana commit (bertahap)

1. `chore: add project scaffold and license`
2. `test: add failing engine specs for generic input`
3. `refactor: extract text detection helpers`
4. `feat: generate requirements from any problem statement`
5. `feat: derive process analysis from detected evidence`
6. `feat: generate category-aware UAT scenarios`
7. `feat: build BRD sections from input instead of fixed text`
8. `feat: add EN/ID language toggle`
9. `feat: allow optional user-supplied API key`
10. `fix: key session state by input text`
11. `test: cover engine, i18n, and regression cases`
12. `docs: update README and Indonesian guide`
13. `ci: run tests on push`

Setiap commit harus lolos `python -m unittest` sebelum lanjut.

## 11. Risiko

- Heuristik ID/EN bisa salah kategori. Mitigasi: label `Needs analyst review`
  + pertanyaan klarifikasi, dan catatan bahwa output adalah draft.
- Perubahan output membuat `docs/*.md` dan README harus diselaraskan.
- Nama project di GitHub dan lisensi perlu keputusan pemilik.
