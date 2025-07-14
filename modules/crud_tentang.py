import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw
import os, shutil
from database.db import get_connection

class CrudTentangTokoPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f5f6fa")
        self.data = None
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="CRUD Tentang Toko", font=("Poppins", 24, "bold"), text_color="#1976d2")
        self.label_title.pack(pady=(20,10))
        self.frame_info = ctk.CTkFrame(self, corner_radius=18, fg_color="#ffffff", border_width=2, border_color="#e0e0e0")
        self.frame_info.pack(pady=10, padx=60, fill="x")
        self.label_nama = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 18, "bold"), text_color="#1976d2")
        self.label_nama.pack(pady=(18,2))
        self.label_gambar = ctk.CTkLabel(self.frame_info, text="", cursor="hand2")
        self.label_gambar.pack(pady=6)
        self.label_gambar.bind("<Button-1>", lambda e: self.zoom_gambar())
        self.label_desc = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 12), wraplength=600, justify="center", text_color="#616161")
        self.label_desc.pack(pady=2)
        self.label_alamat = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 11), text_color="#424242")
        self.label_alamat.pack(pady=2)
        self.label_hp = ctk.CTkLabel(self.frame_info, text="", font=("Poppins", 11), text_color="#424242")
        self.label_hp.pack(pady=(2,18))
        self.btn_edit = ctk.CTkButton(self, text="Edit Data Toko", command=self.edit_toko, width=180, height=36, font=("Poppins", 13, "bold"), fg_color="#1976d2", hover_color="#1565c0")
        self.btn_edit.pack(pady=12)

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama_toko, gambar_toko, deskripsi, alamat, no_hp FROM tentang_toko ORDER BY id DESC LIMIT 1")
        self.data = cursor.fetchone()
        cursor.close()
        conn.close()
        if self.data:
            _, nama, gambar, deskripsi, alamat, no_hp = self.data
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

    def edit_toko(self):
        data = self.data
        form = ctk.CTkToplevel(self)
        form.title("Edit Data Toko" if data else "Tambah Data Toko")
        form.geometry("480x500")
        form.resizable(False, False)
        entry_nama = ctk.CTkEntry(form, placeholder_text="Nama Toko", font=("Poppins", 13))
        entry_nama.pack(pady=8, fill="x", padx=40)
        entry_desc = ctk.CTkEntry(form, placeholder_text="Deskripsi", font=("Poppins", 13))
        entry_desc.pack(pady=8, fill="x", padx=40)
        entry_alamat = ctk.CTkEntry(form, placeholder_text="Alamat", font=("Poppins", 13))
        entry_alamat.pack(pady=8, fill="x", padx=40)
        entry_hp = ctk.CTkEntry(form, placeholder_text="No. HP", font=("Poppins", 13))
        entry_hp.pack(pady=8, fill="x", padx=40)
        gambar_path = [None]
        def pilih_gambar():
            path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if path:
                gambar_path[0] = str(path)
                btn_gambar.configure(text=os.path.basename(str(path)))
        btn_gambar = ctk.CTkButton(form, text="Pilih Gambar", command=pilih_gambar, fg_color="#1976d2", hover_color="#1565c0")
        btn_gambar.pack(pady=8)
        if data:
            entry_nama.insert(0, str(data[1]))
            entry_desc.insert(0, str(data[3]))
            entry_alamat.insert(0, str(data[4]))
            entry_hp.insert(0, str(data[5]))
            if data[2]:
                btn_gambar.configure(text=os.path.basename(str(data[2])))
                gambar_path[0] = str(data[2])
        def simpan():
            try:
                nama = entry_nama.get().strip()
                deskripsi = entry_desc.get().strip()
                alamat = entry_alamat.get().strip()
                no_hp = entry_hp.get().strip()
                if not all([nama, deskripsi, alamat, no_hp]):
                    messagebox.showerror("Error", "Semua field harus diisi!")
                    return
                gambar_lama = data[2] if data else ""
                gambar_baru = gambar_path[0]
                gambar_db = gambar_lama
                if gambar_baru and os.path.exists(gambar_baru):
                    folder = os.path.join("assets", "images", "toko")
                    os.makedirs(folder, exist_ok=True)
                    ext = os.path.splitext(gambar_baru)[1]
                    dest = os.path.join(folder, f"logo{ext}")
                    if os.path.abspath(gambar_baru) != os.path.abspath(dest):
                        shutil.copy(gambar_baru, dest)
                    gambar_db = dest
                conn = get_connection()
                cursor = conn.cursor()
                if data:
                    cursor.execute("UPDATE tentang_toko SET nama_toko=%s, gambar_toko=%s, deskripsi=%s, alamat=%s, no_hp=%s WHERE id=%s",
                        (nama, gambar_db, deskripsi, alamat, no_hp, data[0]))
                else:
                    cursor.execute("INSERT INTO tentang_toko (nama_toko, gambar_toko, deskripsi, alamat, no_hp) VALUES (%s,%s,%s,%s,%s)",
                        (nama, gambar_db, deskripsi, alamat, no_hp))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_data()
                form.destroy()
                messagebox.showinfo("Sukses", "Data toko berhasil disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan data: {e}")
        btn_simpan = ctk.CTkButton(form, text="Simpan", command=simpan, font=("Poppins", 13, "bold"), height=36, fg_color="#1976d2", hover_color="#1565c0")
        btn_simpan.pack(pady=16, fill="x", padx=40) 