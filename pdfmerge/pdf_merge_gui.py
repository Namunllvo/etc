import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    file_list.set(files)

def merge_files():
    pdfs = file_list.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_path:
        merger = PdfMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        messagebox.showinfo("Success", f"PDFs merged and saved to {output_path}")

root = tk.Tk()
root.title("PDF Merger")

file_list = tk.Variable(value=[])

select_button = tk.Button(root, text="Select PDFs", command=select_files)
merge_button = tk.Button(root, text="Merge PDFs", command=merge_files)

select_button.pack(pady=20)
merge_button.pack(pady=20)

root.mainloop()
