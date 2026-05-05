import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x600")

        # Данные для генерации
        self.history = []
        self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Ползунок длины пароля
        tk.Label(self.root, text="Длина пароля:").pack(pady=5)
        self.length_scale = ttk.Scale(
            self.root, from_=4, to=50, orient=tk.HORIZONTAL, length=300
        )
        self.length_scale.set(12)
        self.length_scale.pack(pady=5)

        # Отображение текущей длины
        self.length_label = tk.Label(self.root, text="12 символов")
        self.length_scale.bind("<Motion>", self.update_length_label)
        self.length_label.pack()

        # Чекбоксы для символов
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        tk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.use_digits).pack(anchor=tk.W)
        tk.Checkbutton(self.root, text="Буквы (a-z, A-Z)", variable=self.use_letters).pack(anchor=tk.W)
        tk.Checkbutton(self.root, text="Спецсимволы (!@#$%)", variable=self.use_special).pack(anchor=tk.W)

        # Кнопка генерации
        self.generate_btn = tk.Button(
            self.root, text="Сгенерировать пароль", command=self.generate_password
        )
        self.generate_btn.pack(pady=10)

        # Поле вывода пароля
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            self.root, textvariable=self.password_var, font=("Courier", 12), width=40
        )
        self.password_entry.pack(pady=5)

        # Таблица истории
        tk.Label(self.root, text="История паролей:").pack(pady=(20, 5))
        columns = ("ID", "Пароль", "Длина", "Дата создания")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Кнопка очистки истории
        self.clear_btn = tk.Button(
            self.root, text="Очистить историю", command=self.clear_history
        )
        self.clear_btn.pack(pady=5)

        self.refresh_history_table()

    def update_length_label(self, event=None):
        length = int(self.length_scale.get())
        self.length_label.config(text=f"{length} символов")

    def generate_password(self):
        length = int(self.length_scale.get())

        # Проверка минимальной длины
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа!")
            return

        # Формирование набора символов
        chars = ""
        if self.use_digits.get():
            chars += "0123456789"
        if self.use_letters.get():
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.use_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавление в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "timestamp": timestamp
        }
        self.history.append(record)
        self.save_history()
        self.refresh_history_table()

    def refresh_history_table(self):
        # Очистка таблицы
    for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for record in self.history:
            self.tree.insert("", "end", values=(
                record["id"], record["password"], record["length"], record["timestamp"]
            ))

    def save_history(self):
        with open("password_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def load_history(self):
        try:
            if os.path.exists("password_history.json"):
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Не удалось загрузить историю: {e}")
            self.history = []

    def clear_history(self):
        self.history = []
        self.save_history()
        self.refresh_history_table()
        messagebox.showinfo("Успех", "История очищена!")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()