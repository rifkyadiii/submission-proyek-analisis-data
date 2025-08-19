import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

# --- KONFIGURASI DAN GAYA ---
# Mengatur gaya visual untuk semua plot Seaborn dan Matplotlib
sns.set_style("whitegrid")

# Palet warna untuk konsistensi visual
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
ACCENT_COLOR_DARK = "#d62728"
ACCENT_COLOR_LIGHT = "#aec7e8"

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Peminjaman Sepeda",
    page_icon="🚲",
    layout="wide"
)

# --- FUNGSI BANTUAN (HELPER FUNCTIONS) ---
@st.cache_data
def load_data():
    """Memuat data dari file CSV dan melakukan pra-pemrosesan dasar."""
    try:
        hour_df = pd.read_csv('data/hour.csv')
        day_df = pd.read_csv('data/day.csv')
    except FileNotFoundError:
        # Fallback jika path 'data/' tidak ditemukan
        hour_df = pd.read_csv('../data/hour.csv')
        day_df = pd.read_csv('../data/day.csv')
    
    # Konversi kolom tanggal ke format datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

def style_plot(ax, title, xlabel, ylabel, rotation=0):
    """Menerapkan gaya standar ke plot Matplotlib untuk konsistensi."""
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', rotation=rotation)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    if ax.get_legend_handles_labels()[0]: # Hanya tampilkan legenda jika ada
        ax.legend(fontsize=10)

# --- MEMUAT DATA UTAMA ---
main_day_df, main_hour_df = load_data()

# --- SIDEBAR DAN FILTER ---
with st.sidebar:
    st.markdown("**Nama:** Moch Rifky Aulia Adikusumah")
    st.markdown("**Email:** rifkyadi67@gmail.com")
    st.markdown("**ID Dicoding:** rifkyadi")
    st.markdown("---")
    
    st.header("⚙️ Filter Data")


    # Filter 2: Musim
    selected_season = st.selectbox(
        "Pilih Musim", 
        ["Semua", "Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]
    )

    # Filter 3: Tahun
    selected_years = st.multiselect(
        "Pilih Tahun",
        options=[2011, 2012],
        default=[2011, 2012]
    )

    # Filter 4: Kondisi Cuaca
    selected_weathers = st.multiselect(
        "Pilih Kondisi Cuaca",
        options=["Cerah", "Berawan", "Hujan Ringan", "Hujan Deras"],
        default=["Cerah", "Berawan", "Hujan Ringan", "Hujan Deras"]
    )

# --- LOGIKA FILTERING DATA ---
# Salin dataframe utama agar data asli tidak berubah
day_df = main_day_df.copy()
hour_df = main_hour_df.copy()

# Terapkan filter musim
if selected_season != "Semua":
    season_map = {"Musim Semi": 1, "Musim Panas": 2, "Musim Gugur": 3, "Musim Dingin": 4}
    day_df = day_df[day_df['season'] == season_map[selected_season]]
    hour_df = hour_df[hour_df['season'] == season_map[selected_season]]

# Terapkan filter tahun
if selected_years:
    year_map = {2011: 0, 2012: 1}
    selected_year_values = [year_map[y] for y in selected_years]
    day_df = day_df[day_df['yr'].isin(selected_year_values)]
    hour_df = hour_df[hour_df['yr'].isin(selected_year_values)]

# Terapkan filter cuaca
if selected_weathers:
    weather_map = {"Cerah": 1, "Berawan": 2, "Hujan Ringan": 3, "Hujan Deras": 4}
    selected_weather_values = [weather_map[w] for w in selected_weathers]
    day_df = day_df[day_df['weathersit'].isin(selected_weather_values)]
    hour_df = hour_df[hour_df['weathersit'].isin(selected_weather_values)]


# --- JUDUL UTAMA DASHBOARD ---
st.title("📊 Dashboard Analisis Peminjaman Sepeda")
st.markdown("Gunakan filter di sidebar untuk menjelajahi pola peminjaman sepeda berdasarkan berbagai kondisi.")
st.markdown("---")


# --- TAMPILKAN VISUALISASI JIKA DATA TERSEDIA ---
if day_df.empty or hour_df.empty:
    st.warning("Tidak ada data yang tersedia untuk filter yang dipilih. Silakan ubah pilihan filter Anda.")
else:
    # --- TABS UNTUK VISUALISASI ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Perbandingan Pengguna",
        "📈 Fluktuasi Tahunan",
        "🚀 Pertumbuhan Bulanan",
        "⏰ Pola Penggunaan Harian"
    ])

    # Tab 1: Perbandingan Pengguna Kasual dan Terdaftar
    with tab1:
        st.header("Perbandingan Jumlah Pengguna Kasual dan Terdaftar per Bulan")
        
        monthly_users = day_df.groupby('mnth')[['casual', 'registered']].sum().rename(
            columns={'casual': 'Kasual', 'registered': 'Terdaftar'}
        )
        
        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_users.plot(kind='bar', color=[PRIMARY_COLOR, SECONDARY_COLOR], ax=ax, edgecolor='black', linewidth=0.7)
        
        # Menambahkan garis rata-rata
        ax.axhline(monthly_users['Kasual'].mean(), color=PRIMARY_COLOR, linestyle='--', label='Rata-rata Kasual')
        ax.axhline(monthly_users['Terdaftar'].mean(), color=SECONDARY_COLOR, linestyle='--', label='Rata-rata Terdaftar')
        
        style_plot(ax, 'Jumlah Pengguna per Bulan', 'Bulan', 'Jumlah Pengguna')
        st.pyplot(fig)
        
        st.info("""
        **Insight:**
        - Pengguna **terdaftar** secara konsisten mendominasi total peminjaman, menunjukkan adanya basis pelanggan yang loyal.
        - Peminjaman oleh pengguna **kasual** menunjukkan puncak yang lebih tinggi selama bulan-bulan hangat, menandakan ketergantungan pada cuaca dan musim liburan.
        """)
        
        with st.expander("Lihat Data Detail"):
            st.dataframe(monthly_users)

    # Tab 2: Fluktuasi Sepanjang Tahun
    with tab2:
        st.header("Fluktuasi Jumlah Pengguna Sepanjang Tahun")
        
        monthly_trends = day_df.groupby('mnth')[['casual', 'registered']].sum()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(monthly_trends.index, monthly_trends['casual'], marker='o', linestyle='-', color=PRIMARY_COLOR, label="Kasual")
        ax.plot(monthly_trends.index, monthly_trends['registered'], marker='o', linestyle='-', color=SECONDARY_COLOR, label="Terdaftar")
        
        style_plot(ax, 'Tren Pengguna Kasual vs Terdaftar Sepanjang Tahun', 'Bulan', 'Jumlah Pengguna')
        ax.set_xticks(monthly_trends.index)
        st.pyplot(fig)
        
        st.info("""
        **Insight:**
        - Kedua tipe pengguna menunjukkan tren serupa dengan puncak di pertengahan tahun dan titik terendah di awal tahun.
        - Fluktuasi pengguna kasual jauh lebih tajam, menegaskan sifat sensitif mereka terhadap musim dan cuaca.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Statistik Pengguna Kasual")
            st.metric("Rata-rata Bulanan", f"{int(monthly_trends['casual'].mean()):,}")
            st.metric("Puncak Tertinggi", f"Bulan {monthly_trends['casual'].idxmax()} ({int(monthly_trends['casual'].max()):,})")
        with col2:
            st.subheader("Statistik Pengguna Terdaftar")
            st.metric("Rata-rata Bulanan", f"{int(monthly_trends['registered'].mean()):,}")
            st.metric("Puncak Tertinggi", f"Bulan {monthly_trends['registered'].idxmax()} ({int(monthly_trends['registered'].max()):,})")

    # Tab 3: Pertumbuhan Bulanan
    with tab3:
        st.header("Analisis Pertumbuhan Pengguna Bulanan")
        
        monthly_growth = day_df.groupby('mnth')[['casual', 'registered']].sum().pct_change().fillna(0) * 100
        
        if not monthly_growth.empty and len(monthly_growth) > 1:
            fig, ax = plt.subplots(figsize=(12, 6))
            x_labels = np.arange(len(monthly_growth.index))
            
            bars1 = ax.bar(x_labels - 0.2, monthly_growth['casual'], width=0.4, label='Kasual', color=ACCENT_COLOR_LIGHT)
            bars2 = ax.bar(x_labels + 0.2, monthly_growth['registered'], width=0.4, label='Terdaftar', color=SECONDARY_COLOR)
            
            max_casual_pos = np.argmax(monthly_growth['casual'].values)
            max_registered_pos = np.argmax(monthly_growth['registered'].values)
            max_casual_month = monthly_growth.index[max_casual_pos]
            max_registered_month = monthly_growth.index[max_registered_pos]

            bars1[max_casual_pos].set_color(PRIMARY_COLOR)
            bars2[max_registered_pos].set_color(ACCENT_COLOR_DARK)
            
            ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
            style_plot(ax, 'Pertumbuhan Pengguna per Bulan (%)', 'Bulan', 'Pertumbuhan (%)')
            ax.set_xticks(x_labels)
            ax.set_xticklabels(monthly_growth.index)
            st.pyplot(fig)
            
            st.info("""
            **Insight:**
            - Pertumbuhan paling signifikan umumnya terjadi saat transisi musim, seperti dari musim dingin ke musim semi.
            - Pertumbuhan negatif menunjukkan penurunan jumlah pengguna dibandingkan bulan sebelumnya.
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Pertumbuhan Tertinggi (Kasual)")
                st.metric("Bulan", f"{max_casual_month}", f"{monthly_growth.loc[max_casual_month, 'casual']:.1f}%")
            with col2:
                st.subheader("Pertumbuhan Tertinggi (Terdaftar)")
                st.metric("Bulan", f"{max_registered_month}", f"{monthly_growth.loc[max_registered_month, 'registered']:.1f}%")
        else:
            st.info("Data tidak cukup untuk menampilkan grafik pertumbuhan bulanan.")

    # Tab 4: Pola Penggunaan Harian
    with tab4:
        st.header("Pola Penggunaan Sepeda Sepanjang Hari")
        
        hourly_avg = hour_df.groupby('hr')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        hourly_avg.plot(kind='line', ax=ax, marker='o', color=PRIMARY_COLOR)
        
        peak_morning_hour = 8
        peak_evening_hour = 17
        peak_morning = hourly_avg.get(peak_morning_hour, 0)
        peak_evening = hourly_avg.get(peak_evening_hour, 0)

        ax.scatter([peak_morning_hour, peak_evening_hour], [peak_morning, peak_evening], color=ACCENT_COLOR_DARK, s=100, zorder=5, label='Jam Puncak')
        
        style_plot(ax, 'Rata-rata Penggunaan Sepeda per Jam', 'Jam dalam Sehari', 'Jumlah Peminjaman Rata-rata')
        ax.set_xticks(range(24))
        st.pyplot(fig)

        st.info("""
        **Insight:**
        - Terdapat dua puncak penggunaan yang jelas: **pagi (sekitar 08:00)** dan **sore (sekitar 17:00)**, yang berkorelasi dengan jam komuter.
        - Pola ini menunjukkan bahwa sepeda banyak digunakan sebagai moda transportasi untuk aktivitas rutin harian.
        """)

        st.subheader("Perbandingan Jam Sibuk vs Jam Tidak Sibuk")
        
        def group_hours(hour):
            return 'Jam Sibuk' if 7 <= hour <= 9 or 16 <= hour <= 18 else 'Jam Tidak Sibuk'
        
        hour_df['kelompok_jam'] = hour_df['hr'].apply(group_hours)
        cluster_counts = hour_df.groupby('kelompok_jam')['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='cnt', y='kelompok_jam', data=cluster_counts.sort_values('cnt', ascending=False), palette=[PRIMARY_COLOR, ACCENT_COLOR_LIGHT], ax=ax)
        
        ax.set_title('Total Peminjaman: Jam Sibuk vs Tidak Sibuk', fontsize=14, fontweight='bold')
        ax.set_xlabel('Total Peminjaman')
        ax.set_ylabel('Kelompok Jam')
        st.pyplot(fig)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2024 Dibuat oleh Moch Rifky Aulia Adikusumah | Proyek Akhir Analisis Data")