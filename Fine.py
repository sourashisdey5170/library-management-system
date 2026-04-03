import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import time
import datetime
import mysql.connector

mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='12345',
    database='Library2024XIIB2'
)
con = mydb.cursor()

def Fine_Creation():
    try:
        con.execute("""
            create table if not exists Fine (
                IssueID int not null,
                Day_of_Return date,
                No_of_Days int,
                Amount_₹ int,
                foreign key (IssueID) references Issue(IssueID)
            )
        """)
        mydb.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def add_fine_record(issue_id, day_of_return):
    try:
        day_of_return_obj = datetime.datetime.strptime(day_of_return, '%Y-%m-%d').date()
        con.execute("select Return_Date from Issue where IssueID = %s", (issue_id,))
        result = con.fetchone()
        
        if result is None:
            messagebox.showerror("Error", f"IssueID {issue_id} does not exist.")
            return
        
        return_date = result[0]
        if return_date:
            no_of_days = (day_of_return_obj - return_date).days
        else:
            messagebox.showerror("Error", "Return Date is missing.")
            return
        
        amount = max(no_of_days, 0) * 10
        query = "insert into Fine (IssueID, Day_of_Return, No_of_Days, Amount_₹) values (%s, %s, %s, %s)"
        con.execute(query, (issue_id, day_of_return, no_of_days, amount,))
        mydb.commit()
        messagebox.showinfo("Success", "Fine record inserted successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Ensure correct data types for your inputs.")

def update_fine_record(issue_id, field, new_value):
    try:
        if field == 'Day_of_Return':
            query = "update Fine set Day_of_Return = %s where IssueID = %s"
        elif field == 'No_of_Days':
            query = "update Fine set No_of_Days = %s where IssueID = %s"
        elif field == 'Amount_₹':
            query = "update Fine set Amount_₹ = %s where IssueID = %s"
        else:
            messagebox.showerror("Error", "Invalid field selected.")
            return
        
        con.execute(query, (new_value, issue_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Fine record updated successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Ensure correct data types for your inputs.")

def delete_fine_record(issue_id):
    try:
        query = "delete from Fine where IssueID = %s"
        con.execute(query, (issue_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Fine record deleted successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! IssueID should be an integer.")

def show_add_fine_record():
    add_window = tk.Toplevel(window)
    add_window.title("ADD FINE RECORD")
    add_window.geometry("900x700")
    add_window.resizable(False, False)
    load_background_image(add_window)

    def add_record():
        issue_id = issue_id_entry.get()
        day_of_return = day_of_return_entry.get()
        if issue_id and day_of_return:
            add_fine_record(issue_id, day_of_return)
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    tk.Label(add_window, text="ADD FINE RECORD", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(add_window, text="ISSUE ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_id_entry = tk.Entry(add_window, font=("Courier New", 16))
    issue_id_entry.pack(pady=5)
    tk.Label(add_window, text="DAY OF RETURN (YYYY-MM-DD)", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    day_of_return_entry = tk.Entry(add_window, font=("Courier New", 16))
    day_of_return_entry.pack(pady=5)
    tk.Button(add_window, text="ADD FINE", command=add_record, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_update_fine_record():
    update_window = tk.Toplevel(window)
    update_window.title("UPDATE FINE RECORD")
    update_window.geometry("900x700")
    update_window.resizable(False, False)
    load_background_image(update_window)

    def update_record():
        issue_id = issue_id_entry.get()
        field = field_var.get()
        new_value = new_value_entry.get()
        if issue_id and field and new_value:
            update_fine_record(issue_id, field, new_value)
            messagebox.showinfo("Success", "Fine record updated successfully!")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    def update_label(*args):
        selected_field = field_var.get()
        if selected_field:
            a = selected_field 
            if(a == "Day_of_Return"):
                labelname = "Day Of Return"
            else:
                labelname = a
            new_value_label.config(text=f"Enter New {labelname.upper()}")
        else:
            new_value_label.config(text="NEW VALUE")

    tk.Label(update_window, text="UPDATE FINE", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(update_window, text="ISSUE ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_id_entry = tk.Entry(update_window, font=("Courier New", 16))
    issue_id_entry.pack(pady=5)

    tk.Label(update_window, text="SELECT FIELD TO UPDATE", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=10)
    field_var = tk.StringVar()
    field_var.trace_add("write", update_label)
    fields = [("DAY OF RETURN", "Day_of_Return")]

    for text, mode in fields:
        tk.Radiobutton(update_window, text=text, variable=field_var, value=mode, font=("Courier New", 16), bg="#2C3E50", fg="white", indicatoron=0, selectcolor="#2980B9").pack(anchor="center", padx=10, pady=5)

    new_value_label = tk.Label(update_window, text="NEW VALUE", font=("Courier New", 16), bg="#2C3E50", fg="white")
    new_value_label.pack(pady=5)
    new_value_entry = tk.Entry(update_window, font=("Courier New", 16))
    new_value_entry.pack(pady=5)

    tk.Button(update_window, text="UPDATE FINE", command=update_record, font=("Courier New", 16), bg="#2980B9", fg="white").pack(pady=20)

def show_delete_fine_record():
    delete_window = tk.Toplevel(window)
    delete_window.title("DELETE FINE RECORD")
    delete_window.geometry("500x300")
    delete_window.resizable(False, False)
    load_background_image(delete_window)

    def delete_record():
        issue_id = issue_id_entry.get()
        if issue_id:
            delete_fine_record(issue_id)
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Issue ID must be provided.")

    tk.Label(delete_window, text="DELETE FINE RECORD", font=("Times New Roman", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)
    tk.Label(delete_window, text="ISSUE ID", font=("Courier New", 16), bg="#2C3E50", fg="white").pack(pady=5)
    issue_id_entry = tk.Entry(delete_window, font=("Courier New", 16))
    issue_id_entry.pack(pady=5)
    tk.Button(delete_window, text="DELETE FINE", command=delete_record, font=("Courier New", 16), bg="#C0392B", fg="white").pack(pady=20)

def show_view_fine_records():
    view_window = tk.Toplevel(window)
    view_window.title("View Fine Records")
    view_window.geometry("1000x900")
    view_window.resizable(False, False)
    load_background_image(view_window)

    table_frame = tk.Frame(view_window, bg="#2C3E50")
    table_frame.place(relx=0.5, rely=0.5, anchor="center")

    headers = ["ISSUE ID", "DAY OF RETURN", "LATE BY(DAYS)", "AMOUNT(₹)"]
    for header_index, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Courier New", 16, "bold"), bg="#2C3E50", fg="white", borderwidth=2, relief="solid").grid(row=0, column=header_index, padx=5, pady=5, sticky="nsew")

    con.execute("select IssueID, concat(day(Day_of_Return), case when day(Day_of_Return) in (1,21,31) then 'st' when day(Day_of_Return) in (2,22) then 'nd' when day(Day_of_Return) in (3,23) then 'rd' else 'th' end, ' ', date_format(Day_of_Return, '%M'), ' ', date_format(Day_of_Return, '%Y')) as FormattedDate, No_of_Days, Amount_₹ from Fine order by IssueID asc")
    rows = con.fetchall()
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            tk.Label(table_frame, text=value, font=("Courier New", 16), bg="#2C3E50", fg="white", borderwidth=2, relief="solid").grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="nsew")

def load_background_image(window):
    try:
        bg_image_bk = Image.open("images/fine.jpg")
        bg_image_bk = bg_image_bk.resize((1920, 1080), Image.Resampling.LANCZOS)
        enhancer_bk = ImageEnhance.Brightness(bg_image_bk)
        bg_image_bk = enhancer_bk.enhance(0.5)
        bg_photo_bk = ImageTk.PhotoImage(bg_image_bk)
        window.bg_photo_bk = bg_photo_bk
        bg_label_bk = tk.Label(window, image=bg_photo_bk)
        bg_label_bk.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading background image: {e}")

def fade_in(window):
    alpha = 0.0
    window.attributes('-alpha', alpha)
    while alpha < 1.0:
        alpha += 0.05
        window.attributes('-alpha', alpha)
        window.update()
        time.sleep(0.05)

def animation():
    title_text = "FINE MANAGEMENT"
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

def open_add_fine():
    show_add_fine_record()
    window.deiconify()

def open_view_fines():
    show_view_fine_records()
    window.deiconify()

def open_update_fine():
    show_update_fine_record()
    window.deiconify()

def open_delete_fine():
    show_delete_fine_record()
    window.deiconify()

def open_exit():
    window.destroy()

def open_fines():
    global window, title_label, subtitle_label
    window = tk.Tk()
    window.title("Configure Fines")
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
        create_button("ADD FINE RECORD", open_add_fine),
        create_button("VIEW FINE RECORDS", open_view_fines),
        create_button("UPDATE FINE RECORD", open_update_fine),
        create_button1("DELETE FINE RECORD", open_delete_fine),
        create_button1("EXIT", open_exit)
    ]  

    window.after(100, animation)  

    window.mainloop()

if __name__ == "__main__":
    Fine_Creation()
    open_fines()
