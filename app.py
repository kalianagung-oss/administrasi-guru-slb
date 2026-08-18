import io
import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
from google import genai
import streamlit as st

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="SLB-AdminFlow AI",
    layout="wide",
    page_icon="🏫",
)

st.title("🏫 SLB-AdminFlow (AI Powered)")
st.caption("Platform Generator Administrasi Pembelajaran Inklusif Terintegrasi AI")

# --- SIDEBAR: PENGATURAN API KEY & KOP SURAT ---
st.sidebar.header("🔑 Integrasi AI (Gratis)")
gemini_api_key = st.sidebar.text_input(
    "Masukkan Gemini API Key",
    type="password",
    help="Tempelkan kode API Key (AQ...) dari Google AI Studio",
)

st.sidebar.header("⚙️ Pengaturan Profil & Logo")
uploaded_logo = st.sidebar.file_uploader(
    "Upload Logo Sekolah (PNG/JPG)", type=["png", "jpg", "jpeg"]
)
nama_dinas = st.sidebar.text_input(
    "Nama Dinas",
    "PEMERINTAH DAERAH DIY - DINAS PENDIDIKAN, PEMUDA, DAN OLAHRAGA",
)
nama_sekolah = st.sidebar.text_input("Nama Sekolah", "SLB NEGERI 1 KULON PROGO")
alamat_sekolah = st.sidebar.text_input(
    "Alamat Sekolah", "Jl. Srikandi, Pengasih, Kulon Progo, DIY"
)
nama_kepsek = st.sidebar.text_input("Nama Kepala Sekolah", "Dra. Hj. ...")
nip_kepsek = st.sidebar.text_input("NIP Kepala Sekolah", "19670101...")
nama_guru = st.sidebar.text_input("Nama Guru Pengampu", "Nama Guru, S.Pd.")
nip_guru = st.sidebar.text_input("NIP Guru Pengampu", "19900101...")
kota_tgl = st.sidebar.text_input(
    "Tempat & Tanggal Cetak", "Kulon Progo, 18 Agustus 2026"
)

# --- INISIALISASI SESSION STATE UNTUK FORM ---
if "form_data" not in st.session_state:
  st.session_state.form_data = {
      "elemen": "Menyimak",
      "ruang_lingkup": "Komunikasi Lisan & Instruksi Harian",
      "materi_pokok": "Mengenal Nama Benda di Kelas",
      "tp_text": (
          "Peserta didik mampu menunjukkan dan menyebutkan nama benda-benda"
          " yang ada di lingkungan kelas setelah mendengarkan instruksi lisan"
          " dari guru."
      ),
      "atp1": (
          "1. Murid dapat mengamati dan mengenali bentuk serta warna benda"
          " konkret yang ditunjukkan oleh guru di depan kelas."
      ),
      "atp2": (
          "2. Murid dapat menunjuk dengan tepat benda-benda kelas saat guru"
          " menyebutkan namanya."
      ),
      "atp3": (
          "3. Murid dapat menyebutkan kembali nama benda kelas sederhana yang"
          " ditunjuk."
      ),
      "kegiatan_konkret": (
          "• Bermain kartu gambar konkret (PECS) dan mencocokkan benda"
          " asli.\n• Permainan 'Tebak & Tunjuk Benda'."
      ),
      "bentuk_asesmen": (
          "• Unjuk Kerja (Observasi Langsung)\n• Lembar Ceklis Perilaku /"
          " Kinerja"
      ),
      "alokasi_waktu": "6 JP (2 x Pertemuan)",
  }

# --- FORM INPUT ADMINISTRASI ---
st.header("📝 Modul Input CP & AI Generator")

col1, col2, col3 = st.columns(3)
with col1:
  mata_pelajaran = st.selectbox(
      "Mata Pelajaran",
      ["Bahasa Indonesia", "Matematika", "IPAS", "Seni Budaya"],
  )
with col2:
  fase_kelas = st.selectbox(
      "Fase / Kelas",
      ["Fase A / Kelas III", "Fase A / Kelas I", "Fase B / Kelas IV"],
  )
with col3:
  kekhususan = st.selectbox(
      "Kekhususan",
      [
          "Hambatan Intelektual",
          "Hambatan Pendengaran",
          "Hambatan Penglihatan",
          "Autisme",
      ],
  )

cp_input = st.text_area(
    "Tempel / Tulis Teks Capaian Pembelajaran (CP) di sini:",
    "Mengurutkan dan membandingkan banyak-sedikit dengan benda konkret sampai"
    " dengan 10 serta memahami besar-kecil suatu benda",
    height=100,
)

# --- TOMBOL AI GENERATE ---
if st.button("🤖 Analisis CP Menggunakan AI", type="secondary"):
  api_key_clean = gemini_api_key.strip()
  if not api_key_clean:
    st.error(
        "⚠️ Silakan masukkan API Key terlebih dahulu di panel sebelah kiri"
        " (Sidebar)!"
    )
  else:
    with st.spinner("AI sedang menganalisis CP dan merumuskan TP, ATP..."):
      try:
        client = genai.Client(api_key=api_key_clean)

        prompt = f"""
                Kamu adalah pakar kurikulum pembelajaran inklusif SLB di Indonesia.
                Tolong analisis Capaian Pembelajaran (CP) berikut untuk siswa SLB dengan Kekhususan: {kekhususan}, Fase/Kelas: {fase_kelas}, Mata Pelajaran: {mata_pelajaran}.

                Teks CP: "{cp_input}"

                Berikan respon HANYA dalam format teks terstruktur persis seperti pola di bawah ini (gunakan pemisah tanda titik dua ':'):

                ELEMEN: [Nama Elemen CP]
                RUANG LINGKUP: [Ruang Lingkup Materi]
                MATERI POKOK: [Materi Pokok]
                TP: [Tujuan Pembelajaran Adaptif yang terukur]
                ATP1: 1. Murid dapat [Tahap 1 pengenalan/konkret]
                ATP2: 2. Murid dapat [Tahap 2 pemahaman/koneksi]
                ATP3: 3. Murid dapat [Tahap 3 penerapan/respon]
                KEGIATAN: [List kegiatan konkret/sensorik adaptif SLB]
                ASESMEN: [Bentuk asesmen adaptif/observasi]
                ALOKASI: [Estimasi JP, misal: 6 JP (2 x Pertemuan)]
                """

        # Pemanggilan menggunakan model gemini-3.6-flash terbaru
        response = client.models.generate_content(
            model="gemini-3.6-flash", contents=prompt
        )

        res_text = response.text
        parsed = {}
        for line in res_text.split("\n"):
          if ":" in line:
            key, val = line.split(":", 1)
            parsed[key.strip()] = val.strip()

        # Update Session State
        if "ELEMEN" in parsed:
          st.session_state.form_data["elemen"] = parsed["ELEMEN"]
        if "RUANG LINGKUP" in parsed:
          st.session_state.form_data["ruang_lingkup"] = parsed["RUANG LINGKUP"]
        if "MATERI POKOK" in parsed:
          st.session_state.form_data["materi_pokok"] = parsed["MATERI POKOK"]
        if "TP" in parsed:
          st.session_state.form_data["tp_text"] = parsed["TP"]
        if "ATP1" in parsed:
          st.session_state.form_data["atp1"] = parsed["ATP1"]
        if "ATP2" in parsed:
          st.session_state.form_data["atp2"] = parsed["ATP2"]
        if "ATP3" in parsed:
          st.session_state.form_data["atp3"] = parsed["ATP3"]
        if "KEGIATAN" in parsed:
          st.session_state.form_data["kegiatan_konkret"] = parsed["KEGIATAN"]
        if "ASESMEN" in parsed:
          st.session_state.form_data["bentuk_asesmen"] = parsed["ASESMEN"]
        if "ALOKASI" in parsed:
          st.session_state.form_data["alokasi_waktu"] = parsed["ALOKASI"]

        st.success("✅ Analisis AI Berhasil! Hasil telah diisikan ke form.")
        st.rerun()
      except Exception as e:
        st.error(f"Pesan Detail Error dari AI: {e}")

st.markdown("---")
st.subheader("📋 Hasil Analisis CP → TP → ATP (Bisa Diedit Manual)")

elemen = st.text_input("Elemen CP", st.session_state.form_data["elemen"])
ruang_lingkup = st.text_input(
    "Ruang Lingkup Materi", st.session_state.form_data["ruang_lingkup"]
)
materi_pokok = st.text_input(
    "Materi Pokok", st.session_state.form_data["materi_pokok"]
)
tp_text = st.text_area(
    "Tujuan Pembelajaran (TP)", st.session_state.form_data["tp_text"]
)

st.write("**Alur Tujuan Pembelajaran (ATP):**")
atp1 = st.text_input("ATP Tahap 1", st.session_state.form_data["atp1"])
atp2 = st.text_input("ATP Tahap 2", st.session_state.form_data["atp2"])
atp3 = st.text_input("ATP Tahap 3", st.session_state.form_data["atp3"])

col_a, col_b, col_c = st.columns(3)
with col_a:
  kegiatan_konkret = st.text_area(
      "Kegiatan Konkret", st.session_state.form_data["kegiatan_konkret"]
  )
with col_b:
  bentuk_asesmen = st.text_area(
      "Bentuk Asesmen", st.session_state.form_data["bentuk_asesmen"]
  )
with col_c:
  alokasi_waktu = st.text_input(
      "Alokasi Waktu", st.session_state.form_data["alokasi_waktu"]
  )


# --- FUNGSIONALITAS GENERATE WORD ---
def generate_docx():
  doc = docx.Document()

  sec = doc.sections[0]
  sec.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
  sec.page_width = Inches(11.69)
  sec.page_height = Inches(8.27)
  sec.top_margin = Inches(0.5)
  sec.bottom_margin = Inches(0.5)
  sec.left_margin = Inches(0.6)
  sec.right_margin = Inches(0.6)

  def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

  def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [
        ('top', top),
        ('bottom', bottom),
        ('left', left),
        ('right', right),
    ]:
      node = OxmlElement(f'w:{m}')
      node.set(qn('w:w'), str(val))
      node.set(qn('w:type'), 'dxa')
      tcMar.append(node)
    tcPr.append(tcMar)

  # Kop Surat
  kop_tbl = doc.add_table(rows=1, cols=2)
  kop_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
  c_logo, c_info = kop_tbl.rows[0].cells
  c_logo.width = Inches(1.2)
  c_info.width = Inches(9.29)

  p_logo = c_logo.paragraphs[0]
  p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
  if uploaded_logo:
    p_logo.add_run().add_picture(uploaded_logo, width=Inches(0.9))
  else:
    p_logo.add_run("[ LOGO ]").font.size = Pt(8)

  p_info = c_info.paragraphs[0]
  p_info.add_run(f'{nama_dinas.upper()}\n').font.size = Pt(9)
  r_sch = p_info.add_run(f'{nama_sekolah.upper()}\n')
  r_sch.font.size = Pt(13)
  r_sch.font.bold = True
  p_info.add_run(f'Alamat: {alamat_sekolah}').font.size = Pt(8)

  p_hr = doc.add_paragraph()
  p_hr.paragraph_format.space_before = Pt(4)
  p_hr.paragraph_format.space_after = Pt(8)
  p_hr._element.get_or_add_pPr().append(
      parse_xml(
          f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12"'
          ' w:space="1" w:color="1B365D"/></w:pBdr>'
      )
  )

  # Judul Dokumen
  p_title = doc.add_paragraph()
  p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
  r_t = p_title.add_run("ANALISIS CP, TP, ATP, DAN RENCANA PEMBELAJARAN INKLUSIF")
  r_t.font.bold = True
  r_t.font.size = Pt(13)
  r_t.font.color.rgb = RGBColor(27, 54, 93)

  p_sub = doc.add_paragraph()
  p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p_sub.paragraph_format.space_after = Pt(10)
  p_sub.add_run(
      f"Mapel: {mata_pelajaran} | {fase_kelas} | Kekhususan: {kekhususan}"
  ).font.size = Pt(9)

  # Tabel 10 Kolom Berwarna
  headers = [
      "No",
      "Elemen",
      "Capaian Pembelajaran (CP)",
      "Ruang Lingkup Materi",
      "Materi Pokok",
      "Tujuan Pembelajaran (TP)",
      "Alur Tujuan Pembelajaran (ATP)",
      "Kegiatan Konkret",
      "Bentuk Asesmen",
      "Alokasi Waktu",
  ]
  col_widths = [0.4, 0.9, 1.4, 1.0, 0.9, 1.3, 1.6, 1.4, 0.9, 0.69]

  table = doc.add_table(rows=1, cols=10)
  table.alignment = WD_TABLE_ALIGNMENT.CENTER

  for idx, text in enumerate(headers):
    cell = table.rows[0].cells[idx]
    cell.width = Inches(col_widths[idx])
    set_cell_background(cell, "1B365D")
    set_cell_margins(cell)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(8)

  row_cells = table.add_row().cells
  atp_combined = f"{atp1}\n\n{atp2}\n\n{atp3}"
  data = [
      "1",
      elemen,
      cp_input,
      ruang_lingkup,
      materi_pokok,
      tp_text,
      atp_combined,
      kegiatan_konkret,
      bentuk_asesmen,
      alokasi_waktu,
  ]

  for idx, val in enumerate(data):
    row_cells[idx].width = Inches(col_widths[idx])
    set_cell_background(row_cells[idx], "FFFFFF")
    set_cell_margins(row_cells[idx])
    p = row_cells[idx].paragraphs[0]
    p.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER if idx in [0, 9] else WD_ALIGN_PARAGRAPH.LEFT
    )
    run = p.add_run(val)
    run.font.size = Pt(7.5)

  doc.add_paragraph().paragraph_format.space_before = Pt(12)

  # Tanda Tangan
  sig_tbl = doc.add_table(rows=1, cols=2)
  sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
  cL, cR = sig_tbl.rows[0].cells
  cL.width = Inches(5.2)
  cR.width = Inches(5.2)

  cL.paragraphs[0].add_run(
      f"Mengetahui,\nKepala {nama_sekolah}\n\n\n\n{nama_kepsek}\nNIP. {nip_kepsek}"
  ).font.size = Pt(8.5)
  cR.paragraphs[0].add_run(
      f"{kota_tgl}\nGuru Kelas /"
      f" Pengampu,\n\n\n\n{nama_guru}\nNIP. {nip_guru}"
  ).font.size = Pt(8.5)

  bio = io.BytesIO()
  doc.save(bio)
  return bio.getvalue()


# --- TOMBOL CETAK ---
st.markdown("---")
if st.button("🚀 Buat Dokumen Analisis CP-TP-ATP (.docx)", type="primary"):
  docx_bytes = generate_docx()
  st.download_button(
      label="📥 Download File Word (.docx)",
      data=docx_bytes,
      file_name="Analisis_CP_TP_ATP_SLB.docx",
      mime=(
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ),
  )
