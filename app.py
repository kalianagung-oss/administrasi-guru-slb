import streamlit as st
import requests
import json

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Asisten Administrasi Guru SLB",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# STYLING CSS KUSTOM (TAMPILAN MENARIK & MODERN)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Styling Header & Banner Utama */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white !important;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .main-header p {
        color: #E0E7FF !important;
        font-size: 1.05rem;
        margin: 0;
    }
    
    /* Styling Card/Box Form Input */
    .stCard {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Custom Styling Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Tombol Utama */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=unsafe_allow_html)

# -----------------------------------------------------------------------------
# PENGATURAN API KEY GEMINI (Mendukung Input Manual & Secrets)
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ Pengaturan Aplikasi")

secrets_key = st.secrets.get("GEMINI_API_KEY", "")

if secrets_key:
    api_key = secrets_key
    st.sidebar.success("✅ API Key Terhubung Otomatis!")
else:
    api_key = st.sidebar.text_input("🔑 Masukkan Gemini API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Petunjuk Penggunaan")
st.sidebar.write("1. Isi **Identitas Guru & Sekolah** pada form utama.\n2. Pilih **Tab Dokumen** yang ingin dibuat.\n3. Masukkan materi/topik pembelajaran.\n4. Klik tombol **Hasilkan Dokumen**.")

# -----------------------------------------------------------------------------
# FUNGSI PEMANGGILAN REST API DENGAN FALLBACK MULTI-MODEL
# -----------------------------------------------------------------------------
def generate_ai_content(prompt_text, user_key):
    # Menguji kandidat model dan versi API secara berurutan
    attempts = [
        ("v1beta", "gemini-2.0-flash"),
        ("v1beta", "gemini-1.5-flash"),
        ("v1", "gemini-1.5-flash")
    ]
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    
    last_err = ""
    for api_ver, model_id in attempts:
        url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{model_id}:generateContent?key={user_key}"
        try:
            res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                last_err = res.json().get('error', {}).get('message', res.text)
        except Exception as e:
            last_err = str(e)
            continue
            
    raise Exception(f"Gagal memproses dokumen dari server AI. Detail: {last_err}")

# -----------------------------------------------------------------------------
# HEADER UTAMA APLIKASI
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎓 Asisten Administrasi Guru SLB</h1>
    <p>Aplikasi Pembuat Perangkat Ajar & Modul Kurikulum Merdeka Terintegrasi untuk Sekolah Luar Biasa</p>
</div>
""", unsafe_allow_html=unsafe_allow_html)

# -----------------------------------------------------------------------------
# FORM IDENTITAS (GLOBAL INPUT CARD)
# -----------------------------------------------------------------------------
with st.expander("📌 **Identitas Guru & Satuan Pendidikan** (Klik untuk membuka/menutup)", expanded=True):
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
            "Jenis Kekhususan / Hambatan",
            ["Hambatan Intelektual (Tunagrahita)", "Hambatan Pendengaran (Tunarungu)", 
             "Hambatan Penglihatan (Tunanetra)", "Hambatan Anggota Gerak (Tunadaksa)", 
             "Autis / Spektrum Autisme", "Ganda / Kombinasi"]
        )
        fase_kelas = st.selectbox("Fase / Kelas", ["Fase A (Kelas 1-2)", "Fase B (Kelas 3-4)", "Fase C (Kelas 5-6)", "Fase D (SMPLB)", "Fase E/F (SMALB)"])
        mata_pelajaran = st.text_input("Mata Pelajaran", "IPAS / IPA")

# -----------------------------------------------------------------------------
# MENU UTAMA TAB DOKUMEN
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Pemetaan CP, TP, ATP & Prota/Promes", 
    "📝 Modul Ajar / RPP Mendalam", 
    "🎨 Lembar Kerja Murid (LKM / LKPD)", 
    "🖼️ Generator Prompt Sampul A4"
])

# =============================================================================
# TAB 1: PEMETAAN CP, TP, ATP, PROTA, PROSEM & KKTP
# =============================================================================
with tab1:
    st.subheader("📋 Pemetaan Kurikulum & Program Tahunan/Semester")
    
    col_t1_left, col_t1_right = st.columns([1, 1])
    with col_t1_left:
        cp_text = st.text_area("Capaian Pembelajaran (CP) Resmi:", "Peserta didik dapat mengidentifikasi benda-benda di sekitar dan mengelompokkannya...", height=120)
    with col_t1_right:
        materi_list = st.text_area("Daftar Materi / Bab per Semester:", "Semester 1:\n- Mengenal Anggota Tubuh\n- Merawat Diri\n\nSemester 2:\n- Lingkungan Rumah", height=120)
    
    sub_option = st.radio("Pilih Dokumen yang Ingin Dihasilkan:", 
                          ["CP, TP & ATP", "Program Tahunan (Prota)", "Program Semester (Prosem)", "KKTP & Asesmen Sumatif"],
                          horizontal=True)

    if st.button("🚀 Hasilkan Pemetaan Kurikulum"):
        if not api_key:
            st.error("⚠️ API Key Gemini belum terpasang di sidebar atau Secrets!")
        else:
            with st.spinner("⏳ Sedang menyusun dokumen kurikulum..."):
                try:
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
                    
                    hasil = generate_ai_content(prompt_tab1, api_key)
                    st.success("✨ Dokumen Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"❌ {e}")

# =============================================================================
# TAB 2: MODUL AJAR / RPP MENDALAM
# =============================================================================
with tab2:
    st.subheader("📝 Rencana Pembelajaran Mendalam (RPP / Modul Ajar)")
    
    col_rpp1, col_rpp2 = st.columns(2)
    with col_rpp1:
        topik_rpp = st.text_input("Topik Pembelajaran:", "Mengenal Buah-Buahan Segar")
        tp_rpp = st.text_area("Tujuan Pembelajaran (TP):", "Peserta didik dapat menunjukkan 3 jenis buah segar melalui benda konkret/gambar.")
        alokasi_waktu = st.text_input("Alokasi Waktu:", "2 x 35 menit")
    with col_rpp2:
        model_pembelajaran = st.selectbox("Model Pembelajaran:", ["Direct Instruction", "Contextual Learning", "Problem Based Learning", "Discovery Learning", "Project Based Learning (PjBL)"])
        prinsip_pembelajaran = st.multiselect("Prinsip Pembelajaran:", ["Bermakna", "Menggembirakan", "Berkesadaran"], default=["Bermakna", "Menggembirakan"])

    if st.button("🚀 Hasilkan Modul Ajar / RPP"):
        if not api_key:
            st.error("⚠️ API Key Gemini belum terpasang!")
        else:
            with st.spinner("⏳ Merancang Modul Ajar Khusus SLB..."):
                try:
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
                    hasil = generate_ai_content(prompt_rpp, api_key)
                    st.success("✨ Modul Ajar Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"❌ {e}")

# =============================================================================
# TAB 3: LEMBAR KERJA MURID (LKM / LKPD) INTERAKTIF
# =============================================================================
with tab3:
    st.subheader("🎨 Lembar Kerja Murid (LKM) / LKPD Interaktif A4")
    
    col_lkm1, col_lkm2 = st.columns(2)
    with col_lkm1:
        materi_lkm = st.text_input("Materi / Topik LKM:", "Mewarnai dan Menghitung Buah")
    with col_lkm2:
        tp_lkm = st.text_input("Tujuan Pembelajaran LKM:", "Murid dapat menghitung jumlah buah 1-5 dan mewarnainya.")
    
    if st.button("🚀 Hasilkan LKPD Interaktif"):
        if not api_key:
            st.error("⚠️ API Key Gemini belum terpasang!")
        else:
            with st.spinner("⏳ Menyusun Lembar Kerja Murid..."):
                try:
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
                    hasil = generate_ai_content(prompt_lkm, api_key)
                    st.success("✨ LKPD Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"❌ {e}")

# =============================================================================
# TAB 4: GENERATOR PROMPT SAMPUL/COVER
# =============================================================================
with tab4:
    st.subheader("🖼️ Generator Prompt Sampul Dokumen A4")
    
    judul_sampul = st.text_input("Judul Dokumen Sampul:", "MODUL AJAR IPAS FASE A - KELAS 3 SLB")
    
    if st.button("🚀 Buatkan Prompt Sampul"):
        if not api_key:
            st.error("⚠️ API Key Gemini belum terpasang!")
        else:
            with st.spinner("⏳ Merancang konsep visual sampul..."):
                try:
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
                    hasil = generate_ai_content(prompt_cover, api_key)
                    st.success("✨ Prompt Sampul Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"❌ {e}")
