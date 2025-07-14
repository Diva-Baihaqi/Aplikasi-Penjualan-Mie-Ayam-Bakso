import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import os
from modules.produk import ProdukPage
from modules.history import HistoryPage
from modules.login import LoginPage
from modules.admin_dashboard import AdminDashboard
from modules.tentang import TentangTokoPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DEFAULT_IMAGE_PATH = os.path.join("assets", "images", "logo_toko.png")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kedai Mie Ayam & Bakso")
        self.geometry("900x600")
        self.resizable(True, True)
        self.configure(bg="#f5f6fa")
        self.current_page = None
        self.create_widgets()

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=16, border_width=0)
        header_frame.pack(padx=0, pady=(10,0), fill="x")
        logo_path = os.path.join("assets", "images", "toko", "logo.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).resize((48,48))
            logo_img_ctk = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(48,48))
            logo_label = ctk.CTkLabel(header_frame, image=logo_img_ctk, text="")
            logo_label.pack(side="left", padx=(24,12), pady=8)
        label_header = ctk.CTkLabel(header_frame, text="Kedai Mie Ayam & Bakso", font=("Poppins", 28, "bold"), text_color="#1976d2")
        label_header.pack(side="left", pady=8)
        self.main_frame = ctk.CTkFrame(self, corner_radius=24, fg_color="#ffffff", border_width=2, border_color="#e0e0e0")
        self.main_frame.pack(padx=40, pady=20, fill="both", expand=True)
        self.show_home()
        nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_frame.pack(pady=10)
        def nav_icon(path):
            if os.path.exists(path):
                img = Image.open(path).resize((24,24))
                return ctk.CTkImage(light_image=img, dark_image=img, size=(24,24))
            return None
        btn_style = {"width": 130, "height": 40, "corner_radius": 10, "font": ("Poppins", 14, "bold"), "fg_color": "#1976d2", "hover_color": "#1565c0"}
        self.btn_produk = ctk.CTkButton(nav_frame, text="Produk", image=nav_icon(os.path.join("assets","icons","box.png")), compound="left", command=self.goto_produk, **btn_style)
        self.btn_history = ctk.CTkButton(nav_frame, text="History", image=nav_icon(os.path.join("assets","icons","history.png")), compound="left", command=self.goto_history, **btn_style)
        self.btn_bantuan = ctk.CTkButton(nav_frame, text="Bantuan", image=nav_icon(os.path.join("assets","icons","cart.png")), compound="left", command=self.goto_bantuan, **btn_style)
        self.btn_tentang = ctk.CTkButton(nav_frame, text="Tentang", image=nav_icon(os.path.join("assets","icons","info.png")), compound="left", command=self.goto_tentang, **btn_style)
        self.btn_login = ctk.CTkButton(nav_frame, text="Login", image=nav_icon(os.path.join("assets","icons","user.png")), compound="left", command=self.goto_login, **btn_style)
        self.btn_produk.grid(row=0, column=0, padx=8)
        self.btn_history.grid(row=0, column=1, padx=8)
        self.btn_bantuan.grid(row=0, column=2, padx=8)
        self.btn_tentang.grid(row=0, column=3, padx=8)
        self.btn_login.grid(row=0, column=4, padx=8)
        footer = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        footer.pack(side="bottom", fill="x")
        label_footer = ctk.CTkLabel(footer, text=" 2025 Kedai Mie Ayam & Bakso | Mas Diva Baihaqi | All rights reserved", font=("Poppins", 12), text_color="#b0b0b0")
        label_footer.pack(pady=4)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            if not isinstance(widget, ctk.CTkFrame):
                widget.destroy()

    def show_home(self):
        if self.current_page:
            self.current_page.destroy()
        content = ctk.CTkFrame(self.main_frame, corner_radius=18, fg_color="#f8fafc", border_width=1, border_color="#e0e0e0")
        content.pack(pady=(30, 10), padx=60, fill="both", expand=True)
        label_nama = ctk.CTkLabel(content, text="Kedai Mie Ayam & Bakso", font=("Poppins", 34, "bold"), text_color="#1976d2")
        label_nama.pack(pady=(36, 10))
        if os.path.exists(DEFAULT_IMAGE_PATH):
            img = Image.open(DEFAULT_IMAGE_PATH).resize((200, 200))
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([0,0,img.size[0],img.size[1]], 32, fill=255)
            img.putalpha(mask)
        else:
            img = Image.new("RGBA", (200, 200), color="#dfe4ea")
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
        label_gambar = ctk.CTkLabel(content, image=img_ctk, text="", cursor="hand2")
        label_gambar.pack(pady=10)
        label_gambar.bind("<Button-1>", lambda e: self.zoom_gambar(DEFAULT_IMAGE_PATH))
        label_desc = ctk.CTkLabel(content, text="Selamat datang di Kedai Mie Ayam & Bakso! Nikmati berbagai menu lezat, minuman segar, dan cemilan favorit.", font=("Poppins", 16), wraplength=600, justify="center", text_color="#616161")
        label_desc.pack(pady=(10, 30))
        self.current_page = content

    def zoom_gambar(self, img_path):
        if not os.path.exists(img_path):
            messagebox.showinfo("Gambar tidak ditemukan", "Gambar tidak tersedia.")
            return
        top = ctk.CTkToplevel(self)
        top.title("Zoom Gambar Toko")
        img = Image.open(img_path)
        try:
            resample = getattr(Image, 'LANCZOS', 1)
        except Exception:
            resample = 1
        img = img.resize((min(500, img.width), min(500, img.height)), resample)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        lbl = ctk.CTkLabel(top, image=img_ctk, text="")
        lbl.pack(padx=20, pady=20)
        top.grab_set()

    def goto_produk(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = ProdukPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True)
    def goto_history(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = HistoryPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True)
    def goto_bantuan(self):
        import webbrowser
        webbrowser.open_new_tab("https://wa.me/6282125184884")
    def goto_tentang(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = TentangTokoPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True)
    def goto_login(self):
        if self.current_page:
            self.current_page.destroy()
        def on_login_success():
            self.withdraw()
            AdminDashboard(self)
        LoginPage(self, on_login_success)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 