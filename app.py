<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#0284C7">
    <title>SIKEMASKU - Terintegrasi SLBN 1 Kulon Progo</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brandPrimary: '#0284C7',
                        brandDark: '#0369A1',
                        brandAccent: '#38BDF8',
                    }
                }
            }
        }
    </script>
    
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

    <!-- Firebase SDK -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged, sendPasswordResetEmail } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
        import { getDatabase, ref, set, get, child } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";

        const firebaseConfig = {
            apiKey: "AIzaSyA6_tTvQiXfG1ocW03SS_ZjlWrEQXAaE98",
            authDomain: "sikemasku.firebaseapp.com",
            projectId: "sikemasku",
            databaseURL: "https://sikemasku-default-rtdb.asia-southeast1.firebasedatabase.app",
            storageBucket: "sikemasku.firebasestorage.app",
            messagingSenderId: "12680768946",
            appId: "1:12680768946:web:38fde0da590b12026648ab",
            measurementId: "G-NLS6FVD5YL"
        };

        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const db = getDatabase(app);

        window.fbAuth = auth;
        window.fbDb = db;
        window.fbRef = ref;
        window.fbSet = set;
        window.fbGet = get;
        window.fbChild = child;
        window.fbSignIn = signInWithEmailAndPassword;
        window.fbSignUp = createUserWithEmailAndPassword;
        window.fbSignOut = signOut;
        window.fbOnAuth = onAuthStateChanged;
        window.fbResetPass = sendPasswordResetEmail;
    </script>

    <style>
        * { -webkit-tap-highlight-color: transparent; }
        body { background-color: #f0f4f8; min-height: 100dvh; }
        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.2s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.99); } to { opacity: 1; transform: scale(1); } }
        button, input, select, textarea { min-height: 38px; }

        @media print {
            html, body {
                width: 100% !important;
                height: auto !important;
                background: #ffffff !important;
                color: #000000 !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            aside, header, nav, button, input, select, .no-print, #bannerSafeLocal, .card-identity-box, .month-picker-container, #toast, #hmTeacherDetailArea > div:not(.is-printing) { 
                display: none !important; 
            }

            .tab-content { display: none !important; }
            .tab-content.active { display: block !important; width: 100% !important; }

            .is-printing {
                display: block !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
                box-shadow: none !important;
            }

            table {
                width: 100% !important;
                min-width: 100% !important;
                table-layout: auto !important;
                font-size: 9px !important;
            }

            th, td {
                padding: 3px 2px !important;
                border: 1px solid #000000 !important;
            }

            .print-footer { page-break-inside: avoid !important; }
        }
    </style>
</head>
<body class="bg-slate-100 text-slate-800 font-sans">

    <!-- TAMPILAN HALAMAN DEPAN / LOGIN -->
    <div id="landingScreen" class="min-h-screen flex flex-col justify-between p-4 bg-gradient-to-br from-sky-900 via-sky-800 to-slate-900 text-white no-print">
        <div class="max-w-md mx-auto w-full my-auto py-6">
            <div class="text-center space-y-3 mb-6">
                <div class="w-20 h-20 bg-white/10 backdrop-blur-md rounded-3xl mx-auto flex items-center justify-center border border-white/20 shadow-2xl p-2 overflow-hidden" id="landingLogoBox">
                    <i class="fa-solid fa-graduation-cap text-sky-300 text-4xl"></i>
                </div>
                <div>
                    <h1 class="text-3xl font-black tracking-wider text-sky-300">SIKEMASKU</h1>
                    <p class="text-sky-100 text-xs font-bold uppercase tracking-wide mt-1">SISTEM KEHADIRAN MURID</p>
                    <p class="text-sky-200/90 text-sm font-bold uppercase tracking-wide mt-1" id="landingSchoolName">SLBN 1 KULON PROGO</p>
                </div>
            </div>

            <div class="bg-white/95 backdrop-blur-md rounded-3xl p-5 text-slate-800 shadow-2xl space-y-4 border border-white/40">
                <div class="flex border-b text-xs font-bold text-center">
                    <button id="tabBtnLogin" onclick="toggleAuthTab('login')" class="flex-1 py-2 border-b-2 border-sky-600 text-sky-700">Masuk Akun</button>
                    <button id="tabBtnRegister" onclick="toggleAuthTab('register')" class="flex-1 py-2 text-slate-400">Daftar Akun Baru</button>
                </div>

                <form id="formLogin" onsubmit="handleFirebaseLogin(event)" class="space-y-3">
                    <div>
                        <label class="block text-xs font-bold text-slate-600 mb-1">Email Pengguna</label>
                        <input type="email" id="loginEmail" placeholder="nama@sekolah.sch.id" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold" required>
                    </div>
                    <div>
                        <div class="flex justify-between items-center mb-1">
                            <label class="block text-xs font-bold text-slate-600">Password</label>
                            <button type="button" onclick="handleForgotPassword()" class="text-[11px] font-bold text-sky-700 hover:underline">Lupa Password?</button>
                        </div>
                        <input type="password" id="loginPass" placeholder="••••••••" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold" required>
                    </div>
                    <button type="submit" id="btnLoginSubmit" class="w-full py-2.5 bg-sky-700 hover:bg-sky-800 text-white font-bold text-xs rounded-xl shadow-md">
                        Masuk Akun <i class="fa-solid fa-right-to-bracket ml-1"></i>
                    </button>
                </form>

                <form id="formRegister" onsubmit="handleFirebaseRegister(event)" class="space-y-3 hidden">
                    <div>
                        <label class="block text-xs font-bold text-slate-600 mb-1">Peran / Hak Akses Pengguna</label>
                        <select id="regRole" class="w-full bg-amber-50 border border-amber-300 font-bold text-amber-900 rounded-xl px-3 py-2 text-xs">
                            <option value="GURU_KELAS">Guru Kelas / Wali Kelas</option>
                            <option value="GURU_MAPEL">Guru Mata Pelajaran / Keterampilan</option>
                            <option value="KEPALA_SEKOLAH">Kepala Sekolah (Super Admin)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-600 mb-1">Email Baru</label>
                        <input type="email" id="regEmail" placeholder="nama@sekolah.sch.id" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold" required>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-600 mb-1">Password Baru (min 6 karakter)</label>
                        <input type="password" id="regPass" placeholder="••••••••" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold" required>
                    </div>
                    <button type="submit" id="btnRegSubmit" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-md">
                        Daftar Akun Baru
                    </button>
                </form>

                <div class="pt-2 border-t text-center">
                    <button onclick="useOfflineMode()" class="text-xs font-bold text-slate-500 hover:text-sky-700 underline">
                        <i class="fa-solid fa-bolt text-amber-500 mr-1"></i> Mode Lokal Cepat (Tanpa Login)
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- TAMPILAN UTAMA APLIKASI -->
    <div id="mainAppContent" class="hidden min-h-screen flex flex-col md:flex-row">

        <!-- SIDEBAR NAV KIRI -->
        <aside id="sidebarNav" class="w-full md:w-64 bg-sky-900 text-white flex-shrink-0 md:min-h-screen border-r border-sky-800 flex flex-col justify-between shadow-xl no-print">
            <div>
                <div class="p-4 bg-sky-950 flex items-center justify-between border-b border-sky-800">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 rounded-xl bg-white p-1 flex items-center justify-center shrink-0 overflow-hidden" id="sidebarLogoBox">
                            <i class="fa-solid fa-graduation-cap text-sky-700 text-lg"></i>
                        </div>
                        <div class="overflow-hidden">
                            <h1 class="text-xs font-black text-sky-200 truncate" id="sidebarSchoolName">SLBN 1 Kulon Progo</h1>
                            <p class="text-[11px] text-sky-300 truncate font-semibold" id="sidebarClassName">[Role / Kelas]</p>
                        </div>
                    </div>
                </div>

                <nav class="p-3 space-y-1 text-xs font-bold" id="navContainer"></nav>
            </div>

            <div class="p-3 border-t border-sky-800 bg-sky-950/50 flex items-center justify-between text-xs">
                <span id="userEmailBadge" class="text-[10px] text-sky-300 truncate max-w-[130px]">Mode Lokal</span>
                <button onclick="handleFirebaseLogout()" title="Keluar / Logout" class="px-2.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold flex items-center space-x-1 transition">
                    <i class="fa-solid fa-power-off text-xs"></i>
                    <span>Keluar</span>
                </button>
            </div>
        </aside>

        <!-- KONTEN UTAMA KANAN -->
        <div class="flex-1 flex flex-col min-w-0 overflow-y-auto">

            <header class="bg-sky-800 text-white border-b border-sky-700 px-4 py-2.5 flex items-center justify-between sticky top-0 z-30 shadow-sm no-print">
                <div class="flex items-center space-x-2">
                    <button onclick="switchTab('daily')" title="Home / Presensi" class="p-2 bg-sky-700 hover:bg-sky-600 text-white rounded-xl text-xs font-bold flex items-center space-x-1.5 transition">
                        <i class="fa-solid fa-house text-sm"></i>
                        <span class="hidden sm:inline">Home</span>
                    </button>
                    <h2 class="text-xs sm:text-sm font-extrabold text-white ml-2" id="topPageTitle">Presensi Harian</h2>
                </div>
                <div class="text-[11px] font-bold text-sky-100 bg-sky-900/60 px-3 py-1 rounded-xl">
                    <i class="fa-regular fa-calendar mr-1"></i> <span id="topDateBadge">-</span>
                </div>
            </header>

            <main class="p-3 sm:p-5 max-w-5xl w-full mx-auto space-y-4">

                <!-- BANNER SISTEM -->
                <div id="bannerSafeLocal" class="bg-sky-600 text-white rounded-2xl p-3 sm:p-4 shadow-sm flex items-center justify-between no-print">
                    <div class="flex items-center space-x-3">
                        <div class="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center shrink-0">
                            <i class="fa-solid fa-network-wired text-lg"></i>
                        </div>
                        <div>
                            <h3 class="font-bold text-xs sm:text-sm" id="bannerTitle">SIKEMASKU - Sistem Terintegrasi Active</h3>
                            <p class="text-[10px] sm:text-xs text-sky-100" id="bannerDesc">Data otomatis tersinkron antara Guru Kelas, Guru Mapel, & Kepala Sekolah.</p>
                        </div>
                    </div>
                    <button onclick="forceReloadCloudData()" class="px-3 py-1.5 bg-white text-sky-800 rounded-xl text-xs font-bold shadow hover:bg-sky-50 shrink-0">
                        <i class="fa-solid fa-rotate mr-1"></i> Muat Data
                    </button>
                </div>

                <!-- KARTU IDENTITAS GURU / AKUN -->
                <div class="card-identity-box bg-white rounded-2xl p-4 shadow-sm border border-slate-200 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs no-print">
                    <div class="flex items-center space-x-3 border-b sm:border-b-0 sm:border-r border-slate-200 pb-3 sm:pb-0 pr-0 sm:pr-4">
                        <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center shrink-0 text-lg">
                            <i class="fa-solid fa-user-tie"></i>
                        </div>
                        <div>
                            <span class="text-[10px] font-bold text-slate-400 uppercase" id="cardRoleBadge">GURU / PENGAJAR</span>
                            <h4 class="font-bold text-slate-800 text-sm" id="cardTeacherName">[Nama Pengguna]</h4>
                        </div>
                    </div>
                    <div class="flex items-center justify-between sm:justify-end space-x-3 pl-0 sm:pl-4">
                        <div class="text-left sm:text-right">
                            <span class="text-[10px] font-bold text-slate-400 uppercase">KEPALA SEKOLAH</span>
                            <h4 class="font-bold text-slate-800 text-sm" id="cardHeadmasterName">[Nama Kepala Sekolah]</h4>
                        </div>
                    </div>
                </div>

                <!-- TAB SPECIAL KEPALA SEKOLAH -->
                <section id="tab-headmaster" class="tab-content space-y-4">
                    <div class="bg-gradient-to-br from-sky-900 to-slate-900 text-white rounded-2xl p-4 sm:p-5 shadow-lg space-y-4">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-sky-800 pb-3">
                            <div>
                                <h3 class="font-black text-base text-sky-300 flex items-center">
                                    <i class="fa-solid fa-chart-line mr-2"></i> DASHBOARD PEMANTAUAN KEPALA SEKOLAH
                                </h3>
                                <p class="text-xs text-sky-100 mt-0.5">Pemantauan real-time kehadiran seluruh kelas dan aktivitas pengisian presensi guru.</p>
                            </div>
                            <span class="px-3 py-1 bg-sky-800 text-sky-200 rounded-xl text-xs font-bold" id="hmTodayDate">-</span>
                        </div>

                        <!-- STATISTIK GABUNGAN SEKOLAH -->
                        <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 text-center">
                            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-3 border border-white/10">
                                <span class="text-[10px] font-bold text-sky-200 block uppercase">TOTAL MURID</span>
                                <span class="text-2xl font-black text-white" id="hmTotalStudents">0</span>
                            </div>
                            <div class="bg-indigo-500/20 backdrop-blur-md rounded-2xl p-3 border border-indigo-400/30">
                                <span class="text-[10px] font-bold text-indigo-300 block uppercase">TOTAL GURU</span>
                                <span class="text-2xl font-black text-indigo-300" id="hmTotalTeachers">0</span>
                            </div>
                            <div class="bg-emerald-500/20 backdrop-blur-md rounded-2xl p-3 border border-emerald-400/30">
                                <span class="text-[10px] font-bold text-emerald-300 block uppercase">HADIR HARI INI</span>
                                <span class="text-2xl font-black text-emerald-300" id="hmTotalHadir">0</span>
                            </div>
                            <div class="bg-amber-500/20 backdrop-blur-md rounded-2xl p-3 border border-amber-400/30">
                                <span class="text-[10px] font-bold text-amber-300 block uppercase">SAKIT / IZIN</span>
                                <span class="text-2xl font-black text-amber-300" id="hmTotalSakitIzin">0</span>
                            </div>
                            <div class="bg-rose-500/20 backdrop-blur-md rounded-2xl p-3 border border-rose-400/30 col-span-2 sm:col-span-1">
                                <span class="text-[10px] font-bold text-rose-300 block uppercase">ALFA</span>
                                <span class="text-2xl font-black text-rose-300" id="hmTotalAlfa">0</span>
                            </div>
                        </div>
                    </div>

                    <!-- FITUR UTAMA: PEMILIH GURU & INSPEKSI DATA MANDIRI -->
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-4">
                        <div class="border-b pb-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                            <div>
                                <h4 class="font-extrabold text-xs text-slate-800 uppercase tracking-wider flex items-center">
                                    <i class="fa-solid fa-user-check text-sky-700 mr-2 text-sm"></i> Inspeksi Data Rekap & Jurnal Per Guru
                                </h4>
                                <p class="text-[11px] text-slate-500">Pilih nama guru di bawah ini untuk melihat dan mencetak rekapitulasi atau jurnal perkembangannya secara terpisah.</p>
                            </div>
                            
                            <!-- DROPDOWN PEMILIH GURU -->
                            <div class="w-full sm:w-72">
                                <label class="block text-[10px] font-bold text-sky-900 uppercase mb-1">Pilih Guru / Kelas</label>
                                <select id="hmTeacherSelector" onchange="renderHeadmasterTeacherDetail()" class="w-full bg-sky-50 border border-sky-300 text-sky-900 font-extrabold rounded-xl px-3 py-2 text-xs focus:ring-2 focus:ring-sky-500">
                                    <option value="">-- Memuat Daftar Guru... --</option>
                                </select>
                            </div>
                        </div>

                        <!-- PANEL HASIL AUDIT GURU TERPILIH -->
                        <div id="hmTeacherDetailArea" class="hidden space-y-4">
                            
                            <!-- METADATA GURU DIBUKA -->
                            <div class="bg-slate-50 border border-slate-200 rounded-2xl p-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-xs">
                                <div>
                                    <span class="text-[10px] font-bold text-slate-400 uppercase">GURU / PENGAJAR AKTIF</span>
                                    <h5 class="font-extrabold text-slate-800 text-sm" id="hmInspectorTeacherName">-</h5>
                                    <p class="text-[11px] text-sky-700 font-bold" id="hmInspectorClassName">-</p>
                                </div>
                                <div class="flex items-center space-x-2 self-end sm:self-auto">
                                    <button onclick="printHeadmasterTeacherReport('monthly')" class="px-3 py-2 bg-sky-700 hover:bg-sky-800 text-white font-bold rounded-xl shadow flex items-center space-x-1 transition">
                                        <i class="fa-solid fa-print"></i><span>Cetak Presensi Saja</span>
                                    </button>
                                    <button onclick="printHeadmasterTeacherReport('sensory')" class="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-white font-bold rounded-xl shadow flex items-center space-x-1 transition">
                                        <i class="fa-solid fa-book-open"></i><span>Cetak Jurnal Saja</span>
                                    </button>
                                </div>
                            </div>

                            <!-- TERPISAH 1: BLOK TABEL REKAP PRESENSI -->
                            <div class="border rounded-2xl p-3 overflow-x-auto space-y-2 bg-white" id="hmMonthlyPrintBlock">
                                <h5 class="font-bold text-xs text-slate-700 flex items-center no-print">
                                    <i class="fa-solid fa-table-cells text-sky-600 mr-1.5"></i> Rekapitulasi Presensi Bulanan Guru Terpilih
                                </h5>
                                
                                <div id="hmPrintMonthlyArea">
                                    <div class="hidden print:block text-center border-b border-slate-400 pb-2 mb-3 space-y-1">
                                        <h1 class="font-black text-base uppercase tracking-wider text-slate-900" id="hmPrintMonthlyTitle">REKAPITULASI PRESENSI - [KELAS]</h1>
                                        <h2 class="font-extrabold text-sm uppercase text-slate-800" id="hmPrintMonthlySchool">SLBN 1 KULON PROGO</h2>
                                        <p class="text-xs text-slate-600 font-semibold">Periode Bulan: <span id="hmPrintMonthPeriod">-</span></p>
                                    </div>

                                    <div class="overflow-x-auto">
                                        <table class="w-full text-[11px] text-left border-collapse border border-slate-300">
                                            <thead class="bg-slate-100 font-bold text-slate-700"><tr id="hmDaysHeaderRow"></tr></thead>
                                            <tbody id="hmMonthlyTableBody" class="divide-y border-slate-200"></tbody>
                                        </table>
                                    </div>

                                    <div class="hidden print:grid grid-cols-2 gap-8 mt-6 text-xs font-bold text-center print-footer">
                                        <div>
                                            <p class="text-[10px] font-normal">Mengetahui,</p>
                                            <p>Kepala SLBN 1 Kulon Progo</p>
                                            <br><br><br>
                                            <p class="underline" id="hmPrintHMName"></p>
                                            <p class="text-[10px] font-normal" id="hmPrintHMNip"></p>
                                        </div>
                                        <div>
                                            <p class="text-[10px] font-normal" id="hmPrintTodayDate"></p>
                                            <p>Guru Kelas / Mapel</p>
                                            <br><br><br>
                                            <p class="underline" id="hmPrintTRName"></p>
                                            <p class="text-[10px] font-normal" id="hmPrintTRNip"></p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- TERPISAH 2: BLOK JURNAL PERKEMBANGAN -->
                            <div class="border rounded-2xl p-3 space-y-2 bg-white" id="hmSensoryPrintBlock">
                                <h5 class="font-bold text-xs text-slate-700 flex items-center no-print">
                                    <i class="fa-solid fa-book text-amber-600 mr-1.5"></i> Jurnal Perkembangan Siswa Dari Guru Terpilih
                                </h5>
                                
                                <div id="hmPrintSensoryArea">
                                    <div class="hidden print:block text-center border-b border-slate-400 pb-3 mb-6 space-y-1">
                                        <h1 class="font-black text-lg uppercase tracking-wider text-slate-900" id="hmPrintSensoryTitle">LAPORAN JURNAL PERKEMBANGAN SISWA</h1>
                                        <h2 class="font-extrabold text-sm uppercase text-slate-800" id="hmPrintSensorySchool">SLBN 1 KULON PROGO</h2>
                                        <p class="text-xs text-slate-600 font-semibold">Periode Bulan: <span id="hmPrintSensoryMonth">-</span></p>
                                    </div>

                                    <div id="hmSensoryNotesList" class="space-y-3"></div>

                                    <div class="hidden print:grid grid-cols-2 gap-8 mt-12 text-xs font-bold text-center print-footer">
                                        <div>
                                            <p class="text-[10px] font-normal">Mengetahui,</p>
                                            <p>Kepala SLBN 1 Kulon Progo</p>
                                            <br><br><br>
                                            <p class="underline" id="hmSensoryHMName"></p>
                                            <p class="text-[10px] font-normal" id="hmSensoryHMNip"></p>
                                        </div>
                                        <div>
                                            <p class="text-[10px] font-normal" id="hmSensoryTodayDate"></p>
                                            <p>Guru Kelas / Mapel</p>
                                            <br><br><br>
                                            <p class="underline" id="hmSensoryTRName"></p>
                                            <p class="text-[10px] font-normal" id="hmSensoryTRNip"></p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                        <div id="hmNoTeacherPlaceholder" class="text-center py-8 border border-dashed rounded-2xl text-xs text-slate-400">
                            Pilih salah satu nama guru pada dropdown di atas untuk membuka rekap presensi dan jurnal perkembangannya.
                        </div>
                    </div>

                    <!-- RINGKASAN STATUS PENGISIAN ALL GURU -->
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-3">
                        <h4 class="font-extrabold text-xs text-slate-800 uppercase tracking-wider flex items-center">
                            <i class="fa-solid fa-list-check text-sky-700 mr-2"></i> Status Pengisian Presensi Harian Seluruh Guru Hari Ini
                        </h4>
                        <div id="hmClassStatusContainer" class="space-y-2 text-xs"></div>
                    </div>
                </section>

                <!-- TAB 1: PRESENSI HARIAN -->
                <section id="tab-daily" class="tab-content active space-y-3">
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-3 sm:p-4 space-y-3">
                        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
                            <div class="flex-1">
                                <label class="block text-[11px] font-bold text-slate-500 mb-1">Pilih Tanggal Presensi</label>
                                <div class="flex items-center space-x-2">
                                    <input type="date" id="selectedDate" class="flex-1 bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-bold text-slate-800">
                                    <button onclick="changeDate(-1)" class="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-xl text-xs font-bold text-slate-600">&lt; Kemarin</button>
                                    <button onclick="setToday()" class="px-3 py-1.5 bg-sky-600 text-white rounded-xl text-xs font-bold shadow flex items-center space-x-1">
                                        <span>Hari Ini</span>
                                        <span id="btnTodayShortDate" class="text-[10px] opacity-80"></span>
                                    </button>
                                    <button onclick="changeDate(1)" class="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-xl text-xs font-bold text-slate-600">Besok &gt;</button>
                                </div>
                            </div>

                            <div class="w-full sm:w-56">
                                <label class="block text-[11px] font-bold text-amber-700 mb-1"><i class="fa-solid fa-filter mr-1"></i> Kelompok / Mapel</label>
                                <select id="dailyGroupFilter" onchange="renderDailyCards()" class="w-full bg-amber-50 border border-amber-300 text-amber-900 rounded-xl px-3 py-1.5 text-xs font-bold">
                                    <option value="ALL">-- Semua Siswa / Umum --</option>
                                </select>
                            </div>
                        </div>

                        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2 border-t pt-3">
                            <div class="flex items-center space-x-2">
                                <span class="text-xs font-bold text-slate-700" id="dailyDateTitle">-</span>
                                <span class="px-2 py-0.5 bg-sky-600 text-white text-[10px] font-extrabold rounded-full" id="dailyStudentCountCount">0 Murid</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <button onclick="markAllHadir()" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow flex items-center space-x-1">
                                    <i class="fa-solid fa-check-double text-xs"></i>
                                    <span>Tandai Semua Hadir</span>
                                </button>
                                <input type="text" id="searchStudentInput" oninput="renderDailyCards()" placeholder="Cari siswa..." class="bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-medium w-36 sm:w-48">
                            </div>
                        </div>
                    </div>

                    <div class="space-y-4" id="studentCardsContainer"></div>
                </section>

                <!-- TAB 2: REKAP BULANAN -->
                <section id="tab-monthly" class="tab-content space-y-3">
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-3 no-print">
                        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 month-picker-container">
                            <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3 flex-wrap">
                                <div>
                                    <label class="block text-[11px] font-bold text-slate-500 mb-1">Pilih Bulan & Tahun</label>
                                    <input type="month" id="selectedMonth" class="bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-bold text-slate-800">
                                </div>
                                <div>
                                    <label class="block text-[11px] font-bold text-amber-700 mb-1">Filter Kelompok / Mapel</label>
                                    <select id="monthlyGroupFilter" onchange="renderMonthlyTable()" class="bg-amber-50 border border-amber-300 text-amber-900 rounded-xl px-3 py-1.5 text-xs font-bold">
                                        <option value="ALL">-- Semua Siswa / Umum --</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-[11px] font-bold text-slate-500 mb-1">Tanggal Cetak Dokumen</label>
                                    <input type="date" id="printDateMonthlyInput" class="bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-bold text-slate-800">
                                </div>
                            </div>
                            <div class="flex items-center space-x-2 self-end sm:self-auto">
                                <button onclick="exportCSV()" class="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow flex items-center space-x-1">
                                    <i class="fa-solid fa-file-excel"></i><span>Ekspor CSV</span>
                                </button>
                                <button onclick="printMonthlyReport()" class="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-xl text-xs font-bold shadow flex items-center space-x-1">
                                    <i class="fa-solid fa-print"></i><span>Cetak / PDF</span>
                                </button>
                            </div>
                        </div>

                        <div class="grid grid-cols-4 gap-2 pt-2 text-center text-xs font-bold no-print">
                            <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-2.5">
                                <span class="text-emerald-700 text-[10px] block">HADIR (H)</span>
                                <span class="text-xl font-black text-emerald-800" id="statHadir">0</span>
                            </div>
                            <div class="bg-amber-50 border border-amber-200 rounded-xl p-2.5">
                                <span class="text-amber-700 text-[10px] block">SAKIT (S)</span>
                                <span class="text-xl font-black text-amber-800" id="statSakit">0</span>
                            </div>
                            <div class="bg-sky-50 border border-sky-200 rounded-xl p-2.5">
                                <span class="text-sky-700 text-[10px] block">IZIN (I)</span>
                                <span class="text-xl font-black text-sky-800" id="statIzin">0</span>
                            </div>
                            <div class="bg-rose-50 border border-rose-200 rounded-xl p-2.5">
                                <span class="text-rose-700 text-[10px] block">ALFA (A)</span>
                                <span class="text-xl font-black text-rose-800" id="statAlfa">0</span>
                            </div>
                        </div>
                    </div>

                    <!-- AREA TABEL CETAK REKAP BULANAN GURU -->
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 overflow-x-auto print-area">
                        <div class="hidden print:block text-center border-b border-slate-400 pb-2 mb-3 space-y-1">
                            <h1 class="font-black text-base uppercase tracking-wider text-slate-900" id="printMonthlyTitle">REKAPITULASI PRESENSI - [NAMA KELAS]</h1>
                            <h2 class="font-extrabold text-sm uppercase text-slate-800" id="printMonthlySchool">SLBN 1 KULON PROGO</h2>
                            <p class="text-xs text-slate-600 font-semibold">Periode Bulan: <span id="printMonthPeriod">-</span></p>
                        </div>

                        <table class="w-full text-[11px] text-left border-collapse border border-slate-300">
                            <thead class="bg-slate-100 font-bold text-slate-700"><tr id="daysHeaderRow"></tr></thead>
                            <tbody id="monthlyTableBody" class="divide-y border-slate-200"></tbody>
                        </table>

                        <div class="hidden print:grid grid-cols-2 gap-8 mt-6 text-xs font-bold text-center print-footer">
                            <div>
                                <p class="text-[10px] font-normal">Mengetahui,</p>
                                <p id="printMonthlyHeadmasterLabel">Kepala Sekolah</p>
                                <br><br><br>
                                <p class="underline" id="printHeadmasterName"></p>
                                <p class="text-[10px] font-normal" id="printHeadmasterNip"></p>
                            </div>
                            <div>
                                <p class="text-[10px] font-normal" id="printDateToday"></p>
                                <p id="printMonthlyTeacherLabel">Guru Kelas / Mapel</p>
                                <br><br><br>
                                <p class="underline" id="printTeacherName"></p>
                                <p class="text-[10px] font-normal" id="printTeacherNip"></p>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- TAB 3: JURNAL PERKEMBANGAN -->
                <section id="tab-sensory" class="tab-content space-y-3">
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-3">
                        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border-b pb-3 no-print">
                            <div class="flex-1 flex flex-col sm:flex-row gap-3">
                                <div class="flex-1">
                                    <label class="block text-[11px] font-bold text-slate-500 mb-1">Filter Siswa</label>
                                    <select id="sensoryStudentFilter" onchange="renderSensoryJournal()" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-bold text-slate-800">
                                        <option value="ALL">-- Semua Siswa --</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-[11px] font-bold text-slate-500 mb-1">Tanggal Cetak Dokumen</label>
                                    <input type="date" id="printDateSensoryInput" class="bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-bold text-slate-800">
                                </div>
                            </div>
                            <button onclick="printSensoryReport()" class="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs rounded-xl shadow flex items-center justify-center space-x-1.5 self-end sm:self-auto">
                                <i class="fa-solid fa-print"></i>
                                <span>Cetak Jurnal Siswa</span>
                            </button>
                        </div>

                        <!-- AREA CETAK JURNAL PERKEMBANGAN GURU -->
                        <div class="print-area">
                            <div class="hidden print:block text-center border-b border-slate-400 pb-3 mb-6 space-y-1">
                                <h1 class="font-black text-lg sm:text-xl uppercase tracking-wider text-slate-900" id="printSensoryTitle">LAPORAN JURNAL PERKEMBANGAN SISWA - [NAMA KELAS]</h1>
                                <h2 class="font-extrabold text-sm sm:text-base uppercase text-slate-800" id="printSensorySchool">SLBN 1 KULON PROGO</h2>
                                <p class="text-xs text-slate-600 font-semibold">Periode Bulan: <span id="printSensoryMonth">-</span></p>
                            </div>

                            <div id="monthlyNotesList" class="space-y-4"></div>

                            <div class="hidden print:grid grid-cols-2 gap-8 mt-12 text-xs font-bold text-center print-footer">
                                <div>
                                    <p class="text-[10px] font-normal">Mengetahui,</p>
                                    <p id="printSensoryHeadmasterLabel">Kepala Sekolah</p>
                                    <br><br><br>
                                    <p class="underline" id="printSensoryHMName"></p>
                                    <p class="text-[10px] font-normal" id="printSensoryHMNip"></p>
                                </div>
                                <div>
                                    <p class="text-[10px] font-normal" id="printSensoryDateToday"></p>
                                    <p id="printSensoryTeacherLabel">Guru Kelas / Mapel</p>
                                    <br><br><br>
                                    <p class="underline" id="printSensoryTRName"></p>
                                    <p class="text-[10px] font-normal" id="printSensoryTRNip"></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- TAB 4: PENGATURAN & IMPOR JSON / TARIK DATA CLOUD -->
                <section id="tab-settings" class="tab-content space-y-4">
                    
                    <!-- FITUR TARIK DATA DARI WALI KELAS -->
                    <div class="bg-gradient-to-br from-sky-800 via-sky-900 to-slate-900 text-white rounded-2xl shadow-md p-4 space-y-3 border border-sky-700">
                        <div class="flex items-center justify-between border-b border-sky-700 pb-2">
                            <h3 class="font-black text-xs sm:text-sm text-sky-200 flex items-center">
                                <i class="fa-solid fa-cloud-arrow-down text-amber-400 mr-2 text-base"></i> Tarik Data Murid dari Wali Kelas (Otomatis Cloud)
                            </h3>
                            <span class="px-2 py-0.5 bg-sky-700 text-sky-100 rounded text-[10px] font-bold">Fitur Guru Mapel</span>
                        </div>
                        <p class="text-[11px] text-sky-100/90 leading-relaxed">
                            Khusus Guru Mata Pelajaran/Keterampilan: Anda dapat memilih nama kelas sasaran di bawah untuk menyinkronkan seluruh daftar siswa dari Wali Kelas secara instan tanpa perlu mengetik manual.
                        </p>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3 items-end pt-1">
                            <div class="sm:col-span-8">
                                <label class="block text-[10px] font-bold text-sky-200 uppercase mb-1">Pilih Kelas / Rombel Sasaran</label>
                                <select id="cloudClassPullSelector" class="w-full bg-slate-800 border border-sky-600 text-white font-bold rounded-xl px-3 py-2 text-xs focus:ring-2 focus:ring-sky-400">
                                    <option value="">-- Memuat Daftar Kelas Sekolah... --</option>
                                </select>
                            </div>
                            <div class="sm:col-span-4">
                                <button onclick="pullStudentDataFromClass()" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-md transition flex items-center justify-center space-x-1.5">
                                    <i class="fa-solid fa-sync"></i>
                                    <span>Tarik Data Murid</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- IMPOR FILE JSON CADANGAN -->
                    <div class="bg-gradient-to-br from-amber-600 via-amber-700 to-slate-900 text-white rounded-2xl shadow-sm p-4 space-y-3">
                        <h3 class="font-bold text-xs flex items-center">
                            <i class="fa-solid fa-file-import text-amber-200 mr-2 text-sm"></i> Upload / Sync File JSON Cadangan (Pilihan / Opsional)
                        </h3>
                        <p class="text-[11px] text-amber-100/90 leading-relaxed">
                            Gunakan tombol di bawah jika Anda ingin memuat file JSON cadangan secara manual.
                        </p>
                        <input type="file" id="importJsonInput" accept=".json,application/json" class="block w-full text-xs text-slate-200 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-white file:text-amber-900 hover:file:bg-amber-50 cursor-pointer">
                    </div>

                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-3">
                        <h3 class="font-bold text-slate-800 text-xs border-b pb-2">Logo Sekolah</h3>
                        <div class="flex items-center space-x-4">
                            <div class="w-16 h-16 border rounded-2xl bg-slate-50 p-1 flex items-center justify-center overflow-hidden shrink-0" id="previewLogoBox">
                                <i class="fa-solid fa-graduation-cap text-slate-400 text-2xl"></i>
                            </div>
                            <div class="space-y-1.5 text-xs">
                                <label class="block font-bold text-slate-600">Unggah Gambar Logo Baru</label>
                                <input type="file" id="logoFileInput" accept="image/*" onchange="handleLogoUpload(event)" class="text-xs text-slate-500 file:mr-2 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-sky-50 file:text-sky-700">
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-3">
                        <h3 class="font-bold text-slate-800 text-xs border-b pb-2">Identitas Sekolah & Pengajar</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                            <div>
                                <label class="block font-bold text-slate-600 mb-1">Nama Sekolah</label>
                                <input type="text" id="cfgSchoolName" placeholder="SLBN 1 Kulon Progo" class="w-full border rounded-xl px-3 py-1.5 bg-slate-50 font-semibold">
                            </div>
                            <div>
                                <label class="block font-bold text-slate-600 mb-1">Nama Kelas / Mata Pelajaran</label>
                                <input type="text" id="cfgClassName" placeholder="Contoh: Kelas I Autisme / Keterampilan" class="w-full border rounded-xl px-3 py-1.5 bg-slate-50 font-semibold">
                            </div>
                            <div>
                                <label class="block font-bold text-slate-600 mb-1">Nama Guru / Pengajar</label>
                                <input type="text" id="cfgTeacherName" placeholder="Nama Lengkap & Gelar Guru" class="w-full border rounded-xl px-3 py-1.5 bg-slate-50 font-semibold">
                            </div>
                            <div>
                                <label class="block font-bold text-slate-600 mb-1">NIP Guru</label>
                                <input type="text" id="cfgTeacherNip" placeholder="Nomor Induk Pegawai Guru" class="w-full border rounded-xl px-3 py-1.5 bg-slate-50 font-semibold">
                            </div>
                            <div>
                                <label class="block font-bold text-slate-600 mb-1">Nama Kepala Sekolah</label>
                                <input type="text" id="cfgHeadmasterName" placeholder="Nama Lengkap & Gelar Kepala Sekolah" class="w-full border rounded-xl px-3 py-1.5 bg-slate-50 font-semibold">
                            </div>
                            <div>
                                <label class="block font-bold text-slate-600 mb-1">NIP Kepala Sekolah</label>
                                <input type="text" id="cfgHeadmasterNip" placeholder="Nomor Induk Pegawai Kepala Sekolah" class="w-full border rounded-xl px-3 py-1.5 bg-slate-50 font-semibold">
                            </div>
                        </div>
                        <button onclick="saveSchoolConfigToStorage()" class="px-4 py-2 bg-sky-700 hover:bg-sky-800 text-white text-xs font-bold rounded-xl shadow transition">
                            Simpan Identitas
                        </button>
                    </div>

                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-4">
                        <div class="border-b pb-3 flex justify-between items-center">
                            <h3 class="font-bold text-slate-800 text-xs sm:text-sm flex items-center space-x-2">
                                <i class="fa-solid fa-users text-sky-700"></i>
                                <span>Kelola Daftar Siswa & Kelompok Keterampilan</span>
                            </h3>
                            <button onclick="addNewStudent()" class="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow flex items-center space-x-1">
                                <i class="fa-solid fa-user-plus"></i>
                                <span>+ Tambah Siswa</span>
                            </button>
                        </div>

                        <div id="studentsEditContainer" class="space-y-3"></div>

                        <div class="pt-2 flex justify-end">
                            <button onclick="saveStudentSettingsToStorage()" class="px-5 py-2.5 bg-sky-700 hover:bg-sky-800 text-white text-xs font-bold rounded-xl shadow flex items-center space-x-1.5">
                                <i class="fa-solid fa-floppy-disk"></i>
                                <span>Simpan Perubahan Siswa</span>
                            </button>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    </div>

    <div id="toast" class="fixed top-4 right-4 bg-slate-900 text-white px-4 py-2 rounded-xl text-xs font-bold opacity-0 transition-opacity duration-200 z-50 shadow-lg">
        <span id="toastMsg">Tersimpan</span>
    </div>

    <!-- SCRIPT UTAMA -->
    <script>
        let currentUser = null;
        let currentUserRole = 'GURU_KELAS';
        let availableCloudClassesMap = {};
        let globalUsersDatabaseCache = {};

        function getDefaultConfig() {
            return { 
                schoolName: 'SLBN 1 Kulon Progo', 
                className: '[Nama Kelas / Mapel]', 
                teacherName: '[Nama Pengguna]', 
                teacherNip: '',
                headmasterName: '[Nama Kepala Sekolah]',
                headmasterNip: '',
                customLogo: ''
            };
        }

        window.schoolConfig = getDefaultConfig();
        window.students = [];
        window.attendanceData = {};

        const MOOD_OPTIONS = [
            { label: 'Kondusif', icon: '😌' },
            { label: 'Fokus/Semangat', icon: '🎯' },
            { label: 'Gelisah/Tantrum', icon: '😟' },
            { label: 'Sensori Overload', icon: '🤯' },
            { label: 'Kurang Sehat', icon: '🤒' }
        ];

        function localISODate(d = new Date()) {
            return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        }

        function formatFullDateIndonesian(dateString) {
            if (!dateString) return '';
            const [year, month, day] = dateString.split('-').map(Number);
            const dateObj = new Date(year, month - 1, day);
            const days = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
            const months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
            return `${days[dateObj.getDay()]},${day} ${months[month - 1]}${year}`;
        }

        function formatPrintDateIndonesian(dateString) {
            if (!dateString) return 'Kulon Progo, -';
            const [year, month, day] = dateString.split('-').map(Number);
            const months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
            return `Kulon Progo, ${day} ${months[month - 1]}${year}`;
        }

        function formatMonthYearIndonesian(monthString) {
            if (!monthString) return '-';
            const [year, month] = monthString.split('-').map(Number);
            const months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
            return `${months[month - 1]}${year}`;
        }

        function formatShortDateIndonesian(dateString) {
            if (!dateString) return '';
            const [year, month, day] = dateString.split('-');
            return `(${day}/${month}/${year})`;
        }

        const selectedDateInput = document.getElementById('selectedDate');
        const selectedMonthInput = document.getElementById('selectedMonth');
        const printDateMonthlyInput = document.getElementById('printDateMonthlyInput');
        const printDateSensoryInput = document.getElementById('printDateSensoryInput');

        window.addEventListener('DOMContentLoaded', () => {
            const today = localISODate();
            selectedDateInput.value = today;
            selectedMonthInput.value = today.substring(0, 7);
            printDateMonthlyInput.value = today;
            printDateSensoryInput.value = today;
            
            document.getElementById('topDateBadge').textContent = formatFullDateIndonesian(today);
            document.getElementById('hmTodayDate').textContent = formatFullDateIndonesian(today);
            document.getElementById('dailyDateTitle').textContent = formatFullDateIndonesian(today);
            document.getElementById('btnTodayShortDate').textContent = formatShortDateIndonesian(today);

            document.getElementById('importJsonInput').addEventListener('change', handleJsonFileSelect);

            const checkFirebaseLoaded = setInterval(() => {
                if (window.fbOnAuth) {
                    clearInterval(checkFirebaseLoaded);
                    window.fbOnAuth(window.fbAuth, (user) => {
                        if (user) {
                            currentUser = user;
                            document.getElementById('userEmailBadge').textContent = user.email;
                            openMainApp();
                            loadUserDataFromFirebase(user.uid);
                        } else {
                            currentUser = null;
                            clearLocalCache();
                            showLandingScreen();
                        }
                    });
                }
            }, 100);

            selectedDateInput.addEventListener('change', () => { 
                const dt = selectedDateInput.value;
                document.getElementById('topDateBadge').textContent = formatFullDateIndonesian(dt);
                document.getElementById('dailyDateTitle').textContent = formatFullDateIndonesian(dt);
                renderDailyCards(); 
            });

            selectedMonthInput.addEventListener('change', () => { 
                renderMonthlyTable(); 
                renderSensoryJournal(); 
                if (currentUserRole === 'KEPALA_SEKOLAH') renderHeadmasterTeacherDetail();
            });
        });

        function showLandingScreen() {
            document.getElementById('mainAppContent').classList.add('hidden');
            document.getElementById('landingScreen').classList.remove('hidden');
        }

        function openMainApp() {
            document.getElementById('landingScreen').classList.add('hidden');
            document.getElementById('mainAppContent').classList.remove('hidden');
            
            renderNavigationForRole();
            applyConfigToDOM();
            updateGroupDropdowns();
            renderDailyCards();
            renderMonthlyTable();
            renderStudentsEdit();
            renderSensoryJournal();
            populateStudentFilter();
            populateCloudClassSelector();
        }

        function renderNavigationForRole() {
            const nav = document.getElementById('navContainer');
            if (currentUserRole === 'KEPALA_SEKOLAH') {
                nav.innerHTML = `
                    <button onclick="switchTab('headmaster')" id="nav-headmaster" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-white bg-sky-700 shadow-sm transition">
                        <i class="fa-solid fa-chart-pie text-base w-5 text-center"></i>
                        <span>Dashboard Pantau</span>
                    </button>
                    <button onclick="switchTab('daily')" id="nav-daily" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-house text-base w-5 text-center"></i>
                        <span>Presensi Harian</span>
                    </button>
                    <button onclick="switchTab('monthly')" id="nav-monthly" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-table-cells text-base w-5 text-center"></i>
                        <span>Rekap Bulanan</span>
                    </button>
                    <button onclick="switchTab('sensory')" id="nav-sensory" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-book-open text-base w-5 text-center"></i>
                        <span>Jurnal Perkembangan</span>
                    </button>
                    <button onclick="switchTab('settings')" id="nav-settings" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-sliders text-base w-5 text-center"></i>
                        <span>Pengaturan & JSON</span>
                    </button>
                `;
                switchTab('headmaster');
            } else {
                nav.innerHTML = `
                    <button onclick="switchTab('daily')" id="nav-daily" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-white bg-sky-700 shadow-sm transition">
                        <i class="fa-solid fa-house text-base w-5 text-center"></i>
                        <span>Presensi Harian</span>
                    </button>
                    <button onclick="switchTab('monthly')" id="nav-monthly" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-table-cells text-base w-5 text-center"></i>
                        <span>Rekap Bulanan</span>
                    </button>
                    <button onclick="switchTab('sensory')" id="nav-sensory" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-book-open text-base w-5 text-center"></i>
                        <span>Jurnal Perkembangan</span>
                    </button>
                    <button onclick="switchTab('settings')" id="nav-settings" class="nav-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sky-100 hover:bg-sky-800 transition">
                        <i class="fa-solid fa-sliders text-base w-5 text-center"></i>
                        <span>Pengaturan & JSON</span>
                    </button>
                `;
                switchTab('daily');
            }
        }

        function useOfflineMode() {
            localStorage.removeItem('sikemasku_force_logged_out');
            loadLocalCache();
            openMainApp();
        }

        function saveLocalCache() {
            const prefix = currentUser ? currentUser.uid : 'guest';
            localStorage.setItem(`sikemasku_config_${prefix}`, JSON.stringify(schoolConfig));
            localStorage.setItem(`sikemasku_students_${prefix}`, JSON.stringify(students));
            localStorage.setItem(`sikemasku_attendance_${prefix}`, JSON.stringify(attendanceData));
            localStorage.setItem(`sikemasku_role_${prefix}`, currentUserRole);
        }

        function loadLocalCache() {
            const prefix = currentUser ? currentUser.uid : 'guest';
            try {
                const c = localStorage.getItem(`sikemasku_config_${prefix}`);
                const s = localStorage.getItem(`sikemasku_students_${prefix}`);
                const a = localStorage.getItem(`sikemasku_attendance_${prefix}`);
                const r = localStorage.getItem(`sikemasku_role_${prefix}`);
                if (c) schoolConfig = Object.assign(getDefaultConfig(), JSON.parse(c));
                if (s) students = JSON.parse(s);
                if (a) attendanceData = JSON.parse(a);
                if (r) currentUserRole = r;
            } catch(e) {}
        }

        function clearLocalCache() {
            schoolConfig = getDefaultConfig();
            students = [];
            attendanceData = {};
            currentUserRole = 'GURU_KELAS';
        }

        function toggleAuthTab(type) {
            if (type === 'login') {
                document.getElementById('formLogin').classList.remove('hidden');
                document.getElementById('formRegister').classList.add('hidden');
                document.getElementById('tabBtnLogin').className = "flex-1 py-2 border-b-2 border-sky-600 text-sky-700";
                document.getElementById('tabBtnRegister').className = "flex-1 py-2 text-slate-400";
            } else {
                document.getElementById('formLogin').classList.add('hidden');
                document.getElementById('formRegister').classList.remove('hidden');
                document.getElementById('tabBtnRegister').className = "flex-1 py-2 border-b-2 border-sky-600 text-sky-700";
                document.getElementById('tabBtnLogin').className = "flex-1 py-2 text-slate-400";
            }
        }

        async function handleFirebaseLogin(e) {
            e.preventDefault();
            const btn = document.getElementById('btnLoginSubmit');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Memproses...';

            try {
                localStorage.removeItem('sikemasku_force_logged_out');
                const userCred = await window.fbSignIn(window.fbAuth, document.getElementById('loginEmail').value, document.getElementById('loginPass').value);
                currentUser = userCred.user;
                document.getElementById('userEmailBadge').textContent = currentUser.email;
                await loadUserDataFromFirebase(currentUser.uid, true);
                openMainApp();
                showToast("Selamat datang kembali!");
            } catch (err) { 
                console.error(err);
                alert("Gagal Login: Email atau password salah."); 
            } finally {
                btn.disabled = false;
                btn.innerHTML = 'Masuk Akun <i class="fa-solid fa-right-to-bracket ml-1"></i>';
            }
        }

        async function handleForgotPassword() {
            const inputEmail = document.getElementById('loginEmail').value || prompt("Masukkan alamat email Anda yang terdaftar:");
            if (!inputEmail) {
                alert("Silakan masukkan email Anda terlebih dahulu.");
                return;
            }

            try {
                await window.fbResetPass(window.fbAuth, inputEmail);
                alert(`Email tautan pemulihan (reset) password telah dikirimkan ke ${inputEmail}.\n\nSilakan periksa kotak masuk atau folder Spam email Anda.`);
            } catch (err) {
                console.error("Gagal reset password:", err);
                alert("Gagal mengirim email reset password. Pastikan alamat email sudah benar dan terdaftar.");
            }
        }

        async function handleFirebaseRegister(e) {
            e.preventDefault();
            const email = document.getElementById('regEmail').value;
            const pass = document.getElementById('regPass').value;
            const role = document.getElementById('regRole').value;
            const btn = document.getElementById('btnRegSubmit');

            if (pass.length < 6) {
                alert("Password minimal harus 6 karakter!");
                return;
            }

            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Memproses...';

            try {
                localStorage.removeItem('sikemasku_force_logged_out');
                const userCred = await window.fbSignUp(window.fbAuth, email, pass);
                currentUser = userCred.user;
                currentUserRole = role;
                
                if (currentUser) {
                    schoolConfig = getDefaultConfig();
                    students = [];
                    attendanceData = {};
                    await syncAllToFirebase();
                }

                document.getElementById('userEmailBadge').textContent = currentUser.email;
                openMainApp();
                showToast("Akun berhasil dibuat!");
            } catch (err) { 
                console.error(err);
                alert("Gagal Pendaftaran: " + err.message); 
            } finally {
                btn.disabled = false;
                btn.innerHTML = 'Daftar Akun Baru';
            }
        }

        function handleFirebaseLogout() { 
            localStorage.setItem('sikemasku_force_logged_out', 'true');
            if (window.fbAuth) {
                window.fbSignOut(window.fbAuth).then(() => { location.reload(); }).catch(() => { location.reload(); });
            } else {
                location.reload();
            }
        }

        async function loadUserDataFromFirebase(uid, forceCloud = false) {
            if (!uid) return;
            if (!forceCloud) loadLocalCache();

            try {
                const snapshot = await window.fbGet(window.fbChild(window.fbRef(window.fbDb), `users/${uid}`));
                if (snapshot.exists()) {
                    const data = snapshot.val();
                    if (data.students && Array.isArray(data.students)) students = data.students;
                    if (data.config) schoolConfig = Object.assign(getDefaultConfig(), data.config);
                    if (data.attendance) attendanceData = data.attendance;
                    if (data.role) currentUserRole = data.role;
                    saveLocalCache();
                }

                if (currentUserRole === 'KEPALA_SEKOLAH') {
                    await loadHeadmasterGlobalDashboard();
                }

                applyConfigToDOM(); 
                updateGroupDropdowns();
                renderDailyCards(); 
                renderMonthlyTable(); 
                renderStudentsEdit(); 
                renderSensoryJournal(); 
                populateStudentFilter();
                populateCloudClassSelector();
            } catch (e) { console.error("Database note:", e); }
        }

        async function populateCloudClassSelector() {
            const selector = document.getElementById('cloudClassPullSelector');
            if (!selector) return;

            try {
                const snapshot = await window.fbGet(window.fbChild(window.fbRef(window.fbDb), `users`));
                if (!snapshot.exists()) {
                    selector.innerHTML = `<option value="">-- Belum ada data kelas di Cloud --</option>`;
                    return;
                }

                const usersData = snapshot.val();
                availableCloudClassesMap = {};
                let optsHTML = `<option value="">-- Pilih Kelas / Wali Kelas --</option>`;

                Object.keys(usersData).forEach(uid => {
                    const u = usersData[uid];
                    if (u.role !== 'KEPALA_SEKOLAH' && u.students && u.students.length > 0) {
                        const className = u.config?.className || 'Kelas Tanpa Nama';
                        const teacherName = u.config?.teacherName || 'Wali Kelas';
                        const count = u.students.length;

                        availableCloudClassesMap[uid] = u.students;
                        optsHTML += `<option value="${uid}">${className} (${teacherName} -${count} murid)</option>`;
                    }
                });

                selector.innerHTML = optsHTML;
            } catch (err) {
                console.error("Gagal memuat selector kelas:", err);
                selector.innerHTML = `<option value="">-- Gagal memuat data kelas --</option>`;
            }
        }

        async function pullStudentDataFromClass() {
            const selector = document.getElementById('cloudClassPullSelector');
            const targetUid = selector.value;

            if (!targetUid || !availableCloudClassesMap[targetUid]) {
                alert("Silakan pilih kelas sasaran terlebih dahulu dari daftar!");
                return;
            }

            const pulledStudents = availableCloudClassesMap[targetUid];
            if (!pulledStudents || pulledStudents.length === 0) {
                alert("Kelas yang dipilih tidak memiliki data murid.");
                return;
            }

            const confirmMerge = confirm(`Ditemukan ${pulledStudents.length} murid pada kelas tersebut.\n\nKlik 'OK' untuk MENGGABUNGKAN ke daftar murid Anda saat ini.\nKlik 'Cancel' jika ingin MENGGANTI seluruh daftar murid Anda.`);

            if (confirmMerge) {
                const existingNises = new Set(students.map(s => String(s.nis || s.id)));
                let addedCount = 0;

                pulledStudents.forEach(st => {
                    const nisKey = String(st.nis || st.id);
                    if (!existingNises.has(nisKey)) {
                        const maxId = students.length > 0 ? Math.max(...students.map(s => s.id)) + 1 : 1;
                        students.push({
                            id: maxId,
                            name: st.name,
                            nis: st.nis || '',
                            group: st.group || 'Umum',
                            phone: st.phone || ''
                        });
                        addedCount++;
                    }
                });

                await syncAllToFirebase();
                renderStudentsEdit();
                updateGroupDropdowns();
                renderDailyCards();
                populateStudentFilter();
                showToast(`${addedCount} murid baru berhasil ditambahkan!`);
                alert(`Berhasil menambahkan ${addedCount} murid baru dari kelas sasaran!`);
            } else {
                students = pulledStudents.map((st, idx) => ({
                    id: idx + 1,
                    name: st.name,
                    nis: st.nis || '',
                    group: st.group || 'Umum',
                    phone: st.phone || ''
                }));

                await syncAllToFirebase();
                renderStudentsEdit();
                updateGroupDropdowns();
                renderDailyCards();
                populateStudentFilter();
                showToast(`Daftar murid diperbarui (${students.length} murid)!`);
                alert(`Seluruh daftar murid Anda kini disinkronkan dengan kelas sasaran (${students.length} murid)!`);
            }
        }

        async function loadHeadmasterGlobalDashboard() {
            try {
                const snapshot = await window.fbGet(window.fbChild(window.fbRef(window.fbDb), `users`));
                if (!snapshot.exists()) return;

                globalUsersDatabaseCache = snapshot.val();
                const today = localISODate();

                let totalStudents = 0, totalTeachers = 0, totH = 0, totS = 0, totI = 0, totA = 0;
                const statusContainer = document.getElementById('hmClassStatusContainer');
                const teacherSelector = document.getElementById('hmTeacherSelector');
                
                statusContainer.innerHTML = '';
                let selectOpts = `<option value="">-- Pilih Guru / Kelas --</option>`;

                Object.keys(globalUsersDatabaseCache).forEach(uid => {
                    const u = globalUsersDatabaseCache[uid];
                    if (u.role !== 'KEPALA_SEKOLAH') {
                        totalTeachers++;
                        const className = u.config?.className || u.config?.schoolName || 'Kelas Noname';
                        const teacherName = u.config?.teacherName || 'Pengajar';
                        const userStudents = u.students || [];
                        totalStudents += userStudents.length;

                        const todayAtt = u.attendance?.[today] || {};
                        const filledCount = Object.keys(todayAtt).length;
                        const isFilled = filledCount > 0;

                        userStudents.forEach(st => {
                            const rec = todayAtt[st.id]?.status;
                            if (rec === 'H') totH++;
                            else if (rec === 'S') totS++;
                            else if (rec === 'I') totI++;
                            else if (rec === 'A') totA++;
                        });

                        selectOpts += `<option value="${uid}">${teacherName} (${className})</option>`;

                        const row = document.createElement('div');
                        row.className = `p-3 rounded-xl border flex justify-between items-center ${isFilled ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-slate-50 border-slate-200 text-slate-700'}`;
                        row.innerHTML = `
                            <div>
                                <h5 class="font-extrabold">${className}</h5>
                                <p class="text-[10px] text-slate-500">Guru: ${teacherName} (${userStudents.length} murid)</p>
                            </div>
                            <div>
                                ${isFilled ? `<span class="px-2.5 py-1 bg-emerald-600 text-white font-bold rounded-lg text-[10px]"><i class="fa-solid fa-check mr-1"></i> Sudah Diisi</span>` : `<span class="px-2.5 py-1 bg-rose-100 text-rose-700 font-bold rounded-lg text-[10px]"><i class="fa-solid fa-clock mr-1"></i> Belum Diisi</span>`}
                            </div>
                        `;
                        statusContainer.appendChild(row);
                    }
                });

                teacherSelector.innerHTML = selectOpts;

                document.getElementById('hmTotalStudents').textContent = totalStudents;
                document.getElementById('hmTotalTeachers').textContent = totalTeachers;
                document.getElementById('hmTotalHadir').textContent = totH;
                document.getElementById('hmTotalSakitIzin').textContent = (totS + totI);
                document.getElementById('hmTotalAlfa').textContent = totA;
            } catch(err) { console.error("HM Dashboard error:", err); }
        }

        function renderHeadmasterTeacherDetail() {
            const uid = document.getElementById('hmTeacherSelector').value;
            const detailArea = document.getElementById('hmTeacherDetailArea');
            const placeholder = document.getElementById('hmNoTeacherPlaceholder');

            if (!uid || !globalUsersDatabaseCache[uid]) {
                detailArea.classList.add('hidden');
                placeholder.classList.remove('hidden');
                return;
            }

            placeholder.classList.add('hidden');
            detailArea.classList.remove('hidden');

            const targetUser = globalUsersDatabaseCache[uid];
            const cfg = targetUser.config || {};
            const teacherStudents = targetUser.students || [];
            const teacherAtt = targetUser.attendance || {};

            document.getElementById('hmInspectorTeacherName').textContent = cfg.teacherName || '[Nama Guru]';
            document.getElementById('hmInspectorClassName').textContent = cfg.className || '[Nama Kelas / Mapel]';

            const monthStr = selectedMonthInput.value;
            const [year, month] = monthStr.split('-').map(Number);
            const daysInMonth = new Date(year, month, 0).getDate();

            const daysHeaderRow = document.getElementById('hmDaysHeaderRow');
            let headerHTML = `<th class="p-1.5 border text-center">NO</th><th class="p-1.5 border text-center">NIS</th><th class="p-1.5 border">NAMA SISWA</th><th class="p-1.5 border text-center">KELOMPOK</th>`;
            for (let d = 1; d <= daysInMonth; d++) headerHTML += `<th class="p-0.5 border text-center w-6 text-[10px]">${d}</th>`;
            headerHTML += `<th class="p-1 border text-center bg-emerald-100 text-emerald-800">H</th><th class="p-1 border text-center bg-amber-100 text-amber-800">S</th><th class="p-1 border text-center bg-sky-100 text-sky-800">I</th><th class="p-1 border text-center bg-rose-100 text-rose-800">A</th><th class="p-1 border text-center">%</th>`;
            daysHeaderRow.innerHTML = headerHTML;

            const tbody = document.getElementById('hmMonthlyTableBody');
            tbody.innerHTML = '';

            teacherStudents.forEach((student, index) => {
                const nisStr = String(student.nis || student.id).padStart(3, '0');
                let hCount = 0, sCount = 0, iCount = 0, aCount = 0;

                let rowHTML = `<tr>
                    <td class="p-1.5 border text-center font-bold">${index + 1}</td>
                    <td class="p-1.5 border text-center font-bold text-slate-500">${nisStr}</td>
                    <td class="p-1.5 border font-bold text-slate-800">${student.name}</td>
                    <td class="p-1.5 border text-center font-bold text-amber-800 bg-amber-50">${student.group || 'Umum'}</td>`;

                for (let d = 1; d <= daysInMonth; d++) {
                    const fullDate = `${monthStr}-${String(d).padStart(2, '0')}`;
                    const st = teacherAtt[fullDate]?.[student.id]?.status || '-';
                    let bgClass = 'text-slate-300';

                    if (st === 'H') { bgClass = 'bg-emerald-50 text-emerald-700 font-black'; hCount++; }
                    else if (st === 'S') { bgClass = 'bg-amber-100 text-amber-800 font-black'; sCount++; }
                    else if (st === 'I') { bgClass = 'bg-sky-100 text-sky-800 font-black'; iCount++; }
                    else if (st === 'A') { bgClass = 'bg-rose-100 text-rose-800 font-black'; aCount++; }

                    rowHTML += `<td class="p-0.5 border text-center ${bgClass}">${st}</td>`;
                }

                const totalActive = hCount + sCount + iCount + aCount;
                const pct = totalActive > 0 ? Math.round((hCount / totalActive) * 100) : 0;

                rowHTML += `<td class="p-1 border text-center font-black text-emerald-700 bg-emerald-50/50">${hCount}</td><td class="p-1 border text-center font-black text-amber-700 bg-amber-50/50">${sCount}</td><td class="p-1 border text-center font-black text-sky-700 bg-sky-50/50">${iCount}</td><td class="p-1 border text-center font-black text-rose-700 bg-rose-50/50">${aCount}</td><td class="p-1 border text-center font-black text-slate-800">${pct}%</td></tr>`;
                tbody.innerHTML += rowHTML;
            });

            const sensoryNotesContainer = document.getElementById('hmSensoryNotesList');
            sensoryNotesContainer.innerHTML = '';
            let hasEntries = false;

            Object.keys(teacherAtt).sort().reverse().forEach(date => {
                if (date && date.startsWith(monthStr)) {
                    teacherStudents.forEach(student => {
                        const rec = teacherAtt[date]?.[student.id];
                        if (rec && ((rec.note && rec.note.trim() !== '') || (rec.mood && rec.mood.trim() !== ''))) {
                            hasEntries = true;
                            const divCard = document.createElement('div');
                            divCard.className = 'bg-slate-50 rounded-xl p-3 border border-slate-200 text-xs space-y-1.5';
                            divCard.innerHTML = `
                                <div class="flex justify-between items-center border-b pb-1.5">
                                    <div>
                                        <span class="text-slate-900 font-extrabold">${student.name}</span>
                                        <span class="ml-2 px-1.5 py-0.5 bg-amber-100 text-amber-800 rounded text-[10px] font-bold">${student.group || 'Umum'}</span>
                                    </div>
                                    <span class="text-slate-500 font-semibold text-[11px]">${formatFullDateIndonesian(date)}</span>${rec.mood ? `<span class="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full font-bold text-[10px]">${rec.mood}</span>` : ''}
                                </div>
                                ${rec.note && rec.note.trim() !== '' ? `<p class="text-slate-700 leading-relaxed font-medium">${rec.note}</p>` : '<p class="text-slate-400 italic text-[11px]">Tidak ada catatan tertulis.</p>'}
                            `;
                            sensoryNotesContainer.appendChild(divCard);
                        }
                    });
                }
            });

            if (!hasEntries) {
                sensoryNotesContainer.innerHTML = `<p class="text-xs text-slate-400 italic text-center py-4">Belum ada catatan jurnal pada periode bulan ini dari guru terpilih.</p>`;
            }
        }

        function printHeadmasterTeacherReport(type) {
            const uid = document.getElementById('hmTeacherSelector').value;
            if (!uid || !globalUsersDatabaseCache[uid]) return;

            const targetUser = globalUsersDatabaseCache[uid];
            const cfg = targetUser.config || {};
            const hmName = schoolConfig.teacherName || schoolConfig.headmasterName || '[Nama Kepala Sekolah]';
            const hmNip = schoolConfig.headmasterNip ? `NIP. ${schoolConfig.headmasterNip}` : '';

            const teacherName = cfg.teacherName || '[Nama Guru]';
            const teacherNip = cfg.teacherNip ? `NIP. ${cfg.teacherNip}` : '';
            const classNameUpper = (cfg.className || '[KELAS]').toUpperCase();
            const schoolNameUpper = (schoolConfig.schoolName || 'SLBN 1 KULON PROGO').toUpperCase();
            const formattedMonthText = formatMonthYearIndonesian(selectedMonthInput.value);
            const formattedPrintDate = formatPrintDateIndonesian(localISODate());

            document.getElementById('hmMonthlyPrintBlock').classList.remove('is-printing');
            document.getElementById('hmSensoryPrintBlock').classList.remove('is-printing');

            if (type === 'monthly') {
                document.getElementById('hmPrintMonthlyTitle').textContent = `REKAPITULASI PRESENSI - ${classNameUpper}`;
                document.getElementById('hmPrintMonthlySchool').textContent = schoolNameUpper;
                document.getElementById('hmPrintMonthPeriod').textContent = formattedMonthText;

                document.getElementById('hmPrintHMName').textContent = hmName;
                document.getElementById('hmPrintHMNip').textContent = hmNip;
                document.getElementById('hmPrintTRName').textContent = teacherName;
                document.getElementById('hmPrintTRNip').textContent = teacherNip;
                document.getElementById('hmPrintTodayDate').textContent = formattedPrintDate;

                document.getElementById('hmMonthlyPrintBlock').classList.add('is-printing');
                setTimeout(() => { window.print(); }, 100);
            } else if (type === 'sensory') {
                document.getElementById('hmPrintSensoryTitle').textContent = `LAPORAN JURNAL PERKEMBANGAN SISWA - ${classNameUpper}`;
                document.getElementById('hmPrintSensorySchool').textContent = schoolNameUpper;
                document.getElementById('hmPrintSensoryMonth').textContent = formattedMonthText;

                document.getElementById('hmSensoryHMName').textContent = hmName;
                document.getElementById('hmSensoryHMNip').textContent = hmNip;
                document.getElementById('hmSensoryTRName').textContent = teacherName;
                document.getElementById('hmSensoryTRNip').textContent = teacherNip;
                document.getElementById('hmSensoryTodayDate').textContent = formattedPrintDate;

                document.getElementById('hmSensoryPrintBlock').classList.add('is-printing');
                setTimeout(() => { window.print(); }, 100);
            }
        }

        async function forceReloadCloudData() {
            if (!currentUser) {
                alert("Silakan login dengan akun Anda terlebih dahulu.");
                return;
            }
            showToast("Mengunduh data terbaru...");
            await loadUserDataFromFirebase(currentUser.uid, true);
            showToast("Data terbaru berhasil dimuat!");
        }

        async function syncToFirebase(path, data) {
            saveLocalCache();
            if (!currentUser) return;
            try {
                await window.fbSet(window.fbRef(window.fbDb, `users/${currentUser.uid}/${path}`), data);
            } catch(e) { console.error("Firebase sync error: ", e); }
        }

        async function syncAllToFirebase() {
            saveLocalCache();
            if (!currentUser) return;
            try {
                await window.fbSet(window.fbRef(window.fbDb, `users/${currentUser.uid}`), {
                    config: schoolConfig,
                    students: students,
                    attendance: attendanceData,
                    role: currentUserRole
                });
                showToast("Tersimpan di Cloud!");
            } catch(e) {
                alert("Gagal menyimpan ke Cloud. Pastikan koneksi internet aktif.");
            }
        }

        async function handleJsonFileSelect(e) {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = async function(evt) {
                try {
                    const raw = JSON.parse(evt.target.result);

                    const cfg = raw.schoolConfig || raw.config || {};
                    schoolConfig = {
                        schoolName: cfg.schoolName || schoolConfig.schoolName,
                        className: cfg.className || schoolConfig.className,
                        teacherName: cfg.teacherName || schoolConfig.teacherName,
                        teacherNip: cfg.teacherNip || schoolConfig.teacherNip || '',
                        headmasterName: cfg.headmasterName || schoolConfig.headmasterName || '',
                        headmasterNip: cfg.headmasterNip || schoolConfig.headmasterNip || '',
                        customLogo: cfg.customLogo || schoolConfig.customLogo || ''
                    };

                    const rawStudents = raw.students || [];
                    if (Array.isArray(rawStudents) && rawStudents.length > 0) {
                        students = rawStudents.map((s, idx) => ({
                            id: s.id !== undefined ? s.id : (idx + 1),
                            name: s.name || `Siswa ${idx + 1}`,
                            nis: String(s.nis || ''),
                            group: s.group || 'Umum',
                            phone: String(s.phone || '')
                        }));
                    }

                    const rawAtt = raw.attendanceData || raw.attendance || {};
                    if (Object.keys(rawAtt).length > 0) attendanceData = rawAtt;

                    saveLocalCache();
                    await syncAllToFirebase();

                    applyConfigToDOM();
                    updateGroupDropdowns();
                    renderDailyCards();
                    renderMonthlyTable();
                    renderStudentsEdit();
                    renderSensoryJournal();
                    populateStudentFilter();

                    alert(`BERHASIL DISINKRONKAN KE CLOUD!\nSekolah: ${schoolConfig.schoolName}\nTotal Siswa:${students.length} anak`);
                } catch (err) { alert("Format JSON tidak sesuai: " + err.message); }
            };
            reader.readAsText(file);
        }

        function handleLogoUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                schoolConfig.customLogo = evt.target.result;
                applyConfigToDOM();
                syncToFirebase('config', schoolConfig);
                showToast("Logo berhasil diubah!");
            };
            reader.readAsDataURL(file);
        }

        function applyConfigToDOM() {
            const schoolName = schoolConfig.schoolName || 'SLBN 1 Kulon Progo';
            const className = schoolConfig.className || '[Nama Kelas / Mapel]';
            const teacherName = schoolConfig.teacherName || '[Nama Pengguna]';
            const headmasterName = schoolConfig.headmasterName || '[Nama Kepala Sekolah]';

            const roleLabels = { 'GURU_KELAS': 'Guru Kelas', 'GURU_MAPEL': 'Guru Mapel', 'KEPALA_SEKOLAH': 'Kepala Sekolah' };

            document.getElementById('sidebarSchoolName').textContent = schoolName;
            document.getElementById('sidebarClassName').textContent = `${roleLabels[currentUserRole]} -${className}`;
            
            document.getElementById('cardRoleBadge').textContent = roleLabels[currentUserRole] || 'GURU / PENGAJAR';
            document.getElementById('cardTeacherName').textContent = teacherName;
            document.getElementById('cardHeadmasterName').textContent = headmasterName;

            document.getElementById('cfgSchoolName').value = schoolConfig.schoolName || '';
            document.getElementById('cfgClassName').value = schoolConfig.className || '';
            document.getElementById('cfgTeacherName').value = schoolConfig.teacherName || '';
            document.getElementById('cfgTeacherNip').value = schoolConfig.teacherNip || '';
            document.getElementById('cfgHeadmasterName').value = schoolConfig.headmasterName || '';
            document.getElementById('cfgHeadmasterNip').value = schoolConfig.headmasterNip || '';

            if (schoolConfig.customLogo) {
                const imgHTML = `<img src="${schoolConfig.customLogo}" class="w-full h-full object-contain">`;
                document.getElementById('sidebarLogoBox').innerHTML = imgHTML;
                document.getElementById('landingLogoBox').innerHTML = imgHTML;
                document.getElementById('previewLogoBox').innerHTML = imgHTML;
            }
        }

        function updateGroupDropdowns() {
            const groups = Array.from(new Set(students.map(s => s.group || 'Umum'))).filter(Boolean);
            
            const dailySel = document.getElementById('dailyGroupFilter');
            const monthlySel = document.getElementById('monthlyGroupFilter');
            
            let opts = `<option value="ALL">-- Semua Siswa / Umum --</option>`;
            groups.forEach(g => { opts += `<option value="${g}">${g}</option>`; });

            dailySel.innerHTML = opts;
            monthlySel.innerHTML = opts;
        }

        function switchTab(t) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            const targetTab = document.getElementById(`tab-${t}`);
            if (targetTab) targetTab.classList.add('active');
            
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('text-white', 'bg-sky-700', 'shadow-sm');
                btn.classList.add('text-sky-100');
            });
            
            const activeBtn = document.getElementById(`nav-${t}`);
            if (activeBtn) {
                activeBtn.classList.remove('text-sky-100');
                activeBtn.classList.add('text-white', 'bg-sky-700', 'shadow-sm');
            }

            const titles = { headmaster: 'Dashboard Kepala Sekolah', daily: 'Presensi Harian', monthly: 'Rekap Bulanan', sensory: 'Jurnal Perkembangan', settings: 'Pengaturan & JSON' };
            document.getElementById('topPageTitle').textContent = titles[t] || 'Presensi';

            if (t === 'monthly') renderMonthlyTable();
            if (t === 'sensory') renderSensoryJournal();
            if (t === 'settings') { renderStudentsEdit(); populateCloudClassSelector(); }
            if (t === 'headmaster') loadHeadmasterGlobalDashboard();
        }

        function setToday() {
            const today = localISODate();
            selectedDateInput.value = today;
            document.getElementById('topDateBadge').textContent = formatFullDateIndonesian(today);
            document.getElementById('dailyDateTitle').textContent = formatFullDateIndonesian(today);
            renderDailyCards();
        }

        function changeDate(days) {
            const current = new Date(selectedDateInput.value || localISODate());
            current.setDate(current.getDate() + days);
            const iso = localISODate(current);
            selectedDateInput.value = iso;
            document.getElementById('topDateBadge').textContent = formatFullDateIndonesian(iso);
            document.getElementById('dailyDateTitle').textContent = formatFullDateIndonesian(iso);
            renderDailyCards();
        }

        function markAllHadir() {
            const date = selectedDateInput.value;
            const groupFilter = document.getElementById('dailyGroupFilter').value;
            if (!attendanceData[date]) attendanceData[date] = {};
            
            students.forEach(s => {
                if (groupFilter === 'ALL' || (s.group || 'Umum') === groupFilter) {
                    if (!attendanceData[date][s.id]) attendanceData[date][s.id] = { status: 'H', mood: 'Kondusif', note: '' };
                    attendanceData[date][s.id].status = 'H';
                }
            });
            syncToFirebase('attendance', attendanceData);
            renderDailyCards();
            showToast("Semua siswa ditandai Hadir!");
        }

        function renderDailyCards() {
            const date = selectedDateInput.value;
            const container = document.getElementById('studentCardsContainer');
            const query = (document.getElementById('searchStudentInput')?.value || '').toLowerCase();
            const groupFilter = document.getElementById('dailyGroupFilter').value;
            container.innerHTML = '';

            let filtered = students;
            if (groupFilter !== 'ALL') filtered = filtered.filter(s => (s.group || 'Umum') === groupFilter);
            if (query) filtered = filtered.filter(s => s.name.toLowerCase().includes(query));

            document.getElementById('dailyStudentCountCount').textContent = `${filtered.length} Murid`;

            if (filtered.length === 0) {
                container.innerHTML = `<div class="text-center py-10 bg-white rounded-2xl border border-dashed text-xs text-slate-400 space-y-2"><p class="font-bold text-slate-600">Tidak ada siswa pada kelompok ini.</p></div>`;
                return;
            }

            filtered.forEach(student => {
                const rec = attendanceData[date]?.[student.id] || { status: 'H', mood: 'Kondusif', note: '' };
                const nisStr = String(student.nis || student.id).padStart(3, '0');
                const studentGroup = student.group || 'Umum';
                
                const card = document.createElement('div');
                card.className = 'bg-white rounded-2xl p-4 border border-slate-200 space-y-3 shadow-sm';
                card.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 rounded-full bg-sky-600 text-white font-bold flex items-center justify-center text-xs shadow">${nisStr}</div>
                            <div>
                                <h3 class="font-bold text-slate-800 text-sm sm:text-base">${student.name}</h3>
                                <div class="flex items-center space-x-2">
                                    <span class="text-[11px] text-slate-400 font-semibold">NIS: ${nisStr}</span>
                                    <span class="px-2 py-0.5 bg-amber-100 text-amber-800 rounded-md text-[10px] font-bold">${studentGroup}</span>
                                </div>
                            </div>
                        </div>
                        <button onclick="sendWhatsApp(${student.id})" class="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 rounded-xl text-xs font-bold flex items-center space-x-1 transition">
                            <i class="fa-brands fa-whatsapp text-sm text-emerald-600"></i>
                            <span>Kirim WA</span>
                        </button>
                    </div>

                    <div>
                        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">STATUS KEHADIRAN</label>
                        <div class="grid grid-cols-4 gap-2 text-xs">
                            ${[ { key: 'H', label: 'Hadir (H)' }, { key: 'S', label: 'Sakit (S)' }, { key: 'I', label: 'Izin (I)' }, { key: 'A', label: 'Alfa (A)' } ].map(st => `
                                <button onclick="saveAttendance(${student.id}, '${st.key}')" class="py-2.5 rounded-xl font-bold border transition text-center ${rec.status === st.key ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm' : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'}">
                                    ${st.label}
                                </button>
                            `).join('')}
                        </div>
                    </div>

                    <div>
                        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">KONDISI / PERILAKU</label>
                        <div class="flex flex-wrap gap-1.5">
                            ${MOOD_OPTIONS.map(m => `
                                <button onclick="saveAttendanceMood(${student.id}, '${m.label}')" class="px-3 py-1.5 rounded-xl text-xs font-bold border transition flex items-center space-x-1 ${rec.mood === m.label ? 'bg-emerald-100 text-emerald-800 border-emerald-400 shadow-sm' : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'}">
                                    <span>${m.icon}</span>
                                    <span>${m.label}</span>
                                </button>
                            `).join('')}
                        </div>
                    </div>

                    <div>
                        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">CATATAN HARIAN</label>
                        <input type="text" value="${rec.note || ''}" placeholder="Tuliskan catatan harian..." onchange="saveAttendanceNote(${student.id}, this.value)" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-700 font-medium">
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function sendWhatsApp(studentId) {
            const dateStr = selectedDateInput.value;
            const student = students.find(s => s.id === studentId);
            if (!student) return;

            const rec = attendanceData[dateStr]?.[student.id] || { status: 'H', mood: 'Kondusif', note: '' };
            const statusMap = { 'H': 'Hadir (H)', 'S': 'Sakit (S)', 'I': 'Izin (I)', 'A': 'Alfa (A)' };

            const fullFormattedDate = formatFullDateIndonesian(dateStr);
            const schoolUpper = (schoolConfig.schoolName || 'SLBN 1 KULON PROGO').toUpperCase();
            const className = schoolConfig.className || '[Nama Kelas / Mapel]';
            const teacherName = schoolConfig.teacherName || '[Nama Guru / Pengajar]';

            let formattedNote = rec.note && rec.note.trim() !== '' ? `_${rec.note.trim()}_` : '-';

            let msg = `Yth. Orang Tua/Wali dari ${student.name},\n*Laporan Presensi ${schoolUpper}*\n\n📅 Tanggal: ${fullFormattedDate}\n📌 Status Kehadiran: *${statusMap[rec.status] || 'Hadir (H)'}*\n`;
            if (rec.mood) msg += `🧠 Kondisi: ${rec.mood}\n`;
            msg += `📝 Catatan: ${formattedNote}\n\nPengajar ${className}:\n${teacherName}`;

            let phone = student.phone ? student.phone.replace(/[^0-9]/g, '') : '';
            if (phone.startsWith('0')) phone = '62' + phone.substring(1);

            window.open(phone ? `https://wa.me/${phone}?text=${encodeURIComponent(msg)}` : `https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
        }

        /* TOGGLE LOGIC: 1x KLIK AKTIF, 2x KLIK BATAL (STATUS) */
        function saveAttendance(studentId, status) {
            const date = selectedDateInput.value;
            if (!attendanceData[date]) attendanceData[date] = {};
            if (!attendanceData[date][studentId]) attendanceData[date][studentId] = { status: '', mood: 'Kondusif', note: '' };
            
            if (attendanceData[date][studentId].status === status) {
                attendanceData[date][studentId].status = '';
                showToast("Status dibatalkan");
            } else {
                attendanceData[date][studentId].status = status;
                showToast("Presensi tersimpan!");
            }

            syncToFirebase('attendance', attendanceData);
            renderDailyCards();
        }

        /* TOGGLE LOGIC: 1x KLIK AKTIF, 2x KLIK BATAL (MOOD) */
        function saveAttendanceMood(studentId, mood) {
            const date = selectedDateInput.value;
            if (!attendanceData[date]) attendanceData[date] = {};
            if (!attendanceData[date][studentId]) attendanceData[date][studentId] = { status: 'H', mood: 'Kondusif', note: '' };
            
            if (attendanceData[date][studentId].mood === mood) {
                attendanceData[date][studentId].mood = '';
                showToast("Kondisi dibatalkan");
            } else {
                attendanceData[date][studentId].mood = mood;
                showToast("Kondisi tersimpan!");
            }

            syncToFirebase('attendance', attendanceData);
            renderDailyCards();
        }

        function saveAttendanceNote(studentId, note) {
            const date = selectedDateInput.value;
            if (!attendanceData[date]) attendanceData[date] = {};
            if (!attendanceData[date][studentId]) attendanceData[date][studentId] = { status: 'H', mood: 'Kondusif', note: '' };
            attendanceData[date][studentId].note = note;
            syncToFirebase('attendance', attendanceData);
            showToast("Catatan tersimpan!");
        }

        function saveSchoolConfigToStorage() {
            schoolConfig.schoolName = document.getElementById('cfgSchoolName').value;
            schoolConfig.className = document.getElementById('cfgClassName').value;
            schoolConfig.teacherName = document.getElementById('cfgTeacherName').value;
            schoolConfig.teacherNip = document.getElementById('cfgTeacherNip').value;
            schoolConfig.headmasterName = document.getElementById('cfgHeadmasterName').value;
            schoolConfig.headmasterNip = document.getElementById('cfgHeadmasterNip').value;

            syncToFirebase('config', schoolConfig);
            applyConfigToDOM();
            showToast("Pengaturan tersimpan!");
        }

        function renderStudentsEdit() {
            const container = document.getElementById('studentsEditContainer');
            container.innerHTML = '';

            if (students.length === 0) {
                container.innerHTML = `<div class="text-center py-6 border border-dashed rounded-xl text-xs text-slate-400">Belum ada siswa yang ditambahkan. Klik tombol "+ Tambah Siswa" di atas atau tarik data dari Wali Kelas.</div>`;
                return;
            }

            students.forEach((s, idx) => {
                const card = document.createElement('div');
                card.className = 'bg-slate-50 border border-slate-200 rounded-2xl p-3 sm:p-4 space-y-2';
                card.innerHTML = `
                    <div class="grid grid-cols-1 sm:grid-cols-12 gap-3 items-center">
                        <div class="sm:col-span-4">
                            <label class="block text-[10px] font-bold text-slate-500 mb-1">Nama Siswa #${idx + 1}</label>
                            <input type="text" value="${s.name}" id="st-name-${s.id}" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold bg-white text-slate-800" placeholder="Nama Siswa">
                        </div>
                        <div class="sm:col-span-2">
                            <label class="block text-[10px] font-bold text-slate-500 mb-1">NIS / NIPD</label>
                            <input type="text" value="${s.nis \vert{}\vert{} ''}" id="st-nis-${s.id}" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold bg-white text-slate-800" placeholder="001">
                        </div>
                        <div class="sm:col-span-3">
                            <label class="block text-[10px] font-bold text-amber-800 mb-1">Kelompok / Mapel</label>
                            <input type="text" value="${s.group \vert{}\vert{} 'Umum'}" id="st-group-${s.id}" class="w-full border border-amber-300 rounded-xl px-3 py-2 text-xs font-bold bg-amber-50 text-amber-900" placeholder="cth: Tata Boga / Pertanian">
                        </div>
                        <div class="sm:col-span-2">
                            <label class="block text-[10px] font-bold text-slate-500 mb-1">No. WA Wali</label>
                            <input type="text" value="${s.phone \vert{}\vert{} ''}" id="st-phone-${s.id}" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold bg-white text-slate-800" placeholder="628123456789">
                        </div>
                        <div class="sm:col-span-1 flex items-end justify-end pt-3 sm:pt-0">
                            <button onclick="removeStudent(${s.id})" title="Hapus Siswa" class="w-full sm:w-10 h-10 bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-200 rounded-xl flex items-center justify-center transition">
                                <i class="fa-solid fa-trash-can text-sm"></i>
                            </button>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function addNewStudent() {
            const newId = students.length > 0 ? Math.max(...students.map(s => s.id)) + 1 : 1;
            students.push({ id: newId, name: ``, nis: '', group: 'Umum', phone: '' });
            renderStudentsEdit();
            updateGroupDropdowns();
            populateStudentFilter();
        }

        function removeStudent(studentId) {
            if (confirm("Apakah Anda yakin ingin menghapus siswa ini?")) {
                students = students.filter(s => s.id !== studentId);
                renderStudentsEdit();
                updateGroupDropdowns();
                populateStudentFilter();
            }
        }

        function saveStudentSettingsToStorage() {
            students.forEach(s => {
                const elN = document.getElementById(`st-name-${s.id}`);
                const elNi = document.getElementById(`st-nis-${s.id}`);
                const elGr = document.getElementById(`st-group-${s.id}`);
                const elPh = document.getElementById(`st-phone-${s.id}`);
                if (elN) s.name = elN.value;
                if (elNi) s.nis = elNi.value;
                if (elGr) s.group = elGr.value || 'Umum';
                if (elPh) s.phone = elPh.value;
            });
            syncToFirebase('students', students);
            updateGroupDropdowns();
            renderDailyCards();
            populateStudentFilter();
            showToast("Daftar siswa & kelompok tersimpan!");
        }

        function renderMonthlyTable() {
            const monthStr = selectedMonthInput.value;
            if (!monthStr) return;
            const [year, month] = monthStr.split('-').map(Number);
            const daysInMonth = new Date(year, month, 0).getDate();
            const groupFilter = document.getElementById('monthlyGroupFilter').value;

            let totH = 0, totS = 0, totI = 0, totA = 0;

            const daysHeaderRow = document.getElementById('daysHeaderRow');
            let headerHTML = `<th class="p-1.5 border text-center">NO</th><th class="p-1.5 border text-center">NIS</th><th class="p-1.5 border">NAMA SISWA</th><th class="p-1.5 border text-center">MAPEL/KELOMPOK</th>`;
            for (let d = 1; d <= daysInMonth; d++) headerHTML += `<th class="p-0.5 border text-center w-6 text-[10px]">${d}</th>`;
            headerHTML += `<th class="p-1 border text-center bg-emerald-100 text-emerald-800">H</th><th class="p-1 border text-center bg-amber-100 text-amber-800">S</th><th class="p-1 border text-center bg-sky-100 text-sky-800">I</th><th class="p-1 border text-center bg-rose-100 text-rose-800">A</th><th class="p-1 border text-center">%</th>`;
            daysHeaderRow.innerHTML = headerHTML;

            const monthlyTableBody = document.getElementById('monthlyTableBody');
            monthlyTableBody.innerHTML = '';

            let filteredStudents = students;
            if (groupFilter !== 'ALL') filteredStudents = filteredStudents.filter(s => (s.group || 'Umum') === groupFilter);

            filteredStudents.forEach((student, index) => {
                const nisStr = String(student.nis || student.id).padStart(3, '0');
                let hCount = 0, sCount = 0, iCount = 0, aCount = 0;

                let rowHTML = `<tr>
                    <td class="p-1.5 border text-center font-bold">${index + 1}</td>
                    <td class="p-1.5 border text-center font-bold text-slate-500">${nisStr}</td>
                    <td class="p-1.5 border font-bold text-slate-800">${student.name}</td>
                    <td class="p-1.5 border text-center font-bold text-amber-800 bg-amber-50">${student.group || 'Umum'}</td>`;
                
                for (let d = 1; d <= daysInMonth; d++) {
                    const fullDate = `${monthStr}-${String(d).padStart(2, '0')}`;
                    const st = attendanceData[fullDate]?.[student.id]?.status || '-';
                    let bgClass = 'text-slate-300';

                    if (st === 'H') { bgClass = 'bg-emerald-50 text-emerald-700 font-black'; hCount++; }
                    else if (st === 'S') { bgClass = 'bg-amber-100 text-amber-800 font-black'; sCount++; }
                    else if (st === 'I') { bgClass = 'bg-sky-100 text-sky-800 font-black'; iCount++; }
                    else if (st === 'A') { bgClass = 'bg-rose-100 text-rose-800 font-black'; aCount++; }

                    rowHTML += `<td class="p-0.5 border text-center ${bgClass}">${st}</td>`;
                }

                totH += hCount; totS += sCount; totI += iCount; totA += aCount;
                const totalActive = hCount + sCount + iCount + aCount;
                const pct = totalActive > 0 ? Math.round((hCount / totalActive) * 100) : 0;

                rowHTML += `<td class="p-1 border text-center font-black text-emerald-700 bg-emerald-50/50">${hCount}</td><td class="p-1 border text-center font-black text-amber-700 bg-amber-50/50">${sCount}</td><td class="p-1 border text-center font-black text-sky-700 bg-sky-50/50">${iCount}</td><td class="p-1 border text-center font-black text-rose-700 bg-rose-50/50">${aCount}</td><td class="p-1 border text-center font-black text-slate-800">${pct}%</td></tr>`;

                monthlyTableBody.innerHTML += rowHTML;
            });

            document.getElementById('statHadir').textContent = totH;
            document.getElementById('statSakit').textContent = totS;
            document.getElementById('statIzin').textContent = totI;
            document.getElementById('statAlfa').textContent = totA;
        }

        function populateStudentFilter() {
            const sel = document.getElementById('sensoryStudentFilter');
            sel.innerHTML = `<option value="ALL">-- Semua Siswa --</option>`;
            students.forEach(s => {
                sel.innerHTML += `<option value="${s.id}">${s.name || ('Siswa ID ' + s.id)} (${s.group || 'Umum'})</option>`;
            });
        }

        /* PERBAIKAN FUNGSI MENCARI & MENAMPILKAN RIWAYAT JURNAL HARIAN BULANAN */
        function renderSensoryJournal() {
            const listContainer = document.getElementById('monthlyNotesList');
            const monthStr = selectedMonthInput.value;
            const filterId = document.getElementById('sensoryStudentFilter').value;
            listContainer.innerHTML = '';
            let hasEntries = false;

            if (!monthStr) {
                listContainer.innerHTML = `<p class="text-xs text-slate-400 italic text-center py-6">Silakan pilih bulan dan tahun terlebih dahulu.</p>`;
                return;
            }

            const sortedDates = Object.keys(attendanceData).sort().reverse();

            sortedDates.forEach(date => {
                if (date && date.startsWith(monthStr)) {
                    const dayRecords = attendanceData[date];
                    if (!dayRecords) return;

                    students.forEach(student => {
                        if (filterId !== 'ALL' && String(student.id) !== filterId) return;

                        const rec = dayRecords[student.id];
                        if (rec && ((rec.note && rec.note.trim() !== '') || (rec.mood && rec.mood.trim() !== ''))) {
                            hasEntries = true;
                            const divCard = document.createElement('div');
                            divCard.className = 'bg-white rounded-2xl p-4 border border-slate-200 text-xs space-y-2 shadow-sm';
                            divCard.innerHTML = `
                                <div class="flex justify-between items-center border-b pb-2">
                                    <div>
                                        <span class="text-slate-900 font-extrabold text-sm sm:text-base">${student.name}</span>
                                        <span class="ml-2 px-2 py-0.5 bg-amber-100 text-amber-800 rounded text-[10px] font-bold">${student.group || 'Umum'}</span>
                                    </div>
                                    <span class="text-slate-500 font-semibold text-xs">${formatFullDateIndonesian(date)}</span>
                                    ${rec.mood ? `<span class="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full font-bold text-[11px]">${rec.mood}</span>` : ''}
                                </div>
                                ${rec.note && rec.note.trim() !== '' ? `<p class="text-slate-700 leading-relaxed font-medium pt-1">${rec.note}</p>` : '<p class="text-slate-400 italic pt-1">Tidak ada catatan tertulis.</p>'}
                            `;
                            listContainer.appendChild(divCard);
                        }
                    });
                }
            });

            if (!hasEntries) {
                listContainer.innerHTML = `<p class="text-xs text-slate-400 italic text-center py-6">Belum ada catatan jurnal pada periode bulan ${formatMonthYearIndonesian(monthStr)}.</p>`;
            }
        }

        function setupPrintData(type) {
            const teacherName = schoolConfig.teacherName || '[Nama Pengguna]';
            const teacherNip = schoolConfig.teacherNip ? `NIP. ${schoolConfig.teacherNip}` : '';
            const hmName = schoolConfig.headmasterName || '[Nama Kepala Sekolah]';
            const hmNip = schoolConfig.headmasterNip ? `NIP. ${schoolConfig.headmasterNip}` : '';

            const classNameUpper = (schoolConfig.className || '[NAMA KELAS]').toUpperCase();
            const schoolNameUpper = (schoolConfig.schoolName || 'SLBN 1 KULON PROGO').toUpperCase();
            const formattedMonthText = formatMonthYearIndonesian(selectedMonthInput.value);

            const roleLabels = { 'GURU_KELAS': 'Guru Kelas', 'GURU_MAPEL': 'Guru Mata Pelajaran', 'KEPALA_SEKOLAH': 'Kepala Sekolah' };

            if (type === 'monthly') {
                const printDateStr = printDateMonthlyInput.value || localISODate();
                const formattedPrintDate = formatPrintDateIndonesian(printDateStr);
                const groupFilter = document.getElementById('monthlyGroupFilter').value;
                
                let titleText = `REKAPITULASI PRESENSI - ${classNameUpper}`;
                if (groupFilter !== 'ALL') titleText += ` (${groupFilter.toUpperCase()})`;

                document.getElementById('printMonthlyTitle').textContent = titleText;
                document.getElementById('printMonthlySchool').textContent = schoolNameUpper;
                document.getElementById('printMonthPeriod').textContent = formattedMonthText;
                document.getElementById('printMonthlyHeadmasterLabel').textContent = `Kepala ${schoolNameUpper}`;
                document.getElementById('printMonthlyTeacherLabel').textContent = roleLabels[currentUserRole] || 'Guru Kelas / Mapel';

                document.getElementById('printTeacherName').textContent = teacherName;
                document.getElementById('printTeacherNip').textContent = teacherNip;
                document.getElementById('printHeadmasterName').textContent = hmName;
                document.getElementById('printHeadmasterNip').textContent = hmNip;
                document.getElementById('printDateToday').textContent = formattedPrintDate;
            } else if (type === 'sensory') {
                const printDateStr = printDateSensoryInput.value || localISODate();
                const formattedPrintDate = formatPrintDateIndonesian(printDateStr);

                const filterId = document.getElementById('sensoryStudentFilter').value;
                let sensoryTitleText = `LAPORAN JURNAL PERKEMBANGAN SISWA - ${classNameUpper}`;
                
                if (filterId !== 'ALL') {
                    const targetStudent = students.find(s => String(s.id) === filterId);
                    if (targetStudent) sensoryTitleText = `LAPORAN JURNAL PERKEMBANGAN (${targetStudent.name.toUpperCase()}) - ${classNameUpper}`;
                }

                document.getElementById('printSensoryTitle').textContent = sensoryTitleText;
                document.getElementById('printSensorySchool').textContent = schoolNameUpper;
                document.getElementById('printSensoryMonth').textContent = formattedMonthText;
                document.getElementById('printSensoryHeadmasterLabel').textContent = `Kepala ${schoolNameUpper}`;
                document.getElementById('printSensoryTeacherLabel').textContent = roleLabels[currentUserRole] || 'Guru Kelas / Mapel';

                document.getElementById('printSensoryTRName').textContent = teacherName;
                document.getElementById('printSensoryTRNip').textContent = teacherNip;
                document.getElementById('printSensoryHMName').textContent = hmName;
                document.getElementById('printSensoryHMNip').textContent = hmNip;
                document.getElementById('printSensoryDateToday').textContent = formattedPrintDate;
            }
        }

        function printMonthlyReport() {
            switchTab('monthly');
            setupPrintData('monthly');
            setTimeout(() => { window.print(); }, 100);
        }

        function printSensoryReport() {
            switchTab('sensory');
            setupPrintData('sensory');
            setTimeout(() => { window.print(); }, 100);
        }

        function exportCSV() {
            let csv = "No,NIS,Nama Siswa,Kelompok/Mapel,Hadir,Sakit,Izin,Alfa,Persentase\n";
            students.forEach((s, idx) => {
                const nisStr = String(s.nis || s.id).padStart(3, '0');
                csv += `"${idx+1}","${nisStr}","${s.name}","${s.group || 'Umum'}",0,0,0,0,"0%"\n`;
            });
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.setAttribute('href', url);
            a.setAttribute('download', `Rekap_Presensi_${selectedMonthInput.value}.csv`);
            a.click();
        }

        function showToast(msg) {
            const t = document.getElementById('toast');
            document.getElementById('toastMsg').textContent = msg;
            t.classList.remove('opacity-0');
            setTimeout(() => t.classList.add('opacity-0'), 2000);
        }
    </script>
</body>
</html>
