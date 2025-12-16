-- 1. Matikan proteksi Foreign Key biar tidak error
SET FOREIGN_KEY_CHECKS = 0;

-- 2. Kosongkan tabel (TRUNCATE mereset ID jadi 1 lagi)
TRUNCATE TABLE penjualan;
TRUNCATE TABLE mobil_sport;
TRUNCATE TABLE mobil_listrik;
TRUNCATE TABLE mobil;
TRUNCATE TABLE users;


-- 3. Nyalakan lagi proteksinya
SET FOREIGN_KEY_CHECKS = 1;