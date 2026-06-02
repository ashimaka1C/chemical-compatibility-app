import streamlit as st
import pandas as pd
import hashlib
import json
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Audit Kompatibilitas Bahan Kimia", layout="wide")

# File untuk menyimpan data pengguna (dalam praktik, gunakan database yang sebenarnya)
USERS_FILE = "users_data.json"

# Data pengguna default
DEFAULT_USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
}

# Data kompatibilitas bahan kimia yang sangat diperluas
compatibility_data = {
    "Bahan Kimia": [
        "Asam Klorida (HCl)",
        "Asam Sulfat (H2SO4)",
        "Asam Nitrat (HNO3)",
        "Asam Fosfat (H3PO4)",
        "Asam Asetat (CH3COOH)",
        "Asam Sitrat (C6H8O7)",
        "Natrium Hidroksida (NaOH)",
        "Kalium Hidroksida (KOH)",
        "Kalsium Hidroksida (Ca(OH)2)",
        "Amonium Nitrat (NH4NO3)",
        "Amonium Klorida (NH4Cl)",
        "Amonium Sulfat ((NH4)2SO4)",
        "Aseton (CH3COCH3)",
        "Etanol (C2H5OH)",
        "Metanol (CH3OH)",
        "Isopropanol (C3H8O)",
        "Bensin",
        "Toluena (C7H8)",
        "Xilena (C8H10)",
        "Eter Dietil (C4H10O)",
        "Hidrogen Peroksida (H2O2)",
        "Klor (Cl2)",
        "Bromin (Br2)",
        "Iodium (I2)",
        "Ammonia (NH3)",
        "Formalin (HCHO + H2O)",
        "Permanganat Kalium (KMnO4)",
        "Natrium Hipoklorit (NaClO)",
        "Kalsium Hipoklorit (Ca(ClO)2)",
        "Kalium Bikromat (K2Cr2O7)",
        "Tembaga Sulfat (CuSO4)",
        "Besi Klorida (FeCl3)",
        "Besi Sulfat (FeSO4)",
        "Seng Klorida (ZnCl2)",
        "Timbal Asetat (Pb(CH3COO)2)",
        "Merkuri Klorida (HgCl2)",
        "Perak Nitrat (AgNO3)",
        "Natrium Karbonat (Na2CO3)",
        "Kalium Karbonat (K2CO3)",
        "Natrium Bikarbonat (NaHCO3)",
        "Kalsium Karbonat (CaCO3)",
        "Natrium Fosfat (Na3PO4)",
        "Kalium Fosfat (K3PO4)",
        "Natrium Sulfat (Na2SO4)",
        "Natrium Klorida (NaCl)",
        "Kalium Klorida (KCl)",
        "Kalium Sulfat (K2SO4)",
        "Magnesium Sulfat (MgSO4)",
        "Kalsium Sulfat (CaSO4)",
        "Natrium Tiosulfat (Na2S2O3)",
        "Benzena (C6H6)"
    ],
    "Asam Klorida (HCl)": ["✅", "⚠️", "⚠️", "⚠️", "✅", "✅", "❌", "❌", "❌", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "✅", "⚠️", "⚠️"],
    "Asam Sulfat (H2SO4)": ["⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "✅", "⚠️", "⚠️"],
    "Asam Nitrat (HNO3)": ["⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "❌", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "✅", "⚠️", "❌"],
    "Asam Fosfat (H3PO4)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Asam Asetat (CH3COOH)": ["✅", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Asam Sitrat (C6H8O7)": ["✅", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Natrium Hidroksida (NaOH)": ["❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "✅", "⚠️", "❌", "✅", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Kalium Hidroksida (KOH)": ["❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "✅", "⚠️", "❌", "✅", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Kalsium Hidroksida (Ca(OH)2)": ["❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "✅", "⚠️", "❌", "✅", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Amonium Nitrat (NH4NO3)": ["⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "✅", "⚠️", "⚠️"],
    "Amonium Klorida (NH4Cl)": ["✅", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️"],
    "Amonium Sulfat ((NH4)2SO4)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️"],
    "Aseton (CH3COCH3)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Etanol (C2H5OH)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Metanol (CH3OH)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "⚠️", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Isopropanol (C3H8O)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Bensin": ["⚠️", "⚠️", "❌", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Toluena (C7H8)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Xilena (C8H10)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Eter Dietil (C4H10O)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Hidrogen Peroksida (H2O2)": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "❌", "⚠️", "❌", "⚠️", "❌", "❌", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Klor (Cl2)": ["❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "✅", "✅", "✅", "❌", "❌", "❌", "❌", "❌"],
    "Bromin (Br2)": ["❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "✅", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "✅", "✅", "✅", "❌", "❌", "❌", "❌", "❌"],
    "Iodium (I2)": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️"],
    "Ammonia (NH3)": ["❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "✅", "⚠️", "❌", "✅", "✅", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Formalin (HCHO + H2O)": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "✅", "❌", "⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "⚠️"],
    "Permanganat Kalium (KMnO4)": ["⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "✅", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌", "❌", "❌", "❌", "✅", "✅", "✅", "❌", "⚠️", "⚠️", "❌", "❌"],
    "Natrium Hipoklorit (NaClO)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "⚠️", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalsium Hipoklorit (Ca(ClO)2)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "⚠️", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalium Bikromat (K2Cr2O7)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "❌", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "❌", "❌", "⚠️", "❌", "❌", "❌", "⚠️", "⚠️", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️"],
    "Tembaga Sulfat (CuSO4)": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Besi Klorida (FeCl3)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Besi Sulfat (FeSO4)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Seng Klorida (ZnCl2)": ["⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Timbal Asetat (Pb(CH3COO)2)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Merkuri Klorida (HgCl2)": ["⚠️", "⚠️", "❌", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌"],
    "Perak Nitrat (AgNO3)": ["⚠️", "⚠️", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️"],
    "Natrium Karbonat (Na2CO3)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalium Karbonat (K2CO3)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Natrium Bikarbonat (NaHCO3)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalsium Karbonat (CaCO3)": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Natrium Fosfat (Na3PO4)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalium Fosfat (K3PO4)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "✅", "✅", "⚠️", "✅", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Natrium Sulfat (Na2SO4)": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Natrium Klorida (NaCl)": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalium Klorida (KCl)": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalium Sulfat (K2SO4)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Magnesium Sulfat (MgSO4)": ["⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Kalsium Sulfat (CaSO4)": ["✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Natrium Tiosulfat (Na2S2O3)": ["⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "❌", "❌", "⚠️", "✅", "✅", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Benzena (C6H6)": ["⚠️", "⚠️", "❌", "⚠️", "✅", "✅", "⚠️", "⚠️", "⚠️", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "⚠️", "❌", "✅", "✅", "⚠️", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"]
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
    "Asam Fosfat (H3PO4)": {
        "level_bahaya": "🟠 BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi",
        "wadah": "Botol kaca dengan tutup plastik",
        "lokasi": "Kabinet asam, jauh dari basa",
        "catatan": "Asam lemah tapi dapat menyebabkan iritasi, jangan dicampur dengan basa kuat"
    },
    "Asam Asetat (CH3COOH)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik",
        "wadah": "Botol plastik atau kaca dengan tutup aman",
        "lokasi": "Area berventilasi baik, jauh dari api",
        "catatan": "Mudah menguap, iritasi mata, gunakan di area ventilasi"
    },
    "Asam Sitrat (C6H8O7)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa, jauh dari panas",
        "catatan": "Asam organik lemah, relatif aman, tetap hindari kontak mata"
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
    "Kalsium Hidroksida (Ca(OH)2)": {
        "level_bahaya": "🟠 BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap",
        "wadah": "Wadah plastik atau kaca dengan tutup aman",
        "lokasi": "Area penyimpanan biasa, jauh dari asam",
        "catatan": "Bersifat kaustik lemah, dapat mengiritasi kulit, hindari kontak"
    },
    "Amonium Nitrat (NH4NO3)": {
        "level_bahaya": "🟠 BERBAHAYA (Pengoksidasi)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap, berventilasi",
        "wadah": "Wadah plastik atau kaca dengan tutup aman",
        "lokasi": "Area terpisah, jauh dari bahan mudah terbakar",
        "catatan": "Pengoksidasi, dapat meningkatkan risiko kebakaran, jauhkan dari materi organik"
    },
    "Amonium Klorida (NH4Cl)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, tetap hindari inhalasi debu"
    },
    "Amonium Sulfat ((NH4)2SO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Fertilizer aman, tetap hindari paparan berlebihan"
    },
    "Aseton (CH3COCH3)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, jauh dari api",
        "wadah": "Botol kaca atau plastik tahan aseton dengan tutup aman",
        "lokasi": "Kabinet flammable khusus, area ventilasi baik",
        "catatan": "Sangat mudah terbakar, volatile, jauh dari sumber api dan panas"
    },
    "Etanol (C2H5OH)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, area terbuka",
        "wadah": "Botol kaca atau plastik dengan tutup aman",
        "lokasi": "Kabinet flammable, jauh dari sumber api",
        "catatan": "Mudah terbakar, volatile, simpan di area yang aman dari api dan panas"
    },
    "Metanol (CH3OH)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar, Beracun)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik, jauh dari panas",
        "wadah": "Botol kaca dengan tutup aman",
        "lokasi": "Kabinet flammable khusus, area ventilasi maksimal",
        "catatan": "Beracun dan mudah terbakar, hindari inhalasi dan kontak kulit, simpan aman"
    },
    "Isopropanol (C3H8O)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca atau plastik dengan tutup aman",
        "lokasi": "Kabinet flammable, jauh dari api",
        "catatan": "Mudah terbakar, iritasi mata, gunakan di area berventilasi"
    },
    "Bensin": {
        "level_bahaya": "🟡 BERBAHAYA (Sangat Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi maksimal, jauh dari api",
        "wadah": "Wadah metal atau plastik tahan bensin dengan tutup aman",
        "lokasi": "Kabinet flammable metal, area ventilasi eksternal",
        "catatan": "Sangat volatile dan mudah terbakar, simpan di area khusus dengan sistem keselamatan"
    },
    "Toluena (C7H8)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca atau plastik tahan toluena dengan tutup aman",
        "lokasi": "Kabinet flammable, area ventilasi baik",
        "catatan": "Mudah terbakar, hindari inhalasi debu, gunakan di fume hood"
    },
    "Xilena (C8H10)": {
        "level_bahaya": "🟡 BERBAHAYA (Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelak, berventilasi baik",
        "wadah": "Botol kaca dengan tutup aman",
        "lokasi": "Kabinet flammable, area ventilasi maksimal",
        "catatan": "Mudah terbakar dan beracun, hindari inhalasi"
    },
    "Eter Dietil (C4H10O)": {
        "level_bahaya": "🟡 BERBAHAYA (Sangat Mudah Terbakar)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi ekstensif",
        "wadah": "Botol kaca berwarna dengan tutup aman",
        "lokasi": "Kabinet flammable khusus, ventilasi maksimal",
        "catatan": "Sangat volatile dan mudah terbakar, dapat membentuk peroksida"
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
    "Bromin (Br2)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA (Cairan Beracun)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi ekstensif",
        "wadah": "Botol kaca dengan tutup plastik (tidak metal)",
        "lokasi": "Area berventilasi maksimal, area terbatas",
        "catatan": "Cairan sangat beracun dan mudah menguap, gunakan hanya di fume hood"
    },
    "Iodium (I2)": {
        "level_bahaya": "🟠 BERBAHAYA (Beracun)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca berwarna gelap dengan tutup aman",
        "lokasi": "Kabinet berventilasi baik, area terbatas",
        "catatan": "Beracun, dapat menguap, hindari inhalasi dan kontak"
    },
    "Ammonia (NH3)": {
        "level_bahaya": "🟠 BERBAHAYA (Gas Beracun)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, berventilasi baik, jauh dari asam",
        "wadah": "Botol atau silinder khusus tahan ammonia",
        "lokasi": "Area berventilasi baik, jauh dari asam dan oksidator",
        "catatan": "Gas pungent dan beracun, dapat menyebabkan iritasi, simpan di area terbuka"
    },
    "Formalin (HCHO + H2O)": {
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
    },
    "Natrium Hipoklorit (NaClO)": {
        "level_bahaya": "🟠 BERBAHAYA",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik",
        "wadah": "Botol plastik dengan tutup aman",
        "lokasi": "Area berventilasi baik, jauh dari asam",
        "catatan": "Dapat mengeluarkan gas klorin jika dicampur dengan asam, hindari"
    },
    "Kalsium Hipoklorit (Ca(ClO)2)": {
        "level_bahaya": "🟠 BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap, berventilasi",
        "wadah": "Botol plastik atau wadah dengan tutup aman",
        "lokasi": "Area berventilasi, jauh dari asam",
        "catatan": "Pengoksidasi, dapat menyebabkan kebakaran, jangan dicampur dengan asam"
    },
    "Kalium Bikromat (K2Cr2O7)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca dengan tutup aman",
        "lokasi": "Kabinet khusus, jauh dari bahan organik",
        "catatan": "Karsinogen, pengoksidasi kuat, hindari kontak dan inhalasi debu"
    },
    "Tembaga Sulfat (CuSO4)": {
        "level_bahaya": "🟠 BERBAHAYA (Beracun)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Botol kaca atau wadah plastik dengan tutup aman",
        "lokasi": "Area penyimpanan biasa, jauh dari pakan ternak",
        "catatan": "Beracun jika tertelan, hindari kontak dengan makanan"
    },
    "Besi Klorida (FeCl3)": {
        "level_bahaya": "🟠 BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca dengan tutup plastik",
        "lokasi": "Area terpisah, jauh dari basa",
        "catatan": "Asam dan hygroscopik, dapat menyerap kelembaban, korosif pada metal"
    },
    "Besi Sulfat (FeSO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, tetap hindari kontak dengan makanan"
    },
    "Seng Klorida (ZnCl2)": {
        "level_bahaya": "🟠 BERBAHAYA",
        "suhu": "20-25°C",
        "kondisi": "Tempat kering, sejuk, gelap",
        "wadah": "Botol kaca dengan tutup plastik",
        "lokasi": "Area penyimpanan biasa, jauh dari basa",
        "catatan": "Hygroscopik, dapat menyerap kelembaban, iritasi mata"
    },
    "Timbal Asetat (Pb(CH3COO)2)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA (Beracun Berat)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap, berventilasi baik",
        "wadah": "Botol kaca dengan tutup aman",
        "lokasi": "Kabinet khusus, area terbatas, jauh dari makanan",
        "catatan": "Metal berat beracun, dapat menyebabkan keracunan kronis, hindari kontak"
    },
    "Merkuri Klorida (HgCl2)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA (Beracun Berat)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelak, berventilasi ekstensif",
        "wadah": "Botol kaca dengan tutup aman, dalam kemasan sekunder",
        "lokasi": "Kabinet khusus terkunci, area terbatas maksimal",
        "catatan": "Sangat beracun, dapat meracuni melalui inhalasi dan kontak, hanya ahli yang menangani"
    },
    "Perak Nitrat (AgNO3)": {
        "level_bahaya": "🟠 BERBAHAYA (Korosif)",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi baik",
        "wadah": "Botol kaca coklat dengan tutup plastik",
        "lokasi": "Area penyimpanan khusus, jauh dari organik",
        "catatan": "Korosif dan dapat membakar kulit, menyebabkan noda hitam"
    },
    "Natrium Karbonat (Na2CO3)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, tetap hindari debu dan kontak dengan asam"
    },
    "Kalium Karbonat (K2CO3)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, tetap hindari debu"
    },
    "Natrium Bikarbonat (NaHCO3)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, biasanya digunakan di rumah tangga"
    },
    "Kalsium Karbonat (CaCO3)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, relatif inert"
    },
    "Natrium Fosfat (Na3PO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, basa lemah"
    },
    "Kalium Fosfat (K3PO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, basa lemah"
    },
    "Natrium Sulfat (Na2SO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, relatively inert"
    },
    "Natrium Klorida (NaCl)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, garam dapur biasa"
    },
    "Kalium Klorida (KCl)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, relatif inert"
    },
    "Kalium Sulfat (K2SO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, fertilizer"
    },
    "Magnesium Sulfat (MgSO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, garam Epsom"
    },
    "Kalsium Sulfat (CaSO4)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Aman, relatif inert"
    },
    "Natrium Tiosulfat (Na2S2O3)": {
        "level_bahaya": "🟢 AMAN",
        "suhu": "20-25°C",
        "kondisi": "Tempat sejuk, kering, gelap",
        "wadah": "Wadah plastik atau kaca biasa",
        "lokasi": "Area penyimpanan biasa",
        "catatan": "Relatif aman, gunakan dalam fotografi"
    },
    "Benzena (C6H6)": {
        "level_bahaya": "🔴 SANGAT BERBAHAYA (Karsinogen)",
        "suhu": "15-25°C",
        "kondisi": "Tempat sejuk, gelap, berventilasi ekstensif",
        "wadah": "Botol kaca dengan tutup aman",
        "lokasi": "Kabinet flammable khusus, area terbatas",
        "catatan": "Karsinogen, mudah terbakar, hindari inhalasi, gunakan hanya di fume hood"
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

def load_users():
    """Load data pengguna dari file atau gunakan default"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_USERS.copy()

def save_users(users):
    """Simpan data pengguna ke file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_admin():
    """Cek apakah user adalah admin"""
    return st.session_state.username == "admin"

def login_page():
    """Halaman login"""
    st.markdown("<h1 style='text-align: center'>🔐 Login / Register</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center'>Sistem Audit Kompatibilitas Bahan Kimia</h3>", unsafe_allow_html=True)
    
    # Tabs untuk Login dan Register
    tab_login, tab_register = st.tabs(["🔓 Login", "📝 Daftar Akun Baru"])
    
    with tab_login:
        st.subheader("Masuk ke Akun Anda")
        
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.info("📝 Masukkan kredensial Anda untuk login")
                
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                    users = load_users()
                    if username in users:
                        if hash_password(password) == users[username]:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.login_time = datetime.now()
                            st.success(f"Selamat datang, {username}! 👋")
                            st.rerun()
                        else:
                            st.error("❌ Password salah!")
                    else:
                        st.error("❌ Username tidak ditemukan!")
    
    with tab_register:
        st.subheader("Buat Akun Baru")
        
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.info("📝 Isi formulir di bawah untuk membuat akun baru")
                
                new_username = st.text_input("Username baru", key="reg_username", 
                    help="Username harus unik dan terdiri dari huruf, angka, dan underscore")
                new_password = st.text_input("Password", type="password", key="reg_password",
                    help="Gunakan password yang kuat (minimal 6 karakter)")
                confirm_password = st.text_input("Konfirmasi Password", type="password", key="reg_confirm",
                    help="Ketik ulang password Anda")
                
                if st.button("📝 Daftar", use_container_width=True, key="register_btn"):
                    # Validasi input
                    if not new_username or not new_password:
                        st.error("❌ Username dan password tidak boleh kosong!")
                    elif len(new_password) < 6:
                        st.error("❌ Password minimal 6 karakter!")
                    elif new_password != confirm_password:
                        st.error("❌ Password dan konfirmasi password tidak cocok!")
                    else:
                        users = load_users()
                        if new_username in users:
                            st.error("❌ Username sudah terdaftar! Gunakan username lain.")
                        else:
                            # Daftar akun baru
                            users[new_username] = hash_password(new_password)
                            save_users(users)
                            st.success(f"✅ Akun '{new_username}' berhasil dibuat! Silakan login dengan akun baru Anda.")
                            st.balloons()

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
        col1, col2, col3 = st.columns(3)
        
        chemicals = df["Bahan Kimia"].tolist()
        chunk_size = (len(chemicals) + 2) // 3
        
        with col1:
            st.markdown("**Daftar Bahan Kimia (Part 1):**")
            for i, chem in enumerate(chemicals[:chunk_size], 1):
                st.write(f"{i}. {chem}")
        
        with col2:
            st.markdown("**Daftar Bahan Kimia (Part 2):**")
            for i, chem in enumerate(chemicals[chunk_size:chunk_size*2], chunk_size + 1):
                st.write(f"{i}. {chem}")
        
        with col3:
            st.markdown("**Daftar Bahan Kimia (Part 3):**")
            for i, chem in enumerate(chemicals[chunk_size*2:], chunk_size*2 + 1):
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
        - **🟢 AMAN**: Bahan yang relatif aman tapi tetap memerlukan penanganan hati-hati dan penyimpanan yang benar.
        """)

# Jalankan aplikasi
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
