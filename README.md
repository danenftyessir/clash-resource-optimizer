<h1 align="center" style="font-size: 3.5em;">Model Prediktif Relasi Rekurens untuk Optimasi Resource</h1>
<div align="center">
  <img src="docs/clash_of_clans_logo.png" alt="Clash of Clans Logo" width="200"/>
  <br><br>
  <h2 align="center" style="font-size: 2em; font-weight: bold;">Tugas Makalah IF1220 Matematika Diskrit</h2>
  <h3 align="center" style="font-size: 1.75em; font-weight: bold;">Institut Teknologi Bandung</h3>
  <h3 align="center" style="font-size: 1.75em; font-weight: bold;">Semester I Tahun 2024/2025</h3>
</div>
</div>

## Deskripsi
Model prediktif berbasis relasi rekurens untuk optimasi pengelolaan sumber daya dan waktu di Clash of Clans Town Hall 11. Menggunakan Python dan CSV untuk visualisasi dan analisis ROI bangunan, waktu builder, serta distribusi resource. Dibuat untuk tugas IF1220 Matematika Diskrit.

## Fitur

* Pemodelan produksi resource menggunakan relasi rekurens
* Analisis ROI dan prioritas upgrade bangunan
* Optimasi penggunaan waktu builder
* Visualisasi data interaktif
* Database statis berbasis CSV
* Fokus analisis khusus TH11

## Struktur Project
```bash
optimasi-resource-coc/
├── data/
│   ├── th11_buildings.csv
│   ├── upgrade_cost.csv
│   └── production_rates.csv
├── src/
│   ├── models.py
│   ├── utils.py
│   └── analysis.py
├── requirements.txt
└── README.md
```

## Teknologi yang Digunakan

* Python 3.8+
* Pandas untuk pengolahan data
* NumPy untuk komputasi numerik
* Matplotlib dan Seaborn untuk visualisasi
* CSV untuk penyimpanan data

Cara Penggunaan

1. Clone repository:
```bash
git clone https://github.com/username/optimasi-resource-coc.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
Jalankan program:
```bash
python src/analysis.py
```

## Kontributor
Danendra Shafi Athallah - 13523136
Program Studi Teknik Informatika
Institut Teknologi Bandung

## Catatan
Repository ini hanya berisi alat analisis dan tidak memodifikasi file game atau berinteraksi dengan klien Clash of Clans. Dibuat untuk tujuan pendidikan sebagai bagian dari tugas IF1220 Matematika Diskrit.

## Kontak
Untuk pertanyaan dan saran, silakan hubungi:
* Email: danendra1967@gmail.com
* GitHub: @danennftyessir

<div align="center">
© 2024 Danendra Shafi Athallah. All rights reserved.
</div>
