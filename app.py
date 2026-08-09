import streamlit as st
import requests

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Asisten Administrasi Guru SLB",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .main-header h1 { color: white !important; font-size: 2rem; margin-bottom: 8px; }
    .main-header p { color: #E0E7FF !important; margin: 0; }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 20px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover { background-color: #1D4ED8; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PENGATURAN API KEY GEMINI
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ Pengaturan AI")
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

if api_key:
    st.sidebar.success("✅ API Key Terhubung!")
else:
    st.sidebar.warning("⚠️ Masukkan API Key di atas atau di Secrets.")

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi Administrasi Guru SLB - Kurikulum Merdeka")

# -----------------------------------------------------------------------------
# FUNGSI PEMANGGILAN REST API DENGAN PEMILIHAN MODEL DEDIKASI
# -----------------------------------------------------------------------------
def minta_bantuan_ai(prompt_text, key_val):
    # Mengutamakan model v1beta/gemini-2.5-flash dan gemini-2.0-flash
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key_val}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key_val}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key_val}"
    ]
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    headers = {"Content-Type": "application/json"}
    
    last_err = ""
    for url in endpoints:
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                last_err = res.json().get("error", {}).get("message", res.text)
        except Exception as e:
            last_err = str(e)
            continue
            
    raise Exception(f"Gagal dari Server AI: {last_err}")

# -----------------------------------------------------------------------------
# BANNER UTAMA
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎓 Asisten Administrasi Guru SLB</h1>
    <p>Generator Perangkat Ajar & Modul Kurikulum Merdeka Sekolah Luar Biasa</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FORM INPUT IDENTITAS
# -----------------------------------------------------------------------------
with st.expander("📌 **Identitas Guru & Satuan Pendidikan**", expanded=True):
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
        mata_pelajaran = st.text_input("Mata Pelajaran", "Matematika")

# -----------------------------------------------------------------------------
# MENU UTAMA TAB DOKUMEN
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Pemetaan CP, TP & ATP", 
    "📝 RPP / Modul Ajar SLB", 
    "🎨 Lembar Kerja Murid (LKPD)", 
    "🖼️ Prompt Sampul A4"
])

# TAB 1: PEMETAAN CP, TP, ATP
with tab1:
    st.subheader("📋 Pemetaan Capaian & Tujuan Pembelajaran")
    cp_input = st.text_area("Masukkan Capaian Pembelajaran (CP):", "Mengenal benda-benda bangun ruang dan mengelompokkannya sesuai dengan jenis dan sifatnya...", height=100)
    materi_input = st.text_area("Masukkan Materi / Bab:", "Bilangan dan Lambang Bilangan\nUkuran dan Perbandingan\nBentuk dan Pola Sederhana", height=100)
    
    if st.button("🚀 Buat Pemetaan CP, TP & ATP"):
        if not api_key:
            st.error("Masukkan API Key terlebih dahulu pada menu di sebelah kiri!")
        else:
            with st.spinner("Sedang memproses dokumen..."):
                try:
                    p = f"""
                    Bertindaklah sebagai Ahli Kurikulum Merdeka SLB.
                    Identitas: Guru {nama_guru}, Sekolah {nama_sekolah}, Kekhususan {jenis_kekhususan}, Fase {fase_kelas}, Mapel {mata_pelajaran}.
                    CP: {cp_input}
                    Materi: {materi_input}
                    
                    Tugas: Buatkan tabel pemetaan CP, Tujuan Pembelajaran (TP), dan Alur Tujuan Pembelajaran (ATP) yang sesuai dengan karakter anak berkebutuhan khusus. Sajikan rapi berformat Markdown.
                    """
                    hasil = minta_bantuan_ai(p, api_key)
                    st.success("✨ Dokumen Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"Terjadi Kesalahan: {e}")

# TAB 2: RPP / MODUL AJAR
with tab2:
    st.subheader("📝 Modul Ajar Pembelajaran Khusus")
    topik = st.text_input("Topik Pembelajaran:", "Mengenal Bangun Ruang Kubus dan Balok")
    tp = st.text_area("Tujuan Pembelajaran (TP):", "Siswa dapat menunjukkan benda berbentuk kubus dan balok di sekitar kelas.")
    
    if st.button("🚀 Buat Modul Ajar / RPP"):
        if not api_key:
            st.error("Masukkan API Key terlebih dahulu!")
        else:
            with st.spinner("Sedang merancang Modul Ajar..."):
                try:
                    p = f"""
                    Bertindaklah sebagai Guru SLB Profesional.
                    Buatkan RPP / Modul Ajar LENGKAP Kurikulum Merdeka untuk murid {jenis_kekhususan} ({fase_kelas}).
                    Mata Pelajaran: {mata_pelajaran}, Topik: {topik}, TP: {tp}.
                    Sertakan: Identitas, Langkah Pembelajaran (Pendahuluan, Inti Kontekstual, Penutup), dan Asesmen Sederhana. Format Markdown.
                    """
                    hasil = minta_bantuan_ai(p, api_key)
                    st.success("✨ Modul Ajar Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"Terjadi Kesalahan: {e}")

# TAB 3: LKPD INTERAKTIF
with tab3:
    st.subheader("🎨 Lembar Kerja Murid (LKPD)")
    materi_lkpd = st.text_input("Topik LKPD:", "Mewarnai & Mengelompokkan Bangun Ruang")
    
    if st.button("🚀 Buat LKPD Interaktif"):
        if not api_key:
            st.error("Masukkan API Key terlebih dahulu!")
        else:
            with st.spinner("Membuat LKPD..."):
                try:
                    p = f"""
                    Buatkan Lembar Kerja Murid (LKPD) sederhana siap cetak A4 untuk anak SLB ({jenis_kekhususan}).
                    Mata Pelajaran: {mata_pelajaran}, Topik: {materi_lkpd}.
                    Sertakan petunjuk visual, gambar deskriptif, dan instruksi sederhana.
                    """
                    hasil = minta_bantuan_ai(p, api_key)
                    st.success("✨ LKPD Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"Terjadi Kesalahan: {e}")

# TAB 4: PROMPT SAMPUL
with tab4:
    st.subheader("🖼️ Generator Prompt Sampul Dokumen")
    judul_cover = st.text_input("Judul Sampul:", "MODUL AJAR MATEMATIKA FASE A SLB")
    
    if st.button("🚀 Buat Prompt Sampul"):
        if not api_key:
            st.error("Masukkan API Key terlebih dahulu!")
        else:
            with st.spinner("Merancang Prompt Sampul..."):
                try:
                    p = f"""
                    Buatkan prompt Bahasa Inggris untuk image generator (Canva/Midjourney/DALL-E) untuk membuat cover modul ajar A4 dengan judul '{judul_cover}', mata pelajaran {mata_pelajaran}, gaya ilustrasi flat design edukatif ramah anak.
                    """
                    hasil = minta_bantuan_ai(p, api_key)
                    st.success("✨ Prompt Sampul Berhasil Dibuat!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"Terjadi Kesalahan: {e}")
