import customtkinter as ctk
from tkinter import messagebox, filedialog
from database.db import get_connection
import pandas as pd
from fpdf import FPDF

class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f5f6fa")
        self.data = []
        self.create_widgets()
        self.load_data()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="History Pembelian", font=("Poppins", 24, "bold"), text_color="#1976d2")
        self.label_title.pack(pady=(20,10))
        self.table_frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#ffffff", border_width=2, border_color="#e0e0e0")
        self.table_frame.pack(padx=30, pady=10, fill="both", expand=True)
        columns = ["Nama Pembeli", "No. HP", "Nama Produk", "Harga", "Jumlah", "Total Harga", "Delivery/Pickup", "Metode Pembayaran", "Waktu"]
        self.headers = []
        for i, col in enumerate(columns):
            lbl = ctk.CTkLabel(self.table_frame, text=col, font=("Poppins", 12, "bold"), anchor="w", fg_color="#e3f2fd", text_color="#1976d2", corner_radius=8)
            lbl.grid(row=0, column=i, sticky="nsew", padx=2, pady=2, ipadx=2, ipady=2)
            self.headers.append(lbl)
        self.rows = []
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        btn_style = {"fg_color": "#1976d2", "hover_color": "#1565c0", "font": ("Poppins", 12, "bold"), "corner_radius": 8, "width": 140, "height": 36}
        self.btn_excel = ctk.CTkButton(btn_frame, text="Ekspor ke Excel", command=self.export_excel, **btn_style)
        self.btn_pdf = ctk.CTkButton(btn_frame, text="Ekspor ke PDF", command=self.export_pdf, **btn_style)
        self.btn_excel.grid(row=0, column=0, padx=10)
        self.btn_pdf.grid(row=0, column=1, padx=10)

    def load_data(self):
        for widget in self.table_frame.winfo_children():
            if widget not in self.headers:
                widget.destroy()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nama_pembeli, no_hp, nama_produk, harga, jumlah, total_harga, delivery_pickup, metode_pembayaran, waktu FROM history_pembelian ORDER BY waktu DESC")
        self.data = cursor.fetchall()
        cursor.close()
        conn.close()
        for r, row in enumerate(self.data, start=1):
            for c, val in enumerate(row):
                lbl = ctk.CTkLabel(self.table_frame, text=str(val), font=("Poppins", 11), anchor="w", fg_color="#f8fafc", text_color="#424242")
                lbl.grid(row=r, column=c, sticky="nsew", padx=2, pady=2, ipadx=2, ipady=2)

    def export_excel(self):
        if not self.data:
            messagebox.showwarning("Kosong", "Tidak ada data untuk diekspor.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        columns = ["Nama Pembeli", "No. HP", "Nama Produk", "Harga", "Jumlah", "Total Harga", "Delivery/Pickup", "Metode Pembayaran", "Waktu"]
        df = pd.DataFrame(self.data, columns=columns)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukses", f"Data berhasil diekspor ke {file_path}")

    def export_pdf(self):
        if not self.data:
            messagebox.showwarning("Kosong", "Tidak ada data untuk diekspor.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        columns = ["Nama Pembeli", "No. HP", "Nama Produk", "Harga", "Jumlah", "Total Harga", "Delivery/Pickup", "Metode Pembayaran", "Waktu"]
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        for col in columns:
            pdf.cell(40, 10, col, 1, 0, 'C')
        pdf.ln()
        pdf.set_font("Arial", "", 10)
        for row in self.data:
            for val in row:
                pdf.cell(40, 8, str(val), 1, 0, 'C')
            pdf.ln()
        pdf.output(file_path)
        messagebox.showinfo("Sukses", f"Data berhasil diekspor ke {file_path}")

    def on_resize(self, event):
        pass 