import sqlite3
from datetime import date

conn = sqlite3.connect('Library_Management.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_information(
        student_id INTEGER PRIMARY KEY NOT NULL
        username TEXT NOT NULL
        email TEXT NOT NULL
        password INTIGIER NOT NULL
        phone_num INTIGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS catalog(
        unique_id INTEGER PRIMARY KEY NOT NULL
        book_name TEXT NOT NULL
        author TEXT NOT NULL
        price TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS issue_book(
        student_id INTEGER PRIMARY KEY NOT NULL
        username TEXT NOT NULL
        issue_date DATE NOT NULL
        return_date DATE NOT NULL
    )
''')

def see_catalog():
    try:
        cursor.execute("SELECT * FROM catalog")
        
        for row in cursor.fetchall():
            print(row)
    except:
        print("Internal error!!!")

def search_book():
    book_name = input("Enter the book name: ")
    
    try:
        book = cursor.execute("SELECT * FROM catalog WHERE book_name=?", [book_name]).fetchone()
        
        if book is not None:
            try:
                cursor.execute("SELECT * FROM catalog")
                for row in corsor.fetchall():
                    print(f"Book ID: {row[unique_id]} Book name: {row[book_name]} Author: {row[author]} Price: {row[price]}\n")
                    print("1. Issue the book\n2. Exit")
                    
                    choice = input("Enter the choice: ")
                    
                    match choice:
                        case '1':
                            issue_book()
                        case '2':
                            break
                        case _:
                            print("Wrong input!!!")
            except:
                print("Internal error!!!")
        else:
            print("{book_name} book is not registered in the catalog")

def issue_book():
    issue_date = datetime.utcnow().strftime('%Y-%m-%d')
    return_date = input('Enter the return date in format of (YYYY-MM-DD): ')
    
    cursor.execute("INSERT INTO issue_book (student_id, username, issue_date, return_date) VALUES (?, ?, ?, ?)", (issue_date, return_date))
    conn.commit()

def student_role():
    print("1. Sign in\n2. Sign up\n3. Exit")
    
    choice = input("Select one: ")
    
    match choice:
        case '1':
            email = input("Enter the email address: ")
            password = input("Enter the password: ")
            try:
                db_email_info = cursor.execute("SELECT * FROM user_information WHERE email=?", [email]).fetchone()
            
                if db_email_info is not None:
                    db_password_info = cursor.execute("SELECT * FROM user_information WHERE password=?", [password]).fetchone()
                    
                    if db_password_info is not None:
                        print("1. See tha catalog\n2. Search for a book\n3. Issue a book\n4. Return a book\n5. Exit")
                        
                        choice = input("Please select your choice: ")
                        
                        match choice:
                            case '1':
                                see_catalog()
                            case '2':
                                search_book()
                            case '3':
                                issue_book()
                            case '4':
                                return_book()
                            case '5':
                                break
                            case _:
                                print("Invalid choice!!!")
                    else:
                        print("Password is wrong!!!")
                else:
                    print("Email is wrong!!!")
            except:
                print("Internal problem!!!")
        case '2':
            pass
        case '3':
            break

def main():
    while True:
        print("\n")
        print("-" * 70)
        print("Library Mangement System")
        print("1. Student\n2. Librarian\n3. Exit")
        
        choice = input("Select your role: ")
        
        match choice:
            case '1':
                student_role()
            case '2':
                librarian_role()
            case '3':
                break
            case _:
                print("Invalid Choice!!!")

if __name__ = "__main__":
    main()