# Proyek Analisis Data: Bike Sharing Dataset 🚲
Selamat datang di repositori Proyek Analisis Data Bike Sharing. Proyek ini bertujuan untuk melakukan analisis mendalam terhadap dataset penyewaan sepeda dan menyajikan hasilnya dalam sebuah dasbor web interaktif yang dibangun menggunakan Streamlit.

## 📊 Dashboard Demo
Visualisasi dapat dilihat secara langsung di: [Streamlit App](https://bike-sharing-dataset-data-analysis.streamlit.app/)

<img width="1919" height="1080" alt="image" src="https://github.com/user-attachments/assets/3d22e46a-986c-4ab7-b1e5-94833a6f79c6" />

---

## 📜 Latar Belakang

Dataset Bike Sharing berisi informasi historis tentang jumlah penyewaan sepeda per jam dan per hari selama dua tahun (2011-2012) di sistem Capital Bikeshare, Washington D.C. Data ini mencakup berbagai atribut seperti musim, cuaca, suhu, hari libur, dan jenis pengguna (kasual vs. terdaftar). Analisis terhadap data ini dapat memberikan wawasan berharga untuk mengoptimalkan operasional dan strategi pemasaran.

---

## 🎯 Pertanyaan Bisnis

Analisis ini dirancang untuk menjawab beberapa pertanyaan bisnis utama:

1.  Bagaimana perbandingan jumlah pengguna **kasual** dan **terdaftar** setiap bulannya?
2.  Bagaimana fluktuasi jumlah pengguna sepanjang tahun? Apakah ada perbedaan pola antara kedua jenis pengguna?
3.  Bulan apa yang menunjukkan **pertumbuhan pengguna** paling signifikan dibandingkan dengan bulan sebelumnya?
4.  Bagaimana pola penggunaan sepeda bervariasi sepanjang hari, terutama antara **jam sibuk** dan jam tidak sibuk?

---

## ⚙️ Fitur Dasbor

Dasbor interaktif ini memiliki beberapa fitur utama untuk eksplorasi data:

-   **Filter Data Dinamis**: Pengguna dapat memfilter data berdasarkan:
    -   Rentang Tanggal
    -   Musim (Semi, Panas, Gugur, Dingin)
    -   Tahun (2011, 2012)
    -   Kondisi Cuaca (Cerah, Berawan, Hujan Ringan, Hujan Deras)
-   **Visualisasi Multi-Tab**: Analisis disajikan dalam empat tab terpisah untuk fokus pada setiap pertanyaan bisnis.
-   **Wawasan Langsung**: Setiap visualisasi dilengkapi dengan rangkuman *insight* untuk mempermudah pemahaman.

---

## 🛠️ Teknologi yang Digunakan

-   **Analisis Data**: Python, Pandas, NumPy
-   **Visualisasi Data**: Matplotlib, Seaborn
-   **Dashboard Interaktif**: Streamlit

---

## 🚀 Cara Menjalankan Proyek Secara Lokal

Ikuti langkah-langkah berikut untuk menjalankan dasbor ini di mesin lokal Anda.

1.  **Clone Repositori**
    ```bash
    git clone https://github.com/rifkyadiii/submission-proyek-analisis-data
    ```
    ```bash
    cd submission-proyek-analisis-data
    ```

2.  **Buat Lingkungan Virtual (Opsional tapi Direkomendasikan)**
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
    ```

3.  **Install Dependensi**
    Pastikan Anda memiliki file `requirements.txt` dengan konten berikut:
    ```
    streamlit
    pandas
    numpy
    matplotlib
    seaborn
    ```
    Kemudian, jalankan perintah instalasi:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Streamlit**
    Pastikan Anda berada di direktori utama proyek, lalu jalankan:
    ```bash
    streamlit run dashboard/dashboard.py
    ```
    Aplikasi akan terbuka secara otomatis di browser Anda.

---

## 📁 Struktur Repositori
```
.
├── dashboard/
│   └── dashboard.py      # Script utama untuk aplikasi Streamlit
│
├── data/
│   ├── day.csv           # Dataset dengan agregasi harian
│   └── hour.csv          # Dataset dengan agregasi per jam
│
├── notebook.ipynb        # Notebook Jupyter berisi proses analisis data secara lengkap
├── requirements.txt      # File daftar dependensi Python yang diperlukan
└── README.md             # Dokumentasi proyek (file ini)
```
