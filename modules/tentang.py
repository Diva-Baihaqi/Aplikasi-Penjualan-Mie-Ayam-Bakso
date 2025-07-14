import customtkinter as ctk
from PIL import Image, ImageDraw
import os
from database.db import get_connection

class TentangTokoPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f5f6fa")
        self.data = None
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="Tentang Toko", font=("Poppins", 26, "bold"), text_color="#1976d2")
        self.label_title.pack(pady=(20,10))
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

    def load_data(self):
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
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            try:
                resample = Image.LANCZOS
            except AttributeError:
                resample = 1
        img = img.resize((min(400, img.width), min(400, img.height)), resample)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        lbl = ctk.CTkLabel(top, image=img_ctk, text="")
        lbl.pack(padx=20, pady=20)
        top.grab_set() 