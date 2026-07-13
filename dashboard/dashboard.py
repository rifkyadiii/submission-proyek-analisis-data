import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- KONFIGURASI DAN GAYA ---
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
ACCENT_COLOR_DARK = "#d62728"
ACCENT_COLOR_LIGHT = "#aec7e8"

st.set_page_config(
    page_title="Dashboard Peminjaman Sepeda",
    page_icon="🚲",
    layout="wide"
)

# --- FUNGSI BANTUAN ---
@st.cache_data
def load_data():
    """Memuat data dari file CSV dan melakukan pra-pemrosesan dasar."""
    possible_paths = [
        ("data/hour.csv", "data/day.csv"),
        ("../data/hour.csv", "../data/day.csv"),
    ]
    last_error = None
    for hour_path, day_path in possible_paths:
        try:
            hour_df = pd.read_csv(hour_path)
            day_df = pd.read_csv(day_path)
            day_df['dteday'] = pd.to_datetime(day_df['dteday'])
            hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
            return day_df, hour_df
        except FileNotFoundError as e:
            last_error = e
            continue
    # Kalau semua path gagal, jangan biarkan exception mentah membunuh app
    raise FileNotFoundError(
        f"Tidak dapat menemukan data/hour.csv atau data/day.csv. Detail: {last_error}"
    )


def safe_mean(series):
    """Mean yang aman untuk Series kosong / berisi inf."""
    if series is None or len(series) == 0:
        return 0.0
    cleaned = series.replace([np.inf, -np.inf], np.nan).dropna()
    if cleaned.empty:
        return 0.0
    return float(cleaned.mean())


def safe_idxmax(series):
    """idxmax yang aman untuk Series kosong / semua NaN / semua inf.
    Mengembalikan (index_ditemukan: bool, idx, value)."""
    if series is None or len(series) == 0:
        return False, None, None
    cleaned = series.replace([np.inf, -np.inf], np.nan)
    if cleaned.dropna().empty:
        return False, None, None
    idx = cleaned.idxmax()
    return True, idx, series.loc[idx]


# --- MEMUAT DATA UTAMA ---
try:
    main_day_df, main_hour_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# --- SIDEBAR DAN FILTER ---
with st.sidebar:
    st.header("⚙️ Filter Data")

    selected_season = st.selectbox(
        "Pilih Musim",
        ["Semua", "Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]
    )

    selected_years = st.multiselect(
        "Pilih Tahun",
        options=[2011, 2012],
        default=[2011, 2012]
    )

    selected_weathers = st.multiselect(
        "Pilih Kondisi Cuaca",
        options=["Cerah", "Berawan", "Hujan Ringan", "Hujan Deras"],
        default=["Cerah", "Berawan", "Hujan Ringan", "Hujan Deras"]
    )

# --- LOGIKA FILTERING DATA (dengan guard di setiap langkah) ---
day_df = main_day_df.copy()
hour_df = main_hour_df.copy()

try:
    if selected_season != "Semua":
        season_map = {"Musim Semi": 1, "Musim Panas": 2, "Musim Gugur": 3, "Musim Dingin": 4}
        season_val = season_map.get(selected_season)
        if season_val is not None:
            day_df = day_df[day_df['season'] == season_val]
            hour_df = hour_df[hour_df['season'] == season_val]

    if selected_years:
        year_map = {2011: 0, 2012: 1}
        selected_year_values = [year_map[y] for y in selected_years if y in year_map]
        if selected_year_values:
            day_df = day_df[day_df['yr'].isin(selected_year_values)]
            hour_df = hour_df[hour_df['yr'].isin(selected_year_values)]
        else:
            day_df = day_df.iloc[0:0]
            hour_df = hour_df.iloc[0:0]
    else:
        day_df = day_df.iloc[0:0]
        hour_df = hour_df.iloc[0:0]

    if selected_weathers:
        weather_map = {"Cerah": 1, "Berawan": 2, "Hujan Ringan": 3, "Hujan Deras": 4}
        selected_weather_values = [weather_map[w] for w in selected_weathers if w in weather_map]
        if selected_weather_values:
            day_df = day_df[day_df['weathersit'].isin(selected_weather_values)]
            hour_df = hour_df[hour_df['weathersit'].isin(selected_weather_values)]
        else:
            day_df = day_df.iloc[0:0]
            hour_df = hour_df.iloc[0:0]
    else:
        day_df = day_df.iloc[0:0]
        hour_df = hour_df.iloc[0:0]
except Exception as e:
    st.error(f"Terjadi kesalahan saat menerapkan filter: {e}")
    day_df = day_df.iloc[0:0]
    hour_df = hour_df.iloc[0:0]

# Reset index supaya semua operasi berikutnya konsisten (0..n-1)
day_df = day_df.reset_index(drop=True)
hour_df = hour_df.reset_index(drop=True)

# --- JUDUL UTAMA ---
st.title("📊 Dashboard Analisis Peminjaman Sepeda")
st.markdown("Gunakan filter di sidebar untuk menjelajahi pola peminjaman sepeda berdasarkan berbagai kondisi.")
st.markdown("---")

# --- VISUALISASI ---
if day_df.empty or hour_df.empty:
    st.warning("Tidak ada data yang tersedia untuk filter yang dipilih. Silakan ubah pilihan filter Anda.")
else:
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Perbandingan Pengguna",
        "📈 Fluktuasi Tahunan",
        "🚀 Pertumbuhan Bulanan",
        "⏰ Pola Penggunaan Harian"
    ])

    # Tab 1
    with tab1:
        st.header("Perbandingan Jumlah Pengguna Kasual dan Terdaftar per Bulan")
        try:
            monthly_users = (
                day_df.groupby('mnth')[['casual', 'registered']]
                .sum()
                .rename(columns={'casual': 'Kasual', 'registered': 'Terdaftar'})
                .reset_index(drop=False)
            )

            if monthly_users.empty:
                st.info("Tidak cukup data untuk menampilkan grafik ini.")
            else:
                fig1 = go.Figure()
                fig1.add_bar(x=monthly_users['mnth'], y=monthly_users['Kasual'], name='Kasual', marker_color=PRIMARY_COLOR)
                fig1.add_bar(x=monthly_users['mnth'], y=monthly_users['Terdaftar'], name='Terdaftar', marker_color=SECONDARY_COLOR)
                fig1.add_hline(y=safe_mean(monthly_users['Kasual']), line_dash="dash", line_color=PRIMARY_COLOR,
                                annotation_text="Rata-rata Kasual")
                fig1.add_hline(y=safe_mean(monthly_users['Terdaftar']), line_dash="dash", line_color=SECONDARY_COLOR,
                                annotation_text="Rata-rata Terdaftar")
                fig1.update_layout(title="Jumlah Pengguna per Bulan", xaxis_title="Bulan", yaxis_title="Jumlah Pengguna",
                                    barmode='group', xaxis=dict(tickmode='linear'))
                st.plotly_chart(fig1, use_container_width=True)

                st.info("""
                **Insight:**
                - Pengguna **terdaftar** secara konsisten mendominasi total peminjaman, menunjukkan adanya basis pelanggan yang loyal.
                - Peminjaman oleh pengguna **kasual** menunjukkan puncak yang lebih tinggi selama bulan-bulan hangat, menandakan ketergantungan pada cuaca dan musim liburan.
                """)

                with st.expander("Lihat Data Detail"):
                    st.dataframe(monthly_users.set_index('mnth'))
        except Exception as e:
            st.error(f"Gagal menampilkan grafik: {e}")

    # Tab 2
    with tab2:
        st.header("Fluktuasi Jumlah Pengguna Sepanjang Tahun")
        try:
            monthly_trends = day_df.groupby('mnth')[['casual', 'registered']].sum().reset_index(drop=False)

            if monthly_trends.empty:
                st.info("Tidak cukup data untuk menampilkan grafik ini.")
            else:
                fig2 = go.Figure()
                fig2.add_scatter(x=monthly_trends['mnth'], y=monthly_trends['casual'], mode='lines+markers',
                                  name='Kasual', line_color=PRIMARY_COLOR)
                fig2.add_scatter(x=monthly_trends['mnth'], y=monthly_trends['registered'], mode='lines+markers',
                                  name='Terdaftar', line_color=SECONDARY_COLOR)
                fig2.update_layout(title="Tren Pengguna Kasual vs Terdaftar Sepanjang Tahun",
                                    xaxis_title="Bulan", yaxis_title="Jumlah Pengguna", xaxis=dict(tickmode='linear'))
                st.plotly_chart(fig2, use_container_width=True)

                st.info("""
                **Insight:**
                - Kedua tipe pengguna menunjukkan tren serupa dengan puncak di pertengahan tahun dan titik terendah di awal tahun.
                - Fluktuasi pengguna kasual jauh lebih tajam, menegaskan sifat sensitif mereka terhadap musim dan cuaca.
                """)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Statistik Pengguna Kasual")
                    found, idx, _ = safe_idxmax(monthly_trends['casual'])
                    st.metric("Rata-rata Bulanan", f"{int(safe_mean(monthly_trends['casual'])):,}")
                    if found:
                        casual_idxmax = monthly_trends.loc[idx, 'mnth']
                        st.metric("Puncak Tertinggi", f"Bulan {casual_idxmax} ({int(monthly_trends['casual'].max()):,})")
                    else:
                        st.metric("Puncak Tertinggi", "Tidak tersedia")
                with col2:
                    st.subheader("Statistik Pengguna Terdaftar")
                    found, idx, _ = safe_idxmax(monthly_trends['registered'])
                    st.metric("Rata-rata Bulanan", f"{int(safe_mean(monthly_trends['registered'])):,}")
                    if found:
                        reg_idxmax = monthly_trends.loc[idx, 'mnth']
                        st.metric("Puncak Tertinggi", f"Bulan {reg_idxmax} ({int(monthly_trends['registered'].max()):,})")
                    else:
                        st.metric("Puncak Tertinggi", "Tidak tersedia")
        except Exception as e:
            st.error(f"Gagal menampilkan grafik: {e}")

    # Tab 3
    with tab3:
        st.header("Analisis Pertumbuhan Pengguna Bulanan")
        try:
            monthly_sum = day_df.groupby('mnth')[['casual', 'registered']].sum()
            monthly_growth = monthly_sum.pct_change()
            # Bersihkan inf/-inf akibat pembagian dengan 0 sebelum dipakai
            monthly_growth = monthly_growth.replace([np.inf, -np.inf], np.nan).fillna(0) * 100
            monthly_growth = monthly_growth.reset_index(drop=False)

            if len(monthly_growth) > 1:
                found_c, max_casual_idx, _ = safe_idxmax(monthly_growth['casual'])
                found_r, max_registered_idx, _ = safe_idxmax(monthly_growth['registered'])

                n = len(monthly_growth)
                colors_casual = [ACCENT_COLOR_LIGHT] * n
                if found_c and max_casual_idx in monthly_growth.index:
                    colors_casual[monthly_growth.index.get_loc(max_casual_idx)] = PRIMARY_COLOR

                colors_registered = [SECONDARY_COLOR] * n
                if found_r and max_registered_idx in monthly_growth.index:
                    colors_registered[monthly_growth.index.get_loc(max_registered_idx)] = ACCENT_COLOR_DARK

                fig3 = go.Figure()
                fig3.add_bar(x=monthly_growth['mnth'], y=monthly_growth['casual'], name='Kasual',
                             marker_color=colors_casual)
                fig3.add_bar(x=monthly_growth['mnth'], y=monthly_growth['registered'], name='Terdaftar',
                             marker_color=colors_registered)
                fig3.add_hline(y=0, line_color="black", line_width=1)
                fig3.update_layout(title="Pertumbuhan Pengguna per Bulan (%)", xaxis_title="Bulan",
                                    yaxis_title="Pertumbuhan (%)", barmode='group', xaxis=dict(tickmode='linear'))
                st.plotly_chart(fig3, use_container_width=True)

                st.info("""
                **Insight:**
                - Pertumbuhan paling signifikan umumnya terjadi saat transisi musim, seperti dari musim dingin ke musim semi.
                - Pertumbuhan negatif menunjukkan penurunan jumlah pengguna dibandingkan bulan sebelumnya.
                """)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Pertumbuhan Tertinggi (Kasual)")
                    if found_c:
                        row = monthly_growth.loc[max_casual_idx]
                        st.metric("Bulan", f"{int(row['mnth'])}", f"{row['casual']:.1f}%")
                    else:
                        st.metric("Bulan", "Tidak tersedia")
                with col2:
                    st.subheader("Pertumbuhan Tertinggi (Terdaftar)")
                    if found_r:
                        row = monthly_growth.loc[max_registered_idx]
                        st.metric("Bulan", f"{int(row['mnth'])}", f"{row['registered']:.1f}%")
                    else:
                        st.metric("Bulan", "Tidak tersedia")
            else:
                st.info("Data tidak cukup untuk menampilkan grafik pertumbuhan bulanan.")
        except Exception as e:
            st.error(f"Gagal menampilkan grafik: {e}")

    # Tab 4
    with tab4:
        st.header("Pola Penggunaan Sepeda Sepanjang Hari")
        try:
            hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index(drop=False)

            if hourly_avg.empty:
                st.info("Tidak cukup data untuk menampilkan grafik ini.")
            else:
                fig4 = go.Figure()
                fig4.add_scatter(x=hourly_avg['hr'], y=hourly_avg['cnt'], mode='lines+markers',
                                  line_color=PRIMARY_COLOR, name='Rata-rata')

                peak_morning_hour = 8
                peak_evening_hour = 17
                peak_rows = hourly_avg[hourly_avg['hr'].isin([peak_morning_hour, peak_evening_hour])]
                if not peak_rows.empty:
                    fig4.add_scatter(x=peak_rows['hr'], y=peak_rows['cnt'], mode='markers',
                                      marker=dict(color=ACCENT_COLOR_DARK, size=12), name='Jam Puncak')

                fig4.update_layout(title="Rata-rata Penggunaan Sepeda per Jam", xaxis_title="Jam dalam Sehari",
                                    yaxis_title="Jumlah Peminjaman Rata-rata", xaxis=dict(tickmode='linear', dtick=1))
                st.plotly_chart(fig4, use_container_width=True)

                st.info("""
                **Insight:**
                - Terdapat dua puncak penggunaan yang jelas: **pagi (sekitar 08:00)** dan **sore (sekitar 17:00)**, yang berkorelasi dengan jam komuter.
                - Pola ini menunjukkan bahwa sepeda banyak digunakan sebagai moda transportasi untuk aktivitas rutin harian.
                """)

                st.subheader("Perbandingan Jam Sibuk vs Jam Tidak Sibuk")

                def group_hours(hour):
                    return 'Jam Sibuk' if 7 <= hour <= 9 or 16 <= hour <= 18 else 'Jam Tidak Sibuk'

                hour_df_tab4 = hour_df.copy()
                hour_df_tab4['kelompok_jam'] = hour_df_tab4['hr'].apply(group_hours)
                cluster_counts = hour_df_tab4.groupby('kelompok_jam')['cnt'].sum().reset_index(drop=False)
                cluster_counts = cluster_counts.sort_values('cnt', ascending=False)

                if not cluster_counts.empty:
                    colors_cluster = ([PRIMARY_COLOR, ACCENT_COLOR_LIGHT] * len(cluster_counts))[:len(cluster_counts)]
                    fig5 = go.Figure()
                    fig5.add_bar(
                        x=cluster_counts['cnt'],
                        y=cluster_counts['kelompok_jam'],
                        orientation='h',
                        marker_color=colors_cluster
                    )
                    fig5.update_layout(title="Total Peminjaman: Jam Sibuk vs Tidak Sibuk",
                                        xaxis_title="Total Peminjaman", yaxis_title="Kelompok Jam")
                    st.plotly_chart(fig5, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal menampilkan grafik: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Proyek Analisis Data dan Dashboard Bike Sharing")