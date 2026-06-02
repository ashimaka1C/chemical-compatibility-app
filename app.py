import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Audit Kompatibilitas Bahan Kimia",
    page_icon="🧪",
    layout="wide"
)

# Data pengguna (dalam praktik, gunakan database)
USERS = {
    "admin": "admin123",
    "user": "user123",
    "lab_tech": "tech456"
}

# Data kompatibilitas bahan kimia yang lebih lengkap
compatibility_data = {
    "Bahan Kimia": [
        "Asam Klorida (HCl)",
        "Asam Sulfat (H₂SO₄)",
        "Natrium Hidroksida (NaOH)",
        "Kalium Hidroksida (KOH)",
        "Amonium Nitrat (NH₄NO₃)",
        "Natrium Klorit (NaClO₂)",
        "Aseton",
        "Etanol",
        "Metanol",
        "Kalsium Hipoklorit",
        "Hidrogen Peroksida (H₂O₂)",
        "Asam Nitrat (HNO₃)",
        "Fenol",
        "Benzena",
        "Toluena"
    ],
    "Asam Klorida (HCl)": ["✅", "⚠️", "❌", "❌", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️"],
    "Asam Sulfat (H₂SO₄)": ["⚠️", "✅", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "❌", "⚠️", "⚠️"],
    "Natrium Hidroksida (NaOH)": ["❌", "❌", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "❌", "❌", "⚠️", "⚠️"],
    "Kalium Hidroksida (KOH)": ["❌", "❌", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "❌", "❌", "⚠️", "⚠️"],
    "Amonium Nitrat (NH₄NO₃)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️"],
    "Natrium Klorit (NaClO₂)": ["❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "❌", "❌"],
    "Aseton": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅"],
    "Etanol": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅"],
    "Metanol": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅"],
    "Kalsium Hipoklorit": ["❌", "❌", "❌", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "✅", "❌", "❌", "⚠️", "❌", "❌"],
    "Hidrogen Peroksida (H₂O₂)": ["❌", "❌", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "❌", "✅", "❌", "⚠️", "⚠️", "⚠️"],
    "Asam Nitrat (HNO₃)": ["❌", "⚠️", "❌", "❌", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "❌", "❌", "✅", "❌", "❌", "❌"],
    "Fenol": ["⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "⚠️", "⚠️"],
    "Benzena": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "✅", "✅", "❌", "⚠️", "❌", "⚠️", "✅", "✅"],
    "Toluena": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "✅", "✅", "❌", "⚠️", "❌", "⚠️", "✅", "✅"]
}

# Keterangan status
status_info = {
    "✅": {"label": "Kompatibel", "color": "green"},
    "⚠️": {"label": "Perhatian (Kompatibel dengan Hati-hati)", "color": "orange"},
    "❌": {"label": "Tidak Kompatibel", "color": "red"}
}

def hash_password(password):
    """Hash password untuk keamanan"""
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    """Fungsi untuk halaman login"""
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1>🧪 Sistem Audit Kompatibilitas Bahan Kimia</h1>
        <p style="font-size: 18px; color: gray;">Masuk untuk melanjutkan</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        
        if st.button("Login", use_container_width=True, type="primary"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.login_time = datetime.now()
                st.rerun()
            else:
                st.error("❌ Username atau password salah!")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 12px; color: gray;">
            <p><strong>Demo Credentials:</strong></p>
            <p>Username: <code>admin</code> | Password: <code>admin123</code></p>
            <p>Username: <code>user</code> | Password: <code>user123</code></p>
            <p>Username: <code>lab_tech</code> | Password: <code>tech456</code></p>
        </div>
        """, unsafe_allow_html=True)

def logout():
    """Fungsi untuk logout"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

def main_app():
    """Aplikasi utama setelah login"""
    # Header dengan info user dan logout
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"### 👋 Selamat datang, **{st.session_state.username}**!")
    with col3:
        if st.button("🚪 Logout"):
            logout()
    
    st.markdown("---")
    
    # Judul
    st.title("🧪 Aplikasi Audit Kompatibilitas Bahan Kimia")
    
    # Deskripsi
    st.markdown("""
    Aplikasi ini membantu Anda memeriksa kompatibilitas antara dua bahan kimia 
    untuk memastikan keamanan penyimpanan dan penanganan di laboratorium.
    
    **Legenda:**
    - ✅ **Kompatibel** - Dapat disimpan atau dicampur dengan aman
    - ⚠️ **Perhatian** - Kompatibel dengan hati-hati, ikuti prosedur khusus
    - ❌ **Tidak Kompatibel** - Jangan disimpan atau dicampur bersama
    """)
    
    st.markdown("---")
    
    # Membuat DataFrame
    df = pd.DataFrame(compatibility_data)
    
    # Tab untuk berbagai fungsi
    tab1, tab2, tab3 = st.tabs(["Cek Kompatibilitas", "Tabel Lengkap", "Panduan Keselamatan"])
    
    with tab1:
        st.subheader("Periksa Kompatibilitas Dua Bahan Kimia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chemical_1 = st.selectbox(
                "Pilih Bahan Kimia Pertama:",
                df["Bahan Kimia"],
                key="chemical_1"
            )
        
        with col2:
            chemical_2 = st.selectbox(
                "Pilih Bahan Kimia Kedua:",
                df["Bahan Kimia"],
                key="chemical_2"
            )
        
        if st.button("🔍 Cek Kompatibilitas", type="primary", use_container_width=True):
            if chemical_1 == chemical_2:
                st.info("ℹ️ Pilih dua bahan kimia yang berbeda untuk diperiksa")
            else:
                # Mencari indeks bahan kimia
                index_1 = df[df["Bahan Kimia"] == chemical_1].index[0]
                index_2 = df[df["Bahan Kimia"] == chemical_2].index[0]
                
                # Menampilkan status kompatibilitas
                compatibility_status = df.iloc[index_1, index_2 + 1]
                
                # Menampilkan hasil
                st.markdown("---")
                st.markdown("### 📋 Hasil Pemeriksaan")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Bahan Kimia 1:**\n{chemical_1}")
                
                with col2:
                    st.markdown(f"**Status:**\n{compatibility_status}")
                
                with col3:
                    st.markdown(f"**Bahan Kimia 2:**\n{chemical_2}")
                
                st.markdown("---")
                
                # Menampilkan penjelasan berdasarkan status
                if compatibility_status == "✅":
                    st.success(f"""
                    ✅ **KOMPATIBEL**
                    
                    Kedua bahan kimia ini dapat disimpan atau dikerjakan bersama dengan aman.
                    Ikuti prosedur standar laboratorium untuk penanganan masing-masing bahan.
                    """)
                
                elif compatibility_status == "⚠️":
                    st.warning(f"""
                    ⚠️ **PERLU PERHATIAN**
                    
                    Kedua bahan kimia ini dapat dikompatibilkan tetapi memerlukan tindakan pencegahan khusus:
                    - Pastikan ventilasi yang cukup
                    - Pisahkan dalam kontainer terpisah jika memungkinkan
                    - Hindari kontak langsung
                    - Pastikan pelat pemisah atau absorbent tersedia
                    - Monitor kondisi penyimpanan secara berkala
                    """)
                
                else:  # ❌
                    st.error(f"""
                    ❌ **TIDAK KOMPATIBEL**
                    
                    Kedua bahan kimia ini TIDAK BOLEH disimpan atau dikerjakan bersama:
                    - Simpan di lokasi terpisah
                    - Gunakan area kerja berbeda untuk menangani keduanya
                    - Pastikan tidak ada kemungkinan tercampur
                    - Patuhi protokol keselamatan khusus
                    - Hubungi supervisor jika ada pertanyaan
                    """)
                
                # Log aktivitas
                st.markdown("---")
                st.markdown(f"**⏰ Diperiksa pada:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with tab2:
        st.subheader("Tabel Kompatibilitas Lengkap")
        
        st.markdown("""
        Tabel di bawah menunjukkan kompatibilitas antara semua bahan kimia dalam sistem.
        Baca baris untuk bahan kimia pertama dan kolom untuk bahan kimia kedua.
        """)
        
        # Menampilkan tabel dengan styling
        st.dataframe(df, use_container_width=True, height=400)
        
        # Statistik
        st.markdown("---")
        st.subheader("📊 Statistik Kompatibilitas")
        
        col1, col2, col3 = st.columns(3)
        
        # Hitung total kompatibilitas
        all_values = df.iloc[:, 1:].values.flatten().tolist()
        compatible = all_values.count("✅")
        caution = all_values.count("⚠️")
        incompatible = all_values.count("❌")
        
        with col1:
            st.metric("✅ Kompatibel", compatible)
        
        with col2:
            st.metric("⚠️ Perhatian", caution)
        
        with col3:
            st.metric("❌ Tidak Kompatibel", incompatible)
    
    with tab3:
        st.subheader("📋 Panduan Keselamatan Penanganan Bahan Kimia")
        
        st.markdown("""
        ### Prosedur Umum Keselamatan:
        
        1. **Sebelum Bekerja:**
           - Baca label dan Safety Data Sheet (SDS) untuk setiap bahan kimia
           - Kenakan alat pelindung diri (APD): sarung tangan, kacamata, jas lab
           - Pastikan area kerja bersih dan terorganisir
        
        2. **Saat Bekerja:**
           - Selalu gunakan fume hood untuk bahan kimia yang menguap
           - Jangan pernah mencampur bahan kimia tanpa petunjuk
           - Hindarkan kontak dengan kulit dan mata
           - Bekerja dengan pasangan jika memungkinkan
        
        3. **Penyimpanan:**
           - Simpan sesuai dengan kategori bahaya
           - Pisahkan bahan kimia yang tidak kompatibel
           - Simpan di tempat yang sejuk, kering, dan berventilasi baik
           - Jauhkan dari cahaya langsung
        
        4. **Jika Terjadi Kecelakaan:**
           - Segera beri tahu supervisor
           - Gunakan prosedur darurat yang sesuai
           - Hubungi layanan medis jika diperlukan
           - Buat laporan insiden
        
        ### Kontak Darurat:
        - **First Aid:** Hubungi perawat laboratorium
        - **Emergency:** Hubungi keamanan kampus atau layanan darurat lokal
        - **Paparan Bahan Kimia:** Segera cuci dengan air dan cari bantuan medis
        """)

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Tampilkan aplikasi berdasarkan status login
if st.session_state.logged_in:
    main_app()
else:
    login()
