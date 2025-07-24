import tkinter as tk
from tkinter import messagebox
import requests
import hashlib
import pyperclip
from zxcvbn import zxcvbn
import random
import string

# --- Check if password is in a data breach ---
def checkpass(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{first5}"
    response = requests.get(url)
    
    hashes = (line.split(':') for line in response.text.splitlines())
    return any(tail == h for h, _ in hashes)

# --- Check password strength using zxcvbn ---
def check_strength(password):
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']['warning'] or 'Strong Password!'
    return score, feedback

# --- Generate strong random password ---
def generate_pass(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# --- Evaluate password function ---
def evaluate_password():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("WARNING", "Please enter a password:")
        return
    score, feedback = check_strength(password)
    breached = checkpass(password)
    
    strength_label.config(text=f"Strength: {'★' * (score + 1)}")
    feedback_label.config(text=f"Note: {feedback}")
    if breached:
        breach_label.config(text="⚠️ This password has been breached!")
    else:
        breach_label.config(text="✅ This password is safe.")

# --- Generate password button ---
def gen_password():
    password = generate_pass()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# --- Copy to clipboard ---
def copy_password():
    pyperclip.copy(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard.")

# --- Toggle show/hide password ---
def toggle_password():
    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# --- GUI Setup ---
app = tk.Tk()
app.title("🔐 PassGuardian")
app.geometry("400x350")
app.configure(bg="#1e1e1e")

# Label + Entry
tk.Label(app, text="Enter Password:", fg="white", bg="#1e1e1e").pack(pady=5)
password_entry = tk.Entry(app, show="*", width=30, font=('Arial', 12))
password_entry.pack(pady=5)

# Show password checkbox
show_password = tk.BooleanVar()
tk.Checkbutton(app, text="Show Password", variable=show_password, command=toggle_password, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack(pady=2)

# Buttons
tk.Button(app, text="Check Password", command=evaluate_password, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(app, text="Generate Password", command=gen_password, bg="#2196F3", fg="white").pack(pady=5)
tk.Button(app, text="Copy to Clipboard", command=copy_password, bg="#FF5722", fg="white").pack(pady=5)

# Output Labels
strength_label = tk.Label(app, text="", fg="gold", bg="#1e1e1e", font=('Arial', 10))
strength_label.pack(pady=5)

feedback_label = tk.Label(app, text="", fg="white", bg="#1e1e1e", wraplength=350)
feedback_label.pack(pady=5)

breach_label = tk.Label(app, text="", fg="red", bg="#1e1e1e", font=('Arial', 10))
breach_label.pack(pady=5)

# Run App
app.mainloop()
