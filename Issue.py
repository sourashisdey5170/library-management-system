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

def Issue_Creation():
    try:
        con.execute("""
            create table if not exists Issue (
                IssueID int not null primary key,
                BookID int not null,
                MemberID int not null,
                Issue_Date date,
                Return_Date date,
                foreign key (BookID) references Book(BookID),
                foreign key (MemberID) references Member(MemberID) 
            )
        """)
        mydb.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def add_issue_to_db(issue_id, book_id, member_id, issue_date, return_date):
    try:
        con.execute("select count(*) from Book where BookID = %s", (book_id,))
        if con.fetchone()[0] == 0:
            raise ValueError(f"BookID {book_id} does not exist.")

        con.execute("select count(*) from Member where MemberID = %s", (member_id,))
        if con.fetchone()[0] == 0:
            raise ValueError(f"MemberID {member_id} does not exist.")

        query = "insert into Issue (IssueID, BookID, MemberID, Issue_Date, Return_Date) values (%s, %s, %s, %s, %s)"
        con.execute(query, (issue_id, book_id, member_id, issue_date, return_date))
        mydb.commit()
        messagebox.showinfo("Success", "Issue record added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except ValueError as ve:
        messagebox.showerror("Value Error", str(ve))

def update_issue_in_db(issue_id, field, new_value):
    try:
        if field == 'BookID':
            query = "update Issue set BookID = %s where IssueID = %s"
        elif field == 'MemberID':
            query = "update Issue set MemberID = %s where IssueID = %s"
        elif field == 'Issue_Date':
            query = "update Issue set Issue_Date = %s where IssueID = %s"
        elif field == 'Return_Date':
            query = "update Issue set Return_Date = %s where IssueID = %s"
        else:
            raise ValueError("Invalid field selected.")

        con.execute(query, (new_value, issue_id))
        mydb.commit()
        messagebox.showinfo("Success", "Issue record updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except ValueError as ve:
        messagebox.showerror("Value Error", str(ve))

def delete_issue_from_db(issue_id):
    try:
        query = "delete from Issue where IssueID = %s"
        con.execute(query, (issue_id))
        mydb.commit()
        messagebox.showinfo("Success", "Issue record deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def show_add_issue():
    add_window = tk.Toplevel(window)
    add_window.title("ADD ISSUE")
    add_window.geometry("900x700")
    add_window.resizable(False, False)

    load_background_image(add_window)

    def add_issue():
        issue_id = issue_id_entry.get()
        book_id = book_id_entry.get()
        member_id = member_id_entry.get()
        issue_date = issue_date_entry.get()
        return_date = return_date_entry.get()
        if issue_id and book_id and member_id and issue_date and return_date:
            add_issue_to_db(issue_id, book_id, member_id, issue_date, return_date)
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    tk.Label(add_window, text="ADD ISSUE", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(add_window, text="ISSUE ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_id_entry = tk.Entry(add_window, font=("Courier New", 16))
    issue_id_entry.pack(pady=5)
    tk.Label(add_window, text="BOOK ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    book_id_entry = tk.Entry(add_window, font=("Courier New", 16))
    book_id_entry.pack(pady=5)
    tk.Label(add_window, text="MEMBER ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    member_id_entry = tk.Entry(add_window, font=("Courier New", 16))
    member_id_entry.pack(pady=5)
    tk.Label(add_window, text="ISSUE DATE", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_date_entry = tk.Entry(add_window, font=("Courier New", 16))
    issue_date_entry.pack(pady=5)
    tk.Label(add_window, text="RETURN DATE", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    return_date_entry = tk.Entry(add_window, font=("Courier New", 16))
    return_date_entry.pack(pady=5)
    tk.Button(add_window, text="ADD ISSUE", command=add_issue, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_update_issue():
    update_window = tk.Toplevel(window)
    update_window.title("UPDATE ISSUE")
    update_window.geometry("900x700")  
    update_window.resizable(False, False)

    load_background_image(update_window)

    update_frame = tk.Frame(update_window, bg="#2C3E50")
    update_frame.place(relx=0.5, rely=0.5, anchor="center")

    def update_issue():
        issue_id = issue_id_entry.get()
        field = field_var.get()
        new_value = new_value_entry.get()
        if issue_id and field and new_value:
            update_issue_in_db(issue_id, field, new_value)
            messagebox.showinfo("Success", f"Issue record '{issue_id}' updated successfully!")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    def update_label(*args):
        selected_field = field_var.get()
        if selected_field:
            a = selected_field
            if (a == "Issue_Date"):
                labelname = "Issue Date"
            elif (a == "Return_Date"):
                labelname = "Return Date"
            else:
                labelname = a
            new_value_label.config(text=f"ENTER NEW {labelname.upper()}")
        else:
            new_value_label.config(text="NEW VALUE")

    tk.Label(update_frame, text="UPDATE ISSUE", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)

    tk.Label(update_frame, text="ISSUE ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_id_entry = tk.Entry(update_frame, font=("Courier New", 16))
    issue_id_entry.pack(pady=5)

    tk.Label(update_frame, text="SELECT FIELD TO UPDATE", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=10)

    field_var = tk.StringVar()
    field_var.trace_add("write", update_label)  
    fields = [("BOOK ID", "BookID"), ("MEMBER ID", "MemberID"), ("ISSUE DATE", "Issue_Date"), ("RETURN DATE", "Return_Date")]

    for text, mode in fields:
        tk.Radiobutton(update_frame, text=text, variable=field_var, value=mode, font=("Courier New", 16), bg="#2C3E50", fg="white", indicatoron=0, selectcolor="#2980B9").pack(anchor="center", padx=10, pady=5)

    new_value_label = tk.Label(update_frame, text="NEW VALUE", font=("Courier New", 16), bg="#2C3E50", fg="white")
    new_value_label.pack(pady=5)
    new_value_entry = tk.Entry(update_frame, font=("Courier New", 16))
    new_value_entry.pack(pady=5)

    tk.Button(update_frame, text="UPDATE ISSUE", command=update_issue, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_delete_issue():
    delete_window = tk.Toplevel(window)
    delete_window.title("DELETE ISSUE")
    delete_window.geometry("500x300")
    delete_window.resizable(False, False)

    load_background_image(delete_window)

    def delete_issue():
        issue_id = issue_id_entry.get()
        if issue_id:
            delete_issue_from_db(issue_id)
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Issue ID must be provided.")

    tk.Label(delete_window, text="DELETE ISSUE", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(delete_window, text="ISSUE ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_id_entry = tk.Entry(delete_window, font=("Courier New", 16))
    issue_id_entry.pack(pady=5)
    tk.Button(delete_window, text="DELETE ISSUE", command=delete_issue, font=("Courier New", 16), bg="#C0392B", fg="white").pack(pady=20)

def show_view_issues():
    view_window = tk.Toplevel(window)
    view_window.title("View Issues")
    view_window.geometry("1000x900")
    view_window.resizable(False, False)

    load_background_image(view_window)

    table_frame = tk.Frame(view_window, bg="#2C3E50")
    table_frame.place(relx=0.5, rely=0.5, anchor="center")

    headers = ["ISSUE ID", "BOOK ID", "MEMBER ID", "ISSUE DATE", "RETURN DATE"]
    for header_index, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Courier New", 16, "bold"), bg="#2C3E50", fg="white", padx=10).grid(row=0, column=header_index, padx=10, pady=5, sticky="w")

    try:
        con.execute("select IssueID, BookID, MemberID, concat(day(Issue_Date), case when day(Issue_Date) in (1,21,31) then 'st' when day(Issue_Date) in (2,22) then 'nd' when day(Issue_Date) in (3,23) then 'rd' else 'th' end, ' ', date_format(Issue_Date, '%M'), ' ', date_format(Issue_Date, '%Y')) as FormattedDate, concat(day(Return_Date), case when day(Return_Date) in (1,21,31) then 'st' when day(Return_Date) in (2,22) then 'nd' when day(Return_Date) in (3,23) then 'rd' else 'th' end, ' ', date_format(Return_Date, '%M'), ' ', date_format(Return_Date, '%Y')) as FormattedDate from Issue order by IssueID asc")
        issues = con.fetchall()

        for row_index, issue in enumerate(issues, start=1):
            for col_index, data in enumerate(issue):
                tk.Label(table_frame, text=data, font=("Courier New", 16), bg="#2C3E50", fg="white", padx=10).grid(row=row_index, column=col_index, padx=10, pady=5, sticky="w")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def load_background_image(window, image_path="images/issue.jpg"):
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

def fade_in(window):
    alpha = 0.0
    window.attributes('-alpha', alpha)
    while alpha < 1.0:
        alpha += 0.05
        window.attributes('-alpha', alpha)
        window.update()
        time.sleep(0.05)

def animation():
    title_text = "ISSUE MANAGEMENT"
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

def open_add_issue():
    show_add_issue()
    window.deiconify()

def open_view_issues():
    show_view_issues()
    window.deiconify()

def open_update_issue():
    show_update_issue()
    window.deiconify()

def open_delete_issue():
    show_delete_issue()
    window.deiconify()

def open_exit():
    window.destroy()

def open_issues():
    global window, title_label, subtitle_label
    window = tk.Tk()
    window.title("Configure Issues")
    window.geometry("1920x1080")
    window.resizable(False, False)

    load_background_image(window)

    title_label = tk.Label(window, text="", font=("Times New Roman", 22, "bold"), bg="#2C3E50", fg="white")
    title_label.pack(pady=20)  

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
        create_button("ADD ISSUE", open_add_issue),
        create_button("VIEW ISSUES", open_view_issues),
        create_button("UPDATE ISSUE", open_update_issue),
        create_button1("DELETE ISSUE", open_delete_issue),
        create_button1("EXIT", open_exit)
    ]  
    
    window.after(100, animation) 

    window.mainloop()

if __name__ == "__main__":
    Issue_Creation()
    open_issues()
