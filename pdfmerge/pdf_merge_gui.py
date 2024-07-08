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

# 화면 크기
windows_width = root.winfo_screenwidth()
windows_height = root.winfo_screenheight()

print(windows_width, windows_height)

# 센터
center_width = (windows_width/2)-(300/2)
center_height = (windows_height/2)-(300/2)

file_list = tk.Variable(value=[])

select_button = tk.Button(root, text="Select PDFs", command=select_files)
merge_button = tk.Button(root, text="Merge PDFs", command=merge_files)

select_button.pack(padx=20, pady=10, ipadx=20, ipady=10)
merge_button.pack(padx=20, pady=10, ipadx=20, ipady=10)

root.geometry(f"300x300+{int(center_width)}+{int(center_height)}")

root.mainloop()
