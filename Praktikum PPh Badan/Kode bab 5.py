import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Parameter dasar
pendapatan = 1_000_000_000  # Pendapatan tahunan (Rp)
biaya_operasional = 400_000_000  # Biaya operasional (Rp)
nilai_aset = 500_000_000  # Nilai aset untuk depresiasi (Rp)
umur_aset = 5  # Umur ekonomis aset (tahun)
tarif_pph = 0.25  # Tarif PPh Badan 25%

# Fungsi untuk menghitung depresiasi garis lurus
def depresiasi_garis_lurus(nilai_aset, umur_aset):
    return nilai_aset / umur_aset

# Fungsi untuk menghitung depresiasi saldo menurun (double declining balance)
def depresiasi_saldo_menurun(nilai_aset, umur_aset, tahun):
    tarif = 2 / umur_aset
    nilai_buku = nilai_aset
    for i in range(tahun):
        nilai_buku = nilai_buku * (1 - tarif)
    return nilai_aset * tarif if tahun == 1 else (nilai_aset - sum(depresiasi_saldo_menurun(nilai_aset, umur_aset, i) for i in range(1, tahun))) * tarif

# Skenario 1: Normal
def skenario_normal(pendapatan, biaya_operasional, nilai_aset, umur_aset):
    depresiasi = depresiasi_garis_lurus(nilai_aset, umur_aset)
    laba_kotor = pendapatan - biaya_operasional
    laba_bersih = laba_kotor - depresiasi
    pph = laba_bersih * tarif_pph if laba_bersih > 0 else 0
    return {"depresiasi": depresiasi, "laba_kotor": laba_kotor, "laba_bersih": laba_bersih, "pph": pph}

# Skenario 2: Tax Holiday
def skenario_tax_holiday(pendapatan, biaya_operasional, nilai_aset, umur_aset):
    depresiasi = depresiasi_garis_lurus(nilai_aset, umur_aset)
    laba_kotor = pendapatan - biaya_operasional
    laba_bersih = laba_kotor - depresiasi
    pph = 0  # Tax holiday, PPh dibebaskan
    return {"depresiasi": depresiasi, "laba_kotor": laba_kotor, "laba_bersih": laba_bersih, "pph": pph}

# Skenario 3: Perbandingan Metode Depresiasi
def skenario_perbandingan_depresiasi(pendapatan, biaya_operasional, nilai_aset, umur_aset):
    # Depresiasi garis lurus
    dep_garis_lurus = depresiasi_garis_lurus(nilai_aset, umur_aset)
    laba_kotor_gl = pendapatan - biaya_operasional
    laba_bersih_gl = laba_kotor_gl - dep_garis_lurus
    pph_gl = laba_bersih_gl * tarif_pph if laba_bersih_gl > 0 else 0

    # Depresiasi saldo menurun
    dep_saldo_menurun = depresiasi_saldo_menurun(nilai_aset, umur_aset, 1)
    laba_kotor_sm = pendapatan - biaya_operasional
    laba_bersih_sm = laba_kotor_sm - dep_saldo_menurun
    pph_sm = laba_bersih_sm * tarif_pph if laba_bersih_sm > 0 else 0

    return {
        "garis_lurus": {"depresiasi": dep_garis_lurus, "laba_kotor": laba_kotor_gl, "laba_bersih": laba_bersih_gl, "pph": pph_gl},
        "saldo_menurun": {"depresiasi": dep_saldo_menurun, "laba_kotor": laba_kotor_sm, "laba_bersih": laba_bersih_sm, "pph": pph_sm}
    }

# Menjalankan perhitungan
hasil_normal = skenario_normal(pendapatan, biaya_operasional, nilai_aset, umur_aset)
hasil_tax_holiday = skenario_tax_holiday(pendapatan, biaya_operasional, nilai_aset, umur_aset)
hasil_depresiasi = skenario_perbandingan_depresiasi(pendapatan, biaya_operasional, nilai_aset, umur_aset)

# Data untuk visualisasi
labels = ['Normal', 'Tax Holiday', 'Garis Lurus', 'Saldo Menurun']
pph_values = [
    hasil_normal['pph'],
    hasil_tax_holiday['pph'],
    hasil_depresiasi['garis_lurus']['pph'],
    hasil_depresiasi['saldo_menurun']['pph']
]

# Diagram Batang
plt.figure(figsize=(10, 6))
plt.bar(labels, pph_values, color=['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728'])
plt.title('Perbandingan PPh - Diagram Batang')
plt.ylabel('PPh (Rp)')
plt.xlabel('Skenario')
plt.grid(axis='y')
plt.savefig('pph_bar_chart.png')
plt.close()

# Diagram Garis
plt.figure(figsize=(10, 6))
plt.plot(labels, pph_values, marker='o', linestyle='-', color='#1f77b4', markersize=8)
plt.title('Perbandingan PPh - Diagram Garis')
plt.ylabel('PPh (Rp)')
plt.xlabel('Skenario')
plt.grid(True)
plt.savefig('pph_line_chart.png')
plt.close()

# Diagram Lingkaran (Pie Chart)
plt.figure(figsize=(8, 8))
colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
explode = (0, 0.1, 0, 0)  # Memisahkan Tax Holiday untuk penekanan
plt.pie(pph_values, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)
plt.title('Perbandingan PPh - Diagram Lingkaran')
plt.savefig('pph_pie_chart.png')
plt.close()

# Narasi analitis
narasi = f"""
# Analisis Perhitungan PPh

## Skenario 1: Normal
- **Pendapatan**: Rp {pendapatan:,.0f}
- **Biaya Operasional**: Rp {biaya_operasional:,.0f}
- **Depresiasi (Garis Lurus)**: Rp {hasil_normal['depresiasi']:,.0f}
- **Laba Kotor**: Rp {hasil_normal['laba_kotor']:,.0f}
- **Laba Bersih**: Rp {hasil_normal['laba_bersih']:,.0f}
- **PPh**: Rp {hasil_normal['pph']:,.0f}

**Analisis**: Dalam skenario normal, PPh dihitung berdasarkan laba bersih setelah dikurangi biaya operasional dan depresiasi garis lurus. PPh sebesar Rp {hasil_normal['pph']:,.0f} mencerminkan tarif standar 25%.

## Skenario 2: Tax Holiday
- **Pendapatan**: Rp {pendapatan:,.0f}
- **Biaya Operasional**: Rp {biaya_operasional:,.0f}
- **Depresiasi (Garis Lurus)**: Rp {hasil_tax_holiday['depresiasi']:,.0f}
- **Laba Kotor**: Rp {hasil_tax_holiday['laba_kotor']:,.0f}
- **Laba Bersih**: Rp {hasil_tax_holiday['laba_bersih']:,.0f}
- **PPh**: Rp {hasil_tax_holiday['pph']:,.0f}

**Analisis**: Dalam skenario tax holiday, PPh dibebaskan sepenuhnya, sehingga tidak ada kewajiban pajak meskipun laba bersih tetap sama seperti skenario normal. Ini memberikan keuntungan signifikan bagi perusahaan.

## Skenario 3: Perbandingan Metode Depresiasi
### a. Garis Lurus
- **Depresiasi**: Rp {hasil_depresiasi['garis_lurus']['depresiasi']:,.0f}
- **Laba Kotor**: Rp {hasil_depresiasi['garis_lurus']['laba_kotor']:,.0f}
- **Laba Bersih**: Rp {hasil_depresiasi['garis_lurus']['laba_bersih']:,.0f}
- **PPh**: Rp {hasil_depresiasi['garis_lurus']['pph']:,.0f}

### b. Saldo Menurun
- **Depresiasi**: Rp {hasil_depresiasi['saldo_menurun']['depresiasi']:,.0f}
- **Laba Kotor**: Rp {hasil_depresiasi['saldo_menurun']['laba_kotor']:,.0f}
- **Laba Bersih**: Rp {hasil_depresiasi['saldo_menurun']['laba_bersih']:,.0f}
- **PPh**: Rp {hasil_depresiasi['saldo_menurun']['pph']:,.0f}

**Analisis**: Metode depresiasi saldo menurun menghasilkan depresiasi lebih besar di tahun pertama (Rp {hasil_depresiasi['saldo_menurun']['depresiasi']:,.0f}) dibandingkan garis lurus (Rp {hasil_depresiasi['garis_lurus']['depresiasi']:,.0f}), sehingga laba bersih lebih rendah dan PPh lebih kecil di awal periode. Namun, total depresiasi selama umur aset tetap sama.

## Visualisasi
- **Diagram Batang** ('pph_bar_chart.png'): Menunjukkan perbandingan langsung nilai PPh antar skenario, dengan Tax Holiday menonjol karena nilainya nol.
- **Diagram Garis** ('pph_line_chart.png'): Menggambarkan tren PPh antar skenario, dengan penanda titik untuk setiap skenario, memperjelas penurunan drastis pada Tax Holiday.
- **Diagram Lingkaran** ('pph_pie_chart.png'): Menampilkan proporsi PPh antar skenario, meskipun Tax Holiday memiliki porsi 0%, memberikan perspektif visual tentang kontribusi masing-masing skenario.

## Kesimpulan
- **Skenario Normal** menghasilkan PPh standar berdasarkan laba bersih.
- **Tax Holiday** memberikan keuntungan maksimal dengan PPh nol.
- **Metode Depresiasi** memengaruhi PPh di tahun-tahun awal, dengan saldo menurun lebih menguntungkan untuk mengurangi PPh awal.
Gambar visualisasi disimpan sebagai 'pph_bar_chart.png', 'pph_line_chart.png', dan 'pph_pie_chart.png'.
"""

# Simpan narasi ke file
with open('analisis_pph_multichart.md', 'w', encoding='utf-8') as f:
    f.write(narasi)

print("Perhitungan selesai. Visualisasi disimpan sebagai 'pph_bar_chart.png', 'pph_line_chart.png', dan 'pph_pie_chart.png'. Narasi analitis disimpan sebagai 'analisis_pph_multichart.md'.")