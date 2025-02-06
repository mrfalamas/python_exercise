import tkinter as tk
from tkinter import filedialog, messagebox
import re
import webbrowser
import os
import html

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Selecteaza fisierul")
        self.root.geometry("400x300")
        self.file_path = ""
        self.html_file_path = ""

        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self.root, text ="Selecteaza fisierul", command=self.select_file, width=25, height=2)
        self.select_button.pack(pady=10)

        self.html_button = tk.Button(self.root, text ="Genereaza HTML", command=self.html_generate, width=25, height=2)
        self.html_button.pack(pady=10)

        self.open_button = tk.Button(self.root, text ="Deschide fisierul HTML", command=self.open_html, width=25, height=2)
        self.open_button.pack(pady=10)
        self.open_button.config(state=tk.DISABLED)

        self.exit_button = tk.Button(self.root, text ="Exit", command=self.root.quit, width=25, height=2)
        self.exit_button.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            self.read_and_display_file()
        
    def read_and_display_file(self):
               
        try:
            with open(self.file_path, "r") as file:
                content = file.read()    
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la citirea fișierului: {e}")

    def html_generate(self):
        if not self.file_path:
            messagebox.showwarning("Atentie","Nu ai selectat un fisier text")
            return

        try:
            with open(self.file_path, "r") as file:
                content = file.read()

            students_data = re.findall(r"([A-Za-z]+):\s*([0-9, ]+)", content)

            table_rows = ""
            for name, grades in students_data:
                grades_list = [int(grade.strip()) for grade in grades.split(',')]
                average = sum(grades_list) / len(grades_list)
                
                result = "Passed" if average >= 50 else "Failed"
                result_color = "green" if average >= 50 else "red"

                table_rows += f"""
                <tr>
                    <td>{name}</td>
                    <td>{grades}</td>
                    <td>{average:.2f}</td>
                    <td style="color: {result_color};">{result}</td>
                </tr>
                """

            template_path = os.path.abspath("template.html")
            with open(template_path, "r") as template_file:
                html_template = template_file.read()

            html_content = html_template.format(
                table_rows = table_rows,
            )

            self.html_file_path = self.file_path.rsplit('.', 1)[0] + "_content.html"
            with open(self.html_file_path, "w") as html_file:
                html_file.write(html_content)

            #messagebox.showinfo("Succes", f"Fisierul HTML a fost creat: {self.html_file_path}")
            self.open_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la generarea fișierului HTML: {e}")

    def open_html(self):
        if self.html_file_path:
            webbrowser.open(f"file://{os.path.abspath(self.html_file_path)}")
        else:
            messagebox.showwarning("Atentie", "Nu a fost generat niciun fisier HTML")


def main():
    print('hello world')
    root = tk.Tk()
    app = Student(root)
    root.mainloop()

     
if __name__ == "__main__": 
    main()