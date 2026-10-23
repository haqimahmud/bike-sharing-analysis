import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])

    df["season_name"] = df["season"].map({
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    })

    df["year_name"] = df["yr"].map({
        0: 2011,
        1: 2012
    })

    df["day_type"] = df["workingday"].map({
        0: "Hari Libur",
        1: "Hari Kerja"
    })

    return df


day_df = load_data()

st.title("🚲 Bike Sharing Dashboard")
st.write(
    "Analisis penyewaan sepeda berdasarkan musim "
    "dan jenis hari selama 2011–2012."
)

st.sidebar.header("Filter Data")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua Tahun", 2011, 2012]
)

selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    ["Semua Musim", "Spring", "Summer", "Fall", "Winter"]
)

filtered_df = day_df.copy()

if selected_year != "Semua Tahun":
    filtered_df = filtered_df[
        filtered_df["year_name"] == selected_year
    ]

if selected_season != "Semua Musim":
    filtered_df = filtered_df[
        filtered_df["season_name"] == selected_season
    ]

if filtered_df.empty:
    st.warning("Data tidak ditemukan untuk filter yang dipilih.")
    st.stop()

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
    "Jumlah Hari",
    f"{len(filtered_df):,}"
)

st.divider()

st.subheader("1. Rata-rata Penyewaan Berdasarkan Musim")

season_order = ["Spring", "Summer", "Fall", "Winter"]

season_df = (
    filtered_df.groupby("season_name")["cnt"]
    .mean()
    .reindex(season_order)
    .dropna()
)

fig1, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(season_df.index, season_df.values)

ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan per Hari")
ax1.set_title("Rata-rata Penyewaan Sepeda per Musim")
ax1.bar_label(bars, fmt="%.0f", padding=3)
ax1.set_ylim(0, season_df.max() * 1.15)
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

if not season_df.empty:
    st.info(
        f"Rata-rata penyewaan tertinggi terdapat pada musim "
        f"{season_df.idxmax()}, sekitar "
        f"{season_df.max():,.0f} sepeda per hari."
    )

st.divider()

st.subheader("2. Penyewaan pada Hari Kerja dan Hari Libur")

workingday_df = (
    filtered_df.groupby("day_type")["cnt"]
    .mean()
    .reindex(["Hari Kerja", "Hari Libur"])
    .dropna()
)

fig2, ax2 = plt.subplots(figsize=(9, 5))
bars = ax2.bar(workingday_df.index, workingday_df.values)

ax2.set_xlabel("Jenis Hari")
ax2.set_ylabel("Rata-rata Penyewaan per Hari")
ax2.set_title("Hari Kerja vs Hari Libur")
ax2.bar_label(bars, fmt="%.0f", padding=3)
ax2.set_ylim(0, workingday_df.max() * 1.15)
fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2)

if not workingday_df.empty:
    st.info(
        f"Rata-rata penyewaan tertinggi terdapat pada "
        f"{workingday_df.idxmax().lower()}, sekitar "
        f"{workingday_df.max():,.0f} sepeda per hari."
    )

st.caption("Sumber: Bike Sharing Dataset, 2011–2012.")

