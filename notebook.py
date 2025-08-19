#!/usr/bin/env python
# coding: utf-8

# # Proyek Analisis Data: Bike Sharing Dataset
# - **Nama:** Moch Rifky Aulia Adikusumah
# - **Email:** rifkyadi67@gmail.com
# - **ID Dicoding:** rifkyadi

# ## Menentukan Pertanyaan Bisnis

# 1. Bagaimana perbandingan jumlah pengguna kasual dan terdaftar setiap bulannya?
# 2. Bagaimana fluktuasi jumlah pengguna kasual dan terdaftar sepanjang tahun? Apakah ada perbedaan pola fluktuasi antara kedua jenis pengguna?
# 3. Bulan apa yang menunjukkan pertumbuhan pengguna kasual dan terdaftar paling signifikan dibandingkan dengan bulan sebelumnya?
# 4. Bagaimana pola penggunaan sepeda bervariasi sepanjang hari, terutama antara jam sibuk dan jam tidak sibuk, dan faktor-faktor apa saja yang mempengaruhi variasi tersebut?

# ## Import Semua Packages/Library yang Digunakan

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ## Data Wrangling

# ### Gathering Data

# In[2]:


# Tabel day

day_df = pd.read_csv("data/day.csv")
day_df.head()


# In[3]:


# Tabel hour

hour_df = pd.read_csv("data/hour.csv")
hour_df.head()


# **Insight:**
# - Kedua dataset memiliki struktur yang serupa, dengan kolom-kolom yang memberikan informasi tentang waktu, kondisi cuaca, dan jumlah penyewaan sepeda.
# - Dataset hour.csv memberikan detail per jam, sedangkan day.csv memberikan detail per hari.

# ### Assessing Data

# In[4]:


# MENILAI DATA day_df

# Periksa Tipe Data
day_df.info()


# In[5]:


# Periksa duplikasi
print("Jumlah duplikasi: ", day_df.duplicated().sum())


# In[6]:


# Ringkasam Parameter Statistik
day_df.describe()


# In[7]:


# MENILAI DATA hour_df

# Periksa Tipe Data
hour_df.info()


# In[8]:


# Periksa duplikasi
print("Jumlah duplikasi: ", hour_df.duplicated().sum())


# In[9]:


# Ringkasam Parameter Statistik
hour_df.describe()


# **Insight:**
# - Tipe Data:
# 
#     - Kolom dteday perlu diubah menjadi tipe data datetime untuk analisis berbasis waktu.
# 
# - Dropping:
#     - Kolom instant hanya record index, sepertinya tidak terpakai jadi lebih baik dihapus agar data lebih bersih
# 
# - Missing Values:
# 
#     Kedua dataset tidak memiliki missing values.
# 
# - Duplikasi Data:
# 
#     Kedua dataset tidak memiliki duplikasi data.
# 
# - Statistik Deskriptif:
# 
#     - Jumlah penyewaan sepeda bervariasi secara signifikan, baik per jam maupun per hari.
#     - Rata-rata pengguna terdaftar jauh lebih tinggi daripada pengguna kasual.
#     - Kondisi cuaca (suhu, kelembaban, kecepatan angin) bervariasi sepanjang waktu.
#     - Pada dataset hour, rata-rata jam adalah sekitar jam 11,5 yang berarti data tersebar selama 24 jam.

# ### Cleaning Data

# In[10]:


# Hapus kolom instant

hour_df.drop(['instant'], axis = 1, inplace= True)
day_df.drop(['instant'], axis = 1, inplace= True)

hour_df.head()


# In[11]:


# Ubah tipe data object ke date
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

print(hour_df['dteday'].dtype)
print(day_df['dteday'].dtype)


# **Insight:**
# - Sudah berhasil mengubah tipe data kolom dteday menjadi datetime
# - Menghapus kolom instant

# ## Exploratory Data Analysis (EDA)

# ### Explore ...

# In[12]:


# Penggunaan sepeda per musim (day_df)
pivot_season = pd.pivot_table(day_df, values='cnt', index='season', aggfunc='sum', observed=True)
pivot_season.head()


# In[13]:


# Penggunaan sepeda per hari kerja (day_df)
pivot_workingday = pd.pivot_table(day_df, values='cnt', index='workingday', aggfunc='mean')
pivot_workingday.head()


# In[14]:


# Penggunaan sepeda per bulan (day_df)
pivot_month = pd.pivot_table(day_df, values='cnt', index='mnth', aggfunc='mean', observed=True)
pivot_month.head(12)


# In[15]:


# Penggunaan sepeda per jam (hour_df)
pivot_hour = pd.pivot_table(hour_df, values='cnt', index='hr', aggfunc='mean')
pivot_hour.head(24)


# In[16]:


# Distribusi Penggunaan Sepeda (Harian)
distribusi_harian = day_df['cnt'].describe()
distribusi_harian.head(10)


# In[17]:


# Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda
pengaruh_cuaca = pd.pivot_table(day_df, values='cnt', index='weathersit', aggfunc='mean', observed=True)
pengaruh_cuaca.head()


# In[18]:


# Hubungan Suhu dan Penggunaan Sepeda
korelasi_suhu = day_df[['temp', 'cnt']].corr()
korelasi_suhu.head()


# In[19]:


# Pengaruh Hari dalam Seminggu terhadap Penggunaan Sepeda
pengaruh_hari = pd.pivot_table(day_df, values='cnt', index='weekday', aggfunc='mean', observed=True)
pengaruh_hari.head(7)


# In[20]:


# Perbandingan Pengguna Casual dan Registered per Bulan
perbandingan_pengguna = day_df.groupby('mnth', observed=True)[['casual', 'registered']].sum()
perbandingan_pengguna.head(12)


# In[21]:


# Bandingkan pengguna kasual dan terdaftar
data = day_df.groupby('mnth')[['casual', 'registered']].sum()
data = data.rename(columns={'casual': 'Kasual', 'registered': 'Terdaftar'})

# Hitung rata-rata
data.loc['Rata-rata'] = data.mean()

# Tampilkan tabel
print(data)


# In[22]:


# Menghitung pertumbuhan pengguna per bulan
casual_growth = day_df.groupby('mnth')['casual'].sum().pct_change() * 100
registered_growth = day_df.groupby('mnth')['registered'].sum().pct_change() * 100

# Menggabungkan data ke dalam tabel
growth_table = pd.DataFrame({
    'Kasual (%)': casual_growth,
    'Terdaftar (%)': registered_growth
})

# Menampilkan tabel
print(growth_table)


# **Insight:**
# - Musiman: Penggunaan sepeda sangat dipengaruhi oleh musim, dengan puncak penggunaan di musim hangat (musim semi dan musim panas) dan penurunan di musim dingin.
# - Harian: Penggunaan sepeda juga dipengaruhi oleh hari dalam seminggu, dengan hari kerja menunjukkan tingkat penggunaan yang lebih tinggi dan puncak pada hari Jumat.
# - Jam: Penggunaan sepeda memiliki pola harian yang jelas, dengan puncak di jam sibuk komuter (pagi dan sore) dan penggunaan terendah di jam sepi (dini hari).
# - Cuaca: Kondisi cuaca memiliki pengaruh signifikan terhadap penggunaan sepeda, dengan cuaca cerah mendorong penggunaan dan cuaca buruk menghambatnya.
# - Suhu: Terdapat korelasi positif yang cukup kuat antara suhu dan penggunaan sepeda. Semakin tinggi suhu, semakin tinggi kemungkinan orang menggunakan sepeda.
# - Tipe Pengguna: Pengguna terdaftar secara konsisten mendominasi penggunaan sepeda dibandingkan pengguna kasual.

# ## Visualization & Explanatory Analysis

# ### Pertanyaan 1: Bagaimana perbandingan jumlah pengguna kasual dan terdaftar setiap bulannya?

# In[23]:


sns.set_style("white")
plt.figure(figsize=(12, 6))

colors = ["#1f77b4", "#ff7f0e"]  
data = day_df.groupby('mnth')[['casual', 'registered']].sum()
data = data.rename(columns={'casual': 'Kasual', 'registered': 'Terdaftar'})

kasual_avg = data['Kasual'].mean()
terdaftar_avg = data['Terdaftar'].mean()

data.plot(kind='bar', color=colors, edgecolor='black', linewidth=0.7)

plt.axhline(kasual_avg, color='#1f77b4', linestyle='--', linewidth=1.5, alpha=0.8)
plt.axhline(terdaftar_avg, color='#ff7f0e', linestyle='--', linewidth=1.5, alpha=0.8)

plt.title('Perbandingan Pengguna Kasual dan Terdaftar per Bulan', fontsize=14, fontweight='bold')
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Jumlah Pengguna', fontsize=12)

plt.xticks(rotation=0)
plt.legend(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


# Grafik menunjukkan bahwa pengguna terdaftar mendominasi jumlah pengguna secara keseluruhan. Meskipun pengguna kasual mengalami fluktuasi, jumlah mereka selalu jauh lebih rendah dibandingkan pengguna terdaftar. Hal ini menunjukkan bahwa strategi untuk mempertahankan dan meningkatkan jumlah pengguna terdaftar mungkin lebih efektif dalam jangka panjang.

# ### Pertanyaan 2: Bagaimana fluktuasi jumlah pengguna kasual dan terdaftar sepanjang tahun? Apakah ada perbedaan pola fluktuasi antara kedua jenis pengguna?

# In[24]:


sns.set_style("white")

plt.figure(figsize=(16, 5))

casual_data = day_df.groupby('mnth')['casual'].sum()
registered_data = day_df.groupby('mnth')['registered'].sum()

casual_avg = casual_data.mean()
registered_avg = registered_data.mean()

x_labels = np.arange(len(casual_data.index))

plt.plot(x_labels, casual_data, marker='o', linestyle='-', linewidth=2, color='tab:blue', label="Kasual")
plt.plot(x_labels, registered_data, marker='o', linestyle='-', linewidth=2, color='tab:orange', label="Terdaftar")

plt.axhline(casual_avg, color='blue', linestyle='--', linewidth=1.5)
plt.axhline(registered_avg, color='orange', linestyle='--', linewidth=1.5)

plt.xticks(x_labels, casual_data.index)

plt.title("Tren Pengguna Kasual dan Terdaftar Sepanjang Tahun", fontsize=16, fontweight='bold')
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Jumlah Pengguna', fontsize=12)
plt.legend(fontsize=10, loc="upper left")

plt.grid(False)
plt.show()


# Kedua jenis pengguna mengalami fluktuasi sepanjang tahun, namun dengan pola dan amplitudo yang berbeda. Pengguna kasual menunjukkan fluktuasi yang lebih besar dan pola musiman yang lebih kuat, sementara pengguna terdaftar menunjukkan stabilitas yang lebih besar dan fluktuasi yang lebih halus. Perbedaan ini mungkin disebabkan oleh perbedaan perilaku dan motivasi antara pengguna kasual dan terdaftar.

# ### Pertanyaan 3: Bulan apa yang menunjukkan pertumbuhan pengguna kasual dan terdaftar paling signifikan dibandingkan dengan bulan sebelumnya?

# In[25]:


sns.set_style("white")

casual_growth = day_df.groupby('mnth')['casual'].sum().pct_change() * 100
registered_growth = day_df.groupby('mnth')['registered'].sum().pct_change() * 100

max_casual_idx = casual_growth.idxmax()
max_registered_idx = registered_growth.idxmax()

plt.figure(figsize=(14, 7))
x_labels = np.arange(len(casual_growth.index))

light_blue = "#a6c8ff"
light_orange = "#ffcc99"

bars1 = plt.bar(
    x_labels - 0.2, casual_growth, width=0.4, label='Kasual', color=light_blue
)
bars2 = plt.bar(
    x_labels + 0.2, registered_growth, width=0.4, label='Terdaftar', color=light_orange
)

for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    if casual_growth.index[i] == max_casual_idx:
        bar1.set_color("tab:blue") 
        bar1.set_edgecolor('black')
    if registered_growth.index[i] == max_registered_idx:
        bar2.set_color("tab:orange") 
        bar2.set_edgecolor('black')

plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Pertumbuhan (%)', fontsize=12)
plt.title('Pertumbuhan Pengguna Kasual dan Terdaftar per Bulan Paling Signifikan', fontsize=14, fontweight='bold')

plt.xticks(x_labels, casual_growth.index)
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.legend(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


# Bulan ke-3 adalah bulan di mana baik pengguna kasual maupun terdaftar mengalami pertumbuhan paling signifikan dibandingkan bulan sebelumnya. Hal ini menunjukkan bahwa ada faktor tertentu yang mendorong peningkatan jumlah pengguna, baik kasual maupun terdaftar, di bulan tersebut.

# ## Analisis Lanjutan Menggunakan Clustering

# ### Pertanyaan 4: Bagaimana pola penggunaan sepeda bervariasi sepanjang hari, terutama antara jam sibuk dan jam tidak sibuk, dan faktor-faktor apa saja yang mempengaruhi variasi tersebut?

# In[26]:


# Visualisasi rata-rata penggunaan sepeda per jam
hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_avg)
plt.title('Rata-rata Penggunaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Penggunaan Sepeda')
plt.xticks(range(24))
plt.grid(True)
plt.show()


# In[27]:


# Berdasarkan grafik, asumsikan jam sibuk: 7-9 pagi dan 16-18 sore
def group_hours(hour):
    if 7 <= hour <= 9 or 16 <= hour <= 18:
        return 'Jam Sibuk'
    else:
        return 'Jam Tidak Sibuk'

hour_df['kelompok_jam'] = hour_df['hr'].apply(group_hours)

# Analisis karakteristik kelompok jam
cluster_characteristics = hour_df.groupby('kelompok_jam').agg({
    'weathersit': 'mean',
    'temp': 'mean',
    'weekday': lambda x: np.bincount(x.astype(int)).argmax(),  # Modus hari dalam seminggu
    'cnt': 'mean'
}).reset_index()

cluster_characteristics.head()


# In[28]:


# Urutkan data berdasarkan jumlah penggunaan sepeda
cluster_characteristics = cluster_characteristics.sort_values(by="cnt", ascending=False)

colors = ["#1f77b4" if cnt == cluster_characteristics["cnt"].max() else "#a6c8ff" for cnt in cluster_characteristics["cnt"]]
fig, ax = plt.subplots(figsize=(10, 5))

ax.pie(
    cluster_characteristics["cnt"],
    labels=cluster_characteristics["kelompok_jam"],
    autopct="%1.1f%%",
    colors=colors,
    startangle=180,  
    wedgeprops={"linewidth": 0, "edgecolor": "white"}  
)

plt.title("Rata-rata Penggunaan Sepeda per Kelompok Jam", fontsize=14, fontweight="bold")
plt.show()


# Grafik ini dengan jelas menunjukkan perbedaan signifikan dalam rata-rata penggunaan sepeda antara jam sibuk dan jam tidak sibuk, di mana jam sibuk memiliki rata-rata penggunaan yang jauh lebih tinggi, mengindikasikan dominasi aktivitas bersepeda pada jam-jam tersebut yang kemungkinan besar dipengaruhi oleh rutinitas harian seperti berangkat dan pulang kerja atau sekolah.

# ## Conclusion

# 1. **Perbandingan pengguna kasual dan terdaftar setiap bulan**  
#    Pengguna terdaftar selalu lebih banyak dibandingkan pengguna kasual setiap bulannya. Meskipun jumlah pengguna kasual naik turun, mereka tetap jauh lebih sedikit dibandingkan pelanggan yang sudah berlangganan. Ini menunjukkan bahwa layanan penyewaan sepeda lebih banyak dimanfaatkan oleh pengguna tetap.  
# 
# 2. **Fluktuasi jumlah pengguna sepanjang tahun**  
#    Pengguna kasual dan terdaftar sama-sama mengalami perubahan jumlah sepanjang tahun, tapi dengan pola yang berbeda. Pengguna kasual cenderung mengalami lonjakan besar saat cuaca lebih hangat, sementara pengguna terdaftar lebih stabil dan tidak terlalu banyak berubah. Ini menunjukkan bahwa pengguna kasual lebih dipengaruhi oleh faktor musiman, sedangkan pengguna terdaftar lebih rutin dalam menggunakan layanan.  
# 
# 3. **Bulan dengan pertumbuhan pengguna paling signifikan**  
#    Bulan ketiga dalam setahun menunjukkan peningkatan jumlah pengguna yang paling besar, baik untuk pengguna kasual maupun terdaftar. Kemungkinan besar ini disebabkan oleh faktor seperti cuaca yang lebih mendukung atau adanya promosi yang menarik di bulan tersebut.  
# 
# 4. **Pola penggunaan sepeda sepanjang hari**  
#    Jumlah pengguna sepeda paling tinggi di jam-jam sibuk, terutama pagi dan sore hari, yang bertepatan dengan waktu berangkat dan pulang kerja atau sekolah. Hal ini menunjukkan bahwa banyak orang menggunakan sepeda sebagai bagian dari rutinitas harian mereka.
# 
# Secara keseluruhan, analisis ini memberikan gambaran jelas tentang kebiasaan pengguna sepeda dan faktor-faktor yang memengaruhinya. Wawasan ini bisa digunakan untuk meningkatkan layanan, merancang strategi pemasaran yang lebih efektif, dan membuat pengalaman pengguna jadi lebih baik.
