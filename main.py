import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from docx import Document
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdf_exporter import export_to_pdf

doc1_path = ""
doc2_path = ""
plagiarism_score = 0.0
doc1_text = ""
doc2_text = ""

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text(file_path)
    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format.")

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

def browse_file(target):
    global doc1_path, doc2_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF and DOCX files", "*.pdf *.docx")])
    if file_path:
        if target == 1:
            doc1_path = file_path
            doc1_label.config(text=os.path.basename(file_path))
        else:
            doc2_path = file_path
            doc2_label.config(text=os.path.basename(file_path))

def update_spinner(active, root_ref):
    def toggle_ui():
        if active:
            spinner.start()
            check_btn.config(state=tk.DISABLED)
            export_btn.config(state=tk.DISABLED)
        else:
            spinner.stop()
            check_btn.config(state=tk.NORMAL)
            export_btn.config(state=tk.NORMAL)
    root_ref.after(0, toggle_ui)

def check_plagiarism():
    thread = threading.Thread(target=run_similarity_task)
    thread.start()

def run_similarity_task():
    global doc1_text, doc2_text, plagiarism_score
    update_spinner(True, root)
    try:
        if not doc1_path or not doc2_path:
            raise ValueError("Please upload both documents.")
        doc1_text = extract_text_from_file(doc1_path)
        doc2_text = extract_text_from_file(doc2_path)
        if not doc1_text.strip() or not doc2_text.strip():
            raise ValueError("One or both documents are empty.")
        score = calculate_similarity(doc1_text, doc2_text)
        plagiarism_score = round(score * 100, 2)
        result_str = f"🔍 Plagiarism Score: {plagiarism_score}%"
        result_label.config(text=result_str)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    update_spinner(False, root)

def export_result():
    if not doc1_text or not doc2_text:
        messagebox.showerror("Error", "Run plagiarism check first.")
        return
    try:
        export_to_pdf(doc1_path, doc2_path, plagiarism_score, doc1_text, doc2_text)
        messagebox.showinfo("Success", "Exported to plagiarism_report.pdf")
    except Exception as e:
        messagebox.showerror("Export Failed", str(e))

# GUI Setup
root = tk.Tk()
root.title("🧠 Plagiarism Checker")
root.geometry("600x400")
root.resizable(False, False)

title = tk.Label(root, text="📄 Plagiarism Detection Tool", font=("Helvetica", 16, "bold"))
title.pack(pady=20)

doc1_frame = tk.Frame(root)
doc1_frame.pack(pady=5)
tk.Label(doc1_frame, text="Upload Document 1:").pack(side=tk.LEFT, padx=10)
tk.Button(doc1_frame, text="Browse", command=lambda: browse_file(1)).pack(side=tk.LEFT)
doc1_label = tk.Label(doc1_frame, text="No file selected", fg="gray")
doc1_label.pack(side=tk.LEFT, padx=10)

doc2_frame = tk.Frame(root)
doc2_frame.pack(pady=5)
tk.Label(doc2_frame, text="Upload Document 2:").pack(side=tk.LEFT, padx=10)
tk.Button(doc2_frame, text="Browse", command=lambda: browse_file(2)).pack(side=tk.LEFT)
doc2_label = tk.Label(doc2_frame, text="No file selected", fg="gray")
doc2_label.pack(side=tk.LEFT, padx=10)

check_btn = tk.Button(root, text="✅ Check Plagiarism", font=("Arial", 12), command=check_plagiarism)
check_btn.pack(pady=20)

spinner = ttk.Progressbar(root, mode='indeterminate')
spinner.pack()

result_label = tk.Label(root, text="Result will appear here", font=("Arial", 14), fg="blue")
result_label.pack(pady=10)

export_btn = tk.Button(root, text="📤 Export Report", command=export_result)
export_btn.pack(pady=10)

root.mainloop()