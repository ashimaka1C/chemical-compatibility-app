import streamlit as st
import pandas as pd
import hashlib
import json
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="CHEMICAL COMPATIBILITY APPS", layout="wide")

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

# Data saran penyimpanan untuk setiap bahan kimia (dipotong untuk efisiensi)
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
    st.session_state.current_page = "cek_kompatibel"

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
    """Halaman login dengan form register di bawahnya"""
    st.markdown("<h1 style='text-align: center'>🔐 Sistem Audit Kompatibilitas Bahan Kimia</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔓 Login")
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
            
            st.divider()
            
            st.markdown("### 📝 Buat Akun Baru")
            st.info("Isi formulir di bawah untuk membuat akun baru")
            
            new_username = st.text_input("Username baru", key="reg_username")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Konfirmasi Password", type="password", key="reg_confirm")
            
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
    """Aplikasi utama setelah login dengan sidebar menu"""
    
    # Sidebar menu
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        if is_admin():
            st.markdown("🔑 **ADMIN**")
        st.divider()
        
        st.markdown("### 📋 Menu")
        
        # Menu items
        if st.button("🔍 Cek Kompatibilitas", use_container_width=True, key="menu_check"):
            st.session_state.current_page = "cek_kompatibel"
            st.rerun()
        
        if st.button("📊 Tabel Kompatibilitas", use_container_width=True, key="menu_table"):
            if is_admin():
                st.session_state.current_page = "tabel_kompatibel"
                st.rerun()
            else:
                st.error("🔐 Hanya admin yang dapat mengakses")
        
        if st.button("📖 Panduan", use_container_width=True, key="menu_guide"):
            st.session_state.current_page = "panduan"
            st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.divider()
        st.markdown("**Login time:**")
        st.caption(st.session_state.login_time.strftime('%Y-%m-%d %H:%M:%S'))
    
    # Judul aplikasi - RATA TENGAH
    st.markdown("<h1 style='text-align: center'>CHEMICAL COMPABILITY</h1>", unsafe_allow_html=True)
    
    # Mengubah data menjadi DataFrame
    df = pd.DataFrame(compatibility_data)
    
    # Tampilkan halaman sesuai yang dipilih
    if st.session_state.current_page == "cek_kompatibel":
        st.markdown("Periksa kompatibilitas antara dua bahan kimia sebelum mencampurnya")
        
        st.subheader("🔍 Periksa Kompatibilitas Dua Bahan Kimia")
        
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
    
    elif st.session_state.current_page == "tabel_kompatibel":
        if is_admin():
            st.subheader("📊 Matriks Kompatibilitas Lengkap")
            
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
            
            total_chemicals = len(df["Bahan Kimia"])
            
            with col_stat1:
                st.metric("Total Bahan Kimia", total_chemicals)
            
            with col_stat2:
                st.metric("Total Data Kompatibilitas", total_chemicals * (total_chemicals - 1) // 2)
            
            with col_stat3:
                st.metric("Jumlah Kolom Data", len(df.columns) - 1)
        else:
            st.warning("🔐 Akses Terbatas")
            st.markdown("""
            **Maaf, tabel kompatibilitas lengkap hanya dapat diakses oleh pengguna Admin.**
            """)
    
    elif st.session_state.current_page == "panduan":
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
           - Gunakan menu "Tabel Kompatibilitas" untuk melihat semua data lengkap
           - Download CSV untuk dokumentasi dan laporan
        
        ### Panduan Keselamatan Umum
        
        - **Selalu baca label bahan kimia** sebelum menggunakannya
        - **Gunakan APD (Alat Pelindung Diri)** yang sesuai
        - **Bekerja di area berventilasi baik** atau menggunakan fume hood
        - **Ikuti prosedur SOP** (Standard Operating Procedure) laboratorium
        - **Konsultasikan dengan ahli keselamatan** jika ragu
        - **Simpan bahan dengan benar** sesuai rekomendasi
        - **Jangan campur bahan tanpa pengetahuan** tentang kompatibilitasnya
        """)
        
        st.divider()
        
        st.subheader("🔍 Status Kompatibilitas - Penjelasan Detail")
        
        for status, explanation in status_explanation.items():
            st.write(f"**{status} {explanation}**")
        
        st.divider()
        
        st.subheader("⚠️ Tingkat Bahaya Bahan Kimia")
        
        st.markdown("""
        - **🔴 SANGAT BERBAHAYA**: Bahan yang sangat beracun, korosif, atau mudah meledak
        - **🟠 BERBAHAYA**: Bahan yang bersifat beracun, pengoksidasi, atau dapat menyebabkan kebakaran
        - **🟡 BERBAHAYA (Mudah Terbakar)**: Bahan yang mudah terbakar atau volatile
        - **🟢 AMAN**: Bahan yang relatif aman tapi tetap memerlukan penanganan hati-hati
        """)

# Jalankan aplikasi
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
