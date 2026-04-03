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

def Book_Creation():
    try:
        con.execute("""
            create table if not exists Book (
                BookID int not null primary key,
                Book_Name varchar(50),
                Author varchar(50),
                Edition date
            )
        """)
        mydb.commit()
        print("Table 'Book' created successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def add_book_to_db(book_id, book_name, author, edition):
    try:
        query = "insert into Book (BookID, Book_Name, Author, Edition) values (%s, %s, %s, %s)"
        con.execute(query, (book_id, book_name, author, edition))
        mydb.commit()
        print("Book inserted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def update_book_in_db(book_id, field, new_value):
    try:
        query = f"update Book set {field} = %s where BookID = %s"
        con.execute(query, (new_value, book_id))
        mydb.commit()
        print("Book updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def delete_book_from_db(book_id):
    try:
        query = "delete from Book where BookID = %s"
        con.execute(query, (book_id,))
        mydb.commit()
        print("Book deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def show_update_book():
    update_window = tk.Toplevel(window)
    update_window.title("UPDATE BOOK")
    update_window.geometry("700x600")  
    update_window.resizable(False, False)

    load_background_image(update_window)

    update_frame = tk.Frame(update_window, bg="#2C3E50")
    update_frame.place(relx=0.5, rely=0.5, anchor="center")

    def update_book():
        book_id = book_id_entry.get()
        field = field_var.get()
        new_value = new_value_entry.get()
        if book_id and field and new_value:
            update_book_in_db(book_id, field, new_value)
            messagebox.showinfo("Success", f"Book '{book_id}' updated successfully!")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    def update_label(*args):
        selected_field = field_var.get()
        if selected_field:
            a = selected_field 
            if(a == "Book_Name"):
                labelname = "Book Name"
            else:
                labelname = a
            new_value_label.config(text=f"Enter New {labelname.upper()}")
        else:
            new_value_label.config(text="NEW VALUE")

    tk.Label(update_frame, text="UPDATE BOOK", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)

    tk.Label(update_frame, text="BOOK ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    book_id_entry = tk.Entry(update_frame, font=("Courier New", 16))
    book_id_entry.pack(pady=5)

    tk.Label(update_frame, text="SELECT FIELD TO UPDATE", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=10)

    field_var = tk.StringVar()
    field_var.trace_add("write", update_label)  
    fields = [("BOOK NAME", "Book_Name"), ("AUTHOR", "Author"), ("EDITION", "Edition")]

    for text, mode in fields:
        tk.Radiobutton(update_frame, text=text, variable=field_var, value=mode, font=("Courier New", 16), bg="#2C3E50", fg="white", indicatoron=0, selectcolor="#2980B9").pack(anchor="center", padx=10, pady=5)

    new_value_label = tk.Label(update_frame, text="NEW VALUE", font=("Courier New", 16), bg="#2C3E50", fg="white")
    new_value_label.pack(pady=5)
    new_value_entry = tk.Entry(update_frame, font=("Courier New", 16))
    new_value_entry.pack(pady=5)

    tk.Button(update_frame, text="UPDATE BOOK", command=update_book, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_add_book():
    add_window = tk.Toplevel(window)
    add_window.title("ADD BOOK")
    add_window.geometry("900x700")
    add_window.resizable(False, False)

    load_background_image(add_window)

    def add_book():
        book_id = book_id_entry.get()
        book_name = book_name_entry.get()
        author = author_entry.get()
        edition = edition_entry.get()
        if book_id and book_name and author and edition:
            add_book_to_db(book_id, book_name, author, edition)
            messagebox.showinfo("Success", "Book added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    tk.Label(add_window, text="ADD BOOK", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(add_window, text="BOOK ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    book_id_entry = tk.Entry(add_window, font=("Courier New", 16))
    book_id_entry.pack(pady=5)
    tk.Label(add_window, text="BOOK NAME", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    book_name_entry = tk.Entry(add_window, font=("Courier New", 16))
    book_name_entry.pack(pady=5)
    tk.Label(add_window, text="AUTHOR", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    author_entry = tk.Entry(add_window, font=("Courier New", 16))
    author_entry.pack(pady=5)
    tk.Label(add_window, text="EDITION", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    edition_entry = tk.Entry(add_window, font=("Courier New", 16))
    edition_entry.pack(pady=5)
    tk.Button(add_window, text="ADD BOOK", command=add_book, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)


def show_view_books():
    view_window = tk.Toplevel(window)
    view_window.title("View Books")
    view_window.geometry("1000x900")
    view_window.resizable(False, False)

    load_background_image(view_window)

    table_frame = tk.Frame(view_window, bg="#2C3E50")
    table_frame.place(relx=0.5, rely=0.5, anchor="center")

    headers = ["BOOK ID", "BOOK NAME", "AUTHOR", "EDITION"]
    for header_index, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Courier New", 16, "bold"), bg="#2C3E50", fg="white", padx=10).grid(row=0, column=header_index, padx=10, pady=5, sticky="w")

    try:
        query = "select BookID, Book_Name, Author, YEAR(EDITION) from Book"
        con.execute(query)
        books = con.fetchall()

        for row_index, book in enumerate(books, start=1):
            for col_index, data in enumerate(book):
                tk.Label(table_frame, text=data, font=("Courier New", 16), bg="#2C3E50", fg="white", padx=10).grid(row=row_index, column=col_index, padx=10, pady=5, sticky="w")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def show_delete_book():
    delete_window = tk.Toplevel(window)
    delete_window.title("DELETE BOOK")
    delete_window.geometry("500x300")
    delete_window.resizable(False, False)

    load_background_image(delete_window)

    def delete_book():
        book_id = book_id_entry.get()
        if book_id:
            delete_book_from_db(book_id)
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "BookID must be provided.")

    tk.Label(delete_window, text="DELETE BOOK", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(delete_window, text="BOOK ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    book_id_entry = tk.Entry(delete_window, font=("Courier New", 16))
    book_id_entry.pack(pady=5)
    tk.Button(delete_window, text="DELETE BOOK", command=delete_book, font=("Courier New", 16), bg="#C0392B", fg="white").pack(pady=20)


def fade_in(window):
    alpha = 0.0
    window.attributes('-alpha', alpha)
    while alpha < 1.0:
        alpha += 0.05
        window.attributes('-alpha', alpha)
        window.update()
        time.sleep(0.05)

def load_background_image(window, image_path="images/book.jpg"):
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
    title_text = "BOOK MANAGEMENT"
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

def open_add_book():
    show_add_book()
    window.deiconify()

def open_view_book():
    show_view_books()
    window.deiconify()

def open_update_book():
    show_update_book()
    window.deiconify()

def open_delete_book():
    show_delete_book()
    window.deiconify()

def open_exit():
    window.destroy()

def open_books():
    global window, title_label, subtitle_label
    window = tk.Tk()
    window.title("Configure Books")
    window.geometry("1920x1080")
    window.resizable(False, False)

    load_background_image(window)

    title_label = tk.Label(window, text="", font=("Times New Roman", 22, "bold"), bg="#2C3E50", fg="white")
    title_label.pack(pady=40)
    
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
        create_button("ADD BOOK", open_add_book),
        create_button("VIEW BOOKS", open_view_book),
        create_button("UPDATE BOOK", open_update_book),
        create_button1("DELETE BOOK", open_delete_book),
        create_button1("EXIT", open_exit)
    ]

    
    window.after(100, animation)  

    window.mainloop()

if __name__ == "__main__":
    Book_Creation()
    open_books()
