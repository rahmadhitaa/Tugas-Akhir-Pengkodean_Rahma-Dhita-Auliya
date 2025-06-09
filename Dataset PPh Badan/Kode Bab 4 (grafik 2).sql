WITH Depresiasi AS (
  SELECT
    t.tahun,
    t.skenario,
    t.pendapatan,
    t.beban_operasional,
    t.penyusutan AS penyusutan_aktual,
    CASE
      WHEN a.metode = 'garis_lurus' THEN a.nilai_perolehan / a.umur_ekonomis
      WHEN a.metode = 'saldo_menurun' THEN a.nilai_perolehan * 0.25
      ELSE 0
    END AS penyusutan_teoretis,
    a.metode AS metode_depresiasi
  FROM pph-simulasi-dataset.pphbadan.transaksikeuangan t
  CROSS JOIN pph-simulasi-dataset.pphbadan.asettetap a
  WHERE t.skenario IN ('tax_holiday', 'normal')
),
PPhHitung AS (
  SELECT
    d.tahun,
    d.skenario,
    d.metode_depresiasi,
    (d.pendapatan - (d.beban_operasional + d.penyusutan_aktual)) AS laba_kena_pajak,
    k.tax_rate,
    CASE 
        WHEN d.skenario = 'tax_holiday' AND d.tahun BETWEEN EXTRACT(YEAR FROM k.tax_holiday_awal) AND EXTRACT(YEAR FROM k.tax_holiday_akhir) THEN 0
        ELSE (d.pendapatan - (d.beban_operasional + d.penyusutan_aktual)) * k.tax_rate
    END AS pph_badan
  FROM Depresiasi d
  JOIN pph-simulasi-dataset.pphbadan.kebijakanfiskal k
  ON d.tahun = k.tahun
)
SELECT
    tahun,
    skenario,
    metode_depresiasi,
    ROUND(AVG(pph_badan), 2) AS pph_badan_rata_rata
FROM PPhHitung
GROUP BY tahun, skenario, metode_depresiasi
ORDER BY tahun, skenario, metode_depresiasi;