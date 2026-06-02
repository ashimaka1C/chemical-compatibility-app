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

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

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

def main_app():
    """Aplikasi utama setelah login"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as: **{st.session_state.username}**")
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
    tab1, tab2, tab3 = st.tabs(["🔍 Cek Kompatibilitas", "📊 Tabel Kompatibilitas", "📖 Panduan"])
    
    with tab1:
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
                
                # Tampilkan hasil
                st.divider()
                st.subheader("📋 Hasil Pemeriksaan")
                
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
                
                # Penjelasan
                if compatibility_status == "✅":
                    st.success(f"""
                    ✅ **KOMPATIBEL**
                    
                    {chemical_1} dan {chemical_2} aman untuk dicampur atau disimpan berdekatan.
                    """)
                elif compatibility_status == "⚠️":
                    st.warning(f"""
                    ⚠️ **HATI-HATI - KOMPATIBEL DENGAN TINDAKAN PENCEGAHAN**
                    
                    {chemical_1} dan {chemical_2} dapat dicampur tetapi memerlukan:
                    - Ventilasi yang baik
                    - Perlindungan pribadi (APD)
                    - Kontrol suhu
                    - Tidak boleh disimpan berdekatan dalam jangka panjang
                    """)
                else:
                    st.error(f"""
                    ❌ **TIDAK KOMPATIBEL - SANGAT BERBAHAYA!**
                    
                    JANGAN CAMPUR {chemical_1.upper()} DENGAN {chemical_2.upper()}!
                    
                    Risiko:
                    - Reaksi eksotermik (panas tinggi)
                    - Ledakan atau penyalaan
                    - Gas beracun
                    - Kerusakan peralatan
                    
                    Tindakan:
                    - Pisahkan sepenuhnya
                    - Simpan di lokasi berbeda
                    - Konsultasikan dengan ahli keselamatan
                    """)
                
                # Log aktivitas
                st.divider()
                st.caption(f"✓ Pemeriksaan dilakukan pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} oleh {st.session_state.username}")
    
    with tab2:
        st.subheader("📊 Matriks Kompatibilitas Lengkap")
        
        st.markdown("""
        **Keterangan:**
        - ✅ = Kompatibel (Aman)
        - ⚠️ = Hati-hati (Kompatibel dengan tindakan khusus)
        - ❌ = Tidak Kompatibel (Sangat Berbahaya)
        """)
        
        # Tampilkan tabel
        st.dataframe(df, use_container_width=True)
        
        # Download data
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="kompatibilitas_bahan_kimia.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.subheader("📖 Panduan Penggunaan")
        
        st.markdown("""
        ### Cara Menggunakan Aplikasi
        
        1. **Pilih Bahan Kimia**
           - Pilih dua bahan kimia berbeda dari dropdown menu
           - Klik tombol "Cek Kompatibilitas"
        
        2. **Interpretasi Hasil**
           - **✅ Kompatibel**: Aman untuk dicampur
           - **⚠️ Hati-hati**: Butuh tindakan pencegahan
           - **❌ Tidak Kompatibel**: Sangat berbahaya, jangan dicampur
        
        3. **Lihat Tabel Lengkap**
           - Gunakan tab "Tabel Kompatibilitas" untuk melihat semua data
           - Download CSV untuk dokumentasi
        
        ### Panduan Keselamatan Umum
        
        - Selalu baca label bahan kimia sebelum menggunakannya
        - Gunakan APD (Alat Pelindung Diri) yang sesuai
        - Bekerja di area berventilasi baik
        - Ikuti prosedur SOP (Standard Operating Procedure) laboratorium
        - Konsultasikan dengan ahli keselamatan jika ragu
        
        ### Bahan Kimia Dalam Sistem
        - {total_chemicals} jenis bahan kimia
        - Matriks kompatibilitas lengkap
        - Data diperbarui berkala
        """.format(total_chemicals=len(df["Bahan Kimia"])))
        
        st.divider()
        
        st.subheader("🔍 Status Kompatibilitas - Penjelasan Detail")
        
        for status, explanation in status_explanation.items():
            st.write(f"**{status} {explanation}**")

# Jalankan aplikasi
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
