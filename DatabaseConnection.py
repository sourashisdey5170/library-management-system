import mysql.connector
mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='12345'
)
con = mydb.cursor()
if mydb.is_connected():
    con.execute("create database if not exists Library2024XIIB2")
    con.execute("use Library2024XIIB2")
    print("Database created and selected successfully!")
else:
    print("Failed to connect to the MySQL server.")
