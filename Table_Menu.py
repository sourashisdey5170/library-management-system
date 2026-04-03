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

def fade_in(window, steps=22, delay=35):
    for i in range(steps):
        window.attributes("-alpha", i / steps)
        window.update()
        window.after(delay)

def animation():
    title_text = "LIBRARY MANAGEMENT SYSTEM"
    subtitle_text = "MAIN MENU"
    
    def animate_title(i=0):
        if i <= len(title_text):
            title_label.config(text=title_text[:i])
            window.after(20, animate_title, i + 1)  

    def animate_subtitle(j=0):
        if j <= len(subtitle_text):
            subtitle_label.config(text=subtitle_text[:j])
            window.after(20, animate_subtitle, j + 1)  

    def color_cycle():
        colors = ["#2980B9", "#3498DB", "#2980B9"]
        def cycle_color(index=0):
            if index < len(colors):
                title_label.config(fg=colors[index])
                subtitle_label.config(fg=colors[index])
                window.after(300, lambda: cycle_color(index + 1))  
            else:
                window.after(300, color_cycle)  

        cycle_color()

    def size_animation(size=20):
        if size <= 35:
            title_label.config(font=("Times New Roman", size, "bold"))
            window.after(30, size_animation, size + 1)  

    window.after(100, animate_title)  
    window.after(100 + len(title_text) * 30, animate_subtitle)  
    window.after(100 + len(title_text) * 30 + len(subtitle_text) * 30, color_cycle)  
    window.after(100 + len(title_text) * 30 + len(subtitle_text) * 30 + 1000, size_animation)  

def show_books():
    launch_program("Book.py", window, close_window=False)
    
def show_members():
    launch_program("Member.py", window, close_window=False)

def show_issues():
    launch_program("Issue.py", window, close_window=False)

def show_fines():
    launch_program("Fine.py", window, close_window=False)

def show_graphs():
    launch_program("GR.py", window, close_window=False)

def open_books():
    show_books()
    window.deiconify()
    
def open_members():
    show_members()
    window.deiconify()
    
def open_issues():
    show_issues()
    window.deiconify()
    
def open_fines():
    show_fines()
    window.deiconify()

def open_graphs():
    show_graphs()
    window.deiconify()

def exit_button():
    window.destroy()

def open_table_menu():
    global window, title_label, subtitle_label
    window = tk.Tk()
    window.title("LIBRARY MANAGEMENT SYSTEM")
    window.geometry("1920x1080")
    window.resizable(False, False)

    bg_image = Image.open("images/table_menu.jpg")
    bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Brightness(bg_image)
    bg_image = enhancer.enhance(0.5)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(window, text="", font=("Times New Roman", 18, "bold"), bg="#2C3E50", fg="white", padx=20, pady=20)
    title_label.pack(pady=15)
    subtitle_label = tk.Label(window, text="", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white", padx=10, pady=10)
    subtitle_label.pack(pady=10)

    def create_button(text, command):
        button = tk.Button(window, text=text, command=command, font=("Courier New", 20, "bold"), bg="#2980B9", fg="white", activebackground="#3498DB", bd=0, padx=20, pady=10, relief="flat")
        button.pack(pady=10)
        button.bind("<Enter>", lambda e: button.config(bg="#87CEEB", relief="raised"))
        button.bind("<Leave>", lambda e: button.config(bg="#0096FF", relief="flat"))
        return button

    def create_button1(text, command):
        button = tk.Button(window, text=text, command=command, font=("Courier New", 20, "bold"), bg="#C0392B", fg="white", activebackground="#C0392B", bd=0, padx=20, pady=10, relief="flat")
        button.pack(pady=10)
        button.bind("<Enter>", lambda e: button.config(bg="#EE4B2B", relief="raised"))
        button.bind("<Leave>", lambda e: button.config(bg="#C0392B", relief="flat"))
        return button

    buttons = [
        create_button("MANAGE BOOKS", open_books),
        create_button("MANAGE MEMBERS", open_members),
        create_button("MANAGE ISSUES", open_issues),
        create_button("MANAGE FINES", open_fines),
        create_button("GRAPHICAL REPORTS", open_graphs),
        create_button1("EXIT", exit_button)
        ]

    window.after(100, animation)

    window.mainloop()

if __name__ == "__main__":
    open_table_menu()
