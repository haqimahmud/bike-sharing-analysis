# Proyek Analisis Data: Bike Sharing

## Deskripsi

Proyek ini merupakan proyek akhir dari kelas Belajar Analisis Data dengan Python di Dicoding. Proyek ini bertujuan untuk menganalisis data penyewaan sepeda berdasarkan musim dan jenis hari selama periode 2011–2012.

## Business Questions

1. Bagaimana perbedaan jumlah penyewaan sepeda berdasarkan musim selama periode 2011–2012, dan musim mana yang memiliki rata-rata penyewaan tertinggi?
2. Bagaimana perbedaan jumlah penyewaan sepeda antara hari kerja dan hari libur, serta bagaimana pola tersebut dapat digunakan untuk menentukan kebutuhan operasional?

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset, yang terdiri dari:

- `day.csv`: data penyewaan sepeda harian.
- `hour.csv`: data penyewaan sepeda per jam.
- `all_data.csv`: data yang digunakan oleh dashboard.

## Proses Analisis

Tahapan analisis yang dilakukan meliputi:

1. **Data Wrangling:** mengumpulkan, memeriksa, dan membersihkan data.
2. **Exploratory Data Analysis (EDA):** menganalisis pola penyewaan berdasarkan musim dan jenis hari.
3. **Visualisasi Data:** menyajikan hasil analisis menggunakan grafik.
4. **Dashboard:** menampilkan hasil analisis menggunakan Streamlit.

## Menjalankan Dashboard

1. Buka Terminal

Buka terminal atau PowerShell di folder utama proyek bike.

2. Buat Virtual Environment

Windows:

python -m venv .venv

3. Aktifkan Virtual Environment

.\.venv\Scripts\Activate.ps1

Jika berhasil, terminal akan menampilkan (.venv) di awal baris perintah.

4. Instal Library

Pastikan file requirements.txt berada di folder utama proyek, kemudian jalankan:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Menjalankan Dashboard Secara Lokal

Dari folder utama proyek bike, jalankan:

python -m streamlit run dashboard/dashboard.py
```

## Dashboard Online

Dashboard dapat diakses melalui tautan berikut:

https://bike-sharing-dicoding-4b6hltlrxwk3j6kdfkbbwy.streamlit.app/

## Teknologi yang Digunakan

- Python
- Pandas
- Matplotlib
- Streamlit

## Author

Baihaqi Alwi Mahmudi