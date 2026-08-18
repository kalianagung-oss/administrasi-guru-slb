import io
import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
import streamlit as st

# 1. Konfigurasi Halaman (HARUS DI BARIS PALING ATAS SETELAH IMPORT)
st.set_page_config(
    page_title="SLB-AdminFlow",
    layout="wide",  # Perbaikan: 'layout', bukan 'page_layout'
    page_icon="🏫",
)

st.title("🏫 SLB-AdminFlow")
st.caption(
    "Platform Generator Administrasi Pembelajaran Inklusif Terintegrasi"
)

# --- SIDEBAR: PENGATURAN PROFIL & KOP SURAT ---
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

# --- FORM INPUT ADMINISTRASI ---
st.header("📝 Analisis CP → TP → ATP")

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

elemen = st.text_input("Elemen CP", "Menyimak")
cp_text = st.text_area(
    "Capaian Pembelajaran (CP)",
    "Peserta didik mampu menyimak dan memahami instruksi lisan sederhana yang"
    " berkaitan dengan aktivitas sehari-hari di kelas dan lingkungan sekolah.",
)
ruang_lingkup = st.text_input(
    "Ruang Lingkup Materi", "Komunikasi Lisan & Instruksi Harian"
)
materi_pokok = st.text_input("Materi Pokok", "Mengenal Nama Benda di Kelas")
tp_text = st.text_area(
    "Tujuan Pembelajaran (TP)",
    "Peserta didik mampu menunjukkan dan menyebutkan nama benda-benda yang ada"
    " di lingkungan kelas setelah mendengarkan instruksi lisan dari guru.",
)

st.subheader("📌 Alur Tujuan Pembelajaran (ATP)")
atp1 = st.text_input(
    "ATP Tahap 1",
    "Murid dapat mengamati dan mengenali bentuk serta warna benda konkret yang"
    " ditunjukkan oleh guru di depan kelas.",
)
atp2 = st.text_input(
    "ATP Tahap 2",
    "Murid dapat menunjuk dengan tepat benda-benda kelas (meja, kursi, papan"
    " tulis, buku) saat guru menyebutkan namanya.",
)
atp3 = st.text_input(
    "ATP Tahap 3",
    "Murid dapat menyebutkan kembali nama benda kelas sederhana yang ditunjuk"
    " oleh guru atau teman.",
)

col_a, col_b, col_c = st.columns(3)
with col_a:
  kegiatan_konkret = st.text_area(
      "Kegiatan Konkret",
      "• Bermain kartu gambar konkret (PECS) dan mencocokkan benda asli.\n•"
      " Permainan 'Tebak & Tunjuk Benda'.",
  )
with col_b:
  bentuk_asesmen = st.text_area(
      "Bentuk Asesmen",
      "• Unjuk Kerja (Observasi Langsung)\n• Lembar Ceklis Perilaku / Kinerja",
  )
with col_c:
  alokasi_waktu = st.text_input("Alokasi Waktu", "6 JP (2 x Pertemuan)")


# --- FUNGSIONALITAS GENERATE WORD ---
def generate_docx():
  doc = docx.Document()

  # Set Halaman Landscape A4
  sec = doc.sections[0]
  sec.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
  sec.page_width = Inches(11.69)
  sec.page_height = Inches(8.27)
  sec.top_margin = Inches(0.5)
  sec.bottom_margin = Inches(0.5)
  sec.left_margin = Inches(0.6)
  sec.right_margin = Inches(0.6)

  # Helper Warna dan Margin Tabel
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

  # 1. KOP SURAT
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

  # 2. JUDUL DOKUMEN
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

  # 3. TABEL 10 KOLOM BERWARNA
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
  atp_combined = f"1. {atp1}\n\n2. {atp2}\n\n3. {atp3}"
  data = [
      "1",
      elemen,
      cp_text,
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

  # 4. BLOK TANDA TANGAN
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


# --- TOMBOL CETAK / DOWNLOAD ---
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
