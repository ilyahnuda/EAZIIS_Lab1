import threading
import tkinter as tk
from idlelib.redirector import WidgetRedirector
from tkinter import simpledialog, messagebox
from tkinter.filedialog import askopenfilename

from model import document_handler
from model.dictionary_handler.dictionary_handler import DictionaryHandler, remove_structure_symbols
from model.document_handler.document_handler import DocumentHandler
from model.lexeme_handler.lexeme_handler import pos_representation, cases_representation
from fpdf import FPDF


class MainWindow:
    def __init__(self):
        self._window = tk.Tk()
        self._is_window_opened = False
        self._txt_edit = tk.Text(self._window)
        self._dictionary_documentation_txt_edit = tk.Text(self._window)
        self._frame_buttons = tk.Frame(self._window)
        self._dictionary_documentation_label = tk.Label(self._window, text="Документирование словаря")
        self._button_open = tk.Button(self._frame_buttons, text="Открыть файл", command=self.open_file)
        self._button_append = tk.Button(self._frame_buttons, text="Добавить файл",
                                        command=self.append_file)
        self._button_save = tk.Button(self._frame_buttons, text="Сохранить файл", command=self.save_file)
        self._button_search = tk.Button(self._frame_buttons, text="Поиск лексем",
                                        command=self.search)
        self._button_add = tk.Button(self._frame_buttons, text="Добавление лексемы",
                                     command=self.add)
        self._button_edit = tk.Button(self._frame_buttons, text="Изменение лексемы", command=self.edit)
        self._button_generate = tk.Button(self._frame_buttons, text="Генерация словоформы",
                                          command=self.generate)
        self._button_help = tk.Button(self._frame_buttons, text="Помощь",
                                      command=self.about)
        self._handler = DictionaryHandler

    def start(self):
        self._configure_window()
        self._window.mainloop()

    def _configure_window(self):
        self._window.title("Словарь естественного языка")
        self._window.rowconfigure(0, minsize=100, weight=1)
        self._window.columnconfigure(1, minsize=1100, weight=1)
        self._button_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self._button_append.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self._button_search.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self._button_add.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self._button_edit.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self._button_generate.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self._button_help.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        self._button_save.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        self._frame_buttons.grid(row=0, column=0, sticky="ns")
        self._txt_edit.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self._dictionary_documentation_label.grid(row=1, column=0, ipady=5)
        self._dictionary_documentation_txt_edit.grid(row=2, column=0, sticky="e", ipady=5)
        self._dictionary_documentation_txt_edit.configure(width=30, borderwidth=10)

        # readonly text field
        self._txt_edit.redirector = WidgetRedirector(self._txt_edit)
        self._txt_edit.insert = self._txt_edit.redirector.register("insert", lambda *args, **kw: "break")
        self._txt_edit.delete = self._txt_edit.redirector.register("delete", lambda *args, **kw: "break")

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("Текстовый документ", "*.pdf")]
        )
        if not filepath:
            return
        self._handler = DictionaryHandler(filepath)
        content = self._handler.get_full_dictionary_string(self._handler.get_dictionary())
        self._refill_txt_edit(content)
        self._is_window_opened = True

    def append_file(self):
        if not self._is_window_opened:
            messagebox.showerror("Ошибка добавления файла", "Для начала откройте файл")
            return
        filepath = askopenfilename(
            filetypes=[("Текстовый документ", "*.pdf")]
        )
        if not filepath:
            return
        self._handler.append_document(filepath)
        content = self._handler.get_full_dictionary_string(self._handler.get_dictionary())
        self._refill_txt_edit(content)

    def search(self):
        if not self._is_window_opened:
            messagebox.showerror("Ошибка поиска", "Для начала откройте файл")
            return
        query = simpledialog.askstring("Поиск", "Введите запрос",
                                       parent=self._window)
        if not query:
            return
        normal_form = self._handler.get_lexeme_structure_by_normal_form(query)
        if self._handler.get_lexeme_structure(query):
            messagebox.showinfo("Информация о \"" + query + " \"",
                                remove_structure_symbols(str(self._handler.get_lexeme_structure(query))))
        elif query in list(pos_representation.values()):
            messagebox.showinfo("Лексемы части речи \"" + query + "\"",
                                self._handler.get_lexeme_structures_by_pos(query))
        elif query in list(cases_representation.values()):
            messagebox.showinfo("Лексемы падежа \"" + query + "\"",
                                self._handler.get_lexeme_structures_by_case(query))
        elif normal_form:
            messagebox.showinfo("Начальная форма \"" + query + "\"",
                                normal_form)
        else:
            messagebox.showwarning("Внимание", "Лексема \"" + query + "\" не найдена")

    def add(self):
        if not self._is_window_opened:
            messagebox.showerror("Ошибка добавления лексемы", "Для начала откройте файл")
            return
        lexeme = simpledialog.askstring("Добавление", "Введите лексему",
                                        parent=self._window)
        try:
            self._handler.add_lexeme_structure(lexeme)
            messagebox.showinfo("Лексема \"" + lexeme + "\" добавлена",
                                remove_structure_symbols(str(self._handler.get_lexeme_structure(lexeme))))

            content = self._handler.get_full_dictionary_string(self._handler.get_dictionary())
            self._refill_txt_edit(content)
        except AttributeError:
            messagebox.showerror("Ошибка", "Лексема \"" + lexeme + "\" не найдена")

    def edit(self):
        if not self._is_window_opened:
            messagebox.showerror("Ошибка изменения", "Для начала откройте файл")
            return
        edit_window = tk.Tk()
        edit_window.title("Изменение лексемы")
        edit_window.rowconfigure(0, minsize=200, weight=1)
        edit_window.columnconfigure(1, minsize=300, weight=1)

        frame_entries = tk.Frame(edit_window)

        tk.Label(frame_entries, text="Лексема").grid(row=0, column=0, sticky="ew")
        tk.Label(frame_entries, text="Свойство").grid(row=1, column=0, sticky="ew")
        tk.Label(frame_entries, text="Значение").grid(row=2, column=0, sticky="ew")

        entry_lexeme = tk.Entry(frame_entries)
        entry_prop = tk.Entry(frame_entries)
        entry_value = tk.Entry(frame_entries)

        entry_lexeme.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        entry_prop.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        entry_value.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        button_ok = tk.Button(frame_entries, text="Изменить")
        button_ok['command'] = lambda l=entry_lexeme, p=entry_prop, v=entry_value: self.edit_lexeme(l, p, v)
        button_ok.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        frame_entries.grid(row=0, column=0, sticky="ns")
        edit_window.mainloop()

    def edit_lexeme(self, entry_lexeme, entry_prop, entry_value):
        lexeme = entry_lexeme.get()
        prop = entry_prop.get()
        value = entry_value.get()
        self._handler.edit_lexeme_structure(lexeme, prop, value)
        content = self._handler.get_full_dictionary_string(self._handler.get_dictionary())
        self._refill_txt_edit(content)

    def generate(self):
        if not self._is_window_opened:
            messagebox.showerror("Ошибка генерации", "Для начала откройте файл")
            return
        generate_window = tk.Tk()
        generate_window.title("генерация словоформы")
        generate_window.rowconfigure(0, minsize=200, weight=1)
        generate_window.columnconfigure(1, minsize=300, weight=1)

        frame_entries = tk.Frame(generate_window)

        tk.Label(frame_entries, text="Лексема").grid(row=0, column=0, sticky="ew")
        tk.Label(frame_entries, text="Падеж").grid(row=1, column=0, sticky="ew")
        tk.Label(frame_entries, text="Число").grid(row=2, column=0, sticky="ew")

        entry_lexeme = tk.Entry(frame_entries)
        entry_prop = tk.Entry(frame_entries)
        entry_singular = tk.Entry(frame_entries)

        entry_lexeme.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        entry_prop.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        entry_singular.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        button_ok = tk.Button(frame_entries, text="Сгенерировать словоформу")
        button_ok['command'] = lambda l=entry_lexeme, p=entry_prop, v=entry_singular: self.generate_lexeme(l, p, v)
        button_ok.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        frame_entries.grid(row=0, column=0, sticky="ns")
        generate_window.mainloop()

    def generate_lexeme(self, entry_lexeme, entry_case, entry_singular):
        lexeme = entry_lexeme.get()
        case = entry_case.get()
        singular = entry_singular.get()
        if singular == "Единственное":
            singular = True
        else:
            singular = False
        self._handler.generate_wordform(lexeme, case, singular)
        content = self._handler.get_full_dictionary_string(self._handler.get_dictionary())
        self._refill_txt_edit(content)

    def _refill_txt_edit(self, content: str):
        self._txt_edit.delete("1.0", tk.END)
        self._txt_edit.insert(tk.END, content)

    @staticmethod
    def run_on_new_thread(function):
        threading.Thread(target=function).start()

    @staticmethod
    def about():
        messagebox.showinfo("Помощь",
                            "Для начала работы откройте файл.\nФормат PDF.\nЯзык русский.\nВозможности поиска:"
                            " запись по лексеме или основе слова, поиск всех лексем по падежу, по части речи.")

    def save_file(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Arial", "", "arial.ttf", uni=True)
        pdf.set_font("Arial", size=8)
        sentence = (self._handler.get_full_dictionary_string(self._handler.get_dictionary())).split("\n")
        path = self._handler.get_document().get_file_path().split("\\")
        for i in sentence:
            pdf.cell(0, 5, i, ln=1)
        pdf.output(f"write_{path[-1]}")
