# Query Pengambilan Data (SELECT)

Berikut adalah kumpulan query SQL untuk pengambilan data (SELECT) pada aplikasi Penjualan Mie Ayam Bakso, lengkap dengan penjelasan tabel dan fungsinya.

---

## 1. Pengambilan Data Produk
- **Tabel:** produk, kategori_produk
- **Fungsi:** Menampilkan daftar produk beserta kategori
- **Query:**
```sql
SELECT p.id, p.nama, p.harga, p.stok, p.gambar, p.deskripsi, k.nama AS kategori
FROM produk p
JOIN kategori_produk k ON p.id_kategori = k.id;
```

---

## 2. Pengambilan Data Kategori
- **Tabel:** kategori_produk
- **Fungsi:** Menampilkan daftar kategori produk
- **Query:**
```sql
SELECT id, nama FROM kategori_produk;
```

---

## 3. Pengambilan Data History Pembelian
- **Tabel:** history_pembelian
- **Fungsi:** Menampilkan seluruh riwayat transaksi pembelian
- **Query:**
```sql
SELECT * FROM history_pembelian ORDER BY waktu DESC;
```
- **Query Filter Tanggal:**
```sql
SELECT * FROM history_pembelian WHERE waktu BETWEEN '2024-06-01' AND '2024-06-30';
```

---

## 4. Pengambilan Data Tentang Toko
- **Tabel:** tentang_toko
- **Fungsi:** Menampilkan profil dan informasi toko
- **Query:**
```sql
SELECT id, nama_toko, gambar_toko, deskripsi, alamat, no_hp FROM tentang_toko ORDER BY id DESC LIMIT 1;
```

---

## 5. Pengambilan Data User/Admin (Login)
- **Tabel:** users
- **Fungsi:** Verifikasi login admin
- **Query:**
```sql
SELECT * FROM users WHERE username = 'admin' AND password = 'password';
```

---

## 6. Pengambilan Data Produk Berdasarkan Kategori
- **Tabel:** produk, kategori_produk
- **Fungsi:** Menampilkan produk sesuai kategori yang dipilih user
- **Query:**
```sql
SELECT p.id, p.nama, p.harga, p.stok, p.gambar, p.deskripsi, k.nama AS kategori
FROM produk p
JOIN kategori_produk k ON p.id_kategori = k.id
WHERE k.nama = 'Makanan';
```

---

## 7. Pengambilan Data Detail Produk
- **Tabel:** produk
- **Fungsi:** Menampilkan detail produk tertentu
- **Query:**
```sql
SELECT * FROM produk WHERE id = 1;
```

---

## 8. Pengambilan Data History Berdasarkan Nama Pembeli
- **Tabel:** history_pembelian
- **Fungsi:** Menampilkan riwayat transaksi berdasarkan nama pembeli
- **Query:**
```sql
SELECT * FROM history_pembelian WHERE nama_pembeli = 'Budi';
```

---

## 9. Pengambilan Data History Berdasarkan Produk
- **Tabel:** history_pembelian
- **Fungsi:** Menampilkan riwayat transaksi berdasarkan nama produk
- **Query:**
```sql
SELECT * FROM history_pembelian WHERE nama_produk = 'Mie Ayam';
```

---

**Catatan:**
- Semua query di atas dijalankan menggunakan koneksi dari fungsi `get_connection()` di `database/db.py`.
- Query dapat disesuaikan dengan kebutuhan filter atau pencarian data lain sesuai fitur aplikasi. 