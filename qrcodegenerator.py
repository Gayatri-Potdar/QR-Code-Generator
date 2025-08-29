import qrcode
import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

root = tk.Tk()
root.title("🎓 Student QR Code Generator & Scanner")
root.geometry("700x800")
root.configure(bg="#f0f4f7")
root.resizable(False, False)

current_qr = None
current_data = ""

if not os.path.exists("QRCodes"):
    os.makedirs("QRCodes")

# ---------------- Functions ----------------
def generate_qr():
    global current_qr, current_data

    name = entry_name.get().strip()
    student_class = entry_class.get().strip()
    year = entry_year.get().strip()
    college_id = entry_college_id.get().strip()
    passout_year = entry_passout.get().strip()

    if not (name and student_class and year and college_id and passout_year):
        messagebox.showwarning("⚠ Input Error", "Please fill all fields")
        return

    current_data = (
        f"Name: {name}\n"
        f"Class: {student_class}\n"
        f"Year: {year}\n"
        f"College ID: {college_id}\n"
        f"Passout Year: {passout_year}"
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(current_data)
    qr.make(fit=True)

    current_qr = qr.make_image(fill_color="black", back_color="white")

    preview = current_qr.resize((280, 280), Image.Resampling.LANCZOS)
    qr_photo = ImageTk.PhotoImage(preview)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo


def save_qr():
    global current_qr, current_data

    if current_qr is None:
        messagebox.showwarning("⚠ Error", "Generate a QR code first")
        return

    name = entry_name.get().strip().replace(" ", "_")
    college_id = entry_college_id.get().strip()
    filename = f"{college_id}_{name}.png"
    file_path = os.path.join("QRCodes", filename)

    current_qr.save(file_path)
    messagebox.showinfo("✅ Saved", f"QR Code saved:\n{file_path}")


def scan_qr():
    file_path = filedialog.askopenfilename(
        title="Select QR Code",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if not file_path:
        return

    img = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        messagebox.showinfo("📖 QR Data", f"{data}")
    else:
        messagebox.showerror("❌ Error", "No QR code found!")


# ---------------- UI Design ----------------
title = tk.Label(root, text="🎓 Student QR Code Generator & Scanner",
                 font=("Arial", 20, "bold"), bg="#f0f4f7", fg="#333")
title.pack(pady=15)

# Frame for input fields
frame_inputs = tk.Frame(root, bg="white", bd=2, relief="groove")
frame_inputs.pack(pady=10, padx=20, fill="x")

tk.Label(frame_inputs, text="Enter Student Details", font=("Arial", 14, "bold"),
         bg="white", fg="#222").pack(pady=10)

def add_field(label):
    tk.Label(frame_inputs, text=label, font=("Arial", 11), bg="white").pack(anchor="w", padx=20)
    entry = tk.Entry(frame_inputs, font=("Arial", 11), width=40, bd=2, relief="groove")
    entry.pack(padx=20, pady=5)
    return entry

entry_name = add_field("Name:")
entry_class = add_field("Class:")
entry_year = add_field("Year:")
entry_college_id = add_field("College ID:")
entry_passout = add_field("Passout Year:")

# Buttons
frame_buttons = tk.Frame(root, bg="#f0f4f7")
frame_buttons.pack(pady=15)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=8)

btn_generate = ttk.Button(frame_buttons, text="✨ Generate QR", command=generate_qr)
btn_generate.grid(row=0, column=0, padx=10)

btn_save = ttk.Button(frame_buttons, text="💾 Save QR", command=save_qr)
btn_save.grid(row=0, column=1, padx=10)

btn_scan = ttk.Button(frame_buttons, text="🔍 Scan QR", command=scan_qr)
btn_scan.grid(row=0, column=2, padx=10)

# QR Preview
frame_qr = tk.Frame(root, bg="white", bd=2, relief="groove")
frame_qr.pack(pady=20)

tk.Label(frame_qr, text="QR Preview", font=("Arial", 14, "bold"),
         bg="white", fg="#222").pack(pady=10)

qr_label = tk.Label(frame_qr, bg="white", width=300, height=300)
qr_label.pack(pady=10)

root.mainloop()
