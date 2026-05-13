import sys
import os
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class TicketCalculator:
    def __init__(self):
        self.root = Tk()
        self.root.title("Калькулятор стоимости билетов")
        self.root.geometry("480x740")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F7FA")

        self.set_icon()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        self.entry_host = None
        self.entry_guest = None
        self.entry_price = None
        self.entry_kof = None
        self.result_label = None

        # Переменные
        self.host_var = StringVar()
        self.guest_var = StringVar()
        self.price_var = StringVar()
        self.kof_var = StringVar()
        self.topmost_var = BooleanVar(value=False)

        self.create_widgets()
        self.root.bind("<Return>", lambda e: self.calculate())

    @staticmethod
    def resource_path(relative_path):
        """Получает правильный путь при запуске из .exe"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def set_icon(self):
        """Установка иконки"""
        icon_path = self.resource_path("icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
                return
            except:
                pass

        # Запасной вариант
        icon_path = self.resource_path("icon.png")
        if os.path.exists(icon_path):
            try:
                img = PhotoImage(file=icon_path)
                self.root.iconphoto(True, img)
            except:
                pass

    def _configure_styles(self):
        self.style.configure("TFrame", background="#F5F7FA")
        self.style.configure("TLabel", background="#F5F7FA", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1E3A8A")
        self.style.configure("TEntry", fieldbackground="white", font=("Segoe UI", 11), padding=10)
        self.style.configure("Error.TEntry", fieldbackground="#FFEBEE", foreground="#D32F2F")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10)
        self.style.map("TButton", background=[("active", "#1E40AF")])

        self.style.configure("Result.TFrame", background="#EFF6FF")
        self.style.configure("Result.TLabel", background="#EFF6FF",
                             font=("Segoe UI", 14, "bold"), foreground="#1E40AF", padding=25)
        self.style.configure("Tip.TLabel", font=("Segoe UI", 10, "italic"), foreground="#64748B")

    def _setup_comma_replacement(self, var, entry):
        """Автоматически заменяет запятую на точку и обновляет подсветку поля."""
        def replace_comma(*args):
            val = var.get()
            if ',' in val:
                var.set(val.replace(',', '.'))
                self.validate_field(entry)
        var.trace_add('write', replace_comma)

    def validate_input(self, value):
        """Валидация ввода (поддерживает запятую как разделитель)."""
        if value in ("", "."):
            return True
        # Разрешаем только один разделитель (точка или запятая)
        if value.count('.') + value.count(',') > 1:
            return False
        # Проверяем, можно ли преобразовать в число после замены запятой на точку
        try:
            float(value.replace(',', '.'))
            return True
        except ValueError:
            return False

    def validate_field(self, entry, reset=False):
        """Подсветка поля: красный, если значение <= 0 или невалидное, иначе обычный."""
        if reset:
            entry.configure(style="TEntry")
            return
        value = entry.get().strip().replace(',', '.')
        # Пустое поле, одна точка или минус не считаются ошибкой
        if value in ("", ".", "-"):
            entry.configure(style="TEntry")
            return
        try:
            num = float(value)
            if num <= 0:
                entry.configure(style="Error.TEntry")
            else:
                entry.configure(style="TEntry")
        except ValueError:
            entry.configure(style="Error.TEntry")

    def toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    @staticmethod
    def calculate_result(x1: float, x2: float, ids: float, kof: float) -> int:
        try:
            kf = x1 / (ids / kof)
            price = ((x2 - x1) / kf) + ids
            return math.floor(price)
        except:
            return 0

    def calculate(self):
        try:
            x1 = float(self.host_var.get() or 0)
            x2 = float(self.guest_var.get() or 0)
            ids = float(self.price_var.get() or 0)
            kof = float(self.kof_var.get() or 0)

            if any(v <= 0 for v in (x1, x2, ids, kof)):
                raise ValueError("Все значения должны быть больше 0")

            result = self.calculate_result(x1, x2, ids, kof)
            self.result_label.config(text=f"Рекомендуемая цена: {result}", foreground="#1E40AF")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception:
            messagebox.showerror("Ошибка", "Проверьте корректность данных")

    def clear_fields(self):
        for var in (self.host_var, self.guest_var, self.price_var, self.kof_var):
            var.set("")
        for entry in (self.entry_host, self.entry_guest, self.entry_price, self.entry_kof):
            self.validate_field(entry, reset=True)
        self.result_label.config(text="Результат появится здесь", foreground="#1E40AF")

    def create_widgets(self):
        mainframe = ttk.Frame(self.root, padding="35 30 35 30")
        mainframe.pack(fill="both", expand=True)

        ttk.Label(mainframe, text="Калькулятор стоимости билетов",
                  style="Header.TLabel").pack(anchor="center", pady=(0, 25))

        # Поверх всех окон
        top_frame = ttk.Frame(mainframe)
        top_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(top_frame, text="Поверх всех окон:", font=("Segoe UI", 11)).pack(side="left")
        ttk.Radiobutton(top_frame, text="Вкл", variable=self.topmost_var, value=True,
                        command=self.toggle_topmost).pack(side="left", padx=(15, 8))
        ttk.Radiobutton(top_frame, text="Выкл", variable=self.topmost_var, value=False,
                        command=self.toggle_topmost).pack(side="left")

        # Поля ввода
        card = ttk.Frame(mainframe)
        card.pack(fill="x", pady=10)

        fields = [
            ("КД хозяев:", self.host_var),
            ("КД гостей:", self.guest_var),
            ("Рек. цена:", self.price_var),
            ("КФ:", self.kof_var)
        ]

        for i, (text, var) in enumerate(fields):
            row = ttk.Frame(card)
            row.pack(fill="x", pady=8)

            ttk.Label(row, text=text, width=16).pack(side="left")

            entry = ttk.Entry(row, textvariable=var, width=25,
                              validate="all",
                              validatecommand=(self.root.register(self.validate_input), '%P'))
            entry.pack(side="left", padx=12, fill="x", expand=True)

            # Настройка замены запятой и валидации при любом изменении
            self._setup_comma_replacement(var, entry)
            # Дополнительная подсветка при отпускании клавиши (KeyRelease)
            entry.bind("<KeyRelease>", lambda e, ent=entry: self.validate_field(ent))

            if i == 0: self.entry_host = entry
            elif i == 1: self.entry_guest = entry
            elif i == 2: self.entry_price = entry
            elif i == 3: self.entry_kof = entry

        # Кнопки
        btn_frame = ttk.Frame(mainframe)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="Рассчитать", command=self.calculate, width=18).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_fields, width=18).pack(side="left", padx=6)

        # Результат
        result_frame = ttk.Frame(mainframe, style="Result.TFrame")
        result_frame.pack(fill="x", pady=20, ipadx=10, ipady=15)
        self.result_label = ttk.Label(result_frame, text="Результат появится здесь",
                                      style="Result.TLabel", anchor="center")
        self.result_label.pack(fill="both", expand=True)

        # Подсказка
        tip_frame = ttk.Frame(mainframe)
        tip_frame.pack(fill="x", pady=(10, 0))
        ttk.Label(tip_frame, text="*КФ — коэффициент для вашей команды,\nподбирается индивидуально,\nот 2.1 до 4.9\nСредний по проекту 3.0",
                  style="Tip.TLabel", justify="center").pack()

        self.entry_host.focus()


if __name__ == "__main__":
    app = TicketCalculator()
    app.root.mainloop()