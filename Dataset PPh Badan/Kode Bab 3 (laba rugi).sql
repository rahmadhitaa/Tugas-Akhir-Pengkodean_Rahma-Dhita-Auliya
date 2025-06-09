SELECT
  tahun,
  pendapatan,
  beban_operasional,
  penyusutan,
  skenario,
  (pendapatan - (beban_operasional + penyusutan)) AS laba_kotor
FROM `pphbadan.transaksikeuangan`
ORDER BY tahun, skenario;