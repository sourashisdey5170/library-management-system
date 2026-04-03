import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import time
import mysql.connector

mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='12345',
    database='Library2024XIIB2'
)
con = mydb.cursor()

def Member_Creation():
    try:
        con.execute("""
            create table if not exists Member (
                MemberID int not null primary key,
                Member_Name varchar(50),
                Gender varchar(50),
                City varchar(50)
            )
        """)
        mydb.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def add_member_to_db(member_id, member_name, gender, city):
    try:
        query = "insert into Member (MemberID, Member_Name, Gender, City) values (%s, %s, %s, %s)"
        con.execute(query, (member_id, member_name, gender, city))
        mydb.commit()
        messagebox.showinfo("Success", "Member inserted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except ValueError as ve:
        messagebox.showerror("Value Error", str(ve))

def update_member_in_db(member_id, field, new_value):
    try:
        if field == 'Member_Name':
            query = "update Member set Member_Name = %s where MemberID = %s"
        elif field == 'Gender':
            query = "update Member set Gender = %s where MemberID = %s"
        elif field == 'City':
            query = "update Member set City = %s where MemberID = %s"
        else:
            raise ValueError("Invalid field selected.")

        con.execute(query, (new_value, member_id))
        mydb.commit()
        messagebox.showinfo("Success", "Member details updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except ValueError as ve:
        messagebox.showerror("Value Error", str(ve))

def delete_member_from_db(member_id):
    try:
        query = "delete from Member where MemberID = %s"
        con.execute(query, (member_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Member deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def show_add_member():
    add_window = tk.Toplevel(window)
    add_window.title("ADD MEMBER")
    add_window.geometry("900x700")
    add_window.resizable(False, False)

    load_background_image(add_window)

    def add_member():
        member_id = member_id_entry.get()
        member_name = member_name_entry.get()
        gender = gender_entry.get()
        city = city_entry.get()
        if member_id and member_name and gender and city:
            add_member_to_db(member_id, member_name, gender, city)
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    tk.Label(add_window, text="ADD MEMBER", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(add_window, text="MEMBER ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    member_id_entry = tk.Entry(add_window, font=("Courier New", 16))
    member_id_entry.pack(pady=5)
    tk.Label(add_window, text="MEMBER NAME", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    member_name_entry = tk.Entry(add_window, font=("Courier New", 16))
    member_name_entry.pack(pady=5)
    tk.Label(add_window, text="GENDER", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    gender_entry = tk.Entry(add_window, font=("Courier New", 16))
    gender_entry.pack(pady=5)
    tk.Label(add_window, text="CITY", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    city_entry = tk.Entry(add_window, font=("Courier New", 16))
    city_entry.pack(pady=5)
    tk.Button(add_window, text="ADD MEMBER", command=add_member, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_update_member():
    update_window = tk.Toplevel(window)
    update_window.title("UPDATE MEMBER")
    update_window.geometry("700x600")  
    update_window.resizable(False, False)

    load_background_image(update_window)

    update_frame = tk.Frame(update_window, bg="#2C3E50")
    update_frame.place(relx=0.5, rely=0.5, anchor="center")

    def update_member():
        member_id = member_id_entry.get()
        field = field_var.get()
        new_value = new_value_entry.get()
        if member_id and field and new_value:
            update_member_in_db(member_id, field, new_value)
            messagebox.showinfo("Success", f"Member '{member_id}' updated successfully!")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    def update_label(*args):
        selected_field = field_var.get()
        if selected_field:
            a = selected_field 
            if(a == "Member_Name"):
                labelname = "Member Name"
            else:
                labelname = a
            new_value_label.config(text=f"Enter New {labelname.upper()}")
        else:
            new_value_label.config(text="NEW VALUE")

    tk.Label(update_frame, text="UPDATE MEMBER", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)

    tk.Label(update_frame, text="MEMBER ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    member_id_entry = tk.Entry(update_frame, font=("Courier New", 16))
    member_id_entry.pack(pady=5)

    tk.Label(update_frame, text="SELECT FIELD TO UPDATE", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=10)

    field_var = tk.StringVar()
    field_var.trace_add("write", update_label)  
    fields = [("NAME", "Member_Name"), ("GENDER", "Gender"), ("CITY", "City")]

    for text, mode in fields:
        tk.Radiobutton(update_frame, text=text, variable=field_var, value=mode, font=("Courier New", 16), bg="#2C3E50", fg="white", indicatoron=0, selectcolor="#2980B9").pack(anchor="center", padx=10, pady=5)

    new_value_label = tk.Label(update_frame, text="NEW VALUE", font=("Courier New", 16), bg="#2C3E50", fg="white")
    new_value_label.pack(pady=5)
    new_value_entry = tk.Entry(update_frame, font=("Courier New", 16))
    new_value_entry.pack(pady=5)

    tk.Button(update_frame, text="UPDATE MEMBER", command=update_member, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_delete_member():
    delete_window = tk.Toplevel(window)
    delete_window.title("DELETE MEMBER")
    delete_window.geometry("500x300")
    delete_window.resizable(False, False)

    load_background_image(delete_window)

    def delete_member():
        member_id = member_id_entry.get()
        if member_id:
            delete_member_from_db(member_id)
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Member ID must be provided.")

    tk.Label(delete_window, text="DELETE MEMBER", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(delete_window, text="MEMBER ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    member_id_entry = tk.Entry(delete_window, font=("Courier New", 16))
    member_id_entry.pack(pady=5)
    tk.Button(delete_window, text="DELETE MEMBER", command=delete_member, font=("Courier New", 16), bg="#C0392B", fg="white").pack(pady=20)

def show_view_members():
    view_window = tk.Toplevel(window)
    view_window.title("View Members")
    view_window.geometry("1000x900")
    view_window.resizable(False, False)

    load_background_image(view_window)

    table_frame = tk.Frame(view_window, bg="#2C3E50")
    table_frame.place(relx=0.5, rely=0.5, anchor="center")

    headers = ["MEMBER ID", "MEMBER NAME", "GENDER", "CITY"]
    for header_index, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Courier New", 16, "bold"), bg="#2C3E50", fg="white", padx=10).grid(row=0, column=header_index, padx=10, pady=5, sticky="w")

    try:
        query = "select MemberID, Member_Name, Gender, City from Member"
        con.execute(query)
        members = con.fetchall()

        for row_index, member in enumerate(members, start=1):
            for col_index, data in enumerate(member):
                tk.Label(table_frame, text=data, font=("Courier New", 16), bg="#2C3E50", fg="white", padx=10).grid(row=row_index, column=col_index, padx=10, pady=5, sticky="w")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def fade_in(window, steps=22, delay=35):
    for i in range(steps):
        window.attributes("-alpha", i / steps)
        window.update()
        time.sleep(delay / 1000)

def load_background_image(window, image_path="images/member.jpg"):
    try:
        bg_image_bk = Image.open(image_path)
        bg_image_bk = bg_image_bk.resize((1920, 1080), Image.Resampling.LANCZOS)
        enhancer_bk = ImageEnhance.Brightness(bg_image_bk)
        bg_image_bk = enhancer_bk.enhance(0.5)
        bg_photo_bk = ImageTk.PhotoImage(bg_image_bk)
        window.bg_photo_bk = bg_photo_bk

        bg_label_bk = tk.Label(window, image=bg_photo_bk)
        bg_label_bk.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading image: {e}")
        messagebox.showerror("Image Error", "Failed to load background image. Please check the file path.")

def animation():
    title_text = "MEMBER MANAGEMENT"
    subtitle_text = "MAIN MENU"
    
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

def open_add_member():
    show_add_member()
    window.deiconify()

def open_view_member():
    show_view_members()
    window.deiconify()

def open_update_member():
    show_update_member()
    window.deiconify()

def open_delete_member():
    show_delete_member()
    window.deiconify()

def open_exit():
    window.destroy()

def open_members():
    global window, title_label, subtitle_label
    window = tk.Tk()
    window.title("Configure Members")
    window.geometry("1920x1080")
    window.resizable(False, False)

    load_background_image(window)

    title_label = tk.Label(window, text="", font=("Times New Roman", 22, "bold"), bg="#2C3E50", fg="white")
    title_label.pack(pady=30)
    
    subtitle_label = tk.Label(window, text="", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white")
    subtitle_label.pack(pady=20)

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
        create_button("ADD MEMBER", open_add_member),
        create_button("VIEW MEMBERS", open_view_member),
        create_button("UPDATE MEMBER", open_update_member),
        create_button1("DELETE MEMBER", open_delete_member),
        create_button1("EXIT", open_exit)
    ]

    
    window.after(100, animation)  

    window.mainloop()

if __name__ == "__main__":
    Member_Creation()
    open_members()
