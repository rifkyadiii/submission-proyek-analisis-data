import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Peminjaman Sepeda",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    day_df = pd.read_csv("../data/day.csv")
    hour_df = pd.read_csv("../data/hour.csv")
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Judul dashboard
st.title("🚲 Dashboard Analisis Peminjaman Sepeda")

# Sidebar
st.sidebar.header("Proyek Analisis Data: Bike Sharing Dataset")
st.sidebar.markdown("**Nama:** Moch Rifky Aulia Adikusumah")
st.sidebar.markdown("**Email:** rifkyadi67@gmail.com")
st.sidebar.markdown("**ID Dicoding:** rifkyadi")

# Tab
tab1, tab2, tab3, tab4 = st.tabs([
    "Perbandingan Pengguna",
    "Fluktuasi Tahunan",
    "Pertumbuhan Bulanan",
    "Pola Penggunaan Harian"
])

# Tab 1: Perbandingan Pengguna Kasual dan Terdaftar
with tab1:
    st.header("Perbandingan Jumlah Pengguna Kasual dan Terdaftar per Bulan")
    
    monthly_data = day_df.groupby('mnth')[['casual', 'registered']].sum()
    monthly_data = monthly_data.rename(columns={'casual': 'Kasual', 'registered': 'Terdaftar'})
    
    kasual_avg = monthly_data['Kasual'].mean()
    terdaftar_avg = monthly_data['Terdaftar'].mean()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ["#1f77b4", "#ff7f0e"]
    monthly_data.plot(kind='bar', color=colors, ax=ax, edgecolor='black', linewidth=0.7)
    
    ax.axhline(kasual_avg, color='#1f77b4', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.axhline(terdaftar_avg, color='#ff7f0e', linestyle='--', linewidth=1.5, alpha=0.8)
    
    ax.set_title('Perbandingan Pengguna Kasual dan Terdaftar per Bulan', fontsize=14, fontweight='bold')
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Jumlah Pengguna', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    
    st.pyplot(fig)
    
    st.info("""
    **Insight:**
    -   Pengguna terdaftar secara konsisten mendominasi jumlah pengguna secara keseluruhan.
    -   Pengguna kasual mengalami fluktuasi musiman yang lebih besar.
    -   Strategi untuk mempertahankan dan meningkatkan pengguna terdaftar lebih efektif dalam jangka panjang.
    """)
    
    st.subheader("Data Perbandingan Pengguna")
    st.dataframe(monthly_data)

# Tab 2: Fluktuasi Sepanjang Tahun
with tab2:
    st.header("Fluktuasi Jumlah Pengguna Sepanjang Tahun")
    
    casual_data = day_df.groupby('mnth')['casual'].sum()
    registered_data = day_df.groupby('mnth')['registered'].sum()
    
    casual_avg = casual_data.mean()
    registered_avg = registered_data.mean()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    
    x_labels = np.arange(len(casual_data.index))
    
    ax.plot(x_labels, casual_data, marker='o', linestyle='-', linewidth=2, color='tab:blue', label="Kasual")
    ax.plot(x_labels, registered_data, marker='o', linestyle='-', linewidth=2, color='tab:orange', label="Terdaftar")
    
    ax.axhline(casual_avg, color='blue', linestyle='--', linewidth=1.5)
    ax.axhline(registered_avg, color='orange', linestyle='--', linewidth=1.5)
    
    ax.set_xticks(x_labels)
    ax.set_xticklabels(casual_data.index)
    ax.set_title("Tren Pengguna Kasual dan Terdaftar Sepanjang Tahun", fontsize=16, fontweight='bold')
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Jumlah Pengguna', fontsize=12)
    ax.legend(fontsize=10, loc="upper left")
    
    st.pyplot(fig)
    
    st.info("""
    **Insight:**
    -   Kedua jenis pengguna mengalami fluktuasi sepanjang tahun, tetapi dengan pola yang berbeda.
    -   Pengguna kasual menunjukkan fluktuasi yang lebih besar dan pola musiman yang lebih kuat.
    -   Pengguna terdaftar menunjukkan stabilitas yang lebih besar dan fluktuasi yang lebih halus.
    -   Perbedaan ini mungkin disebabkan oleh perbedaan perilaku dan motivasi antara kedua jenis pengguna.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Statistik Pengguna Kasual")
        st.metric("Rata-rata Bulanan", f"{int(casual_avg):,}")
        st.metric("Bulan Tertinggi", f"Bulan {casual_data.idxmax()} ({int(casual_data.max()):,})")
        st.metric("Bulan Terendah", f"Bulan {casual_data.idxmin()} ({int(casual_data.min()):,})")
    
    with col2:
        st.subheader("Statistik Pengguna Terdaftar")
        st.metric("Rata-rata Bulanan", f"{int(registered_avg):,}")
        st.metric("Bulan Tertinggi", f"Bulan {registered_data.idxmax()} ({int(registered_data.max()):,})")
        st.metric("Bulan Terendah", f"Bulan {registered_data.idxmin()} ({int(registered_data.min()):,})")

# Tab 3: Pertumbuhan Bulanan
with tab3:
    st.header("Pertumbuhan Pengguna Bulanan Yang Signifikan")
    
    casual_growth = day_df.groupby('mnth')['casual'].sum().pct_change() * 100
    registered_growth = day_df.groupby('mnth')['registered'].sum().pct_change() * 100
    
    max_casual_idx = casual_growth.idxmax()
    max_registered_idx = registered_growth.idxmax()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    x_labels = np.arange(len(casual_growth.index))
    
    light_blue = "#a6c8ff"
    light_orange = "#ffcc99"
    
    bars1 = ax.bar(
        x_labels - 0.2, casual_growth, width=0.4, label='Kasual', color=light_blue
    )
    bars2 = ax.bar(
        x_labels + 0.2, registered_growth, width=0.4, label='Terdaftar', color=light_orange
    )
    
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        if casual_growth.index[i] == max_casual_idx:
            bar1.set_color("tab:blue") 
            bar1.set_edgecolor('black')
        if registered_growth.index[i] == max_registered_idx:
            bar2.set_color("tab:orange") 
            bar2.set_edgecolor('black')
    
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Pertumbuhan (%)', fontsize=12)
    ax.set_title('Pertumbuhan Pengguna Kasual dan Terdaftar per Bulan', fontsize=14, fontweight='bold')
    
    ax.set_xticks(x_labels)
    ax.set_xticklabels(casual_growth.index)
    ax.axhline(0, color='black', linewidth=1, linestyle='--')
    ax.legend(fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig)
    
    st.info("""
    **Insight:**
    -   Bulan ke-3 menunjukkan pertumbuhan paling signifikan untuk kedua jenis pengguna.
    -   Hal ini mungkin disebabkan oleh faktor musiman, promosi khusus, atau perubahan kondisi cuaca.
    -   Pertumbuhan negatif di beberapa bulan menunjukkan penurunan dibandingkan bulan sebelumnya.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pertumbuhan Tertinggi - Pengguna Kasual")
        st.metric("Bulan", f"Bulan {max_casual_idx}", f"{casual_growth.max():.1f}%")
    
    with col2:
        st.subheader("Pertumbuhan Tertinggi - Pengguna Terdaftar")
        st.metric("Bulan", f"Bulan {max_registered_idx}", f"{registered_growth.max():.1f}%")

# Tab 4: Pola Penggunaan Harian
with tab4:
    st.header("Pola Penggunaan Sepeda Sepanjang Hari")
    
    hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()
    
    def group_hours(hour):
        if 7 <= hour <= 9 or 16 <= hour <= 18:
            return 'Jam Sibuk'
        else:
            return 'Jam Tidak Sibuk'
    
    hour_df['kelompok_jam'] = hour_df['hr'].apply(group_hours)
    cluster_characteristics = hour_df.groupby('kelompok_jam').agg({
        'weathersit': 'mean',
        'temp': 'mean',
        'weekday': lambda x: np.bincount(x.astype(int)).argmax(),
        'cnt': 'mean'
    }).reset_index()

    # Grafik garis untuk pola per jam
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=hourly_avg, marker='o', linewidth=2, ax=ax1)
        
    peak_morning = hourly_avg.iloc[hourly_avg.loc[(hourly_avg['hr'] >= 7) & (hourly_avg['hr'] <= 9)]['cnt'].idxmax()]
    peak_evening = hourly_avg.iloc[hourly_avg.loc[(hourly_avg['hr'] >= 16) & (hourly_avg['hr'] <= 18)]['cnt'].idxmax()]
        
    ax1.scatter([peak_morning['hr'], peak_evening['hr']], 
               [peak_morning['cnt'], peak_evening['cnt']], 
               color='red', s=100, zorder=5)
        
    ax1.set_title('Rata-rata Penggunaan Sepeda per Jam', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Jam', fontsize=12)
    ax1.set_ylabel('Rata-rata Penggunaan', fontsize=12)
    ax1.set_xticks(range(24))
    ax1.grid(True, linestyle='--', alpha=0.7)
        
    ax1.annotate(f'Puncak Pagi: {int(peak_morning["cnt"])}', 
        xy=(peak_morning['hr'], peak_morning['cnt']),
        xytext=(peak_morning['hr']-1, peak_morning['cnt']+30),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))
        
    ax1.annotate(f'Puncak Sore: {int(peak_evening["cnt"])}', 
        xy=(peak_evening['hr'], peak_evening['cnt']),
        xytext=(peak_evening['hr']+1, peak_evening['cnt']+30),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))
        
    st.pyplot(fig1)
    
    cluster_characteristics = cluster_characteristics.sort_values(by="cnt", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(5, 5))

    colors = ["#1f77b4" if cnt == cluster_characteristics["cnt"].max() else "#a6c8ff" 
            for cnt in cluster_characteristics["cnt"]]

    wedges, texts, autotexts = ax2.pie(
        cluster_characteristics["cnt"],
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"linewidth": 1, "edgecolor": "white"}
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    ax2.set_title("Proporsi Penggunaan Sepeda\nJam Sibuk vs Jam Tidak Sibuk", fontsize=12, fontweight='bold')

    st.pyplot(fig2)

    
    st.info("""
    **Insight:**
    -   Terdapat dua puncak penggunaan sepeda: pagi hari (saat berangkat kerja/sekolah) dan sore hari (saat pulang).
    -   Jam sibuk mendominasi total penggunaan sepeda meskipun durasinya lebih pendek.
    -   Penggunaan terendah terjadi pada dini hari.
    -   Pola ini menunjukkan bahwa banyak pengguna menggunakan sepeda sebagai transportasi untuk aktivitas rutin harian.
    """)
    
st.subheader("Karakteristik Kelompok Jam")

weekday_names = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
cluster_characteristics['weekday'] = cluster_characteristics['weekday'].map(weekday_names)

weather_map = {
    1: "Cerah", 
    2: "Berawan/Berkabut", 
    3: "Hujan Ringan", 
    4: "Hujan Deras"
}

pretty_table = cluster_characteristics.copy()
pretty_table['weathersit'] = pretty_table['weathersit'].apply(lambda x: f"{x:.2f}")
pretty_table['temp'] = pretty_table['temp'].apply(lambda x: f"{x*41:.1f}°C")  # Asumsi temp dinormalisasi
pretty_table['cnt'] = pretty_table['cnt'].apply(lambda x: f"{int(x)}")

pretty_table.columns = ["Kelompok Jam", "Rata-rata Kondisi Cuaca", "Rata-rata Suhu", "Hari Paling Umum", "Rata-rata Jumlah Pengguna"]

st.dataframe(pretty_table, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Moch Rifky Aulia Adikusumah | Submission Dicoding")