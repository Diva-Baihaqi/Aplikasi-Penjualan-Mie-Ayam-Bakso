import customtkinter as ctk
from tkinter import messagebox
from database.db import get_connection

class CrudKategoriPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f5f6fa")
        self.kategori = []
        self.create_widgets()
        self.load_kategori()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="CRUD Kategori Produk", font=("Poppins", 24, "bold"), text_color="#1976d2")
        self.label_title.pack(pady=(20,10))
        self.btn_tambah = ctk.CTkButton(self, text="Tambah Kategori", command=self.tambah_kategori, width=160, height=36, font=("Poppins", 13, "bold"), fg_color="#1976d2", hover_color="#1565c0")
        self.btn_tambah.pack(pady=8)
        self.table_frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#ffffff", border_width=2, border_color="#e0e0e0")
        self.table_frame.pack(padx=30, pady=10, fill="both", expand=True)
        self.headers = ["Nama Kategori", "Aksi"]
        for i, col in enumerate(self.headers):
            lbl = ctk.CTkLabel(self.table_frame, text=col, font=("Poppins", 12, "bold"), anchor="w", fg_color="#e3f2fd", text_color="#1976d2", corner_radius=8)
            lbl.grid(row=0, column=i, sticky="nsew", padx=2, pady=2, ipadx=2, ipady=2)

    def load_kategori(self):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()['row'] != 0:
                widget.destroy()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama FROM kategori_produk")
        self.kategori = cursor.fetchall()
        cursor.close()
        conn.close()
        for r, row in enumerate(self.kategori, start=1):
            kid, nama = row
            ctk.CTkLabel(self.table_frame, text=str(nama), font=("Poppins", 11), fg_color="#f8fafc").grid(row=r, column=0, sticky="nsew", padx=2, pady=2)
            btn_edit = ctk.CTkButton(self.table_frame, text="Edit", width=60, command=lambda kid=kid: self.edit_kategori(kid), fg_color="#1976d2", hover_color="#1565c0")
            btn_hapus = ctk.CTkButton(self.table_frame, text="Hapus", width=60, fg_color="#e74c3c", hover_color="#c62828", command=lambda kid=kid: self.hapus_kategori(kid))
            btn_edit.grid(row=r, column=1, padx=2, sticky="w")
            btn_hapus.grid(row=r, column=1, padx=68, sticky="w")

    def tambah_kategori(self):
        self.show_kategori_form()

    def edit_kategori(self, kid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama FROM kategori_produk WHERE id=%s", (kid,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data:
            self.show_kategori_form(data)

    def hapus_kategori(self, kid):
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus kategori ini?"):
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kategori_produk WHERE id=%s", (kid,))
        conn.commit()
        cursor.close()
        conn.close()
        self.load_kategori()
        messagebox.showinfo("Sukses", "Kategori berhasil dihapus.")

    def show_kategori_form(self, data=None):
        form = ctk.CTkToplevel(self)
        form.title("Edit Kategori" if data else "Tambah Kategori")
        form.geometry("340x200")
        form.resizable(False, False)
        entry_nama = ctk.CTkEntry(form, placeholder_text="Nama Kategori", font=("Poppins", 13))
        entry_nama.pack(pady=16, fill="x", padx=40)
        if data:
            entry_nama.insert(0, str(data[1]))
        def simpan():
            nama = entry_nama.get().strip()
            if not nama:
                messagebox.showerror("Error", "Nama kategori harus diisi!")
                return
            conn = get_connection()
            cursor = conn.cursor()
            if data:
                cursor.execute("UPDATE kategori_produk SET nama=%s WHERE id=%s", (nama, data[0]))
            else:
                cursor.execute("INSERT INTO kategori_produk (nama) VALUES (%s)", (nama,))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_kategori()
            form.destroy()
            messagebox.showinfo("Sukses", "Kategori berhasil disimpan.")
        btn_simpan = ctk.CTkButton(form, text="Simpan", command=simpan, font=("Poppins", 13, "bold"), height=36, fg_color="#1976d2", hover_color="#1565c0")
        btn_simpan.pack(pady=16, fill="x", padx=40)

    def on_resize(self, event):
        pass 