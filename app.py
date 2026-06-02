import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Audit Kompatibilitas Bahan Kimia", layout="wide")

# Data pengguna (dalam praktik, gunakan database)
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user1": hashlib.sha256("password123".encode()).hexdigest(),
    "lab_technician": hashlib.sha256("tech456".encode()).hexdigest()
}

# Data kompatibilitas bahan kimia yang diperluas
compatibility_data = {
    "Bahan Kimia": [
        "Asam Klorida (HCl)",
        "Asam Sulfat (H2SO4)",
        "Asam Nitrat (HNO3)",
        "Natrium Hidroksida (NaOH)",
        "Kalium Hidroksida (KOH)",
        "Amonium Nitrat (NH4NO3)",
        "Aseton",
        "Etanol",
        "Metanol",
        "Bensin",
        "Hidrogen Peroksida (H2O2)",
        "Klor (Cl2)",
        "Ammonia (NH3)",
        "Formalin",
        "Permanganat Kalium (KMnO4)"
    ],
    "Asam Klorida (HCl)": ["✅", "⚠️", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "⚠️"],
    "Asam Sulfat (H2SO4)": ["⚠️", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "⚠️"],
    "Asam Nitrat (HNO3)": ["⚠️", "⚠️", "✅", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "❌", "⚠️", "❌"],
    "Natrium Hidroksida (NaOH)": ["❌", "❌", "❌", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "⚠️", "❌"],
    "Kalium Hidroksida (KOH)": ["❌", "❌", "❌", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "⚠️", "❌"],
    "Amonium Nitrat (NH4NO3)": ["⚠️", "⚠️", "❌", "⚠️", "⚠️", "✅", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️"],
    "Aseton": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️"],
    "Etanol": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "⚠️", "⚠️"],
    "Metanol": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "⚠️", "✅", "⚠️", "⚠️"],
    "Bensin": ["⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️"],
    "Hidrogen Peroksida (H2O2)": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "❌", "⚠️", "❌", "❌"],
    "Klor (Cl2)": ["❌", "❌", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "❌", "❌", "❌"],
    "Ammonia (NH3)": ["❌", "❌", "❌", "✅", "✅", "❌", "⚠️", "✅", "✅", "⚠️", "⚠️", "❌", "✅", "⚠️", "⚠️"],
    "Formalin": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "✅", "⚠️"],
    "Permanganat Kalium (KMnO4)": ["⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "⚠️", "✅"]
}

# Data saran penyimpanan untuk setiap bahan kimia
storage_recommendations = {
    "Asam Klorida (HCl)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi",
        "wadah": "Botol kaca dengan tutup plastik tahan asam",
        "lokasi": "Kabinet asam terpisah, jauh dari basa",
        "catatan": "Dapat mengeluarkan gas berbahaya, simpan di area terbatas, jauh dari logam"
    },
    "Asam Sulfat (H2SO4)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap, berventilasi baik",
        "wadah": "Botol kaca tebal dengan tutup plastik",
        "lokasi": "Kabinet asam terpisah, di lantai atau rak rendah",
        "catatan": "Sangat korosif, dapat menyebabkan luka bakar parah, simpan terpisah dari semua basa"
    },
    "Asam Nitrat (HNO3)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi",
        "wadah": "Botol kaca berwarna coklat/amber",
        "lokasi": "Kabinet asam khusus, jauh dari basa dan zat organik",
        "catatan": "Pengoksidasi kuat, dapat menyebabkan kebakaran, jangan dicampur dengan organik"
    },
    "Natrium Hidroksida (NaOH)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap, berventilasi",
        "wadah": "Botol kaca dengan tutup plastik/tutup berulir",
        "lokasi": "Kabinet basa terpisah, jauh dari asam",
        "catatan": "Bersifat kaustik, dapat menyebabkan luka bakar kimiawi, jangan dicampur dengan asam"
    },
    "Kalium Hidroksida (KOH)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca dengan tutup plastik",
        "lokasi": "Kabinet basa, jauh dari asam dan zat lain",
        "catatan": "Kaustik dan higroskopis, dapat menyerap kelembaban, jauhkan dari asam"
    },
    "Amonium Nitrat (NH4NO3)": {
        "level_bahaya": "🟠 BERBAHAYA (Pengoksidasi)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap, berventilasi",
        "wadah": "Wadah plastik atau kaca dengan tutup aman",
        "lokasi": "Area terpisah, jauh dari bahan mudah terbakar",
        "catatan": "Pengoksidasi, dapat meningkatkan risiko kebakaran, jauhkan dari materi organik"
    },
    "Aseton": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, jauh dari api",
        "wadah": "Botol kaca atau plastik tahan aseton dengan tutup aman",
        "lokasi": "Kabinet flammable khusus, area ventilasi baik",
        "catatan": "Sangat mudah terbakar, volatile, jauh dari sumber api dan panas"
    },
    "Etanol": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, area terbuka",
        "wadah": "Botol kaca atau plastik dengan tutup aman",
        "lokasi": "Kabinet flammable, jauh dari sumber api",
        "catatan": "Mudah terbakar, volatile, simpan di area yang aman dari api dan panas"
    },
    "Metanol": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar, Beracun)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, jauh dari panas",
        "wadah": "Botol kaca dengan tutup aman",
        "lokasi": "Kabinet flammable khusus, area ventilasi maksimal",
        "catatan": "Beracun dan mudah terbakar, hindari inhalasi dan kontak kulit, simpan aman"
    },
    "Bensin": {
        "level_bahaya": "🟡 BERBAHAYA (Sangat Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelak, berventilasi maksimal, jauh dari api",
        "wadah": "Wadah metal atau plastik tahan bensin dengan tutup aman",
        "lokasi": "Kabinet flammable metal, area ventilasi eksternal",
        "catatan": "Sangat volatile dan mudah terbakar, simpan di area khusus dengan sistem keselamatan"
    },
    "Hidrogen Peroksida (H2O2)": {
        "level_bahaya": "🟠 BERBAHAYA (Pengoksidasi)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi, jauh dari sinar matahari",
        "wadah": "Botol kaca berwarna gelap atau plastik khusus",
        "lokasi": "Rak terpisah, jauh dari bahan organik dan reduktor",
        "catatan": "Pengoksidasi, dapat meningkatkan risiko kebakaran, hindari kontaminasi"
    },
    "Klor (Cl2)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA (Gas Beracun)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi ekstensif, sistem keselamatan",
        "wadah": "Silinder gas khusus dengan regulator",
        "lokasi": "Area penyimpanan khusus dengan sistem ventilasi dan evakuasi gas",
        "catatan": "Gas beracun, menyebabkan kerusakan paru, hanya staf terlatih yang boleh menangani"
    },
    "Ammonia (NH3)": {
        "level_bahaya": "🟠 BERBAHAYA (Gas Beracun)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, berventilasi baik, jauh dari asam",
        "wadah": "Botol atau silinder khusus tahan ammonia",
        "lokasi": "Area berventilasi baik, jauh dari asam dan oksidator",
        "catatan": "Gas pungent dan beracun, dapat menyebabkan iritasi, simpan di area terbuka"
    },
    "Formalin": {
        "level_bahaya": "🟠 BERBAHAYA (Beracun, Karsinogen)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, area terbatas",
        "wadah": "Botol kaca atau plastik dengan tutup hermetik",
        "lokasi": "Area ventilasi baik, di kabinet khusus, jauh dari logam",
        "catatan": "Karsinogen potensial, inhalasi dapat menyebabkan penyakit, gunakan dalam fume hood"
    },
    "Permanganat Kalium (KMnO4)": {
        "level_bahaya": "🟠 BERBAHAYA (Pengoksidasi Kuat)",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap, berventilasi",
        "wadah": "Botol kaca atau wadah plastik dengan tutup aman",
        "lokasi": "Rak terpisah, jauh dari bahan organik dan reduktor",
        "catatan": "Pengoksidasi kuat, dapat menyebabkan kebakaran dengan bahan organik"
    }
}

# Penjelasan status kompatibilitas
status_explanation = {
    "✅": "Kompatibel - Aman digunakan bersama",
    "⚠️": "Hati-hati - Kompatibel dengan tindakan pencegahan khusus",
    "❌": "Tidak Kompatibel - Jangan campur, risiko reaksi berbahaya"
}

# Inisialisasi session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.last_check = None

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_admin():
    """Cek apakah user adalah admin"""
    return st.session_state.username == "admin"

def login_page():
    """Halaman login"""
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 30px;
            border-radius: 10px;
            background-color: #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center'>🔐 Login</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center'>Sistem Audit Kompatibilitas Bahan Kimia</h3>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info("📝 Gunakan akun untuk login ke sistem")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔓 Login", use_container_width=True):
                    if username in USERS:
                        if hash_password(password) == USERS[username]:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.login_time = datetime.now()
                            st.success(f"Selamat datang, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Password salah!")
                    else:
                        st.error("❌ Username tidak ditemukan!")
            
            with col_btn2:
                if st.button("ℹ️ Demo", use_container_width=True):
                    st.info("""
                    **Akun Demo:**
                    - Username: `admin`
                    - Password: `admin123`
                    
                    Atau
                    - Username: `user1`
                    - Password: `password123`
                    """)

def display_storage_recommendation(chemical):
    """Menampilkan rekomendasi penyimpanan untuk bahan kimia"""
    if chemical in storage_recommendations:
        rec = storage_recommendations[chemical]
        
        st.markdown("---")
        st.subheader(f"📦 Rekomendasi Penyimpanan: {chemical}")
        
        # Buat kolom untuk menampilkan informasi
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Tingkat Bahaya:** {rec['level_bahaya']}")
            st.markdown(f"**Suhu Penyimpanan:** {rec['suhu']}")
            st.markdown(f"**Kondisi:** {rec['kondisi']}")
        
        with col2:
            st.markdown(f"**Wadah:** {rec['wadah']}")
            st.markdown(f"**Lokasi Penyimpanan:** {rec['lokasi']}")
        
        st.markdown(f"**⚠️ Catatan Penting:** {rec['catatan']}")

def main_app():
    """Aplikasi utama setelah login"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as: **{st.session_state.username}**")
        if is_admin():
            st.markdown("🔑 **Status: ADMIN**")
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.divider()
        st.markdown("**Informasi Sistem:**")
        st.write(f"Login time: {st.session_state.login_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Judul aplikasi
    st.title("🧪 Aplikasi Audit Kompatibilitas Bahan Kimia")
    st.markdown("Periksa kompatibilitas antara dua bahan kimia sebelum mencampurnya")
    
    # Mengubah data menjadi DataFrame
    df = pd.DataFrame(compatibility_data)
    
    # Tabs
    if is_admin():
        tabs = st.tabs(["🔍 Cek Kompatibilitas", "📊 Tabel Kompatibilitas (Admin)", "📖 Panduan"])
    else:
        tabs = st.tabs(["🔍 Cek Kompatibilitas", "📖 Panduan"])
    
    with tabs[0]:
        st.subheader("Periksa Kompatibilitas Dua Bahan Kimia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chemical_1 = st.selectbox(
                "Pilih Bahan Kimia Pertama:",
                df["Bahan Kimia"],
                key="chem_1"
            )
        
        with col2:
            chemical_2 = st.selectbox(
                "Pilih Bahan Kimia Kedua:",
                df["Bahan Kimia"],
                key="chem_2"
            )
        
        if st.button("✅ Cek Kompatibilitas", use_container_width=True):
            if chemical_1 == chemical_2:
                st.warning("⚠️ Silakan pilih dua bahan kimia yang berbeda!")
            else:
                # Mencari indeks bahan kimia
                index_1 = df[df["Bahan Kimia"] == chemical_1].index[0]
                index_2 = df[df["Bahan Kimia"] == chemical_2].index[0]
                
                # Menampilkan status kompatibilitas
                compatibility_status = df.iloc[index_1, index_2 + 1]
                
                # Simpan hasil pemeriksaan terakhir
                st.session_state.last_check = {
                    "chemical_1": chemical_1,
                    "chemical_2": chemical_2,
                    "status": compatibility_status,
                    "timestamp": datetime.now()
                }
                
                # Tampilkan hasil
                st.divider()
                st.subheader("📋 Hasil Pemeriksaan Kompatibilitas")
                
                col_result1, col_result2, col_result3 = st.columns(3)
                
                with col_result1:
                    st.metric("Bahan 1", chemical_1)
                
                with col_result2:
                    if compatibility_status == "✅":
                        st.metric("Status", compatibility_status, delta="Aman")
                    elif compatibility_status == "⚠️":
                        st.metric("Status", compatibility_status, delta="Hati-hati")
                    else:
                        st.metric("Status", compatibility_status, delta="Berbahaya")
                
                with col_result3:
                    st.metric("Bahan 2", chemical_2)
                
                st.divider()
                
                # Penjelasan kompatibilitas
                if compatibility_status == "✅":
                    st.success(f"""
                    ✅ **KOMPATIBEL**
                    
                    {chemical_1} dan {chemical_2} aman untuk dicampur atau disimpan berdekatan.
                    Tidak ada reaksi berbahaya yang terjadi.
                    """)
                elif compatibility_status == "⚠️":
                    st.warning(f"""
                    ⚠️ **HATI-HATI - KOMPATIBEL DENGAN TINDAKAN PENCEGAHAN**
                    
                    {chemical_1} dan {chemical_2} dapat dicampur tetapi memerlukan:
                    - Ventilasi yang baik
                    - Perlindungan pribadi (APD) - sarung tangan, kacamata keselamatan
                    - Kontrol suhu
                    - Tidak boleh disimpan berdekatan dalam jangka panjang
                    - Lakukan di area yang aman atau fume hood
                    """)
                else:
                    st.error(f"""
                    ❌ **TIDAK KOMPATIBEL - SANGAT BERBAHAYA!**
                    
                    🚫 JANGAN CAMPUR {chemical_1.upper()} DENGAN {chemical_2.upper()}! 🚫
                    
                    Risiko Potensial:
                    - Reaksi eksotermik (panas tinggi)
                    - Ledakan atau penyalaan
                    - Gas beracun atau berbahaya
                    - Kerusakan peralatan dan lingkungan
                    
                    Tindakan yang Harus Dilakukan:
                    - Pisahkan sepenuhnya di area berbeda
                    - Simpan di lokasi berbeda dengan sistem keamanan terpisah
                    - Konsultasikan dengan ahli keselamatan sebelum melakukan apapun
                    - Jika sudah tercampur, segera hubungi personil keselamatan
                    """)
                
                # Tampilkan rekomendasi penyimpanan untuk kedua bahan
                st.divider()
                st.subheader("🔒 Panduan Penyimpanan Bahan Kimia")
                
                col_storage1, col_storage2 = st.columns(2)
                
                with col_storage1:
                    display_storage_recommendation(chemical_1)
                
                with col_storage2:
                    display_storage_recommendation(chemical_2)
                
                # Log aktivitas
                st.divider()
                st.caption(f"✓ Pemeriksaan dilakukan pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} oleh {st.session_state.username}")
    
    # Tab Tabel Kompatibilitas (Hanya untuk Admin)
    if is_admin():
        with tabs[1]:
            st.subheader("📊 Matriks Kompatibilitas Lengkap (Akses Admin)")
            
            st.info("🔐 **Informasi Ini Hanya Dapat Diakses oleh Admin**")
            
            st.markdown("""
            **Keterangan:**
            - ✅ = Kompatibel (Aman)
            - ⚠️ = Hati-hati (Kompatibel dengan tindakan khusus)
            - ❌ = Tidak Kompatibel (Sangat Berbahaya)
            """)
            
            # Tampilkan tabel
            st.dataframe(df, use_container_width=True, height=500)
            
            # Download data
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="kompatibilitas_bahan_kimia.csv",
                mime="text/csv"
            )
            
            st.divider()
            st.subheader("📋 Ringkasan Statistik")
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            # Hitung statistik
            total_chemicals = len(df["Bahan Kimia"])
            
            with col_stat1:
                st.metric("Total Bahan Kimia", total_chemicals)
            
            with col_stat2:
                st.metric("Total Data Kompatibilitas", total_chemicals * (total_chemicals - 1) // 2)
            
            with col_stat3:
                st.metric("Jumlah Kolom Data", len(df.columns) - 1)
    else:
        # Tampilkan pesan untuk non-admin
        with tabs[1]:
            st.warning("🔐 Akses Terbatas")
            st.markdown("""
            **Maaf, tabel kompatibilitas lengkap hanya dapat diakses oleh pengguna Admin.**
            
            Anda dapat:
            - Melakukan pemeriksaan kompatibilitas dua bahan kimia di tab pertama
            - Membaca panduan penggunaan di tab terakhir
            
            Jika Anda memerlukan akses penuh, silakan hubungi administrator sistem.
            """)
    
    # Tab Panduan
    with tabs[-1]:
        st.subheader("📖 Panduan Penggunaan")
        
        st.markdown("""
        ### Cara Menggunakan Aplikasi
        
        1. **Pilih Bahan Kimia**
           - Pilih dua bahan kimia berbeda dari dropdown menu
           - Klik tombol "Cek Kompatibilitas"
        
        2. **Interpretasi Hasil**
           - **✅ Kompatibel**: Aman untuk dicampur atau disimpan berdekatan
           - **⚠️ Hati-hati**: Butuh tindakan pencegahan khusus sebelum dicampur
           - **❌ Tidak Kompatibel**: Sangat berbahaya, jangan dicampur dalam kondisi apapun
        
        3. **Lihat Rekomendasi Penyimpanan**
           - Setelah mengecek kompatibilitas, Anda akan melihat rekomendasi penyimpanan
           - Setiap bahan kimia memiliki panduan penyimpanan unik berdasarkan tingkat bahaya
        
        4. **Untuk Admin:**
           - Gunakan tab "Tabel Kompatibilitas" untuk melihat semua data lengkap
           - Download CSV untuk dokumentasi dan laporan
        
        ### Panduan Keselamatan Umum
        
        - **Selalu baca label bahan kimia** sebelum menggunakannya
        - **Gunakan APD (Alat Pelindung Diri)** yang sesuai - sarung tangan, kacamata, masker
        - **Bekerja di area berventilasi baik** atau menggunakan fume hood jika diperlukan
        - **Ikuti prosedur SOP** (Standard Operating Procedure) laboratorium
        - **Konsultasikan dengan ahli keselamatan** jika ragu tentang sesuatu
        - **Simpan bahan dengan benar** sesuai rekomendasi yang diberikan
        - **Jangan campur bahan tanpa pengetahuan** tentang kompatibilitasnya
        
        ### Bahan Kimia Dalam Sistem
        """)
        
        # Tampilkan daftar bahan
        st.info(f"📌 Total: {len(df['Bahan Kimia'])} jenis bahan kimia")
        
        # Buat kolom untuk daftar bahan
        col1, col2 = st.columns(2)
        
        chemicals = df["Bahan Kimia"].tolist()
        mid_point = len(chemicals) // 2
        
        with col1:
            st.markdown("**Daftar Bahan Kimia (Part 1):**")
            for i, chem in enumerate(chemicals[:mid_point], 1):
                st.write(f"{i}. {chem}")
        
        with col2:
            st.markdown("**Daftar Bahan Kimia (Part 2):**")
            for i, chem in enumerate(chemicals[mid_point:], mid_point + 1):
                st.write(f"{i}. {chem}")
        
        st.divider()
        
        st.subheader("🔍 Status Kompatibilitas - Penjelasan Detail")
        
        for status, explanation in status_explanation.items():
            st.write(f"**{status} {explanation}**")
        
        st.divider()
        
        st.subheader("⚠️ Tingkat Bahaya Bahan Kimia")
        
        st.markdown("""
        - **🔴 SANGAT BERBAHAYA**: Bahan yang sangat beracun, korosif, atau mudah meledak. Hanya staf terlatih yang boleh menangani.
        - **🟠 BERBAHAYA**: Bahan yang bersifat beracun, pengoksidasi, atau dapat menyebabkan kebakaran. Memerlukan tindakan keselamatan.
        - **🟡 BERBAHAYA (Mudah Terbakar)**: Bahan yang mudah terbakar atau volatile. Harus disimpan jauh dari api.
        """)

# Jalankan aplikasi
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
