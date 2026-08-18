import io
import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
from google import genai
import streamlit as st

# 1. Konfigurasi Utama & Tampilan Halaman
st.set_page_config(
    page_title="SLB-AdminFlow AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS untuk Mempercantik Tampilan UI/UX
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #ffffff;
        font-weight: 700;
        margin: 0;
        font-size: 28px;
    }
    .main-header p {
        color: #e0e6ed;
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 14px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .info-card {
        background-color: #f8fafc;
        border-left: 4px solid #2563eb;
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 16px;
    }
    </style>
""",
    unsafe_allow_style_scope=True,
)

# Header Banner Aplikasi
st.markdown(
    """
    <div class="main-header">
        <h1>🏫 SLB-AdminFlow AI</h1>
        <p>Platform Generator Administrasi Pembelajaran Inklusif Terintegrasi AI (CP, TP, ATP, Prota, Prosem & Modul Ajar)</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR: INTEGRASI & PENGATURAN DOKUMEN ---
with st.sidebar:
  st.header("🔑 1. Integrasi AI (Gratis)")
  gemini_api_key = st.text_input(
      "Masukkan Gemini API Key",
      type="password",
      help="Dapatkan kode gratis dari Google AI Studio",
  )

  st.divider()
  st.header("⚙️ 2. Profil Sekolah & Guru")
  uploaded_logo = st.file_uploader(
      "Upload Logo Sekolah (PNG/JPG)", type=["png", "jpg", "jpeg"]
  )
  nama_dinas = st.text_input(
      "Nama Dinas",
      "PEMERINTAH DAERAH DIY - DINAS PENDIDIKAN, PEMUDA, DAN OLAHRAGA",
  )
  nama_sekolah = st.text_input("Nama Sekolah", "SLB NEGERI 1 KULON PROGO")
  alamat_sekolah = st.text_input(
      "Alamat Sekolah", "Jl. Srikandi, Pengasih, Kulon Progo, DIY"
  )

  st.caption("Penandatangan Dokumen:")
  nama_kepsek = st.text_input("Nama Kepala Sekolah", "Dra. Hj. ...")
  nip_kepsek = st.text_input("NIP Kepala Sekolah", "19670101...")
  nama_guru = st.text_input("Nama Guru Pengampu", "Nama Guru, S.Pd.")
  nip_guru = st.text_input("NIP Guru Pengampu", "19900101...")
  kota_tgl = st.text_input(
      "Tempat & Tanggal Cetak", "Kulon Progo, 18 Agustus 2026"
  )

# --- INISIALISASI SESSION STATE ---
if "form_data" not in st.session_state:
  st.session_state.form_data = {
      "elemen": "Bilangan / Analisis Data",
      "ruang_lingkup": (
          "• Pengurutan & Perbandingan Benda\n• Konsep Banyak-Sedikit &"
          " Besar-Kecil"
      ),
      "materi_pokok": (
          "1. Membandingkan banyak-sedikit (1-10)\n2. Mengurutkan benda\n3."
          " Konsep ukuran besar-kecil"
      ),
      "tp_text": (
          "1. Peserta didik mampu membandingkan banyak-sedikit benda konkret"
          " sampai 10.\n2. Peserta didik mampu mengurutkan benda konkret"
          " berdasarkan jumlah.\n3. Peserta didik mampu membedakan ukuran"
          " besar dan kecil suatu benda."
      ),
      "atp1": (
          "1.1 Murid dapat mengamati dua kelompok benda konkret dan membedakan"
          " banyak/sedikit.\n1.2 Murid dapat menunjuk kelompok benda yang lebih"
          " banyak atau sedikit."
      ),
      "atp2": (
          "2.1 Murid dapat membilang benda konkret 1-10 secara berurutan.\n2.2"
          " Murid dapat menyusun benda konkret dari jumlah terkecil ke terbesar."
      ),
      "atp3": (
          "3.1 Murid dapat mengidentifikasi benda berukuran besar dan kecil di"
          " kelas.\n3.2 Murid dapat mengelompokkan benda berdasarkan ukuran."
      ),
      "kegiatan_konkret": (
          "• Eksplorasi benda konkret (balok, kartu PECS, kelereng).\n•"
          " Permainan 'Tebak Ukuran & Jumlah'.\n• Praktik mengelompokkan benda"
          " mandiri."
      ),
      "bentuk_asesmen": (
          "• Unjuk Kerja & Observasi Langsung\n• Lembar Ceklis Perilaku"
          " Pembelajaran\n• Tes Lisan Adaptif"
      ),
      "alokasi_waktu": "12 JP (4 x Pertemuan)",
      "prota_sem1": (
          "1. TP 1: Membandingkan banyak-sedikit benda konkret (1-10) [6 JP]\n2."
          " TP 2: Mengurutkan benda konkret berdasarkan jumlah [6 JP]"
      ),
      "prota_sem2": (
          "1. TP 3: Membedakan ukuran besar dan kecil suatu benda [6 JP]\n2."
          " Evaluasi & Asesmen Sumatif Akhir Tahun [6 JP]"
      ),
      "prosem_detail": (
          "Juli M3-M4: TP 1 (6 JP)\nAgustus M1-M2: TP 2 (6 JP)\nJanuari M2-M3:"
          " TP 3 (6 JP)\nMei M3: Asesmen Sumatif (6 JP)"
      ),
  }

# --- BARIS INPUT CAPAIAN PEMBELAJARAN (CP) & PENGATURAN ---
st.subheader("🎯 Langkah 1: Input Capaian Pembelajaran (CP)")

col_a, col_b, col_c = st.columns(3)
with col_a:
  mata_pelajaran = st.selectbox(
      "Mata Pelajaran",
      ["Matematika", "Bahasa Indonesia", "IPAS", "Seni Budaya"],
  )
with col_b:
  fase_kelas = st.selectbox(
      "Fase / Kelas",
      ["Fase A / Kelas I", "Fase A / Kelas III", "Fase B / Kelas IV"],
  )
with col_c:
  kekhususan = st.selectbox(
      "Kekhususan Siswa SLB",
      [
          "Hambatan Intelektual",
          "Hambatan Pendengaran",
          "Hambatan Penglihatan",
          "Autisme",
      ],
  )

cp_input = st.text_area(
    "Tempelkan Teks Capaian Pembelajaran (CP) dari Kurikulum Merdeka:",
    "Mengurutkan dan membandingkan banyak-sedikit dengan benda konkret sampai"
    " dengan 10 serta memahami besar-kecil suatu benda",
    height=100,
)

# Tombol AI Generate
if st.button("🤖 Generasi Otomatis (CP → TP → ATP → Prota → Prosem)", type="primary"):
  api_key_clean = gemini_api_key.strip()
  if not api_key_clean:
    st.error(
        "⚠️ Masukkan Gemini API Key terlebih dahulu pada menu di sebelah kiri"
        " (Sidebar)!"
    )
  else:
    with st.spinner(
        "AI sedang membedah CP dan merumuskan TP, ATP, Prota & Prosem..."
    ):
      try:
        client = genai.Client(api_key=api_key_clean)

        prompt = f"""
                Kamu adalah pakar kurikulum pembelajaran inklusif SLB di Indonesia.
                Tolong analisis Capaian Pembelajaran (CP) berikut secara mendalam untuk siswa SLB.
                Kekhususan: {kekhususan}, Fase/Kelas: {fase_kelas}, Mata Pelajaran: {mata_pelajaran}.

                Teks CP: "{cp_input}"

                Bedah seluruh poin kompetensi CP dan buatkan perencanaan terstruktur meliputi TP, ATP, Prota (Semester 1 & 2), dan Prosem.

                Berikan respon HANYA dalam format teks terstruktur persis seperti pola di bawah ini (gunakan pemisah tanda titik dua ':'):

                ELEMEN: [Nama Elemen CP]
                RUANG LINGKUP: [Rincian Ruang Lingkup Materi]
                MATERI POKOK: [Daftar Materi Pokok]
                TP: [Jabarkan Poin 1, 2, 3... Tujuan Pembelajaran Adaptif lengkap]
                ATP1: [ATP Tahap 1 Pengenalan/Konkret]
                ATP2: [ATP Tahap 2 Pemahaman/Koneksi]
                ATP3: [ATP Tahap 3 Penerapan/Respon Mandiri]
                KEGIATAN: [Kegiatan Konkret Adaptif SLB]
                ASESMEN: [Bentuk Asesmen Adaptif / Observasi]
                ALOKASI: [Total JP, misal: 24 JP]
                PROTA_SEM1: [Daftar TP & Alokasi JP untuk Semester 1]
                PROTA_SEM2: [Daftar TP & Alokasi JP untuk Semester 2]
                PROSEM: [Distribusi Mingguan per Bulan untuk Sem 1 & 2]
                """

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
        for key_map, state_key in [
            ("ELEMEN", "elemen"),
            ("RUANG LINGKUP", "ruang_lingkup"),
            ("MATERI POKOK", "materi_pokok"),
            ("TP", "tp_text"),
            ("ATP1", "atp1"),
            ("ATP2", "atp2"),
            ("ATP3", "atp3"),
            ("KEGIATAN", "kegiatan_konkret"),
            ("ASESMEN", "bentuk_asesmen"),
            ("ALOKASI", "alokasi_waktu"),
            ("PROTA_SEM1", "prota_sem1"),
            ("PROTA_SEM2", "prota_sem2"),
            ("PROSEM", "prosem_detail"),
        ]:
          if key_map in parsed:
            st.session_state.form_data[state_key] = parsed[key_map]

        st.success(
            "✅ Berhasil! Seluruh administrasi (CP-TP-ATP, Prota, dan Prosem)"
            " telah siap diolah pada tab di bawah."
        )
        st.rerun()
      except Exception as e:
        st.error(f"Pesan Error AI: {e}")

st.divider()

# --- TABEL DASHBOARD HASIL ADMINISTRASI ---
st.subheader("📋 Langkah 2: Review & Unduh Dokumen Administrasi")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Analisis CP-TP-ATP",
    "📅 2. Program Tahunan (Prota)",
    "🗓️ 3. Program Semester (Prosem)",
    "📝 4. Panduan Cetak Modul",
])

# --- TAB 1: ANALISIS CP-TP-ATP ---
with tab1:
  st.markdown(
      '<div class="info-card"><b>Hasil Analisis Pembedahan CP ke TP dan'
      ' ATP:</b> Anda dapat menyesuaikan kembali kalimat jika diperlukan sebelum'
      " mengunduh file Word (.docx).</div>",
      unsafe_allow_html=True,
  )

  elemen = st.text_input("Elemen CP", st.session_state.form_data["elemen"])
  col_1, col_2 = st.columns(2)
  with col_1:
    ruang_lingkup = st.text_area(
        "Ruang Lingkup Materi",
        st.session_state.form_data["ruang_lingkup"],
        height=100,
    )
  with col_2:
    materi_pokok = st.text_area(
        "Materi Pokok", st.session_state.form_data["materi_pokok"], height=100
    )

  tp_text = st.text_area(
      "Penjabaran Tujuan Pembelajaran (TP)",
      st.session_state.form_data["tp_text"],
      height=130,
  )

  st.write("**Alur Tujuan Pembelajaran (ATP) Berjenjang:**")
  col_atp1, col_atp2, col_atp3 = st.columns(3)
  with col_atp1:
    atp1 = st.text_area(
        "Tahap 1 (Konkret/Pengenalan)",
        st.session_state.form_data["atp1"],
        height=110,
    )
  with col_atp2:
    atp2 = st.text_area(
        "Tahap 2 (Pemahaman/Koneksi)",
        st.session_state.form_data["atp2"],
        height=110,
    )
  with col_atp3:
    atp3 = st.text_area(
        "Tahap 3 (Penerapan/Respon)",
        st.session_state.form_data["atp3"],
        height=110,
    )

  col_x, col_y, col_z = st.columns(3)
  with col_x:
    kegiatan_konkret = st.text_area(
        "Kegiatan Konkret Adaptif",
        st.session_state.form_data["kegiatan_konkret"],
        height=100,
    )
  with col_y:
    bentuk_asesmen = st.text_area(
        "Bentuk Asesmen Inklusif",
        st.session_state.form_data["bentuk_asesmen"],
        height=100,
    )
  with col_z:
    alokasi_waktu = st.text_input(
        "Alokasi Waktu Total", st.session_state.form_data["alokasi_waktu"]
    )

# --- TAB 2: PROGRAM TAHUNAN (PROTA) ---
with tab2:
  st.markdown(
      '<div class="info-card"><b>Program Tahunan (Prota):</b> Pemetaan alokasi'
      " waktu dan Tujuan Pembelajaran untuk Semester 1 dan Semester 2.</div>",
      unsafe_allow_html=True,
  )

  col_p1, col_p2 = st.columns(2)
  with col_p1:
    prota_sem1 = st.text_area(
        "Program Tahunan Semester 1 (TP & JP)",
        st.session_state.form_data["prota_sem1"],
        height=200,
    )
  with col_p2:
    prota_sem2 = st.text_area(
        "Program Tahunan Semester 2 (TP & JP)",
        st.session_state.form_data["prota_sem2"],
        height=200,
    )

# --- TAB 3: PROGRAM SEMESTER (PROSEM) ---
with tab3:
  st.markdown(
      '<div class="info-card"><b>Program Semester (Prosem):</b> Distribusi'
      " alokasi jam pelajaran ke dalam minggu efektif bulanan.</div>",
      unsafe_allow_html=True,
  )

  prosem_detail = st.text_area(
      "Distribusi Rincian Program Semester (Prosem)",
      st.session_state.form_data["prosem_detail"],
      height=220,
  )

# --- TAB 4: PANDUAN ---
with tab4:
  st.info(
      "💡 **Petunjuk Penggunaan:**\n1. Pastikan Anda telah menginputkan"
      " profil sekolah di Sidebar kiri.\n2. Klik tombol merah di bawah untuk"
      " mengunduh file Word (.docx) analisis CP-TP-ATP resmi.\n3. Dokumen Word"
      " sudah terformat rapi sesuai standar dinas dengan Kop Surat dan Tabel"
      " Berwarna."
  )


# --- FUNGSIONALITAS GENERATE WORD (DOCX) ---
def generate_docx():
  doc = docx.Document()

  # Set Margins & Page Layout (Landscape)
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
  r_t = p_title.add_run(
      "ANALISIS CP, TP, ATP, DAN PERENCANAAN PEMBELAJARAN INKLUSIF"
  )
  r_t.font.bold = True
  r_t.font.size = Pt(12)
  r_t.font.color.rgb = RGBColor(27, 54, 93)

  p_sub = doc.add_paragraph()
  p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p_sub.paragraph_format.space_after = Pt(10)
  p_sub.add_run(
      f"Mata Pelajaran: {mata_pelajaran} | {fase_kelas} | Kekhususan:"
      f" {kekhususan}"
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
  atp_combined = (
      f"Tahap 1:\n{atp1}\n\nTahap 2:\n{atp2}\n\nTahap 3:\n{atp3}"
  )
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

  # Bagian Lampiran Program Tahunan & Prosem Ringkas
  p_pro = doc.add_paragraph()
  p_pro.add_run("PROGRAM TAHUNAN & PROSEM (LAMPIRAN):\n").font.bold = True
  p_pro.add_run(
      f"• Semester 1:\n{prota_sem1}\n\n• Semester 2:\n{prota_sem2}\n\n• Rincian"
      f" Prosem:\n{prosem_detail}"
  ).font.size = Pt(8)

  doc.add_paragraph().paragraph_format.space_before = Pt(12)

  # Tanda Tangan Side-by-Side
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


# --- TOMBOL UTAMA CETAK DOKUMEN ---
st.markdown("---")
col_d1, col_d2 = st.columns([2, 1])
with col_d1:
  st.write("🚀 **Dokumen Siap Dicetak:**")
  st.caption(
      "Unduh dokumen administrasi utuh (termasuk Kop Sekolah, Tabel Berwarna,"
      " Analisis CP-TP-ATP, Prota, Prosem, dan Tanda Tangan) dalam format Word"
      " (.docx)."
  )
with col_d2:
  docx_bytes = generate_docx()
  st.download_button(
      label="📥 Download File Word (.docx)",
      data=docx_bytes,
      file_name="Administrasi_Pembelajaran_SLB_Lengkap.docx",
      mime=(
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ),
      type="primary",
  )
