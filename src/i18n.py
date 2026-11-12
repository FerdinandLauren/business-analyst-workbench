"""Bilingual user-facing text and language detection.

Every key exists in both languages. Tests enforce parity, so adding a string
means adding it to ``en`` and ``id`` in the same commit.
"""
from __future__ import annotations

LANGS = ("en", "id")

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        # ---------------------------------------------------------------- UI
        "ui.app_title": "Business Analyst Workbench",
        "ui.app_caption": (
            "From business problem to candidate requirements, process insights, "
            "a BRD draft, and UAT scenarios."
        ),
        "ui.disclaimer": (
            "Prototype only. Every output is a draft and must be validated by a human "
            "stakeholder. Nothing leaves this machine unless you supply your own API key."
        ),
        "ui.sidebar_project": "Project name",
        "ui.language": "Language",
        "ui.tab_requirements": "1. Requirement Analyzer",
        "ui.tab_brd": "2. BRD Draft",
        "ui.tab_process": "3. Process Analyzer",
        "ui.tab_uat": "4. UAT Generator",
        "ui.btn_analyze": "Analyze requirements",
        "ui.btn_brd": "Generate BRD draft",
        "ui.btn_process": "Analyze process gaps",
        "ui.btn_uat": "Generate UAT scenarios",
        "ui.download_reqs": "Download requirements CSV",
        "ui.download_brd": "Download BRD Markdown",
        "ui.download_uat": "Download UAT CSV",
        "ui.empty_state": "Enter a business problem to begin.",
        "ui.stale_input": "The input changed. Analyze again to refresh the results.",
        "ui.ai_expander": "AI draft (optional)",
        "ui.ai_key": "API key",
        "ui.ai_model": "Model",
        "ui.ai_enable": "Use my key for the BRD draft",
        "ui.ai_caption_local": (
            "Running the local rule-based engine. No key is configured, so nothing "
            "leaves this machine."
        ),
        "ui.ai_caption_llm": (
            "AI-assisted draft generated with your key. Human review is still required."
        ),
        "ui.ai_reset": "Clear session data",
        "ui.step_analyze_hint": (
            "Tip: write one sentence per problem or expectation. The analyzer splits "
            "the text into sentences."
        ),
        # -------------------------------------------------- Requirements
        "req.col_id": "ID",
        "req.col_type": "Type",
        "req.col_category": "Category",
        "req.col_statement": "Statement",
        "req.col_priority": "Priority",
        "req.col_status": "Status",
        "req.type_functional": "Functional",
        "req.type_nonfunctional": "Non-functional",
        "req.status_draft": "Draft",
        "req.status_needs_review": "Needs analyst review",
        "req.priority_high": "High",
        "req.priority_medium": "Medium",
        "req.priority_low": "Low",        "req.clarification": (
            'Clarify with the stakeholder: what outcome is expected for "{fragment}"?'
        ),
        "req.statement_unclassified": 'The system shall support: "{fragment}".',
        "req.nfr_security": (
            "The system shall protect data in transit and at rest, with access limited "
            "to authorised roles."
        ),
        "req.nfr_performance": (
            "The system shall keep response time under the agreed threshold during "
            "normal working hours."
        ),
        "req.nfr_availability": (
            "The system shall stay available during agreed operating hours and recover "
            "from failure within an agreed window."
        ),
        "req.nfr_compliance": (
            "The system shall keep records and processing aligned with applicable "
            "regulation and internal policy."
        ),
        "req.nfr_usability": (
            "The system shall let a new user complete the main task without formal "
            "training."
        ),
        "req.nfr_maintainability": (
            "The system shall stay modular and documented so that changes remain local "
            "and testable."
        ),
        # ---------------------------------------------------- Categories
        "cat.scheduling": "Scheduling",
        "cat.intake": "Request intake",
        "cat.approval": "Approval",
        "cat.payment": "Payment",
        "cat.reporting": "Reporting",
        "cat.tracking": "Tracking",
        "cat.notification": "Notification",
        "cat.validation": "Validation",
        "cat.integration": "Integration",
        "cat.audit": "Audit",
        "cat.search": "Search",
        "cat.access": "Access control",
        "cat.inventory": "Inventory",
        "cat.support": "Support",
        "cat.unclassified": "Unclassified",
        "cat.nfr_security": "Non-functional: security",
        "cat.nfr_performance": "Non-functional: performance",
        "cat.nfr_availability": "Non-functional: availability",
        "cat.nfr_compliance": "Non-functional: compliance",
        "cat.nfr_usability": "Non-functional: usability",
        "cat.nfr_maintainability": "Non-functional: maintainability",
        # ------------------------------------------------------- Process
        "proc.area_visibility": "Visibility",
        "proc.area_validation": "Validation",
        "proc.area_approval": "Approval control",
        "proc.area_notification": "Notifications",
        "proc.area_auditability": "Auditability",
        "proc.severity_improve": "Improve",
        "proc.severity_clarify": "Clarify",
        "proc.severity_regression": "Potential regression",
        "proc.severity_unspecified": "Unspecified",
        "proc.col_area": "Area",
        "proc.col_severity": "Severity",
        "proc.col_observation": "Observation",
        "proc.col_evidence": "Evidence",
        "proc.metric_manual": "Manual markers in As-Is",
        "proc.metric_handoffs": "Handoffs in As-Is",
        "proc.metric_improve": "Areas to improve",
        "proc.obs_improve": (
            "Potential improvement: {area} is explicit in the proposed process but "
            "missing today."
        ),
        "proc.obs_clarify": (
            "{area} appears in both descriptions; clarify what changes in the To-Be "
            "design."
        ),
        "proc.obs_regression": (
            "Potential regression: {area} is used today but no longer described in the "
            "To-Be process."
        ),
        "proc.obs_unspecified": (
            "{area} is not explicit in either description; confirm whether it is "
            "required."
        ),
        # ----------------------------------------------------------- UAT
        "uat.col_test_id": "Test ID",
        "uat.col_requirement_id": "Requirement",
        "uat.col_scenario": "Scenario",
        "uat.col_preconditions": "Preconditions",
        "uat.col_steps": "Steps",
        "uat.col_expected": "Expected result",
        "uat.col_priority": "Priority",
        "uat.col_status": "Status",
        "uat.status_not_run": "Not run",
        "uat.scenario": "Verify that the system can: {statement}",
        "uat.steps_approval": (
            "1. Sign in as the requester and submit a new request.\n"
            "2. Sign in as the approver and approve the request.\n"
            "3. Check that the requester sees the new status.\n"
            "4. Confirm an audit entry exists for the decision."
        ),
        "uat.steps_payment": (
            "1. Record a payment for an existing request.\n"
            "2. Compare the recorded amount with the source document.\n"
            "3. Confirm a receipt is issued with the same amount."
        ),
        "uat.steps_reporting": (
            "1. Open the report.\n"
            "2. Filter the period under test.\n"
            "3. Compare the totals with the source data."
        ),
        "uat.steps_scheduling": (
            "1. Book a slot for a new customer.\n"
            "2. Try to book the same slot again and confirm it is rejected.\n"
            "3. Reschedule the first booking and confirm the history is kept."
        ),
        "uat.steps_unclassified": (
            "1. Sign in with a valid account.\n"
            "2. Open the function described by the requirement.\n"
            "3. Perform the business action with valid data.\n"
            "4. Confirm the outcome and that the data is stored correctly."
        ),
        "uat.precondition_approval": "A request is waiting for approval and both users exist.",
        "uat.precondition_payment": "An approved request with a known amount exists.",
        "uat.precondition_reporting": "Source data for the period is available for reconciliation.",
        "uat.precondition_scheduling": "At least one open slot exists in the schedule.",
        "uat.precondition_validation": "A form with at least one required field is available.",
        "uat.precondition_notification": "An event that should trigger a notification can be created.",
        "uat.precondition_tracking": "A record exists whose status can change during the test.",
        "uat.precondition_integration": "The external system is reachable from the test environment.",
        "uat.precondition_audit": "A test record can be changed while the audit trail is readable.",
        "uat.precondition_intake": "The request form is reachable by a test user.",
        "uat.precondition_search": "At least ten test records exist.",
        "uat.precondition_access": "Two test users with different roles exist.",
        "uat.precondition_inventory": "Stock records exist for two items.",
        "uat.precondition_support": "A complaint can be created by a test user.",
        "uat.precondition_unclassified": "A valid account and test data are available.",
        "uat.expected_approval": "The request moves to the approved state and the decision is recorded.",
        "uat.expected_payment": "The recorded amount matches the source document and a receipt is issued.",
        "uat.expected_reporting": "Totals in the report match the source data for the period.",
        "uat.expected_scheduling": "The duplicate booking is rejected and the reschedule keeps its history.",
        "uat.expected_unclassified": "The function behaves as described and the result is stored.",
        "uat.expected_intake": "The request is submitted with all mandatory fields and appears in the queue.",
        "uat.expected_tracking": "The new status is visible to the user right after the change.",
        "uat.expected_notification": "The user receives the notification on the agreed channel in time.",
        "uat.expected_validation": "Invalid input is rejected with a message that names the field.",
        "uat.expected_integration": "Data is exchanged with the external system without manual re-entry.",
        "uat.expected_audit": "The change appears in the audit trail with user, time, and values.",
        "uat.expected_search": "The expected records are found and filters can be combined.",
        "uat.expected_access": "Each user only sees the actions allowed for their role.",
        "uat.expected_inventory": "Stock quantity changes correctly once the movement is recorded.",
        "uat.expected_support": "The complaint is recorded, assigned, and its status can be followed.",
        # ----------------------------------------------------------- BRD
        "brd.section_summary": "Executive summary",
        "brd.section_problem": "Business problem",
        "brd.section_objectives": "Business objectives",
        "brd.section_stakeholders": "Stakeholders",
        "brd.section_scope_in": "In scope",
        "brd.section_scope_out": "Out of scope",
        "brd.section_requirements": "Candidate requirements",
        "brd.section_traceability": "Traceability to UAT",
        "brd.section_assumptions": "Assumptions and constraints",
        "brd.section_questions": "Open questions",
        "brd.section_acceptance": "Acceptance approach",
        "brd.assumption_scheduling": "Working hours, slot duration, and cancellation rules must be confirmed.",
        "brd.assumption_intake": "Mandatory fields per request type must be confirmed.",
        "brd.assumption_approval": "Approval thresholds and who may approve each request type must be confirmed.",
        "brd.assumption_payment": "Reconciliation rules and who may issue refunds must be confirmed.",
        "brd.assumption_reporting": "Report definitions and the period cut-off must be confirmed.",
        "brd.assumption_tracking": "Which statuses are visible to which role must be confirmed.",
        "brd.assumption_notification": "Channel, template, and quiet hours must be confirmed.",
        "brd.assumption_validation": "Validation rules and error messages must be confirmed.",
        "brd.assumption_integration": (
            "Integration with an external system is subject to API, security, and "
            "data-governance review."
        ),
        "brd.assumption_audit": "Retention period and who may read the audit trail must be confirmed.",
        "brd.assumption_search": "Searchable fields and result limits must be confirmed.",
        "brd.assumption_access": "Role definitions and least-privilege rules must be confirmed.",
        "brd.assumption_inventory": "Stock unit, location, and adjustment rules must be confirmed.",
        "brd.assumption_support": "Service-level targets and escalation paths must be confirmed.",
        "brd.assumption_general": (
            "The scenario is fictional; business rules and role permissions require "
            "stakeholder confirmation."
        ),
        "brd.assumption_nfr": (
            "Non-functional targets need measurable acceptance thresholds agreed with "
            "the business owner."
        ),
        "brd.question_general": "Which stakeholder can confirm the open questions above?",
        "brd.trace_header": "| Requirement | UAT case |",
        "brd.status_line": (
            "Status: draft for human review. Generated by the local rule-based engine."
        ),
        "brd.summary_text": (
            "{project} is drafted from the problem statement below. This version "
            "contains {count} candidate requirements and {uat_count} matching UAT "
            "scenarios in {language}."
        ),
        "brd.acceptance_text": (
            "Acceptance is confirmed through {count} draft UAT scenarios listed in the "
            "traceability section. Each case needs a business sign-off before release."
        ),
        "brd.empty_requirements": (
            "No candidate requirement was extracted. Rewrite the problem as one "
            "concrete sentence per issue, then generate again."
        ),
        "brd.empty_section": "Not provided.",
        "brd.question_area": (
            "Which stakeholder can confirm whether {area} is required in the new process?"
        ),
        "brd.lang_english": "English",
        "brd.lang_indonesian": "Bahasa Indonesia",
        "brd.footer": (
            "*Generated as a draft by the Business Analyst Workbench. Review and approve "
            "before use.*"
        ),
        "brd.objective_derived_automation": "Remove manual re-entry from the process.",
        "brd.objective_derived_accuracy": "Apply one consistent rule to every case.",
        "brd.objective_derived_consolidation": "Keep one source of truth.",
        "brd.objective_derived_visibility": "Make status visible without asking.",
    },
    "id": {
        # ---------------------------------------------------------------- UI
        "ui.app_title": "Business Analyst Workbench",
        "ui.app_caption": (
            "Dari masalah bisnis menjadi kandidat kebutuhan, temuan proses, draf BRD, "
            "dan skenario UAT."
        ),
        "ui.disclaimer": (
            "Hanya prototipe. Semua output adalah draf dan wajib divalidasi oleh "
            "stakeholder. Tidak ada data yang keluar dari mesin ini kecuali kamu "
            "memasukkan API key milikmu sendiri."
        ),
        "ui.sidebar_project": "Nama proyek",
        "ui.language": "Bahasa",
        "ui.tab_requirements": "1. Analisis Kebutuhan",
        "ui.tab_brd": "2. Draf BRD",
        "ui.tab_process": "3. Analisis Proses",
        "ui.tab_uat": "4. Generator UAT",
        "ui.btn_analyze": "Analisis kebutuhan",
        "ui.btn_brd": "Buat draf BRD",
        "ui.btn_process": "Analisis celah proses",
        "ui.btn_uat": "Buat skenario UAT",
        "ui.download_reqs": "Unduh kebutuhan (CSV)",
        "ui.download_brd": "Unduh BRD (Markdown)",
        "ui.download_uat": "Unduh UAT (CSV)",
        "ui.empty_state": "Masukkan masalah bisnis untuk mulai.",
        "ui.stale_input": "Input berubah. Jalankan analisis lagi untuk memperbarui hasil.",
        "ui.ai_expander": "Draf dengan AI (opsional)",
        "ui.ai_key": "API key",
        "ui.ai_model": "Model",
        "ui.ai_enable": "Pakai key saya untuk draf BRD",
        "ui.ai_caption_local": (
            "Menjalankan mesin lokal berbasis aturan. Tidak ada key, jadi tidak ada data "
            "yang keluar dari mesin ini."
        ),
        "ui.ai_caption_llm": (
            "Draf dibantu AI memakai key kamu. Tinjauan manusia tetap wajib."
        ),
        "ui.ai_reset": "Hapus data sesi",
        "ui.step_analyze_hint": (
            "Tips: tulis satu kalimat untuk setiap masalah atau harapan. Analisis "
            "memecah teks per kalimat."
        ),
        # -------------------------------------------------- Requirements
        "req.col_id": "ID",
        "req.col_type": "Tipe",
        "req.col_category": "Kategori",
        "req.col_statement": "Pernyataan",
        "req.col_priority": "Prioritas",
        "req.col_status": "Status",
        "req.type_functional": "Fungsional",
        "req.type_nonfunctional": "Non-fungsional",
        "req.status_draft": "Draf",
        "req.status_needs_review": "Perlu tinjauan analis",
        "req.priority_high": "Tinggi",
        "req.priority_medium": "Sedang",
        "req.priority_low": "Rendah",
        "req.clarification": (
            'Konfirmasi ke stakeholder: hasil apa yang diharapkan dari "{fragment}"?'
        ),
        "req.statement_unclassified": 'Sistem harus mendukung: "{fragment}".',
        "req.nfr_security": (
            "Sistem harus melindungi data saat dikirim dan disimpan, dengan akses "
            "terbatas pada peran berwenang."
        ),
        "req.nfr_performance": (
            "Sistem harus menjaga waktu respons di bawah ambang yang disepakati pada "
            "jam kerja normal."
        ),
        "req.nfr_availability": (
            "Sistem harus tetap tersedia pada jam operasional yang disepakati dan pulih "
            "dari gangguan dalam batas waktu yang disepakati."
        ),
        "req.nfr_compliance": (
            "Sistem harus menjaga pencatatan dan pemrosesan sesuai regulasi yang berlaku "
            "dan kebijakan internal."
        ),
        "req.nfr_usability": (
            "Sistem harus memungkinkan pengguna baru menyelesaikan tugas utama tanpa "
            "pelatihan formal."
        ),
        "req.nfr_maintainability": (
            "Sistem harus modular dan terdokumentasi agar perubahan tetap lokal dan "
            "dapat diuji."
        ),
        # ---------------------------------------------------- Categories
        "cat.scheduling": "Penjadwalan",
        "cat.intake": "Pengajuan",
        "cat.approval": "Persetujuan",
        "cat.payment": "Pembayaran",
        "cat.reporting": "Pelaporan",
        "cat.tracking": "Pelacakan",
        "cat.notification": "Notifikasi",
        "cat.validation": "Validasi",
        "cat.integration": "Integrasi",
        "cat.audit": "Audit",
        "cat.search": "Pencarian",
        "cat.access": "Kontrol akses",
        "cat.inventory": "Inventaris",
        "cat.support": "Dukungan",
        "cat.unclassified": "Belum terklasifikasi",
        "cat.nfr_security": "Non-fungsional: keamanan",
        "cat.nfr_performance": "Non-fungsional: performa",
        "cat.nfr_availability": "Non-fungsional: ketersediaan",
        "cat.nfr_compliance": "Non-fungsional: kepatuhan",
        "cat.nfr_usability": "Non-fungsional: kemudahan penggunaan",
        "cat.nfr_maintainability": "Non-fungsional: pemeliharaan",
        # ------------------------------------------------------- Process
        "proc.area_visibility": "Visibilitas",
        "proc.area_validation": "Validasi",
        "proc.area_approval": "Kontrol persetujuan",
        "proc.area_notification": "Notifikasi",
        "proc.area_auditability": "Keterlacakan audit",
        "proc.severity_improve": "Perbaiki",
        "proc.severity_clarify": "Klarifikasi",
        "proc.severity_regression": "Potensi regresi",
        "proc.severity_unspecified": "Belum disebut",
        "proc.col_area": "Area",
        "proc.col_severity": "Tingkat",
        "proc.col_observation": "Observasi",
        "proc.col_evidence": "Bukti",
        "proc.metric_manual": "Penanda manual di As-Is",
        "proc.metric_handoffs": "Serah terima di As-Is",
        "proc.metric_improve": "Area untuk diperbaiki",
        "proc.obs_improve": (
            "Potensi perbaikan: {area} sudah eksplisit di proses usulan tetapi belum "
            "ada saat ini."
        ),
        "proc.obs_clarify": (
            "{area} muncul di kedua deskripsi; perjelas apa yang berubah pada desain "
            "To-Be."
        ),
        "proc.obs_regression": (
            "Potensi regresi: {area} dipakai saat ini tetapi tidak lagi dijelaskan pada "
            "proses To-Be."
        ),
        "proc.obs_unspecified": (
            "{area} tidak eksplisit di kedua deskripsi; konfirmasi apakah memang "
            "dibutuhkan."
        ),
        # ----------------------------------------------------------- UAT
        "uat.col_test_id": "ID tes",
        "uat.col_requirement_id": "Kebutuhan",
        "uat.col_scenario": "Skenario",
        "uat.col_preconditions": "Prasyarat",
        "uat.col_steps": "Langkah",
        "uat.col_expected": "Hasil yang diharapkan",
        "uat.col_priority": "Prioritas",
        "uat.col_status": "Status",
        "uat.status_not_run": "Belum dijalankan",
        "uat.scenario": "Verifikasi bahwa sistem dapat: {statement}",
        "uat.steps_approval": (
            "1. Masuk sebagai pemohon dan kirim permohonan baru.\n"
            "2. Masuk sebagai penyetuju dan setujui permohonan.\n"
            "3. Pastikan pemohon melihat status terbaru.\n"
            "4. Pastikan ada catatan audit untuk keputusan tersebut."
        ),
        "uat.steps_payment": (
            "1. Catat pembayaran untuk permohonan yang sudah ada.\n"
            "2. Bandingkan jumlah tercatat dengan dokumen sumber.\n"
            "3. Pastikan struk diterbitkan dengan jumlah yang sama."
        ),
        "uat.steps_reporting": (
            "1. Buka laporan.\n"
            "2. Pilih periode yang diuji.\n"
            "3. Bandingkan total dengan data sumber."
        ),
        "uat.steps_scheduling": (
            "1. Buat jadwal untuk pelanggan baru.\n"
            "2. Coba buat jadwal yang sama dan pastikan ditolak.\n"
            "3. Ubah jadwal pertama dan pastikan riwayatnya tersimpan."
        ),
        "uat.steps_unclassified": (
            "1. Masuk dengan akun yang valid.\n"
            "2. Buka fungsi yang disebut pada kebutuhan.\n"
            "3. Lakukan aksi bisnis dengan data yang valid.\n"
            "4. Pastikan hasilnya sesuai dan data tersimpan dengan benar."
        ),
        "uat.precondition_approval": "Ada permohonan menunggu persetujuan dan kedua pengguna tersedia.",
        "uat.precondition_payment": "Ada permohonan disetujui dengan jumlah yang diketahui.",
        "uat.precondition_reporting": "Data sumber untuk periode tersebut tersedia untuk rekonsiliasi.",
        "uat.precondition_scheduling": "Setidaknya ada satu slot kosong pada jadwal.",
        "uat.precondition_validation": "Ada formulir dengan minimal satu field wajib.",
        "uat.precondition_notification": "Ada peristiwa yang seharusnya memicu notifikasi.",
        "uat.precondition_tracking": "Ada data yang statusnya dapat berubah selama pengujian.",
        "uat.precondition_integration": "Sistem eksternal dapat diakses dari lingkungan uji.",
        "uat.precondition_audit": "Data uji dapat diubah sementara jejak audit dapat dibaca.",
        "uat.precondition_intake": "Formulir permohonan dapat diakses pengguna uji.",
        "uat.precondition_search": "Tersedia minimal sepuluh data uji.",
        "uat.precondition_access": "Tersedia dua pengguna uji dengan peran berbeda.",
        "uat.precondition_inventory": "Tersedia data stok untuk dua barang.",
        "uat.precondition_support": "Keluhan dapat dibuat oleh pengguna uji.",
        "uat.precondition_unclassified": "Akun valid dan data uji tersedia.",
        "uat.expected_approval": "Permohonan berpindah ke status disetujui dan keputusannya tercatat.",
        "uat.expected_payment": "Jumlah tercatat sama dengan dokumen sumber dan struk diterbitkan.",
        "uat.expected_reporting": "Total pada laporan sama dengan data sumber periode tersebut.",
        "uat.expected_scheduling": "Jadwal ganda ditolak dan perubahan jadwal menyimpan riwayat.",
        "uat.expected_unclassified": "Fungsi berjalan sesuai deskripsi dan hasilnya tersimpan.",
        "uat.expected_intake": "Permohonan terkirim dengan semua field wajib dan masuk ke antrean.",
        "uat.expected_tracking": "Status terbaru langsung terlihat oleh pengguna setelah perubahan.",
        "uat.expected_notification": "Pengguna menerima notifikasi di kanal yang disepakati tepat waktu.",
        "uat.expected_validation": "Input tidak valid ditolak dengan pesan yang menyebut field terkait.",
        "uat.expected_integration": "Data bertukar dengan sistem eksternal tanpa input ulang manual.",
        "uat.expected_audit": "Perubahan tercatat di jejak audit lengkap dengan pengguna, waktu, dan nilai.",
        "uat.expected_search": "Data yang dicari ditemukan dan filter dapat dikombinasikan.",
        "uat.expected_access": "Setiap pengguna hanya melihat aksi yang diizinkan untuk perannya.",
        "uat.expected_inventory": "Jumlah stok berubah dengan benar setelah pergerakan dicatat.",
        "uat.expected_support": "Keluhan tercatat, ditugaskan, dan statusnya dapat diikuti.",
        # ----------------------------------------------------------- BRD
        "brd.section_summary": "Ringkasan eksekutif",
        "brd.section_problem": "Masalah bisnis",
        "brd.section_objectives": "Tujuan bisnis",
        "brd.section_stakeholders": "Stakeholder",
        "brd.section_scope_in": "Dalam ruang lingkup",
        "brd.section_scope_out": "Di luar ruang lingkup",
        "brd.section_requirements": "Kandidat kebutuhan",
        "brd.section_traceability": "Keterlacakan ke UAT",
        "brd.section_assumptions": "Asumsi dan batasan",
        "brd.section_questions": "Pertanyaan terbuka",
        "brd.section_acceptance": "Pendekatan penerimaan",
        "brd.assumption_scheduling": "Jam kerja, durasi slot, dan aturan pembatalan perlu dikonfirmasi.",
        "brd.assumption_intake": "Field wajib untuk setiap jenis permohonan perlu dikonfirmasi.",
        "brd.assumption_approval": "Ambang persetujuan dan siapa yang boleh menyetujui setiap jenis permohonan perlu dikonfirmasi.",
        "brd.assumption_payment": "Aturan rekonsiliasi dan siapa yang boleh mengembalikan dana perlu dikonfirmasi.",
        "brd.assumption_reporting": "Definisi laporan dan batas akhir periode perlu dikonfirmasi.",
        "brd.assumption_tracking": "Status mana yang terlihat oleh peran mana perlu dikonfirmasi.",
        "brd.assumption_notification": "Kanal, template, dan jam tenang notifikasi perlu dikonfirmasi.",
        "brd.assumption_validation": "Aturan validasi dan pesan kesalahan perlu dikonfirmasi.",
        "brd.assumption_integration": (
            "Integrasi dengan sistem eksternal bergantung pada tinjauan API, keamanan, "
            "dan tata kelola data."
        ),
        "brd.assumption_audit": "Masa retensi dan siapa yang boleh membaca jejak audit perlu dikonfirmasi.",
        "brd.assumption_search": "Field yang dapat dicari dan batas hasil perlu dikonfirmasi.",
        "brd.assumption_access": "Definisi peran dan aturan hak akses minimum perlu dikonfirmasi.",
        "brd.assumption_inventory": "Satuan stok, lokasi, dan aturan penyesuaian perlu dikonfirmasi.",
        "brd.assumption_support": "Target layanan dan jalur eskalasi perlu dikonfirmasi.",
        "brd.assumption_general": (
            "Skenario bersifat fiktif; aturan bisnis dan hak akses peran perlu "
            "dikonfirmasi stakeholder."
        ),
        "brd.assumption_nfr": (
            "Target non-fungsional membutuhkan ambang penerimaan terukur yang disepakati "
            "dengan pemilik bisnis."
        ),
        "brd.question_general": "Stakeholder mana yang dapat mengonfirmasi pertanyaan di atas?",
        "brd.trace_header": "| Kebutuhan | Skenario UAT |",
        "brd.status_line": (
            "Status: draf untuk tinjauan manusia. Dihasilkan mesin lokal berbasis aturan."
        ),
        "brd.summary_text": (
            "{project} disusun dari pernyataan masalah di bawah ini. Versi ini memuat "
            "{count} kandidat kebutuhan dan {uat_count} skenario UAT yang sesuai dalam "
            "bahasa {language}."
        ),
        "brd.acceptance_text": (
            "Penerimaan dikonfirmasi melalui {count} draf skenario UAT pada bagian "
            "keterlacakan. Setiap kasus memerlukan persetujuan bisnis sebelum rilis."
        ),
        "brd.empty_requirements": (
            "Tidak ada kandidat kebutuhan yang diekstrak. Tulis ulang masalah menjadi "
            "satu kalimat konkret per isu, lalu buat ulang."
        ),
        "brd.empty_section": "Belum diisi.",
        "brd.question_area": (
            "Stakeholder mana yang dapat mengonfirmasi apakah {area} diperlukan pada "
            "proses baru?"
        ),
        "brd.lang_english": "Inggris",
        "brd.lang_indonesian": "Bahasa Indonesia",
        "brd.footer": (
            "*Dihasilkan sebagai draf oleh Business Analyst Workbench. Tinjau dan "
            "setujui sebelum dipakai.*"
        ),
        "brd.objective_derived_automation": "Menghilangkan input ulang manual dari proses.",
        "brd.objective_derived_accuracy": "Menerapkan satu aturan yang konsisten untuk setiap kasus.",
        "brd.objective_derived_consolidation": "Menjaga satu sumber data.",
        "brd.objective_derived_visibility": "Menampilkan status tanpa perlu bertanya.",
    },
}

ID_MARKERS = (
    "dan", "atau", "yang", "tidak", "dengan", "untuk", "dari", "agar", "sering",
    "pada", "juga", "masih", "belum", "kami", "kita", "harus", "bisa", "sudah",
    "oleh", "dalam", "kalau", "supaya", "adalah", "akan", "ini", "itu",
)
EN_MARKERS = (
    "the", "and", "or", "with", "for", "from", "that", "this", "need", "needs",
    "must", "should", "users", "user", "system", "not", "can", "we", "our", "is",
    "are", "be", "by", "in", "on", "of", "to",
)


def t(key: str, lang: str = "en", **fmt: object) -> str:
    """Return the localized string for ``key``; raises KeyError when missing."""
    table = STRINGS[lang]
    value = table[key]
    return value.format(**fmt) if fmt else value


def detect_language(text: str) -> str:
    """Return ``"id"`` when Indonesian markers dominate, otherwise ``"en"``.

    Marker words alone fail on short Indonesian sentences that use no function
    words ("Pasien mendaftar lewat telepon"), so Indonesian affixes count as a
    weak signal too.
    """
    words = [w.strip(".,;:!?()\"'-") for w in text.lower().split()]
    words = [w for w in words if w]
    if not words:
        return "en"
    id_score = sum(1 for w in words if w in ID_MARKERS or _looks_indonesian(w))
    en_score = sum(1 for w in words if w in EN_MARKERS)
    return "id" if id_score > en_score else "en"


_ID_PREFIXES = ("me", "men", "mem", "meng", "di", "ber", "ter", "pe", "pen", "peng", "ke")
_ID_SUFFIXES = ("kan", "nya", "lah", "pun")


def _looks_indonesian(word: str) -> bool:
    return word.startswith(_ID_PREFIXES) or word.endswith(_ID_SUFFIXES)
