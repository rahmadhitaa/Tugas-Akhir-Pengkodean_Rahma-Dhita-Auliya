SELECT
    t.tahun,
    k.tax_rate,
    k.tax_holiday_awal,
    k.tax_holiday_akhir,
    (t.pendapatan - (t.beban_operasional + t.penyusutan)) AS laba_kena_pajak,
    CASE 
        WHEN t.tahun BETWEEN EXTRACT(YEAR FROM k.tax_holiday_awal) AND EXTRACT(YEAR FROM k.tax_holiday_akhir) THEN 0
        ELSE (t.pendapatan - (t.beban_operasional + t.penyusutan)) * k.tax_rate
    END AS pph_badan
FROM `pph-simulasi-dataset.pphbadan.transaksikeuangan` t
JOIN `pph-simulasi-dataset.pphbadan.kebijakanfiskal` k
ON t.tahun = k.tahun
ORDER BY t.tahun;