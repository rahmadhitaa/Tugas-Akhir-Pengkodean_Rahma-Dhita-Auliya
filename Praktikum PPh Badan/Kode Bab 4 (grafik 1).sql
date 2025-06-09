SELECT
    t.tahun,
    t.skenario,
    (t.pendapatan - (t.beban_operasional + t.penyusutan)) AS laba_kena_pajak,
    CASE 
        WHEN t.skenario = 'tax_holiday' AND t.tahun BETWEEN EXTRACT(YEAR FROM k.tax_holiday_awal) AND EXTRACT(YEAR FROM k.tax_holiday_akhir) THEN 0
        WHEN t.skenario = 'normal' THEN (t.pendapatan - (t.beban_operasional + t.penyusutan)) * k.tax_rate
        ELSE (t.pendapatan - (t.beban_operasional + t.penyusutan)) * k.tax_rate
    END AS pph_badan,
    (t.pendapatan - (t.beban_operasional + t.penyusutan) - 
     CASE 
         WHEN t.skenario = 'tax_holiday' AND t.tahun BETWEEN EXTRACT(YEAR FROM k.tax_holiday_awal) AND EXTRACT(YEAR FROM k.tax_holiday_akhir) THEN 0
         WHEN t.skenario = 'normal' THEN (t.pendapatan - (t.beban_operasional + t.penyusutan)) * k.tax_rate
         ELSE (t.pendapatan - (t.beban_operasional + t.penyusutan)) * k.tax_rate
     END) AS laba_rugi_bersih
FROM `pph-simulasi-dataset.pphbadan.transaksikeuangan` t
JOIN `pph-simulasi-dataset.pphbadan.kebijakanfiskal` k
ON t.tahun = k.tahun
WHERE t.skenario IN ('tax_holiday', 'normal')
ORDER BY t.tahun, t.skenario;