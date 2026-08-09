import streamlit as st
from google import genai

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Asisten Administrasi Guru SLB",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------------------------------------------------------
# PENGATURAN API KEY GEMINI (Mendukung Input Manual & Secrets)
# -----------------------------------------------------------------------------
st.sidebar.title("🔑 Pengaturan AI")

# Memeriksa apakah API Key sudah tersimpan di Secrets
secrets_key = st.secrets.get("GEMINI_API_KEY", "")

if secrets_key:
    api_key = secrets_key
    st.sidebar.success("API Key terdeteksi dari Secrets Sistem!")
else:
    api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi Asisten Administrasi Guru SLB Kurikulum Merdeka.")

# -----------------------------------------------------------------------------
# FORM IDENTITAS (GLOBAL INPUT)
# -----------------------------------------------------------------------------
st.title("🎓 Asisten Administrasi Guru SLB")
st.subheader("Generator Perangkat Ajar & Modul Kurikulum Merdeka")

with st.expander("📌 **Identitas Guru & Satuan Pendidikan** (Isi Terlebih Dahulu)", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_guru = st.text_input("Nama Guru", "Nama Guru, S.Pd.")
        nip_guru = st.text_input("NIP Guru", "-")
        nama_sekolah = st.text_input("Nama Sekolah", "SLB Negeri 1 Kulon Progo")
    with col2:
        nama_ks = st.text_input("Nama Kepala Sekolah", "Nama KS, M.Pd.")
        nip_ks = st.text_input("NIP Kepala Sekolah", "-")
        tahun_ajaran = st.text_input("Tahun Pelajaran", "2026/2027")
    with col3:
        jenis_kekhususan = st.selectbox(
            "Jenis Kekhususan/Hambatan",
            ["Hambatan Intelektual (Tunagrahita)", "Hambatan Pendengaran (Tunarungu)", 
             "Hambatan Penglihatan (Tunanetra)", "Hambatan Anggota Gerak (Tunadaksa)", 
             "Autis / Spektrum Autisme", "Ganda / Kombinasi"]
        )
        fase_kelas = st.selectbox("Fase / Kelas", ["Fase A (Kelas 1-2)", "Fase B (Kelas 3-4)", "Fase C (Kelas 5-6)", "Fase D (SMPLB)", "Fase E/F (SMALB)"])
        mata_pelajaran = st.text_input("Mata Pelajaran", "IPAS / IPA")

# -----------------------------------------------------------------------------
# MENU UTAMA TAB
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 1. CP, TP, ATP, Prota & Promes", 
    "📝 2. RPP / Modul Ajar Mendalam", 
    "🎨 3. LKM / LKPD Interaktif", 
    "🖼️ 4. Prompt Sampul A4"
])

# =============================================================================
# TAB 1: PEMETAAN CP, TP, ATP, PROTA, PROSEM & KKTP
# =============================================================================
with tab1:
    st.header("Pemetaan CP, TP, ATP, Prota, Prosem & KKTP")
    
    cp_text = st.text_area("Masukkan Capaian Pembelajaran (CP) dari BSKAP/Dokumen Resmi:", height=120)
    materi_list = st.text_area("Masukkan Daftar Materi/Bab per Semester (Pisahkan dengan baris baru):", 
                               "Semester 1:\n- Mengenal Anggota Tubuh\n- Merawat Diri\n\nSemester 2:\n- Mengenal Lingkungan Rumah")
    
    sub_option = st.radio("Pilih Dokumen yang Ingin Dihasilkan:", 
                          ["CP, TP & ATP", "Program Tahunan (Prota)", "Program Semester (Prosem)", "KKTP & Asesmen Sumatif"])

    if st.button("Hasilkan Dokumen Tab 1"):
        if not api_key:
            st.error("API Key Gemini belum diisi di sidebar!")
        else:
            with st.spinner("Sedang memproses dokumen..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt_tab1 = f"""
                    Bertindaklah sebagai Konsultan Kurikulum Sekolah Luar Biasa (SLB).
                    Identitas:
                    - Nama Guru: {nama_guru} (NIP: {nip_guru})
                    - Kepala Sekolah: {nama_ks} (NIP: {nip_ks})
                    - Sekolah: {nama_sekolah}
                    - Jenis Kekhususan: {jenis_kekhususan}
                    - Jenjang/Fase: {fase_kelas}
                    - Mata Pelajaran: {mata_pelajaran}
                    - Tahun Pelajaran: {tahun_ajaran}
                    
                    Capaian Pembelajaran (CP): {cp_text}
                    Daftar Materi: {materi_list}
                    
                    Tugas: Buatkan pemetaan {sub_option} lengkap dalam bentuk tabel Markdown yang rapi.
                    Sesuaikan tingkat kesulitan, instruksi, dan bahasa agar relevan dengan karakter peserta didik berkebutuhan khusus ({jenis_kekhususan}).
                    Gunakan prinsip hierarki konsep (mudah ke sulit, konkret ke abstrak).
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_tab1,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghubungi server AI: {e}")

# =============================================================================
# TAB 2: MODUL AJAR / RPP MENDALAM
# =============================================================================
with tab2:
    st.header("Rencana Pembelajaran Mendalam (RPP / Modul Ajar)")
    
    col_rpp1, col_rpp2 = st.columns(2)
    with col_rpp1:
        topik_rpp = st.text_input("Topik Pembelajaran:", "Mengenal Nama-nama Buah")
        tp_rpp = st.text_area("Tujuan Pembelajaran (TP):", "Peserta didik dapat menunjukkan 3 jenis buah segar melalui benda konkret/gambar.")
        alokasi_waktu = st.text_input("Alokasi Waktu:", "2 x 35 menit")
    with col_rpp2:
        model_pembelajaran = st.selectbox("Model Pembelajaran:", ["Direct Instruction", "Contextual Learning", "Problem Based Learning", "Discovery Learning", "Project Based Learning (PjBL)"])
        prinsip_pembelajaran = st.multiselect("Prinsip Pembelajaran:", ["Bermakna", "Menggembirakan", "Berkesadaran"], default=["Bermakna", "Menggembirakan"])

    if st.button("Hasilkan Modul Ajar / RPP"):
        if not api_key:
            st.error("API Key Gemini belum diisi di sidebar!")
        else:
            with st.spinner("Merancang Modul Ajar..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt_rpp = f"""
                    Bertindaklah sebagai Guru Penggerak dan Ahli Pembelajaran Khusus SLB.
                    Buat RPP/Modul Ajar dengan format Markdown.
                    
                    Identitas:
                    - Guru: {nama_guru} | NIP: {nip_guru}
                    - Sekolah: {nama_sekolah}
                    - Mapel: {mata_pelajaran} | Fase/Kelas: {fase_kelas}
                    - Jenis Kekhususan: {jenis_kekhususan}
                    - Topik: {topik_rpp}
                    - Tujuan Pembelajaran: {tp_rpp}
                    - Alokasi Waktu: {alokasi_waktu}
                    - Model Pembelajaran: {model_pembelajaran}
                    - Prinsip: {', '.join(prinsip_pembelajaran)}
                    
                    Sajikan dalam struktur tabel 2 kolom sesuai instruksi:
                    1. Judul Catchy di bagian atas
                    2. Identitas Pembelajaran
                    3. Identifikasi & Desain Pembelajaran (Integrasi Ice Breaking & Kontekstual)
                    4. Langkah Kegiatan (Pendahuluan, Inti sesuai Sintak {model_pembelajaran}, Penutup)
                    5. Asesmen (Formatif Awal, Proses, dan Akhir beserta Soal & Kunci)
                    6. KKTP, Program Remedial, dan Pengayaan
                    
                    Catatan Khusus: Sesuaikan langkah kegiatan dengan karakteristik anak {jenis_kekhususan}.
                    """
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_rpp,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghubungi server AI: {e}")

# =============================================================================
# TAB 3: LEMBAR KERJA MURID (LKM / LKPD) INTERAKTIF
# =============================================================================
with tab3:
    st.header("Lembar Kerja Murid (LKM) / LKPD Interaktif A4")
    
    materi_lkm = st.text_input("Materi / Topik LKM:", "Mewarnai dan Menghitung Buah")
    tp_lkm = st.text_area("Tujuan Pembelajaran LKM:", "Murid dapat menghitung jumlah buah 1-5 dan mewarnainya.")
    
    if st.button("Hasilkan LKM Interaktif"):
        if not api_key:
            st.error("API Key Gemini belum diisi di sidebar!")
        else:
            with st.spinner("Membuat LKM Workbook..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt_lkm = f"""
                    Bertindaklah sebagai Senior Instructional Designer & Educational Graphic Designer untuk SLB.
                    Tugas Anda adalah membuat Lembar Kerja Murid (LKM) berformat Markdown interaktif siap cetak A4.
                    
                    Informasi LKM:
                    - Mata Pelajaran: {mata_pelajaran}
                    - Kelas/Fase: {fase_kelas}
                    - Jenis Kekhususan: {jenis_kekhususan}
                    - Materi/Topik: {materi_lkm}
                    - Tujuan Pembelajaran: {tp_lkm}
                    
                    Struktur LKM Wajib:
                    1. Cover Mini (Judul, Nama, Kelas, Tanggal)
                    2. Tujuan Belajar Sederhana
                    3. Petunjuk Pengerjaan dengan Ikon
                    4. Apersepsi Visual & Pertanyaan Pemantik
                    5. Aktivitas 1 – Amati (disertai deskripsi visual gambar yang mudah dicari/digambar)
                    6. Aktivitas 2 – Diskusikan/Tanya Jawab
                    7. Aktivitas 3 – Eksplorasi Konkret
                    8. Aktivitas 4 – Berkarya/Mewarnai
                    9. Tantangan Sederhana
                    10. Refleksi Murid (😊 😐 😔)
                    
                    Sajikan dalam format Markdown yang sangat rapi dan ramah cetak.
                    """
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_lkm,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghubungi server AI: {e}")

# =============================================================================
# TAB 4: GENERATOR PROMPT SAMPUL/COVER
# =============================================================================
with tab4:
    st.header("Generator Prompt Sampul Dokumen A4")
    
    judul_sampul = st.text_input("Judul Dokumen Sampul:", "MODUL AJAR IPAS FASE A")
    
    if st.button("Buatkan Prompt Sampul"):
        if not api_key:
            st.error("API Key Gemini belum diisi di sidebar!")
        else:
            with st.spinner("Merancang konsep visual sampul..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt_cover = f"""
                    Bertindaklah sebagai Creative Education Graphic Designer & Art Director.
                    Buatlah instruksi/prompt desain visual sampul A4 untuk dokumen berikut:
                    - Judul Utama: {judul_sampul}
                    - Mata Pelajaran: {mata_pelajaran}
                    - Sekolah: {nama_sekolah}
                    - Penyusun: {nama_guru}
                    - Target Siswa: SLB ({jenis_kekhususan})
                    
                    Berikan detail:
                    1. Tata Letak (Visual Hierarchy)
                    2. Palet Warna Harmonis yang cocok untuk {mata_pelajaran}
                    3. Gaya Ilustrasi (Flat Design / Modern Vector)
                    4. Prompt Text dalam Bahasa Inggris untuk generator gambar (Midjourney/DALL-E/Canva) agar menghasilkan latar belakang sampul A4 portrait yang bersih dan edukatif.
                    """
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_cover,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghubungi server AI: {e}")
