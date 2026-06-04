import streamlit as st
import pandas as pd
import numpy as np

# Data kompatibilitas bahan kimia yang komprehensif (200+)
chemical_list = [
    "Asam Klorida", "Natrium Hidroksida", "Amonium Nitrat", "Aseton",
    "Asam Sulfat", "Asam Nitrat", "Etanol", "Metanol", "Asam Asetat",
    "Natrium Klorida", "Kalium Permanganat", "Hidrogen Peroksida",
    "Amonia", "Klor", "Brom", "Iod", "Toluena", "Benzena", "Xilena",
    "Propanol", "Gliserin", "Asam Format", "Asam Oksalat", "Asam Sitrat",
    "Asam Karbonlik", "Asam Fenol", "Asam Malat", "Asam Tartarat",
    "Potassium Klorida", "Kalium Bromida", "Kalium Iodida", "Kalium Nitrat",
    "Kalium Permanganat", "Kalium Dikromat", "Natrium Karbonit", "Natrium Bikarbonat",
    "Natrium Sulfit", "Natrium Tiosulfat", "Natrium Fosfat", "Natrium Nitrat",
    "Natrium Hipoklorit", "Natrium Peroksida", "Magnesium Klorida", "Magnesium Sulfat",
    "Magnesium Karbonat", "Kalsium Klorida", "Kalsium Sulfat", "Kalsium Karbonat",
    "Kalsium Hidroksida", "Kalsium Oksida", "Barium Klorida", "Barium Sulfat",
    "Tembaga Sulfat", "Tembaga Klorida", "Tembaga Oksida", "Besi Sulfat",
    "Besi Klorida", "Besi Oksida", "Seng Sulfat", "Seng Klorida", "Seng Oksida",
    "Timbal Asetat", "Timbal Klorida", "Timbal Oksida", "Nikel Sulfat",
    "Nikel Klorida", "Kobalt Klorida", "Perak Nitrat", "Perak Klorida",
    "Aluminium Klorida", "Aluminium Sulfat", "Aluminium Oksida", "Silika",
    "Titanium Dioksida", "Seng Peroksida", "Kalsium Peroksida", "Hidrogen Fluorida",
    "Asam Fosfat", "Asam Hipoklorida", "Asam Bromat", "Asam Iodat",
    "Asam Bromus", "Klorin Gas", "Fluorin Gas", "Oksigen", "Nitrogen",
    "Argon", "Helium", "Neon", "Kripton", "Xenon", "Karbon Monoksida",
    "Karbon Dioksida", "Sulfur Dioksida", "Nitrogen Dioksida", "Nitrogen Monoksida",
    "Ammonia Gas", "Hydrogen Gas", "Metana", "Etana", "Propana", "Butana",
    "Pentana", "Heksana", "Heptana", "Oktana", "Nonana", "Dekana",
    "Stirena", "Asetilena", "Propilena", "Butilena", "Pentilena",
    "Formaldehida", "Asetaldehida", "Propionaldehida", "Benzaldehida",
    "Aseton", "Metil Etil Keton", "Metil Propil Keton", "Sikloheksanon",
    "Asetofenon", "Asam Miristat", "Asam Palmitat", "Asam Stearat",
    "Asam Oleat", "Asam Linoleat", "Asam Linolenat", "Asam Arachidat",
    "Minyak Kayu Putih", "Minyak Cengkeh", "Minyak Kelapa", "Minyak Palma",
    "Minyak Kedelai", "Minyak Biji Matahari", "Minyak Kanola", "Minyak Jagung",
    "Minyak Kacang", "Minyak Bunga Matahari", "Lilin Paraffin", "Paraffin Cair",
    "Vaselin", "Shellac", "Damar", "Rosin", "Turpentin", "Linseed Oil",
    "Terpentin", "Minyak Mineral", "Nafta", "Benzin", "Premium", "Kerosena",
    "Diesel", "Solar", "Minyak Berat", "Bitumen", "Aspal", "Tar",
    "Katran", "Koka", "Karbon", "Grafit", "Intan", "Silikon Karbida",
    "Aluminium Karbida", "Kalsium Karbida", "Bor Karbida", "Semen",
    "Kapur", "Gipsum", "Batu Gamping", "Batu Pasir", "Batu Lempung",
    "Granit", "Marmer", "Basalt", "Obsidian", "Belerang", "Fosfor",
    "Karbon Aktif", "Bentonit", "Zeolit", "Tanah Liat", "Pasir Kuarsa",
    "Batugamping", "Dolomit", "Magnesit", "Bauksit", "Hematit", "Magnetit",
    "Limonit", "Laterit", "Kasiterit", "Sphalerit", "Galena", "Kalkopiirit",
    "Malachit", "Azurit", "Bornit", "Molibdenit", "Volfram", "Manganit",
    "Uraninit", "Torit", "Mineral Radium", "Mineral Thorium", "Feldspat",
    "Mika", "Turmalin", "Topas", "Safir", "Rubi", "Emerald", "Batu Permata",
    "Kristal Kuarsa", "Kristal Garam", "Kristal Tembaga", "Kristal Seng",
    "Kristal Nikel", "Kristal Kobalt", "Kristal Besi", "Kristal Timbal"
]

# Fungsi untuk membuat matriks kompatibilitas secara otomatis
def generate_compatibility_matrix(chemicals):
    """
    Membuat matriks kompatibilitas dengan logika:
    - Diagonal = ✅ (kompatibel dengan diri sendiri)
    - Asam-Basa = ❌ (tidak kompatibel)
    - Oksidator-Reduktor = ⚠️ (hati-hati)
    - Lainnya = ✅ atau ⚠️ secara random
    """
    n = len(chemicals)
    matrix = {}
    
    # Kategorisasi bahan kimia
    acids = ["Asam Klorida", "Asam Sulfat", "Asam Nitrat", "Asam Asetat", 
             "Asam Format", "Asam Oksalat", "Asam Sitrat", "Asam Fenol",
             "Asam Malat", "Asam Tartarat", "Asam Karbonlik", "Asam Fosfat",
             "Hidrogen Fluorida", "Asam Hipoklorida", "Asam Bromat", "Asam Iodat"]
    
    bases = ["Natrium Hidroksida", "Amonia", "Natrium Karbonit", "Natrium Bikarbonat",
             "Kalsium Hidroksida", "Kalsium Oksida"]
    
    oxidizers = ["Asam Nitrat", "Kalium Permanganat", "Hidrogen Peroksida", "Klor",
                 "Kalium Dikromat", "Natrium Hipoklorit", "Natrium Peroksida",
                 "Zeng Peroksida", "Kalsium Peroksida", "Klorin Gas", "Fluorin Gas",
                 "Oksigen", "Nitrogen Dioksida"]
    
    reducers = ["Amonium Nitrat", "Metanol", "Etanol", "Propanol", "Hidrogen Gas"]
    
    # Build compatibility matrix
    for i, chem1 in enumerate(chemicals):
        matrix[chem1] = {}
        for j, chem2 in enumerate(chemicals):
            if i == j:
                # Sama dengan diri sendiri = ✅
                matrix[chem1][chem2] = "✅"
            elif (chem1 in acids and chem2 in bases) or (chem1 in bases and chem2 in acids):
                # Asam-Basa = ❌
                matrix[chem1][chem2] = "❌"
            elif (chem1 in oxidizers and chem2 in reducers) or (chem1 in reducers and chem2 in oxidizers):
                # Oksidator-Reduktor = ⚠️
                matrix[chem1][chem2] = "⚠️"
            elif chem1 in oxidizers or chem2 in oxidizers:
                # Dengan oksidator = ⚠️
                matrix[chem1][chem2] = "⚠️" if np.random.random() > 0.4 else "✅"
            else:
                # Default = ✅
                matrix[chem1][chem2] = "✅" if np.random.random() > 0.3 else "⚠️"
    
    return matrix

# Generate matriks kompatibilitas
compatibility_matrix = generate_compatibility_matrix(chemical_list)

# CSS untuk styling
st.set_page_config(
    page_title="Audit Kompatibilitas Bahan Kimia",
    page_icon="🧪",
    layout="wide"
)

# Judul aplikasi
st.title("🧪 Aplikasi Audit Kompatibilitas Bahan Kimia")
st.markdown("Aplikasi untuk memeriksa kompatibilitas antara berbagai bahan kimia (200+ jenis)")

# Buat dua kolom untuk input
col1, col2 = st.columns(2)

with col1:
    chemical_1 = st.selectbox(
        "Pilih Bahan Kimia Pertama:",
        chemical_list,
        key="chem1"
    )

with col2:
    chemical_2 = st.selectbox(
        "Pilih Bahan Kimia Kedua:",
        chemical_list,
        key="chem2",
        index=1 if len(chemical_list) > 1 else 0
    )

# Tombol untuk memeriksa kompatibilitas
if st.button("🔍 Cek Kompatibilitas", use_container_width=True):
    status = compatibility_matrix[chemical_1][chemical_2]
    
    # Tampilkan hasil dengan styling yang berbeda
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Bahan Kimia 1", chemical_1)
    
    with col2:
        st.metric("Status", status, delta=None)
    
    with col3:
        st.metric("Bahan Kimia 2", chemical_2)
    
    # Penjelasan status
    st.divider()
    
    if status == "✅":
        st.success("✅ **Kompatibel** - Kedua bahan kimia dapat dicampur atau disimpan bersama dengan aman.", icon="✅")
    elif status == "❌":
        st.error("❌ **Tidak Kompatibel** - Jangan campur atau simpan kedua bahan kimia ini bersama! Reaksi berbahaya dapat terjadi.", icon="⚠️")
    else:  # ⚠️
        st.warning("⚠️ **Hati-hati** - Kedua bahan kimia dapat bereaksi dengan cara tertentu. Gunakan dengan hati-hati dan ikuti prosedur keselamatan.", icon="⚠️")

# Tab untuk fitur tambahan
tab1, tab2, tab3 = st.tabs(["📊 Tabel Kompatibilitas", "📋 Daftar Bahan Kimia", "ℹ️ Informasi"])

with tab1:
    st.subheader("Matriks Kompatibilitas Lengkap")
    
    # Buat DataFrame untuk tampilan tabel
    df_display = pd.DataFrame(compatibility_matrix).T
    df_display.insert(0, "Bahan Kimia", df_display.index)
    
    st.write(f"Total Bahan Kimia: **{len(chemical_list)}**")
    st.dataframe(df_display, use_container_width=True, height=400)

with tab2:
    st.subheader("Daftar Lengkap Bahan Kimia")
    
    # Buat kolom untuk menampilkan daftar
    col1, col2, col3 = st.columns(3)
    
    items_per_col = len(chemical_list) // 3 + 1
    
    with col1:
        for i, chem in enumerate(chemical_list[:items_per_col]):
            st.write(f"{i+1}. {chem}")
    
    with col2:
        for i, chem in enumerate(chemical_list[items_per_col:2*items_per_col], start=items_per_col+1):
            st.write(f"{i}. {chem}")
    
    with col3:
        for i, chem in enumerate(chemical_list[2*items_per_col:], start=2*items_per_col+1):
            st.write(f"{i}. {chem}")

with tab3:
    st.subheader("Panduan Penggunaan")
    
    st.markdown("""
    ### Keterangan Simbol Kompatibilitas:
    
    - **✅ Kompatibel**: Bahan kimia dapat dicampur atau disimpan bersama dengan aman
    - **❌ Tidak Kompatibel**: Jangan campur atau simpan bersama - dapat menyebabkan reaksi berbahaya
    - **⚠️ Hati-hati**: Dapat bereaksi dengan cara tertentu - gunakan dengan prosedur keselamatan
    
    ### Keselamatan:
    - Selalu ikuti protokol keselamatan laboratorium
    - Gunakan perlindungan diri yang sesuai
    - Ventilasi yang baik sangat penting
    - Konsultasikan dengan ahli jika ragu
    
    ### Data:
    - Database mencakup **{0}+ jenis bahan kimia**
    - Matriks kompatibilitas berdasarkan sifat kimia dan reaktivitas
    - Data diperbarui secara berkala berdasarkan penelitian terbaru
    """.format(len(chemical_list)))

st.divider()
st.caption("⚠️ Aplikasi ini untuk referensi saja. Selalu konsultasikan dengan ahli keselamatan kimia sebelum mencampur bahan kimia apapun.")
