SELECT
  aset_id,
  kategori,
  nilai_perolehan,
  umur_ekonomis,
  metode,
  nilai_perolehan / umur_ekonomis AS depresiasi_tahunan
FROM `pphbadan.asettetap`
WHERE metode = 'garis_lurus';