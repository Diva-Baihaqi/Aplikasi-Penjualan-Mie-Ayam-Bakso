import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw
import os, shutil
from database.db import get_connection

class CrudProdukPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f5f6fa")
        self.produk = []
        self.kategori = []
        self.create_widgets()
        self.load_kategori()
        self.load_produk()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="CRUD Produk", font=("Poppins", 24, "bold"), text_color="#1976d2")
        self.label_title.pack(pady=(20,10))
        self.btn_tambah = ctk.CTkButton(self, text="Tambah Produk", command=self.tambah_produk, width=160, height=36, font=("Poppins", 13, "bold"), fg_color="#1976d2", hover_color="#1565c0")
        self.btn_tambah.pack(pady=8)
        self.table_frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#ffffff", border_width=2, border_color="#e0e0e0")
        self.table_frame.pack(padx=30, pady=10, fill="both", expand=True)
        self.headers = ["Nama", "Harga", "Stok", "Kategori", "Gambar", "Deskripsi", "Aksi"]
        for i, col in enumerate(self.headers):
            lbl = ctk.CTkLabel(self.table_frame, text=col, font=("Poppins", 12, "bold"), anchor="w", fg_color="#e3f2fd", text_color="#1976d2", corner_radius=8)
            lbl.grid(row=0, column=i, sticky="nsew", padx=2, pady=2, ipadx=2, ipady=2)

    def load_kategori(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama FROM kategori_produk")
        self.kategori = cursor.fetchall()
        cursor.close()
        conn.close()

    def load_produk(self):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()['row'] != 0:
                widget.destroy()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT p.id, p.nama, p.harga, p.stok, p.gambar, p.deskripsi, k.nama FROM produk p JOIN kategori_produk k ON p.id_kategori=k.id")
        self.produk = cursor.fetchall()
        cursor.close()
        conn.close()
        for r, row in enumerate(self.produk, start=1):
            pid, nama, harga, stok, gambar, deskripsi, kategori = row
            ctk.CTkLabel(self.table_frame, text=str(nama), font=("Poppins", 11), fg_color="#f8fafc").grid(row=r, column=0, sticky="nsew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=f"Rp {harga:,}", font=("Poppins", 11), fg_color="#f8fafc").grid(row=r, column=1, sticky="nsew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=str(stok), font=("Poppins", 11), fg_color="#f8fafc").grid(row=r, column=2, sticky="nsew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=str(kategori), font=("Poppins", 11), fg_color="#f8fafc").grid(row=r, column=3, sticky="nsew", padx=2, pady=2)
            img_lbl = ctk.CTkLabel(self.table_frame, text=os.path.basename(gambar) if isinstance(gambar, str) and gambar else "-", font=("Poppins", 11), fg_color="#f8fafc", cursor="hand2")
            img_lbl.grid(row=r, column=4, sticky="nsew", padx=2, pady=2)
            img_lbl.bind("<Button-1>", lambda e, path=gambar: self.zoom_gambar(path))
            ctk.CTkLabel(self.table_frame, text=str(deskripsi), font=("Poppins", 11), wraplength=180, fg_color="#f8fafc").grid(row=r, column=5, sticky="nsew", padx=2, pady=2)
            btn_edit = ctk.CTkButton(self.table_frame, text="Edit", width=60, command=lambda pid=pid: self.edit_produk(pid), fg_color="#1976d2", hover_color="#1565c0")
            btn_hapus = ctk.CTkButton(self.table_frame, text="Hapus", width=60, fg_color="#e74c3c", hover_color="#c62828", command=lambda pid=pid: self.hapus_produk(pid))
            btn_edit.grid(row=r, column=6, padx=2, sticky="w")
            btn_hapus.grid(row=r, column=6, padx=68, sticky="w")

    def tambah_produk(self):
        self.show_produk_form()

    def edit_produk(self, pid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, harga, stok, gambar, deskripsi, id_kategori FROM produk WHERE id=%s", (pid,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data:
            self.show_produk_form(data)

    def hapus_produk(self, pid):
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus produk ini?"):
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produk WHERE id=%s", (pid,))
        conn.commit()
        cursor.close()
        conn.close()
        self.load_produk()
        messagebox.showinfo("Sukses", "Produk berhasil dihapus.")

    def show_produk_form(self, data=None):
        form = ctk.CTkToplevel(self)
        form.title("Edit Produk" if data else "Tambah Produk")
        form.geometry("420x600")
        form.resizable(False, False)
        entry_nama = ctk.CTkEntry(form, placeholder_text="Nama Produk", font=("Poppins", 13))
        entry_nama.pack(pady=8, fill="x", padx=40)
        entry_harga = ctk.CTkEntry(form, placeholder_text="Harga", font=("Poppins", 13))
        entry_harga.pack(pady=8, fill="x", padx=40)
        entry_stok = ctk.CTkEntry(form, placeholder_text="Stok", font=("Poppins", 13))
        entry_stok.pack(pady=8, fill="x", padx=40)
        entry_desc = ctk.CTkEntry(form, placeholder_text="Deskripsi", font=("Poppins", 13))
        entry_desc.pack(pady=8, fill="x", padx=40)
        kategori_var = ctk.StringVar(value=str(self.kategori[0][1]) if self.kategori else "")
        option_kategori = ctk.CTkOptionMenu(form, variable=kategori_var, values=[str(k[1]) for k in self.kategori])
        option_kategori.pack(pady=8, fill="x", padx=40)
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
            entry_harga.insert(0, str(data[2]))
            entry_stok.insert(0, str(data[3]))
            entry_desc.insert(0, str(data[5]))
            kategori_nama = ""
            for k in self.kategori:
                if k[0] == data[6]:
                    kategori_nama = str(k[1])
                    break
            kategori_var.set(kategori_nama)
            if data[4]:
                btn_gambar.configure(text=os.path.basename(str(data[4])))
                gambar_path[0] = str(data[4])
        def simpan():
            nama = entry_nama.get().strip()
            harga = entry_harga.get().strip()
            stok = entry_stok.get().strip()
            deskripsi = entry_desc.get().strip()
            kategori_nama = kategori_var.get()
            if not all([nama, harga, stok, deskripsi, kategori_nama]):
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
            id_kat = None
            for k in self.kategori:
                if str(k[1]) == kategori_nama:
                    id_kat = k[0]
                    break
            if id_kat is None:
                messagebox.showerror("Error", "Kategori tidak ditemukan!")
                return
            if gambar_path[0] and os.path.exists(gambar_path[0]):
                folder = os.path.join("assets", "images", nama)
                os.makedirs(folder, exist_ok=True)
                ext = os.path.splitext(gambar_path[0])[1]
                dest = os.path.join(folder, f"gambar{ext}")
                shutil.copy(gambar_path[0], dest)
                gambar_db = dest
            else:
                gambar_db = data[4] if data else ""
            conn = get_connection()
            cursor = conn.cursor()
            if data:
                cursor.execute("UPDATE produk SET nama=%s, harga=%s, stok=%s, gambar=%s, deskripsi=%s, id_kategori=%s WHERE id=%s",
                    (nama, harga, stok, gambar_db, deskripsi, id_kat, data[0]))
            else:
                cursor.execute("INSERT INTO produk (nama, harga, stok, gambar, deskripsi, id_kategori) VALUES (%s,%s,%s,%s,%s,%s)",
                    (nama, harga, stok, gambar_db, deskripsi, id_kat))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_produk()
            form.destroy()
            messagebox.showinfo("Sukses", "Produk berhasil disimpan.")
        btn_simpan = ctk.CTkButton(form, text="Simpan", command=simpan, font=("Poppins", 13, "bold"), height=36, fg_color="#1976d2", hover_color="#1565c0")
        btn_simpan.pack(pady=16, fill="x", padx=40)

    def zoom_gambar(self, img_path):
        if not img_path or not os.path.exists(img_path):
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
        img = img.resize((min(400, img.width), min(400, img.height)), resample)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        lbl = ctk.CTkLabel(top, image=img_ctk, text="")
        lbl.pack(padx=20, pady=20)
        top.grab_set()

    def on_resize(self, event):
        pass 