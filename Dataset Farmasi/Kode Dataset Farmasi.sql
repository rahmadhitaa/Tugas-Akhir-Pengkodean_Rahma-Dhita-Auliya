-- Skrip Analitik untuk Dataset Persediaan Farmasi, Pemakaian, dan Penjualan 2023
-- Diasumsikan tabel sudah ada di Google BigQuery

-- 1. Membuat tabel sementara untuk aggregasi persediaan
CREATE TEMP TABLE Persediaan_Agg AS
SELECT 
  Nama_Obat,
  SUM(Jumlah_Unit) AS Total_Unit_Persediaan,
  SUM(Nilai_Persediaan) AS Total_Nilai_Persediaan
FROM `pph-simulasi-dataset.Farmasi.persediaan`
GROUP BY Nama_Obat;

-- 2. Membuat tabel sementara untuk aggregasi pemakaian rawat inap
CREATE TEMP TABLE Pemakaian_Agg AS
SELECT 
  Nama_Obat,
  EXTRACT(MONTH FROM Tanggal_Pemakaian) AS Bulan,
  EXTRACT(YEAR FROM Tanggal_Pemakaian) AS Tahun,
  SUM(Jumlah_Unit) AS Total_Unit_Pemakaian,
  SUM(Nilai_Pemakaian) AS Total_Nilai_Pemakaian
FROM `pph-simulasi-dataset.Farmasi.pemakaian`
GROUP BY Nama_Obat, EXTRACT(YEAR FROM Tanggal_Pemakaian), EXTRACT(MONTH FROM Tanggal_Pemakaian);

-- 3. Membuat tabel sementara untuk aggregasi penjualan rawat jalan
CREATE TEMP TABLE Penjualan_Agg AS
SELECT 
  Nama_Obat,
  EXTRACT(MONTH FROM Tanggal_Penjualan) AS Bulan,
  EXTRACT(YEAR FROM Tanggal_Penjualan) AS Tahun,
  SUM(Jumlah_Unit) AS Total_Unit_Penjualan,
  SUM(Nilai_Penjualan) AS Total_Nilai_Penjualan
FROM `pph-simulasi-dataset.Farmasi.penjualan`
GROUP BY Nama_Obat, EXTRACT(YEAR FROM Tanggal_Penjualan), EXTRACT(MONTH FROM Tanggal_Penjualan);

-- 4. Analisis 1: Total Nilai Persediaan per Obat
SELECT 
  Nama_Obat,
  Total_Unit_Persediaan,
  Total_Nilai_Persediaan
FROM Persediaan_Agg
ORDER BY Total_Nilai_Persediaan DESC;

-- 5. Analisis 2: Total Pemakaian Obat Rawat Inap per Bulan
SELECT 
  Bulan,
  Tahun,
  SUM(Total_Unit_Pemakaian) AS Total_Unit_Pemakaian,
  SUM(Total_Nilai_Pemakaian) AS Total_Nilai_Pemakaian
FROM Pemakaian_Agg
GROUP BY Tahun, Bulan
ORDER BY Tahun, Bulan;

-- 6. Analisis 3: Total Penjualan Obat Rawat Jalan per Bulan
SELECT 
  Bulan,
  Tahun,
  SUM(Total_Unit_Penjualan) AS Total_Unit_Penjualan,
  SUM(Total_Nilai_Penjualan) AS Total_Nilai_Penjualan
FROM Penjualan_Agg
GROUP BY Tahun, Bulan
ORDER BY Tahun, Bulan;

-- 7. Analisis 4: Margin Keuntungan per Obat (Rawat Jalan)
SELECT 
  pjr.Nama_Obat,
  SUM(pjr.Jumlah_Unit) AS Total_Unit_Terjual,
  SUM(pjr.Nilai_Penjualan) AS Total_Nilai_Penjualan,
  SUM(pjr.Jumlah_Unit * pf.Harga_Pokok_Pembelian) AS Total_Harga_Pokok,
  SUM(pjr.Nilai_Penjualan - (pjr.Jumlah_Unit * pf.Harga_Pokok_Pembelian)) AS Margin_Keuntungan
FROM `pph-simulasi-dataset.Farmasi.penjualan` pjr
JOIN `pph-simulasi-dataset.Farmasi.persediaan` pf
  ON pjr.Kode_Obat = pf.Kode_Obat
GROUP BY pjr.Nama_Obat
ORDER BY Margin_Keuntungan DESC;

-- 8. Analisis 5: Obat dengan Pemakaian dan Penjualan Tertinggi
WITH Total_Pemakaian AS (
  SELECT 
    Nama_Obat,
    SUM(Total_Unit_Pemakaian) AS Total_Unit_Pemakaian
  FROM Pemakaian_Agg
  GROUP BY Nama_Obat
),
Total_Penjualan AS (
  SELECT 
    Nama_Obat,
    SUM(Total_Unit_Penjualan) AS Total_Unit_Penjualan
  FROM Penjualan_Agg
  GROUP BY Nama_Obat
)
SELECT 
  COALESCE(pem.Nama_Obat, pen.Nama_Obat) AS Nama_Obat,
  IFNULL(pem.Total_Unit_Pemakaian, 0) AS Total_Unit_Pemakaian,
  IFNULL(pen.Total_Unit_Penjualan, 0) AS Total_Unit_Penjualan,
  (IFNULL(pem.Total_Unit_Pemakaian, 0) + IFNULL(pen.Total_Unit_Penjualan, 0)) AS Total_Unit
FROM Total_Pemakaian pem
FULL OUTER JOIN Total_Penjualan pen
  ON pem.Nama_Obat = pen.Nama_Obat
ORDER BY Total_Unit DESC;

-- 9. Analisis 6: Sisa Persediaan per Obat (Metode FIFO)
SELECT 
  per.Nama_Obat,
  per.Total_Unit_Persediaan,
  IFNULL(SUM(pem.Total_Unit_Pemakaian), 0) AS Total_Unit_Pemakaian,
  IFNULL(SUM(pen.Total_Unit_Penjualan), 0) AS Total_Unit_Penjualan,
  (per.Total_Unit_Persediaan - IFNULL(SUM(pem.Total_Unit_Pemakaian), 0) - IFNULL(SUM(pen.Total_Unit_Penjualan), 0)) AS Sisa_Persediaan
FROM Persediaan_Agg per
LEFT JOIN Pemakaian_Agg pem ON per.Nama_Obat = pem.Nama_Obat
LEFT JOIN Penjualan_Agg pen ON per.Nama_Obat = pen.Nama_Obat
GROUP BY per.Nama_Obat, per.Total_Unit_Persediaan
ORDER BY Sisa_Persediaan DESC;