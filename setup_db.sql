-- Buat database
CREATE DATABASE IF NOT EXISTS kedai_mie_ayam_bakso;
USE kedai_mie_ayam_bakso;

-- Tabel kategori_produk
CREATE TABLE IF NOT EXISTS kategori_produk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL
);

-- Tabel produk
CREATE TABLE IF NOT EXISTS produk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    harga INT NOT NULL,
    stok INT NOT NULL,
    gambar VARCHAR(255),
    deskripsi TEXT,
    id_kategori INT,
    FOREIGN KEY (id_kategori) REFERENCES kategori_produk(id) ON DELETE SET NULL
);

-- Tabel history_pembelian
CREATE TABLE IF NOT EXISTS history_pembelian (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pembeli VARCHAR(100) NOT NULL,
    no_hp VARCHAR(20) NOT NULL,
    alamat TEXT NOT NULL,
    nama_produk VARCHAR(100) NOT NULL,
    harga INT NOT NULL,
    jumlah INT NOT NULL,
    total_harga INT NOT NULL,
    delivery_pickup ENUM('Delivery','Pickup') NOT NULL,
    metode_pembayaran ENUM('Transfer Bank','COD','QRIS','OVO','Gopay','Dana') NOT NULL,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel tentang_toko
CREATE TABLE IF NOT EXISTS tentang_toko (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_toko VARCHAR(100) NOT NULL,
    gambar_toko VARCHAR(255),
    deskripsi TEXT,
    alamat TEXT,
    no_hp VARCHAR(20)
);

-- Data awal kategori
INSERT INTO kategori_produk (nama) VALUES
('Makanan'),
('Minuman'),
('Cemilan')
ON DUPLICATE KEY UPDATE nama=VALUES(nama);

-- Data awal produk
INSERT INTO produk (nama, harga, stok, gambar, deskripsi, id_kategori) VALUES
('Mie Ayam', 15000, 50, '', 'Mie ayam lezat dengan topping ayam melimpah', 1),
('Bakso', 12000, 40, '', 'Bakso sapi kenyal dan gurih', 1),
('Teh Manis', 5000, 100, '', 'Teh manis segar', 2),
('Air Tawar', 2000, 100, '', 'Air mineral', 2),
('Kerupuk', 2000, 30, '', 'Kerupuk renyah', 3),
('Pangsit', 3000, 25, '', 'Pangsit goreng gurih', 3)
ON DUPLICATE KEY UPDATE nama=VALUES(nama), harga=VALUES(harga), stok=VALUES(stok), gambar=VALUES(gambar), deskripsi=VALUES(deskripsi), id_kategori=VALUES(id_kategori); 

SHOW databases