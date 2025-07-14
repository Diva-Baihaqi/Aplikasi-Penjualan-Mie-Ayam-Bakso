import customtkinter as ctk
from PIL import Image, ImageDraw
import os
from database.db import get_connection
from modules.crud_produk import CrudProdukPage
from modules.crud_kategori import CrudKategoriPage
from modules.crud_tentang import CrudTentangTokoPage

class AdminDashboard(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Dashboard Admin")
        self.geometry("1000x700")
        self.resizable(True, True)
        self.configure(bg="#f5f6fa")
        self.toko = None
        self.current_page = None
        self.master = master
        self.protocol("WM_DELETE_WINDOW", self.logout)
        self.create_widgets()
        self.load_toko()

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="Dashboard Admin", font=("Poppins", 26, "bold"), text_color="#1976d2")
        self.label_title.pack(pady=(20,10))
        self.btn_logout = ctk.CTkButton(self, text="Logout", command=self.logout, width=100, height=36, font=("Poppins", 13, "bold"), fg_color="#e74c3c", hover_color="#c62828")
        self.btn_logout.pack(pady=(0,10), anchor="ne", padx=30)
        self.frame_info = ctk.CTkFrame(self, corner_radius=18, fg_color="#ffffff", border_width=2, border_color="#e0e0e0")
        self.frame_info.pack(pady=10, padx=60, fill="x")
        self.label_nama = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 20, "bold"), text_color="#1976d2")
        self.label_nama.pack(pady=(18,2))
        self.label_gambar = ctk.CTkLabel(self.frame_info, text="", cursor="hand2")
        self.label_gambar.pack(pady=6)
        self.label_gambar.bind("<Button-1>", lambda e: self.zoom_gambar())
        self.label_desc = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 13), wraplength=600, justify="center", text_color="#616161")
        self.label_desc.pack(pady=2)
        self.label_alamat = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 12), text_color="#424242")
        self.label_alamat.pack(pady=2)
        self.label_hp = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 12), text_color="#424242")
        self.label_hp.pack(pady=(2,18))
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=20)
        btn_style = {"width": 180, "height": 40, "corner_radius": 10, "font": ("Poppins", 14, "bold"), "fg_color": "#1976d2", "hover_color": "#1565c0"}
        self.btn_crud_produk = ctk.CTkButton(nav_frame, text="CRUD Produk", command=self.show_crud_produk, **btn_style)
        self.btn_crud_kategori = ctk.CTkButton(nav_frame, text="CRUD Kategori", command=self.show_crud_kategori, **btn_style)
        self.btn_crud_tentang = ctk.CTkButton(nav_frame, text="CRUD Tentang Toko", command=self.show_crud_tentang, **btn_style)
        self.btn_crud_produk.grid(row=0, column=0, padx=12)
        self.btn_crud_kategori.grid(row=0, column=1, padx=12)
        self.btn_crud_tentang.grid(row=0, column=2, padx=12)

    def load_toko(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nama_toko, gambar_toko, deskripsi, alamat, no_hp FROM tentang_toko ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            nama, gambar, deskripsi, alamat, no_hp = row
            self.label_nama.configure(text=str(nama))
            img_path = gambar if isinstance(gambar, str) and gambar and os.path.exists(gambar) else os.path.join("assets", "images", "logo_toko.png")
            img = Image.open(img_path).resize((120,120))
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([0,0,img.size[0],img.size[1]], 24, fill=255)
            img.putalpha(mask)
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(120,120))
            self.label_gambar.configure(image=img_ctk, text="")
            self.label_desc.configure(text=str(deskripsi))
            self.label_alamat.configure(text=f"Alamat: {alamat}")
            self.label_hp.configure(text=f"No. HP: {no_hp}")
            self._img_path = img_path
        else:
            self.label_nama.configure(text="Belum ada data toko")
            self.label_desc.configure(text="")
            self.label_alamat.configure(text="")
            self.label_hp.configure(text="")
            self._img_path = os.path.join("assets", "images", "logo_toko.png")

    def zoom_gambar(self):
        img_path = getattr(self, '_img_path', os.path.join("assets", "images", "logo_toko.png"))
        if not os.path.exists(img_path):
            return
        top = ctk.CTkToplevel(self)
        top.title("Zoom Gambar Toko")
        img = Image.open(img_path)
        try:
            resample = getattr(Image, 'LANCZOS', 1)
        except Exception:
            resample = 1
        img = img.resize((min(400, img.width), min(400, img.height)), resample)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        lbl = ctk.CTkLabel(top, image=img_ctk, text="")
        lbl.pack(padx=20, pady=20)
        top.grab_set()

    def show_crud_produk(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = CrudProdukPage(self)
        self.current_page.pack(fill="both", expand=True, pady=10)

    def show_crud_kategori(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = CrudKategoriPage(self)
        self.current_page.pack(fill="both", expand=True, pady=10)

    def show_crud_tentang(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = CrudTentangTokoPage(self)
        self.current_page.pack(fill="both", expand=True, pady=10)

    def logout(self):
        self.destroy()
        try:
            self.master.deiconify()
        except Exception:
            pass 