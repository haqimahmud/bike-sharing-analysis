import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load dan Cache Data
@st.cache_data
def load_data():
    # Karena dashboard.py dan all_data.csv ada di folder yang sama (dashboard/)
    df = pd.read_csv("dashboard/all_data.csv") 
    df["dteday"] = pd.to_datetime(df["dteday"])

    # Memastikan kolom kategori musim dan jenis hari sudah sesuai
    df["season_name"] = df["season"]
    df["day_type"] = df["workingday"]

    return df

day_df = load_data()

# Judul Utama Dashboard
st.title("🚲 Bike Sharing Dashboard")
st.write(
    "Analisis penyewaan sepeda berdasarkan musim "
    "dan jenis hari selama periode dataset yang tersedia."
)

# ==========================================
# SIDEBAR: FILTER DATA (BERDASARKAN TANGGAL)
# ==========================================
st.sidebar.header("Filter Data")

# Mengambil batas minimum dan maksimum tanggal dari dataset untuk rentang default
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# Widget st.date_input untuk memilih rentang tanggal (Start Date & End Date)
try:
    start_date, end_date = st.sidebar.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
except Exception:
    # Fallback jika hanya satu tanggal yang terpilih atau terjadi error rentang
    start_date, end_date = min_date, max_date

# Filter tambahan berdasarkan Musim (opsional, agar analisis musim tetap berjalan optimal)
selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    ["Semua Musim", "Spring", "Summer", "Fall", "Winter"]
)

# ==========================================
# PROSES PEMFILTERAN DATA
# ==========================================
# Filter berdasarkan tanggal (konversi start_date & end_date ke datetime)
filtered_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) & 
    (day_df["dteday"] <= pd.to_datetime(end_date))
]

# Filter berdasarkan musim jika dipilih
if selected_season != "Semua Musim":
    filtered_df = filtered_df[
        filtered_df["season_name"] == selected_season
    ]

# Validasi jika data kosong setelah difilter
if filtered_df.empty:
    st.warning("Data tidak ditemukan untuk rentang tanggal atau filter yang dipilih.")
    st.stop()

# ==========================================
# MAIN PANEL: RINGKASAN & METRIK
# ==========================================
st.subheader("Ringkasan Penyewaan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Penyewaan",
    f"{filtered_df['cnt'].sum():,.0f}"
)

col2.metric(
    "Rata-rata per Hari",
    f"{filtered_df['cnt'].mean():,.0f}"
)

col3.metric(
    "Jumlah Hari Terdata",
    f"{len(filtered_df):,}"
)

st.divider()

# ==========================================
# VISUALISASI 1: RATA-RATA PENYEWAAN PER MUSIM
# ==========================================
st.subheader("1. Rata-rata Penyewaan Berdasarkan Musim")

season_order = ["Spring", "Summer", "Fall", "Winter"]

season_df = (
    filtered_df.groupby("season_name")["cnt"]
    .mean()
    .reindex(season_order)
    .dropna()
)

fig1, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(season_df.index, season_df.values, color=['#ff9999','#66b3ff','#99ff99','#ffcc99'])

ax1.set_xlabel("Musim", fontsize=11)
ax1.set_ylabel("Rata-rata Penyewaan per Hari", fontsize=11)
ax1.set_title("Rata-rata Penyewaan Sepeda per Musim", fontsize=13, pad=12)
ax1.bar_label(bars, fmt="%.0f", padding=3)
ax1.set_ylim(0, season_df.max() * 1.15 if not season_df.empty else 10)
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

if not season_df.empty:
    st.info(
        f"💡 Rata-rata penyewaan tertinggi berdasarkan rentang tanggal terpilih "
        f"terdapat pada musim **{season_df.idxmax()}**, dengan sekitar "
        f"**{season_df.max():,.0f}** sepeda per hari."
    )

st.divider()

# ==========================================
# VISUALISASI 2: HARI KERJA VS HARI LIBUR
# ==========================================
st.subheader("2. Penyewaan pada Hari Kerja dan Hari Libur")

workingday_df = (
    filtered_df.groupby("day_type")["cnt"]
    .mean()
    .reindex(["Hari Kerja", "Hari Libur"])
    .dropna()
)

fig2, ax2 = plt.subplots(figsize=(9, 5))
bars = ax2.bar(workingday_df.index, workingday_df.values, color=['#72B4EB', '#FFA07A'])

ax2.set_xlabel("Jenis Hari", fontsize=11)
ax2.set_ylabel("Rata-rata Penyewaan per Hari", fontsize=11)
ax2.set_title("Hari Kerja vs Hari Libur", fontsize=13, pad=12)
ax2.bar_label(bars, fmt="%.0f", padding=3)
ax2.set_ylim(0, workingday_df.max() * 1.15 if not workingday_df.empty else 10)
fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2)

if not workingday_df.empty:
    st.info(
        f"💡 Rata-rata penyewaan tertinggi berdasarkan jenis hari "
        f"terdapat pada **{workingday_df.idxmax().lower()}**, dengan sekitar "
        f"**{workingday_df.max():,.0f}** sepeda per hari."
    )

st.caption("Sumber: Bike Sharing Dataset, 2011–2012.")