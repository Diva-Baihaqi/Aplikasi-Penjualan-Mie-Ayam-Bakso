import customtkinter as ctk
from tkinter import messagebox

class LoginPage(ctk.CTkToplevel):
    def __init__(self, master, on_success, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Login Admin")
        self.geometry("400x320")
        self.resizable(False, False)
        self.on_success = on_success
        self.create_widgets()

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="Login Admin", font=("Poppins", 22, "bold"))
        self.label_title.pack(pady=(30,10))
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username", font=("Poppins", 14))
        self.entry_username.pack(pady=12, fill="x", padx=60)
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*", font=("Poppins", 14))
        self.entry_password.pack(pady=12, fill="x", padx=60)
        self.btn_login = ctk.CTkButton(self, text="Login", command=self.login, font=("Poppins", 15, "bold"), height=38)
        self.btn_login.pack(pady=(24,10), fill="x", padx=60)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if username == "admin" and password == "admin":
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!") 