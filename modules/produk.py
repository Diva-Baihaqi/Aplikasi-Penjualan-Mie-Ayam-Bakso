import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageDraw
import os
from database.db import get_connection
from modules.checkout import CheckoutPage
import tkinter.messagebox as messagebox

class ProdukPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f5f6fa")
        self.kategori = []
        self.produk = []
        self.selected_kategori = None
        self.card_refs = []
        self.create_widgets()
        self.load_kategori()
        self.load_produk()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Judul
        self.label_judul = ctk.CTkLabel(self, text="Daftar Produk", font=("Poppins", 28, "bold"))
        self.label_judul.pack(pady=(20,10))
        # Filter kategori
        self.kategori_var = ctk.StringVar(value="Semua Kategori")
        self.option_kategori = ctk.CTkOptionMenu(self, variable=self.kategori_var, command=self.on_kategori_change)
        self.option_kategori.pack(pady=(0,20))
        # Frame produk
        self.frame_produk = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_produk.pack(fill="both", expand=True)

    def load_kategori(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama FROM kategori_produk")
        self.kategori = cursor.fetchall()
        kategori_list = ["Semua Kategori"] + [k[1] if isinstance(k, (tuple, list)) else k['nama'] for k in self.kategori]
        self.option_kategori.configure(values=kategori_list)
        cursor.close()
        conn.close()

    def load_produk(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.selected_kategori and self.selected_kategori != "Semua Kategori":
            cursor.execute("SELECT p.id, p.nama, p.harga, p.stok, p.gambar, p.deskripsi, k.nama FROM produk p JOIN kategori_produk k ON p.id_kategori=k.id WHERE k.nama=%s", (self.selected_kategori,))
        else:
            cursor.execute("SELECT p.id, p.nama, p.harga, p.stok, p.gambar, p.deskripsi, k.nama FROM produk p JOIN kategori_produk k ON p.id_kategori=k.id")
        self.produk = cursor.fetchall()
        cursor.close()
        conn.close()
        self.show_produk()

    def show_produk(self):
        for widget in self.frame_produk.winfo_children():
            widget.destroy()
        self.card_refs = []
        if not self.produk:
            ctk.CTkLabel(self.frame_produk, text="Tidak ada produk.", font=("Poppins", 16)).pack(pady=20)
            return
        # Responsive: hitung jumlah kolom berdasarkan lebar frame
        width = self.frame_produk.winfo_width() or 900
        min_card_width = 260
        cols = max(1, width // min_card_width)
        for idx, p in enumerate(self.produk):
            card = self.create_produk_card(self.frame_produk, p)
            self.card_refs.append(card)
            row, col = divmod(idx, cols)
            card.grid(row=row, column=col, padx=18, pady=18, sticky="nsew")
        for c in range(cols):
            self.frame_produk.grid_columnconfigure(c, weight=1)

    def create_produk_card(self, parent, produk):
        pid, nama, harga, stok, gambar, deskripsi, kategori = produk
        card = ctk.CTkFrame(parent, width=240, height=340, corner_radius=18, fg_color="#ffffff")
        card.grid_propagate(False)
        # Shadow effect (simulasi)
        card.configure(border_width=2, border_color="#e0e0e0")
        # Gambar produk
        img_path = gambar if gambar and os.path.exists(gambar) else os.path.join("assets", "images", "logo_toko.png")
        img = Image.open(img_path)
        # Resize untuk card
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            try:
                resample = Image.LANCZOS
            except AttributeError:
                resample = 1  # LANCZOS = 1
        img_card = img.resize((130,130), resample)
        # Rounded corner manual
        def rounded(img, radius):
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([0,0,img.size[0],img.size[1]], radius, fill=255)
            img.putalpha(mask)
            return img
        try:
            img_card = rounded(img_card.convert('RGBA'), 18)
        except Exception:
            pass
        img_ctk = ctk.CTkImage(light_image=img_card, dark_image=img_card, size=(130,130))
        lbl_img = ctk.CTkLabel(card, image=img_ctk, text="", cursor="hand2")
        lbl_img.pack(pady=(14,7))
        lbl_img.bind("<Button-1>", lambda e, path=img_path: self.zoom_gambar(path))
        # Nama produk
        lbl_nama = ctk.CTkLabel(card, text=nama, font=("Poppins", 16, "bold"))
        lbl_nama.pack(pady=(0,2))
        # Harga
        lbl_harga = ctk.CTkLabel(card, text=f"Rp {harga:,}", font=("Poppins", 14), text_color="#1976d2")
        lbl_harga.pack()
        # Stok
        lbl_stok = ctk.CTkLabel(card, text=f"Stok: {stok}", font=("Poppins", 12), text_color="#757575")
        lbl_stok.pack()
        # Deskripsi
        lbl_desc = ctk.CTkLabel(card, text=deskripsi, font=("Poppins", 11), wraplength=200, justify="center", text_color="#616161")
        lbl_desc.pack(pady=(2,5))
        # Button checkout dengan efek hover
        btn_checkout = ctk.CTkButton(card, text="Checkout", command=lambda: self.checkout_produk(produk), width=120, height=36, corner_radius=10, fg_color="#1976d2", hover_color="#1565c0", font=("Poppins", 13, "bold"))
        btn_checkout.pack(pady=(10,14))
        return card

    def on_kategori_change(self, value):
        self.selected_kategori = value
        self.load_produk()

    def checkout_produk(self, produk):
        CheckoutPage(self, produk)

    def on_resize(self, event):
        self.show_produk()

    def zoom_gambar(self, img_path):
        if not os.path.exists(img_path):
            messagebox.showinfo("Gambar tidak ditemukan", "Gambar tidak tersedia.")
            return
        top = ctk.CTkToplevel(self)
        top.title("Zoom Gambar Produk")
        img = Image.open(img_path)
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            try:
                resample = Image.LANCZOS
            except AttributeError:
                resample = 1
        img = img.resize((min(500, img.width), min(500, img.height)), resample)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        lbl = ctk.CTkLabel(top, image=img_ctk, text="")
        lbl.pack(padx=20, pady=20)
        top.grab_set() 