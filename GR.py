import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import matplotlib.pyplot as mp
mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='12345',
    database='Library2024XIIB2'
)
con = mydb.cursor()
ac = []
def GR_Fine():
    try:
        con.execute("select IssueID, Amount_₹ from Fine")
        rows = con.fetchall()
        issue_ids = [row[0] for row in rows]
        amounts = [row[1] for row in rows]
        mp.bar(issue_ids, amounts)
        mp.title("FINES ANALYSIS")
        mp.xlabel("Issue ID")
        mp.ylabel("Fine Amount(₹)")
        mp.savefig("images/FineAnalysis.jpg")
        mp.show()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def GR_Issue():
    try:
        con.execute("select MemberID, count(BookID) from Issue group by MemberID")
        rows = con.fetchall()
        member_ids = [row[0] for row in rows]
        num_books = [row[1] for row in rows]
        mp.bar(member_ids, num_books)
        mp.title("ISSUES ANALYSIS")
        mp.xlabel("Member ID")
        mp.ylabel("Number of Books Issued")
        mp.savefig("images/IssueAnalysis.jpg")
        mp.show()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def show_gr_issue():
    GR_Issue()

def show_gr_fine():
    GR_Fine()

def open_exit():
    window.destroy()

def load_background_image(window, image_path="images/GR.jpg"):
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        window.bg_photo = bg_photo

        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading image: {e}")
        messagebox.showerror("Image Error", "Failed to load background image. Please check the file path.")

def animate_title(window, title_label):
    title_text = "GRAPHICAL REPORTS"
    def animate(i=0):
        if i <= len(title_text):
            title_label.config(text=title_text[:i])
            ai = window.after(30, animate, i + 1)
            ac.append(ai)
    animate()

def animate_subtitle(window, subtitle_label):
    subtitle_text = "MAIN MENU"
    def animate(j=0):
        if j <= len(subtitle_text):
            subtitle_label.config(text=subtitle_text[:j])
            ai = window.after(30, animate, j + 1)
            ac.append(ai)
    animate()

def color_cycle(window, title_label, subtitle_label):
    colors = ["#2980B9", "#3498DB", "#2980B9"]
    def cycle_color(index=0):
        if index < len(colors):
            title_label.config(fg=colors[index])
            subtitle_label.config(fg=colors[index])
            ai = window.after(500, lambda: cycle_color(index + 1))
            ac.append(ai) 
        else:
            ai = window.after(500, lambda: color_cycle(window, title_label, subtitle_label))
            ac.append(ai)
    cycle_color()

def size_animation(window, title_label):
    def animate(size=20):
        if size <= 35:
            title_label.config(font=("Times New Roman", size, "bold"))
            ai = window.after(50, lambda: animate(size + 1))
            ac.append(ai) 
    animate()

def cancel_after_callbacks():
    for ai in ac:
        window.aca(ai)
    ac.clear()

def on_window_close():
    cancel_after_callbacks()
    window.destroy()

def open_graphs():
    global window
    window = tk.Tk()
    window.title("Graphical Reports")
    window.geometry("1920x1080")
    window.resizable(False, False)

    load_background_image(window)

    title_label = tk.Label(window, text="", font=("Times New Roman", 22, "bold"), bg="#2C3E50", fg="white")
    title_label.pack(pady=40)
    
    subtitle_label = tk.Label(window, text="", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white")
    subtitle_label.pack(pady=20)

    frame = tk.Frame(window, bg="#2C3E50", padx=40, pady=30, relief="flat")
    frame.pack(pady=30)

    def create_button(text, command):
        button = tk.Button(window, text=text, command=command, font=("Courier New", 18, "bold"), bg="#0096FF", fg="white", activebackground="#0096FF", bd=0, padx=20, pady=10, relief="flat")
        button.pack(pady=15)
        button.bind("<Enter>", lambda e: button.config(bg="#87CEEB", relief="raised"))
        button.bind("<Leave>", lambda e: button.config(bg="#0096FF", relief="flat"))
        return button

    def create_button1(text, command):
        button = tk.Button(window, text=text, command=command, font=("Courier New", 18, "bold"), bg="#C0392B", fg="white", activebackground="#C0392B", bd=0, padx=20, pady=10, relief="flat")
        button.pack(pady=15)
        button.bind("<Enter>", lambda e: button.config(bg="#EE4B2B", relief="raised"))
        button.bind("<Leave>", lambda e: button.config(bg="#C0392B", relief="flat"))
        return button

    buttons = [
        create_button("ISSUES ANALYSIS", show_gr_issue),
        create_button("FINES ANALYSIS", show_gr_fine),
        create_button1("EXIT", open_exit)
    ]

    window.after(100, lambda: animate_title(window, title_label))
    window.after(100 + len("GRAPHICAL REPORTS") * 30, lambda: animate_subtitle(window, subtitle_label))
    window.after(100 + len("GRAPHICAL REPORTS") * 30 + len("MAIN MENU") * 30, lambda: color_cycle(window, title_label, subtitle_label))
    window.after(100 + len("GRAPHICAL REPORTS") * 30 + len("MAIN MENU") * 30 + 1000, lambda: size_animation(window, title_label))

    window.protocol("DELETE WINDOW", on_window_close)

    window.mainloop()

if __name__ == "__main__":
    open_graphs()
