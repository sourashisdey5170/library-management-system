import mysql.connector
mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='12345',
    database='Library2024XIIB2')
con = mydb.cursor()
def User_Creation():
    con.execute("""
                    create table if not exists User(
                        UserID int not null primary key,
                        Password varchar(50)
                    )
                """)
    mydb.commit()

if __name__ == "__main__":
    User_Creation()


