import streamlit as st
import pandas as pd

# Data kompatibilitas bahan kimia
compatibility_data = {
    "Bahan Kimia": ["Asam Klorida", "Natrium Hidroksida", "Amonium Nitrat", "Aseton"],
    "Asam Klorida": ["✅", "❌", "⚠️", "⚠️"],
    "Natrium Hidroksida": ["❌", "✅", "⚠️", "⚠️"],
    "Amonium Nitrat": ["⚠️", "⚠️", "✅", "❌"],
    "Aseton": ["⚠️", "⚠️", "❌", "✅"]
}

# Mengubah data menjadi DataFrame
df = pd.DataFrame(compatibility_data)

# Judul aplikasi
st.title("Aplikasi Audit Kompatibilitas Bahan Kimia")

# Pilihan bahan kimia pertama
chemical_1 = st.selectbox("Pilih Bahan Kimia Pertama:", df["Bahan Kimia"])

# Pilihan bahan kimia kedua
chemical_2 = st.selectbox("Pilih Bahan Kimia Kedua:", df["Bahan Kimia"])

# Tombol untuk memeriksa kompatibilitas
if st.button("Cek Kompatibilitas"):
    # Mencari indeks bahan kimia
    index_1 = df[df["Bahan Kimia"] == chemical_1].index[0]
    index_2 = df[df["Bahan Kimia"] == chemical_2].index[0]

    # Menampilkan status kompatibilitas
    compatibility_status = df.iloc[index_1, index_2 + 1]
    st.write(f"Status Kompatibilitas: {compatibility_status}")
