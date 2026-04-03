import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import time

mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='12345',
    database='Library2024XIIB2'
)
con = mydb.cursor()

def register_user():
    UserID = UserID_entry.get()
    Password = Password_entry.get()
    if UserID and Password:
        if register(UserID, Password):
            messagebox.showinfo("Registration Successful!", "User Successfully registered.")
        else:
            messagebox.showerror("Registration Failed", "UserID already exists. Please try again.")
    else:
        messagebox.showerror("Registration Failed", "UserID and Password cannot be empty.")

def conexit():
    window.destroy()

def register(UserID, Password):
    query = "select * from User where UserID = %s"
    con.execute(query, (UserID,))
    result = con.fetchall()
    if result:
        return False
    else:
        query = "insert into User (UserID, Password) values (%s, %s)"
        con.execute(query, (UserID, Password))
        mydb.commit()
        return True

def fade_in(window, steps=22, delay=35):
    for i in range(steps):
        window.attributes("-alpha", i / steps)
        window.update()
        time.sleep(delay / 1000)

def animation():
    title_text = "LIBRARY MANAGEMENT SYSTEM"
    subtitle_text = "REGISTER NEW USER"
    def animate_title(i=0):
        if i <= len(title_text):
            title_label.config(text=title_text[:i])
            window.after(30, animate_title, i + 1)  

    def animate_subtitle(j=0):
        if j <= len(subtitle_text):
            subtitle_label.config(text=subtitle_text[:j])
            window.after(30, animate_subtitle, j + 1)  

    def color_cycle():
        colors = ["#2980B9", "#3498DB", "#2980B9"]
        def cycle_color(index=0):
            if index < len(colors):
                title_label.config(fg=colors[index])
                subtitle_label.config(fg=colors[index])
                window.after(500, lambda: cycle_color(index + 1))  
            else:
                window.after(500, color_cycle)  

        cycle_color()

    def size_animation(size=20):
        if size <= 35:
            title_label.config(font=("Times New Roman", size, "bold"))
            window.after(50, size_animation, size + 1)  

    window.after(100, animate_title)  
    window.after(100 + len(title_text) * 30, animate_subtitle)  
    window.after(100 + len(title_text) * 30 + len(subtitle_text) * 30, color_cycle)  
    window.after(100 + len(title_text) * 30 + len(subtitle_text) * 30 + 1000, size_animation)

window = tk.Tk()
window.title("LIBRARY MANAGEMENT SYSTEM")
window.geometry("1920x1080")
window.resizable(False, False)

bg_image = Image.open("images/register.jpg")
bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
enhancer = ImageEnhance.Brightness(bg_image)
bg_image = enhancer.enhance(0.5)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = tk.Label(window, text="", font=("Times New Roman", 18, "bold"), bg="#2C3E50", fg="white", padx=20, pady=20)
title_label.pack(pady=30)
subtitle_label = tk.Label(window, text="", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white", padx=10, pady=10)
subtitle_label.pack()
animation()

frame = tk.Frame(window, bg="#2C3E50", padx=40, pady=30, relief="flat")
frame.pack(pady=30)

UserID_label = tk.Label(frame, text="USER ID", font=("Courier New", 20, "bold"), bg="#2C3E50", fg="white", pady=10)
UserID_label.grid(row=0, column=0, padx=20, sticky='e')
UserID_entry = tk.Entry(frame, font=("Courier New", 20), bg="#ECF0F1", bd=0, relief="solid", borderwidth=2)
UserID_entry.grid(row=0, column=1, padx=20, pady=10)

Password_label = tk.Label(frame, text="PASSWORD", font=("Courier New", 20, "bold"), bg="#2C3E50", fg="white", pady=10)
Password_label.grid(row=1, column=0, padx=20, sticky='e')
Password_entry = tk.Entry(frame, show="*", font=("Courier New", 20), bg="#ECF0F1", bd=0, relief="solid", borderwidth=2)
Password_entry.grid(row=1, column=1, padx=20, pady=10)

def create_button(text, command):
    button = tk.Button(window, text=text, command=command, font=("Courier New", 20, "bold"), bg="#2980B9", fg="white", activebackground="#3498DB", bd=0, padx=20, pady=10, relief="flat")
    button.pack(pady=15)
    button.bind("<Enter>", lambda e: button.config(bg="#3498DB", relief="raised"))
    button.bind("<Leave>", lambda e: button.config(bg="#2980B9", relief="flat"))
    return button

Register_button = create_button("REGISTER", register_user)
Exit_button = create_button("BACK TO MAIN MENU", conexit)

window.mainloop()
