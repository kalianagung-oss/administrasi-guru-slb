import streamlit as st
from google import genai

# Konfigurasi Halaman & CSS
st.set_page_config(page_title="Asisten Administrasi Guru SLB", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;
    }
    .main-header h1 { color: white !important; font-size: 1.8rem; margin: 0; }
    .main-header p { color: #E0E7FF !important; margin: 0; }
</style>
""", unsafe_allow_html=True)

# Pengaturan API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")

st.sidebar.title("⚙️ Pengaturan")
if api_key:
    st.sidebar.success("✅ API Key Terhubung!")
else:
    api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 Asisten Administrasi Guru SLB</h1>
    <p>Generator Perangkat Ajar & Modul Kurikulum Merdeka</p>
</div>
""", unsafe_allow_html=True)

# Input Form
with st.expander("📌 Identitas Guru & Satuan Pendidikan", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_guru = st.text_input("Nama Guru", "Nama Guru, S.Pd.")
        nama_sekolah = st.text_input("Nama Sekolah", "SLB Negeri 1 Kulon Progo")
    with col2:
        nama_ks = st.text_input("Nama Kepala Sekolah", "Nama KS, M.Pd.")
        tahun_ajaran = st.text_input("Tahun Pelajaran", "2026/2027")
    with col3:
        jenis_kekhususan = st.selectbox("Jenis Kekhususan", ["Hambatan Intelektual (Tunagrahita)", "Hambatan Pendengaran (Tunarungu)", "Hambatan Penglihatan (Tunanetra)", "Autis / Spektrum Autisme"])
        fase_kelas = st.selectbox("Fase / Kelas", ["Fase A (Kelas 1-2)", "Fase B (Kelas 3-4)", "Fase C (Kelas 5-6)", "Fase D (SMPLB)"])
        mata_pelajaran = st.text_input("Mata Pelajaran", "IPAS")

cp_text = st.text_area("Capaian Pembelajaran (CP):", "Peserta didik dapat mengidentifikasi benda-benda di sekitar dan mengelompokkannya...")

if st.button("🚀 Hasilkan Perangkat Ajar"):
    if not api_key:
        st.error("⚠️ API Key Gemini belum terpasang!")
    else:
        with st.spinner("⏳ Sedang memproses dokumen dengan AI..."):
            try:
                # Menggunakan Client dari library google-genai
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Bertindaklah sebagai Konsultan Kurikulum Sekolah Luar Biasa (SLB).
                Identitas:
                - Guru: {nama_guru}
                - Sekolah: {nama_sekolah}
                - Hambatan/Kekhususan: {jenis_kekhususan}
                - Fase/Kelas: {fase_kelas}
                - Mapel: {mata_pelajaran}
                
                Capaian Pembelajaran: {cp_text}
                
                Tugas: Buatkan Modul Ajar Kurikulum Merdeka yang kontekstual, ramah anak berkebutuhan khusus, serta dilengkapi langkah pembelajaran dan asesmen secara lengkap berformat Markdown.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.success("✨ Dokumen Berhasil Dibuat!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {e}")
