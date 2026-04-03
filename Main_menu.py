import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import os
import subprocess
import time

def launch_program(program_name, window, close_window=False):
    if os.path.exists(program_name):
        subprocess.Popen(["python", program_name])
        if close_window:
            window.destroy()
    else:
        messagebox.showerror("Error", f"{program_name} not found.")

def fade_in(window, steps=5, delay=17):
    for i in range(steps):
        window.attributes("-alpha", i / steps)
        window.update()
        time.sleep(delay / 1000)

def animation():
    title_text = "LIBRARY MANAGEMENT SYSTEM"
    def animate_title(i=0):
        if i <= len(title_text):
            title_label.config(text=title_text[:i])
            window.after(22, animate_title, i + 1)

    def color_cycle():
        colors = ["#2980B9", "#3498DB", "#2980B9"]
        def cycle_color(index=0):
            if index < len(colors):
                title_label.config(fg=colors[index])
                window.after(500, lambda: cycle_color(index + 1))  
            else:
                window.after(500, color_cycle)  

        cycle_color()

    def size_animation(size=20):
        if size <= 35:
            title_label.config(font=("Times New Roman", size, "bold"))
            window.after(50, size_animation, size + 1)  
    
    window.after(100, animate_title)  
    window.after(100 + len(title_text) * 30)  
    window.after(100 + len(title_text) * 30, color_cycle)  
    window.after(100 + len(title_text) * 30 + 1000, size_animation)

def exit_button():
    window.destroy()

def create_button(text, command):
    button = tk.Button(window, text=text, command=command, font=("Courier New", 20, "bold"), bg="#2980B9", fg="white", activebackground="#3498DB", bd=0, padx=20, pady=10, relief="flat")
    button.pack(pady=15)
    button.bind("<Enter>", lambda e: button.config(bg="#3498DB", relief="raised"))
    button.bind("<Leave>", lambda e: button.config(bg="#2980B9", relief="flat"))
    return button

window = tk.Tk()
window.title("LIBRARY MANAGEMENT SYSTEM")
window.geometry("1920x1080")
window.resizable(False, False)

bg_image = Image.open(r"images/main_menu.jpg")
bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
enhancer = ImageEnhance.Brightness(bg_image)
bg_image = enhancer.enhance(0.5)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = tk.Label(window, text="", font=("Times New Roman", 18, "bold"), bg="#2C3E50", fg="white", padx=20, pady=20)
title_label.pack(pady=30)
animation()

frame = tk.Frame(window, bg="#2C3E50", padx=40, pady=30, relief="flat")
frame.pack(pady=30)

Login_button = create_button("LOGIN", lambda: launch_program("login.py", window, close_window = True))
Register_button = create_button("REGISTER", lambda: launch_program("register.py", window, close_window = False))
Exit_button = create_button("EXIT", exit_button)

window.mainloop()

