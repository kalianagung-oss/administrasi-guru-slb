import hashlib
import io
import json
import sqlite3
import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
from google import genai
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN & DATABASE
# ==========================================
st.set_page_config(
    page_title="LANTIP AI | Lembar Administrasi Pembelajaran Inklusif",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_NAME = "slb_adminflow.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            full_name TEXT,
            api_key TEXT,
            nama_dinas TEXT,
            nama_sekolah TEXT,
            alamat_sekolah TEXT,
            nama_kepsek TEXT,
            nip_kepsek TEXT,
            nama_guru TEXT,
            nip_guru TEXT,
            kota_tgl TEXT
        )
    """)
  c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT,
            mapel TEXT,
            fase_kelas TEXT,
            kekhususan TEXT,
            cp_input TEXT,
            data_json TEXT,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    """)
  conn.commit()
  conn.close()


init_db()


def hash_password(password):
  return hashlib.sha256(str.encode(password)).hexdigest()


def get_user_profile(username):
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute("SELECT * FROM users WHERE username = ?", (username,))
  row = c.fetchone()
  conn.close()
  return row


def update_user_profile(username, profile_data):
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute(
      """
        UPDATE users SET 
            api_key=?, nama_dinas=?, nama_sekolah=?, alamat_sekolah=?, 
            nama_kepsek=?, nip_kepsek=?, nama_guru=?, nip_guru=?, kota_tgl=?
        WHERE username=?
    """,
      (
          profile_data["api_key"],
          profile_data["nama_dinas"],
          profile_data["nama_sekolah"],
          profile_data["alamat_sekolah"],
          profile_data["nama_kepsek"],
          profile_data["nip_kepsek"],
          profile_data["nama_guru"],
          profile_data["nip_guru"],
          profile_data["kota_tgl"],
          username,
      ),
  )
  conn.commit()
  conn.close()


def save_history(
    username, title, mapel, fase_kelas, kekhususan, cp_input, data_dict
):
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  data_json = json.dumps(data_dict)
  c.execute(
      """
        INSERT INTO history (username, title, mapel, fase_kelas, kekhususan, cp_input, data_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
      (
          username,
          title,
          mapel,
          fase_kelas,
          kekhususan,
          cp_input,
          data_json,
      ),
  )
  conn.commit()
  conn.close()


def get_user_history(username):
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute(
      """
        SELECT id, created_at, title, mapel, fase_kelas, kekhususan, cp_input, data_json 
        FROM history WHERE username = ? ORDER BY id DESC
    """,
      (username,),
  )
  rows = c.fetchall()
  conn.close()
  return rows


def delete_history_item(item_id):
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute("DELETE FROM history WHERE id = ?", (item_id,))
  conn.commit()
  conn.close()


# ==========================================
# 2. STYLING CUSTOM CSS
# ==========================================
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    }
    .main-header h1 { color: #ffffff; font-weight: 800; margin: 0; font-size: 26px; }
    .main-header p { color: #e0e6ed; margin-top: 6px; margin-bottom: 0; font-size: 13px; }
    .stButton>button { border-radius: 8px; font-weight: 600; }
    </style>
""",
    unsafe_allow_html=True,
)

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""

if "form_data" not in st.session_state:
  st.session_state.form_data = {
      "elemen": "Bilangan / Analisis Data",
      "ruang_lingkup": "Pengurutan & Perbandingan Benda",
      "materi_pokok": "Membandingkan banyak-sedikit (1-10)",
      "tp_text": (
          "Peserta didik mampu membandingkan banyak-sedikit benda konkret"
          " sampai 10."
      ),
      "atp_lengkap": (
          "1. Murid mengamati contoh benda konkret.\n2. Murid menunjuk kelompok"
          " benda.\n3. Murid mengenali jumlah benda.\n4. Murid membedakan"
          " kelompok sesuai arahan.\n5. Murid mempraktikkan perbandingan"
          " mandiri.\n6. Murid membiasakan konsep kuantitas sehari-hari."
      ),
      "kegiatan_konkret": "Eksplorasi balok, kartu PECS, kelereng.",
      "bentuk_asesmen": "Observasi unjuk kerja, ceklis kemandirian.",
      "alokasi_waktu": "12 JP",
      "prota_sem1": "1. TP 1: Perbandingan Benda [6 JP]",
      "prota_sem2": "2. TP 2: Pengurutan Bilangan [6 JP]",
      "prosem_detail": "Juli M3-M4: TP 1 (6 JP)",
      "dimensi_lulusan": "Kemandirian & Ketangguhan, Penalaran Kritis",
      "modul_ajar": "Modul Ajar Matematika Inklusif berbasis 8 Dimensi Lulusan.",
      "ppi_text": "Baseline kemampuan awal murid dan target jangka panjang.",
      "rubrik_text": "Ceklis observasi adaptif skala 1-3.",
  }


# ==========================================
# 3. HALAMAN LOGIN & REGISTER
# ==========================================
def login_page():
  st.markdown(
      """
        <div class="main-header">
            <h1>🏫 LANTIP AI</h1>
            <p><b>L</b>embar <b>A</b>dmi<b>N</b>is<b>T</b>ras<b>I</b> <b>P</b>embelajaran — Platform Administrasi Guru SLB & Sekolah Inklusif</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  col1, col2 = st.columns(2)
  with col1:
    st.subheader("🔑 Masuk ke Akun")
    l_user = st.text_input("Username", key="l_u")
    l_pass = st.text_input("Password", type="password", key="l_p")
    if st.button("🚀 Masuk", type="primary"):
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "SELECT * FROM users WHERE username = ? AND password = ?",
          (l_user.strip(), hash_password(l_pass)),
      )
      user = c.fetchone()
      conn.close()
      if user:
        st.session_state.logged_in = True
        st.session_state.username = l_user.strip()
        st.rerun()
      else:
        st.error("Username atau Password salah!")
  with col2:
    st.subheader("📝 Daftar Akun Baru")
    r_user = st.text_input("Pilih Username", key="r_u")
    r_name = st.text_input("Nama Lengkap & Gelar", key="r_n")
    r_pass = st.text_input("Password Baru", type="password", key="r_p")
    if st.button("✨ Daftar"):
      if not r_user or not r_pass:
        st.warning("Isi username dan password!")
      else:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
          c.execute(
              """
                        INSERT INTO users (username, password, full_name, api_key, nama_dinas, nama_sekolah, alamat_sekolah, nama_kepsek, nip_kepsek, nama_guru, nip_guru, kota_tgl)
                        VALUES (?, ?, ?, '', 'PEMERINTAH DAERAH DIY - DINAS PENDIDIKAN, PEMUDA, DAN OLAHRAGA', 'SLB NEGERI 1 KULON PROGO', 'Tanjung I, Gotakan, Panjatan, Kulon Progo, D.I. Yogyakarta', 'Titin Nurhayati, S.Psi., M.Pd.', '19780603 200501 2 016', ?, '19920219 202321 1 012', 'Kulon Progo, 18 Agustus 2026')
                    """,
              (r_user.strip(), hash_password(r_pass), r_name.strip()),
          )
          conn.commit()
          st.success("Berhasil daftar! Silakan login di sebelah kiri.")
        except sqlite3.IntegrityError:
          st.error("Username sudah terdaftar!")
        finally:
          conn.close()


# ==========================================
# 4. DASHBOARD UTAMA DENGAN MENU BAR
# ==========================================
def main_dashboard():
  user_row = get_user_profile(st.session_state.username)

  with st.sidebar:
    st.title("🏫 LANTIP AI")
    st.write(f"Halo, **{user_row[2] or st.session_state.username}**")
    st.divider()

    menu = st.radio(
        "Pilih Menu Administrasi:",
        [
            "⚡ Workspace Generator AI",
            "📊 Analisis CP, TP & ATP",
            "📅 Program Tahunan (Prota)",
            "🗓️ Program Semester (Prosem)",
            "📝 Modul Ajar (RPP)",
            "🩺 PPI & Asesmen",
            "📥 Unduh Dokumen Lengkap",
            "📁 Riwayat Pekerjaan",
        ],
    )

    st.divider()
    st.subheader("⚙️ Profil & Sekolah")
    api_key_db = st.text_input(
        "Gemini API Key", value=user_row[3] or "", type="password"
    )
    nama_sekolah_db = st.text_input("Nama Sekolah", value=user_row[5] or "")
    nama_kepsek_db = st.text_input("Kepala Sekolah", value=user_row[7] or "")
    nip_kepsek_db = st.text_input("NIP Kepsek", value=user_row[8] or "")
    nama_guru_db = st.text_input("Nama Guru", value=user_row[9] or "")
    nip_guru_db = st.text_input("NIP Guru", value=user_row[10] or "")
    kota_tgl_db = st.text_input("Tempat & Tgl", value=user_row[11] or "")

    if st.button("💾 Simpan Profil"):
      p_data = {
          "api_key": api_key_db.strip(),
          "nama_dinas": user_row[4] or "",
          "nama_sekolah": nama_sekolah_db.strip(),
          "alamat_sekolah": user_row[6] or "",
          "nama_kepsek": nama_kepsek_db.strip(),
          "nip_kepsek": nip_kepsek_db.strip(),
          "nama_guru": nama_guru_db.strip(),
          "nip_guru": nip_guru_db.strip(),
          "kota_tgl": kota_tgl_db.strip(),
      }
      update_user_profile(st.session_state.username, p_data)
      st.success("Profil tersimpan!")
      st.rerun()

    if st.button("🚪 Keluar (Logout)"):
      st.session_state.logged_in = False
      st.rerun()

  if menu == "⚡ Workspace Generator AI":
    st.markdown(
        """
            <div class="main-header">
                <h1>⚡ Workspace Generator AI - LANTIP AI</h1>
                <p>Masukkan Capaian Pembelajaran (CP) untuk menghasilkan perangkat pembelajaran rinci standar SLB N 1 Kulon Progo.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
      mata_pelajaran = st.selectbox(
          "Mata Pelajaran",
          ["Matematika", "Bahasa Indonesia", "IPAS", "Bina Diri", "Seni Budaya"],
      )
    with col_b:
      fase_kelas = st.selectbox(
          "Fase / Kelas",
          ["Fase A / Kelas I", "Fase A / Kelas II", "Fase B / Kelas IV"],
      )
    with col_c:
      kekhususan = st.selectbox(
          "Kekhususan Siswa",
          [
              "Hambatan Intelektual",
              "Hambatan Pendengaran",
              "Hambatan Penglihatan",
              "Autisme",
          ],
      )

    cp_input = st.text_area(
        "Tempelkan Teks Capaian Pembelajaran (CP):",
        "Mengurutkan dan membandingkan banyak-sedikit dengan benda konkret"
        " sampai dengan 10 serta memahami besar-kecil suatu benda",
        height=100,
    )

    if st.button(
        "🤖 Generasi Otomatis Perangkat Rinci", type="primary", use_container_width=True
    ):
      if not api_key_db.strip():
        st.error("⚠️ Masukkan Gemini API Key pada sidebar terlebih dahulu!")
      else:
        with st.spinner(
            "LANTIP AI sedang menyusun analisis rinci setara dokumen resmi..."
        ):
          try:
            client = genai.Client(api_key=api_key_db.strip())
            prompt = f"""
                        Kamu adalah pakar kurikulum SLB. Analisis CP berikut untuk {mata_pelajaran}, {fase_kelas}, kekhususan {kekhususan}.
                        Teks CP: "{cp_input}"
                        Berikan format terstruktur persis dengan pemisah titik dua (':'):
                        ELEMEN: [Nama Elemen]
                        RUANG LINGKUP: [Ruang Lingkup Materi]
                        MATERI POKOK: [Materi Pokok]
                        TP: [Tujuan Pembelajaran rinci]
                        ATP_LENGKAP: [6 Langkah ATP berurutan: 1. Murid mengamati... 2. Murid menunjuk... 3. Murid mengenali... 4. Murid membedakan... 5. Murid mempraktikkan... 6. Murid membiasakan...]
                        KEGIATAN: [Kegiatan Konkret Adaptif]
                        ASESMEN: [Bentuk Asesmen]
                        ALOKASI: [Alokasi Waktu, misal 12 JP]
                        PROTA_SEM1: [Prota Sem 1]
                        PROTA_SEM2: [Prota Sem 2]
                        PROSEM: [Distribusi Prosem]
                        DIMENSI_LULUSAN: [8 Dimensi Profil Lulusan]
                        MODUL_AJAR: [Rancangan Modul Ajar Rinci]
                        PPI_TEXT: [Dokumen PPI Baseline & Target]
                        RUBRIK_TEXT: [Rubrik Asesmen & Ceklis]
                        """
            # Menggunakan model gemini-3.6-flash yang aktif dan stabil
            response = client.models.generate_content(
                model="gemini-3.6-flash", contents=prompt
            )
            res_text = response.text
            parsed = {}
            for line in res_text.split("\n"):
              if ":" in line:
                k, v = line.split(":", 1)
                parsed[k.strip()] = v.strip()

            for km, sk in [
                ("ELEMEN", "elemen"),
                ("RUANG LINGKUP", "ruang_lingkup"),
                ("MATERI POKOK", "materi_pokok"),
                ("TP", "tp_text"),
                ("ATP_LENGKAP", "atp_lengkap"),
                ("KEGIATAN", "kegiatan_konkret"),
                ("ASESMEN", "bentuk_asesmen"),
                ("ALOKASI", "alokasi_waktu"),
                ("PROTA_SEM1", "prota_sem1"),
                ("PROTA_SEM2", "prota_sem2"),
                ("PROSEM", "prosem_detail"),
                ("DIMENSI_LULUSAN", "dimensi_lulusan"),
                ("MODUL_AJAR", "modul_ajar"),
                ("PPI_TEXT", "ppi_text"),
                ("RUBRIK_TEXT", "rubrik_text"),
            ]:
              if km in parsed and parsed[km]:
                st.session_state.form_data[sk] = parsed[km]

            save_history(
                st.session_state.username,
                f"Perangkat {mata_pelajaran} {fase_kelas}",
                mata_pelajaran,
                fase_kelas,
                kekhususan,
                cp_input,
                st.session_state.form_data,
            )
            st.success(
                "✅ Perangkat rinci berhasil di-generate! Silakan cek menu"
                " sidebar sebelah kiri untuk melihat/edit tiap bagian."
            )
          except Exception as e:
            st.error(f"Error: {e}")

  elif menu == "📊 Analisis CP, TP & ATP":
    st.header("📊 Analisis Capaian Pembelajaran, TP, & ATP Rinci")
    st.session_state.form_data["elemen"] = st.text_input(
        "Elemen", st.session_state.form_data["elemen"]
    )
    col1, col2 = st.columns(2)
    with col1:
      st.session_state.form_data["ruang_lingkup"] = st.text_area(
          "Ruang Lingkup Materi", st.session_state.form_data["ruang_lingkup"]
      )
    with col2:
      st.session_state.form_data["materi_pokok"] = st.text_area(
          "Materi Pokok", st.session_state.form_data["materi_pokok"]
      )

    st.session_state.form_data["tp_text"] = st.text_area(
        "Tujuan Pembelajaran (TP)", st.session_state.form_data["tp_text"]
    )
    st.session_state.form_data["atp_lengkap"] = st.text_area(
        "ATP Lengkap (6 Langkah Sistematis)",
        st.session_state.form_data["atp_lengkap"],
        height=150,
    )

    c3, c4, c5 = st.columns(3)
    with c3:
      st.session_state.form_data["kegiatan_konkret"] = st.text_area(
          "Kegiatan Konkret", st.session_state.form_data["kegiatan_konkret"]
      )
    with c4:
      st.session_state.form_data["bentuk_asesmen"] = st.text_area(
          "Bentuk Asesmen", st.session_state.form_data["bentuk_asesmen"]
      )
    with c5:
      st.session_state.form_data["alokasi_waktu"] = st.text_input(
          "Alokasi Waktu", st.session_state.form_data["alokasi_waktu"]
      )

  elif menu == "📅 Program Tahunan (Prota)":
    st.header("📅 Program Tahunan (Prota)")
    c1, c2 = st.columns(2)
    with c1:
      st.session_state.form_data["prota_sem1"] = st.text_area(
          "Alokasi & TP Semester 1",
          st.session_state.form_data["prota_sem1"],
          height=200,
      )
    with c2:
      st.session_state.form_data["prota_sem2"] = st.text_area(
          "Alokasi & TP Semester 2",
          st.session_state.form_data["prota_sem2"],
          height=200,
      )

  elif menu == "🗓️ Program Semester (Prosem)":
    st.header("🗓️ Program Semester (Prosem)")
    st.session_state.form_data["prosem_detail"] = st.text_area(
        "Distribusi Jam Pelajaran Mingguan / Bulanan",
        st.session_state.form_data["prosem_detail"],
        height=250,
    )

  elif menu == "📝 Modul Ajar (RPP)":
    st.header("📝 Modul Ajar / RPP Adaptif")
    st.session_state.form_data["dimensi_lulusan"] = st.text_area(
        "Target 8 Dimensi Profil Lulusan",
        st.session_state.form_data["dimensi_lulusan"],
    )
    st.session_state.form_data["modul_ajar"] = st.text_area(
        "Rancangan Langkah Pembelajaran & Media Konkret",
        st.session_state.form_data["modul_ajar"],
        height=250,
    )

  elif menu == "🩺 PPI & Asesmen":
    st.header("🩺 Program Pembelajaran Individual & Rubrik Asesmen")
    c1, c2 = st.columns(2)
    with c1:
      st.session_state.form_data["ppi_text"] = st.text_area(
          "Dokumen PPI (Baseline & Target)",
          st.session_state.form_data["ppi_text"],
          height=250,
      )
    with c2:
      st.session_state.form_data["rubrik_text"] = st.text_area(
          "Rubrik Asesmen & Ceklis Observasi",
          st.session_state.form_data["rubrik_text"],
          height=250,
      )

  elif menu == "📥 Unduh Dokumen Lengkap":
    st.header("📥 Unduh Perangkat Administrasi Word (.docx)")

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
        tcMar = OxmlElement("w:tcMar")
        for m, val in [
            ("top", top),
            ("bottom", bottom),
            ("left", left),
            ("right", right),
        ]:
          node = OxmlElement(f"w:{m}")
          node.set(qn("w:w"), str(val))
          node.set(qn("w:type"), "dxa")
          tcMar.append(node)
        tcPr.append(tcMar)

      # Kop Surat
      kop_tbl = doc.add_table(rows=1, cols=2)
      kop_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
      c_logo, c_info = kop_tbl.rows[0].cells
      c_logo.width = Inches(1.2)
      c_info.width = Inches(9.29)
      c_logo.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
      c_logo.paragraphs[0].add_run("[ LOGO ]").font.size = Pt(8)

      p_info = c_info.paragraphs[0]
      p_info.add_run(
          "PEMERINTAH DAERAH DIY - DINAS PENDIDIKAN, PEMUDA, DAN OLAHRAGA\n"
      ).font.size = Pt(9)
      r_sch = p_info.add_run(f"{nama_sekolah_db.upper()}\n")
      r_sch.font.size = Pt(13)
      r_sch.font.bold = True
      p_info.add_run(
          "Alamat: Tanjung I, Gotakan, Panjatan, Kulon Progo, D.I. Yogyakarta"
      ).font.size = Pt(8)

      p_hr = doc.add_paragraph()
      p_hr.paragraph_format.space_before = Pt(4)
      p_hr.paragraph_format.space_after = Pt(8)
      p_hr._element.get_or_add_pPr().append(
          parse_xml(
              f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12"'
              ' w:space="1" w:color="1B365D"/></w:pBdr>'
          )
      )

      p_title = doc.add_paragraph()
      p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
      r_t = p_title.add_run(
          "ANALISIS CP, TP, ATP RINCI & PERANGKAT PEMBELAJARAN INKLUSIF"
      )
      r_t.font.bold = True
      r_t.font.size = Pt(12)
      r_t.font.color.rgb = RGBColor(27, 54, 93)

      headers = [
          "No",
          "Elemen",
          "Ruang Lingkup",
          "Materi Pokok",
          "Tujuan Pembelajaran (TP)",
          "ATP Lengkap (6 Langkah)",
          "Kegiatan Konkret",
          "Asesmen",
          "JP",
      ]
      col_widths = [0.4, 1.1, 1.2, 1.1, 1.4, 2.2, 1.3, 1.0, 0.6]

      table = doc.add_table(rows=1, cols=9)
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
      data_row = [
          "1",
          st.session_state.form_data["elemen"],
          st.session_state.form_data["ruang_lingkup"],
          st.session_state.form_data["materi_pokok"],
          st.session_state.form_data["tp_text"],
          st.session_state.form_data["atp_lengkap"],
          st.session_state.form_data["kegiatan_konkret"],
          st.session_state.form_data["bentuk_asesmen"],
          st.session_state.form_data["alokasi_waktu"],
      ]

      for idx, val in enumerate(data_row):
        row_cells[idx].width = Inches(col_widths[idx])
        set_cell_background(row_cells[idx], "FFFFFF")
        set_cell_margins(row_cells[idx])
        p = row_cells[idx].paragraphs[0]
        p.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
            if idx in [0, 8]
            else WD_ALIGN_PARAGRAPH.LEFT
        )
        run = p.add_run(val)
        run.font.size = Pt(7.5)

      doc.add_paragraph().paragraph_format.space_before = Pt(12)

      p_pro = doc.add_paragraph()
      r_lamp = p_pro.add_run(
          "LAMPIRAN PROTA, PROSEM, MODUL AJAR, PPI & RUBRIK ASESMEN:\n"
      )
      r_lamp.font.bold = True
      r_lamp.font.size = Pt(9.5)
      r_lamp.font.color.rgb = RGBColor(27, 54, 93)

      lampiran_teks = (
          f"1. PROGRAM TAHUNAN SEMESTER 1:\n{st.session_state.form_data['prota_sem1']}\n\n"
          f"2. PROGRAM TAHUNAN SEMESTER 2:\n{st.session_state.form_data['prota_sem2']}\n\n"
          f"3. DISTRIBUSI PROGRAM SEMESTER (PROSEM):\n{st.session_state.form_data['prosem_detail']}\n\n"
          f"4. TARGET 8 DIMENSI PROFIL LULUSAN:\n{st.session_state.form_data['dimensi_lulusan']}\n\n"
          f"5. MODUL AJAR ADAPTIF:\n{st.session_state.form_data['modul_ajar']}\n\n"
          f"6. PROGRAM PEMBELAJARAN INDIVIDUAL (PPI):\n{st.session_state.form_data['ppi_text']}\n\n"
          f"7. RUBRIK ASESMEN & CEKLIS OBSERVASI:\n{st.session_state.form_data['rubrik_text']}"
      )
      p_pro.add_run(lampiran_teks).font.size = Pt(8.5)

      doc.add_paragraph().paragraph_format.space_before = Pt(14)

      sig_tbl = doc.add_table(rows=1, cols=2)
      sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
      cL, cR = sig_tbl.rows[0].cells
      cL.width = Inches(5.2)
      cR.width = Inches(5.2)
      cL.paragraphs[0].add_run(
          f"Mengetahui,\nKepala {nama_sekolah_db}\n\n\n\n{nama_kepsek_db}\nNIP."
          f" {nip_kepsek_db}"
      ).font.size = Pt(8.5)
      cR.paragraphs[0].add_run(
          f"{kota_tgl_db}\nGuru Kelas /"
          f" Pengampu,\n\n\n\n{nama_guru_db}\nNIP. {nip_guru_db}"
      ).font.size = Pt(8.5)

      bio = io.BytesIO()
      doc.save(bio)
      return bio.getvalue()

    st.download_button(
        label="📥 Download File Word Perangkat Rinci (.docx)",
        data=generate_docx(),
        file_name="Perangkat_LANTIP_Rinci.docx",
        mime=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        type="primary",
    )

  elif menu == "📁 Riwayat Pekerjaan":
    st.header("📁 Riwayat Pekerjaan Saya")
    history_items = get_user_history(st.session_state.username)
    if not history_items:
      st.info("Belum ada riwayat tersimpan.")
    else:
      for item in history_items:
        item_id, created_at, title, mapel, fase, kekhususan, cp_in, json_data = (
            item
        )
        with st.expander(f"📌 [{created_at}] {title} ({kekhususan})"):
          st.write(f"**CP:** {cp_in}")
          if st.button("📥 Muat ke Workspace", key=f"load_{item_id}"):
            st.session_state.form_data = json.loads(json_data)
            st.success("Berhasil dimuat!")
            st.rerun()


if st.session_state.logged_in:
  main_dashboard()
else:
  login_page()
