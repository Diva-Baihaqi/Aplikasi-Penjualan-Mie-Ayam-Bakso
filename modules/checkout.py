import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from database.db import get_connection

class CheckoutPage(ctk.CTkToplevel):
    def __init__(self, master, produk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Checkout Produk")
        self.geometry("480x600")
        self.resizable(False, False)
        self.produk = produk
        self.total_harga = produk[2]
        self.create_widgets()

    def create_widgets(self):
        p = self.produk
        self.label_title = ctk.CTkLabel(self, text="Form Checkout", font=("Poppins", 22, "bold"))
        self.label_title.pack(pady=(20,10))
        self.entry_nama = ctk.CTkEntry(self, placeholder_text="Nama Pembeli", font=("Poppins", 14))
        self.entry_nama.pack(pady=8, fill="x", padx=40)
        self.entry_hp = ctk.CTkEntry(self, placeholder_text="No. HP (Whatsapp)", font=("Poppins", 14))
        self.entry_hp.pack(pady=8, fill="x", padx=40)
        self.entry_alamat = ctk.CTkEntry(self, placeholder_text="Alamat", font=("Poppins", 14))
        self.entry_alamat.pack(pady=8, fill="x", padx=40)
        self.entry_produk = ctk.CTkEntry(self, font=("Poppins", 14))
        self.entry_produk.insert(0, p[1])
        self.entry_produk.configure(state="readonly")
        self.entry_produk.pack(pady=8, fill="x", padx=40)
        self.entry_harga = ctk.CTkEntry(self, font=("Poppins", 14))
        self.entry_harga.insert(0, str(p[2]))
        self.entry_harga.configure(state="readonly")
        self.entry_harga.pack(pady=8, fill="x", padx=40)
        self.entry_jumlah = ctk.CTkEntry(self, font=("Poppins", 14))
        self.entry_jumlah.insert(0, "1")
        self.entry_jumlah.pack(pady=8, fill="x", padx=40)
        self.entry_jumlah.bind("<KeyRelease>", self.update_total)
        self.entry_total = ctk.CTkEntry(self, font=("Poppins", 14))
        self.entry_total.insert(0, str(self.total_harga))
        self.entry_total.configure(state="readonly")
        self.entry_total.pack(pady=8, fill="x", padx=40)
        self.delivery_var = ctk.StringVar(value="Delivery")
        self.option_delivery = ctk.CTkOptionMenu(self, variable=self.delivery_var, values=["Delivery", "Pickup"])
        self.option_delivery.pack(pady=8, fill="x", padx=40)
        self.metode_var = ctk.StringVar(value="Transfer Bank")
        self.option_metode = ctk.CTkOptionMenu(self, variable=self.metode_var, values=["Transfer Bank","COD","QRIS","OVO","Gopay","Dana"])
        self.option_metode.pack(pady=8, fill="x", padx=40)
        self.btn_bayar = ctk.CTkButton(self, text="Bayar", command=self.bayar, font=("Poppins", 16, "bold"), height=40)
        self.btn_bayar.pack(pady=(20,10), fill="x", padx=40)

    def update_total(self, event=None):
        try:
            jumlah = int(self.entry_jumlah.get())
            harga = int(self.entry_harga.get())
            total = jumlah * harga
            self.entry_total.configure(state="normal")
            self.entry_total.delete(0, "end")
            self.entry_total.insert(0, str(total))
            self.entry_total.configure(state="readonly")
        except Exception:
            pass

    def bayar(self):
        nama = self.entry_nama.get().strip()
        hp = self.entry_hp.get().strip()
        alamat = self.entry_alamat.get().strip()
        produk = self.entry_produk.get()
        harga = int(self.entry_harga.get())
        jumlah = int(self.entry_jumlah.get())
        total = int(self.entry_total.get())
        delivery = self.delivery_var.get()
        metode = self.metode_var.get()
        if not all([nama, hp, alamat, produk, harga, jumlah, total, delivery, metode]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO history_pembelian (nama_pembeli, no_hp, alamat, nama_produk, harga, jumlah, total_harga, delivery_pickup, metode_pembayaran) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (nama, hp, alamat, produk, harga, jumlah, total, delivery, metode))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return
        pesan = f"Nama Pembeli: {nama}%0ANo. HP: {hp}%0AAlamat: {alamat}%0ANama Produk: {produk}%0AHarga: {harga}%0AJumlah: {jumlah}%0ATotal Harga: {total}%0ADelivery atau Pickup: {delivery}%0AMetode Pembayaran: {metode}"
        url = f"https://wa.me/6282125184884?text={pesan}"
        webbrowser.open_new_tab(url)
        messagebox.showinfo("Sukses", "Pesanan berhasil! Silakan lanjutkan pembayaran di WhatsApp.")
        self.destroy() 