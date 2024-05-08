import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import odev4  # Metin karşılaştırma algoritmalarını içeren modül

# SQLite veritabanı bağlantısı
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        self.conn.commit()

    def check_credentials(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if self.cur.fetchone():
            return True
        else:
            return False

    def save_credentials(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        self.conn.commit()

    def update_password(self, username, new_password):
        self.cur.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        self.conn.commit()

class TextCompareWindow:
    def __init__(self, master, algorithm_name):
        self.master = master
        self.algorithm_name = algorithm_name

    def create_window(self):
        self.window = tk.Toplevel(self.master)
        self.window.title(f"Metin Karşılaştırma - {self.algorithm_name}")

        self.file1_label = tk.Label(self.window, text="Dosya 1:")
        self.file1_label.pack()
        self.file1_entry = tk.Entry(self.window)
        self.file1_entry.pack()

        self.file2_label = tk.Label(self.window, text="Dosya 2:")
        self.file2_label.pack()
        self.file2_entry = tk.Entry(self.window)
        self.file2_entry.pack()

        self.select_file_button1 = tk.Button(self.window, text="Dosya Seç", command=self.select_file1)
        self.select_file_button1.pack()

        self.select_file_button2 = tk.Button(self.window, text="Dosya Seç", command=self.select_file2)
        self.select_file_button2.pack()

        self.compare_button = tk.Button(self.window, text="Karşılaştır", command=self.compare_texts)
        self.compare_button.pack()

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()

    def select_file1(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file1_entry.delete(0, tk.END)
        self.file1_entry.insert(0, filename)

    def select_file2(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file2_entry.delete(0, tk.END)
        self.file2_entry.insert(0, filename)

    def compare_texts(self):
        file1_path = self.file1_entry.get()
        file2_path = self.file2_entry.get()

        if not file1_path or not file2_path:
            messagebox.showerror("Hata", "Lütfen her iki dosya için de geçerli bir yol belirtin.")
            return

        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
                text1 = file1.read()
                text2 = file2.read()

                # Algoritma adına göre metinleri karşılaştır
                if self.algorithm_name == "Benzerlik Hesapla":
                    similarity_score = odev4.benzerlik_hesapla(text1, text2, 100)
                    self.result_label.config(text=f"Metin Benzerliği: {similarity_score:.2f}")

                elif self.algorithm_name == "Jaccard Hesapla":
                    similarity_index = odev4.jaccard_similarity(text1, text2)
                    result_text = f"Jaccard Benzerlik İndeksi: {similarity_index:.4f}"
                    self.result_label.config(text=result_text)

                # Karşılaştırma sonucunu ekranda göster

        except FileNotFoundError:
            messagebox.showerror("Hata", "Dosya bulunamadı.")

# Ana uygulama sınıfı
class Application:
    def __init__(self, master):
        self.master = master
        self.database = Database()
        self.username = ""  # Kullanıcı adını saklamak için bir özellik ekleyin

        self.create_login_screen()

    def create_login_screen(self):
        self.master.title("Giriş Ekranı")

        self.username_label = tk.Label(self.master, text="Kullanıcı Adı:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Şifre:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Giriş Yap", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.master, text="Kayıt Ol", command=self.register)
        self.register_button.pack()

    def create_main_menu(self):
        # Ana menü oluştur
        self.login_button.destroy()
        self.register_button.destroy()
        self.username_label.destroy()
        self.username_entry.destroy()
        self.password_label.destroy()
        self.password_entry.destroy()
        self.master.title("Ana Menü")

        self.compare_button = tk.Button(self.master, text="Karşılaştır", command=self.compare_menu)
        self.compare_button.pack()

        self.operations_button = tk.Button(self.master, text="İşlemler", command=self.operations_menu)
        self.operations_button.pack()

        self.exit_button = tk.Button(self.master, text="Çıkış", command=self.master.quit)
        self.exit_button.pack()

    def change_password_menu(self):
        # Şifre değiştirme menüsünü oluştur
        self.update_password_frame = tk.Frame(self.master)
        self.update_password_frame.pack()

        self.new_password_label = tk.Label(self.update_password_frame, text="Yeni Şifre:")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.update_password_frame, show="*")
        self.new_password_entry.pack()

        self.update_button = tk.Button(self.update_password_frame, text="Güncelle", command=self.update_password)
        self.update_button.pack()

    def update_password(self):
        new_password = self.new_password_entry.get()

        if self.username:  # Geçerli bir kullanıcı adı varsa
            # Kullanıcı adını kullanarak şifreyi güncelle
            self.database.update_password(self.username, new_password)
            messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi!")
        else:
            messagebox.showerror("Hata", "Kullanıcı adı bulunamadı.")

    def operations_menu(self):
        # İşlemler menüsünü oluştur
        self.operations_frame = tk.Frame(self.master)
        self.operations_frame.pack()

        self.password_button = tk.Button(self.operations_frame, text="Şifre", command=self.password_menu)
        self.password_button.pack()

    def password_menu(self):
        # Şifre menüsünü oluştur
        self.operations_frame.destroy()  # Önceki menüyü kaldır

        self.password_frame = tk.Frame(self.master)
        self.password_frame.pack()

        self.change_password_button = tk.Button(self.password_frame, text="Değiştir", command=self.change_password_menu)
        self.change_password_button.pack()

    def compare_menu(self):
        # Karşılaştırma menüsünü oluştur
        self.compare_window = tk.Toplevel(self.master)
        self.compare_window.title("Metin Karşılaştırma")

        self.algorithm_label = tk.Label(self.compare_window, text="Karşılaştırma Algoritması Seçin:")
        self.algorithm_label.pack()

        # Ödev4 modülündeki algoritmaları burada listeleyebilirsiniz
        algorithms = ["Benzerlik Hesapla", "Jaccard Hesapla"]  # Örnek algoritma adları
        for algorithm in algorithms:
            algorithm_button = tk.Button(self.compare_window, text=algorithm, command=self.open_text_compare_window(algorithm))
            algorithm_button.pack(pady=5)

    def open_text_compare_window(self, algorithm_name):
        def wrapper():
            compare_window = TextCompareWindow(self.compare_window, algorithm_name)
            compare_window.create_window()
        return wrapper

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.database.check_credentials(username, password):
            self.username = username  # Giriş yapan kullanıcı adını saklayın
            self.create_main_menu()  # Ana menüyü oluştur
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.database.check_credentials(username, password):
            messagebox.showerror("Hata", "Bu kullanıcı zaten var!")
        else:
            self.database.save_credentials(username, password)
            messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaydedildi!")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
