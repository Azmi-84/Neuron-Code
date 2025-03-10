import sqlite3
import re
from datetime import date, datetime, timezone

conn = sqlite3.connect('Library_Management.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_information(
        student_id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        phone_num INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS catalog(
        unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_name TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS issue_book(
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        issue_date DATE NOT NULL,
        return_date DATE NOT NULL
    )
''')

def see_catalog():
    try:
        cursor.execute("SELECT * FROM catalog")
        books = cursor.fetchall()
        
        if not books:
            print("No books in catalog.")
            return
            
        for row in books:
            print(f"Book ID: {row[0]} | Book name: {row[1]} | Author: {row[2]} | Price: ${row[3]}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def search_book():
    book_name = input("Enter the book name: ")
    
    try:
        book = cursor.execute("SELECT * FROM catalog WHERE book_name LIKE ?", ['%'+book_name+'%']).fetchone()
        
        if book is not None:
            print(f"Book ID: {book[0]} | Book name: {book[1]} | Author: {book[2]} | Price: ${book[3]}")
            print("1. Issue the book\n2. Exit")
            
            choice = input("Enter the choice: ")
            
            match choice:
                case '1':
                    issue_book()
                case '2':
                    return  
                case _:
                    print("Wrong input!!!")
        else:
            print(f"{book_name} book is not registered in the catalog")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def validate_date_format(date_str):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def issue_book(book_id=None):
    if book_id is None:
        see_catalog()
        book_id = input("Enter the book ID you want to issue: ")
        
        book = cursor.execute("SELECT * FROM catalog WHERE unique_id=?", [book_id]).fetchone()
        if not book:
            print("Book not found.")
            return
    
    issue_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    while True:
        return_date = input('Enter the return date in format of (YYYY-MM-DD): ')
        if validate_date_format(return_date):
            if return_date < issue_date:
                print("Return date must be after issue date.")
                continue
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    student_id = input("Enter your student ID: ")
    username = input("Enter your username: ")
    
    try:
        student = cursor.execute("SELECT * FROM user_information WHERE student_id=?", [student_id]).fetchone()
        if not student:
            print("Student ID not found. Please sign up first.")
            return
            
        existing = cursor.execute("SELECT * FROM issue_book WHERE student_id=? AND book_id=?", [student_id, book_id]).fetchone()
        if existing:
            print("You already have this book issued.")
            return
            
        cursor.execute("INSERT INTO issue_book (student_id, book_id, username, issue_date, return_date) VALUES (?, ?, ?, ?, ?)",(student_id, book_id, username, issue_date, return_date))
        conn.commit()
        print("Book issued successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        

def return_book():
    student_id = input("Enter your student ID: ")
    try:
        issued_books = cursor.execute("""
    SELECT i.issue_id, c.book_name, i.issue_date, i.return_date
    FROM issue_book i
    JOIN catalog c ON i.book_id = c.unique_id
    WHERE i.student_id=?
""", [student_id]).fetchall()
        
        if issued_books:
            for book in issued_books:
                print(f"Issue ID: {book[0]} | Book Name: {book[1]} | Issue Date: {book[2]} | Return Date: {book[3]}")
            
            issue_id = input("Enter the issue ID to return the book: ")
            issue = cursor.execute("SELECT * FROM issue_book WHERE issue_id=? AND student_id=?", [issue_id, student_id]).fetchone()
            if issue:
                cursor.execute("DELETE FROM issue_book WHERE issue_id=?", [issue_id])
                conn.commit()
                print("Book returned successfully!")
            else:
                print("Issue ID not found or does not belong to this student.")
        else:
            print("No books issued with this student ID")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def add_book():
    try:
        book_name = input("Enter book name: ")
        author = input("Enter author name: ")
        price = float(input("Enter book price: "))
        cursor.execute("INSERT INTO catalog (book_name, author, price) VALUES (?, ?, ?)", (book_name, author, price))
        conn.commit()
        print("Book added successfully!")
    except ValueError:
        print("Invalid price. Please enter a number.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def remove_book():
    try:
        book_id = input("Enter book ID to remove: ")
        
        issued_book = cursor.execute("SELECT * FROM issue_book WHERE book_id=?", [book_id]).fetchone()
        if issued_book:
            print("Book is currently issued. Cannot remove.")
            return
        book = cursor.execute("SELECT * FROM catalog WHERE unique_id=?", [book_id]).fetchone()
        if book:
            cursor.execute("DELETE FROM catalog WHERE unique_id=?", [book_id])
            conn.commit()
            print("Book removed successfully!")
        else:
            print("Book not found!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def librarian_role():
    while True:
        print("\nLibrarian Menu")
        print("1. View Catalog\n2. Add New Book\n3. Remove Book\n4. View Issued Books\n5. Return to Main Menu")
        
        choice = input("Select option: ")
        
        match choice:
            case '1':
                see_catalog()
            case '2':
                add_book()
            case '3':
                remove_book()
            case '4':
                try:
                    cursor.execute("SELECT * FROM issue_book")
                    books = cursor.fetchall()
                    if books:
                        for book in books:
                            print(f"Student ID: {book[0]} | Username: {book[1]} | Issue Date: {book[2]} | Return Date: {book[3]}")
                    else:
                        print("No books currently issued")
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
            case '5':
                return
            case _:
                print("Invalid choice!")

def sign_up():
    try:
        student_id = input("Enter student ID: ")
        username = input("Enter username: ")
        
        while True:
            email = input("Enter email: ")
            if '@' in email and '.' in email:
                break
            print("Invalid email address!")
            
        password = input("Enter password: ")

        while True:
            phone_num = input("Enter phone number: ")
            if phone_num.isdigit():
                break
            print("Invalid phone number!")
                    
        existing = cursor.execute("SELECT * FROM user_information WHERE student_id=? OR email=?", 
                                [student_id, email]).fetchone()
        if existing:
            print("Student ID or email already registered!")
            return
            
        cursor.execute("INSERT INTO user_information VALUES (?, ?, ?, ?, ?)", (student_id, username, email, password, phone_num))
        conn.commit()
        print("Registration successful!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def student_role():
    while True:
        print("\nStudent Menu")
        print("1. Sign in\n2. Sign up\n3. Return to Main Menu")
        
        choice = input("Select one: ")
        
        match choice:
            case '1':
                email = input("Enter the email address: ")
                password = input("Enter the password: ")
                try:
                    user = cursor.execute("SELECT * FROM user_information WHERE email=? AND password=?", [email, password]).fetchone()
                
                    if user is not None:
                        while True:
                            print("\nStudent Options")
                            print("1. See the catalog\n2. Search for a book\n3. Issue a book\n4. Return a book\n5. Return to Student Menu")
                            
                            option = input("Please select your choice: ")
                            
                            match option:
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
                        print("Invalid email or password!")
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
            case '2':
                sign_up()
            case '3':
                return
            case _:
                print("Invalid choice!")

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

if __name__ == "__main__":
    main()