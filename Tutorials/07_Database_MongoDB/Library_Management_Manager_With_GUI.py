from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import re
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import uuid
import bcrypt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QFormLayout,
    QDialog,
    QTabWidget,
    QGroupBox,
    QSpinBox,
    QDoubleSpinBox,
    QDateEdit,
    QStackedWidget,
    QScrollArea,
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QDate
import sys

load_dotenv()
# Retrieve the MongoDB connection string from environment variables
uri = os.getenv("MONGODB_URI")
# Check if the URI is set
# if uri is None:
#     raise ValueError("MONGODB_URI environment variable not set. Please set it in your .env file.")
# Print the URI for debugging purposes
# print(f"Connecting to MongoDB URI: {uri}")


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


db = client["library_management_system"]
# print(db)
student_collection = db["student"]
librarian_collection = db["librarian"]
book_collection = db["book"]


# Helper function for consistent book display
def format_book_display(book):
    """Format book details consistently for display"""
    return (
        f"Book ID: {book['book_id']} | Title: {book['book_name']} | "
        f"Author: {book['author']} | Price: {book['price']} | "
        f"Quantity: {book['quantity']} | Publication: {book['publication']} | "
        f"Publication Date: {book['publication_date']}"
    )


def see_catalog():
    try:
        books = list(
            book_collection.find()
        )  # Convert cursor to list to avoid count() deprecation

        if not books:  # Simplified empty check
            print("No books available in the catalog.")
            return

        print("\nCatalog of Books:")
        print("-" * 70)

        for book in books:
            print(format_book_display(book))
        print("-" * 70)
    except Exception as e:
        print(f"An error occurred while fetching the catalog: {e}")


def search_book():
    search_query = input("Enter the book name or author to search: ")

    try:
        books = list(
            book_collection.find(
                {
                    "$or": [
                        {"book_name": {"$regex": search_query, "$options": "i"}},
                        {"author": {"$regex": search_query, "$options": "i"}},
                    ]
                }
            )
        )

        if not books:  # Simplified empty check
            print("No books found matching your search.")
            return

        print("\nSearch Results:")
        print("-" * 70)

        for book in books:
            print(format_book_display(book))
        print("-" * 70)

        choice = input("Do you want to issue this book? (yes/no): ").strip().lower()
        if choice == "yes":
            issue_book()
        elif choice == "no":
            print("Returning to the main menu.")
        else:
            print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred while searching for the book: {e}")


def issue_book():
    # Get and validate book_id
    book_id = input("Enter the book ID to issue: ")
    if not book_id.strip():
        see_catalog()
        book_id = input("Enter the book ID to issue: ")
        if not book_id.strip():
            print("Book ID cannot be empty")
            return

    # Get and validate student information first
    while True:
        student_id = input("Enter your student ID: ")
        if student_id.strip() and student_id.isdigit():
            break
        print("Invalid student ID. Please enter digits only.")

    while True:
        username = input("Enter your username: ")
        if not username.strip():
            print("Username cannot be empty")
            continue

        student = student_collection.find_one(
            {"student_id": student_id, "username": username}
        )
        if student is not None:
            break
        print("Invalid student ID or username. Please try again.")

    # Now check book availability
    book = book_collection.find_one({"book_id": book_id, "quantity": {"$gt": 0}})
    if book is None:
        print("Book not found or not available.")
        return

    # Check if book is already issued to this student
    existing_issue_record = book_collection.find_one(
        {"book_id": book_id, "issued_to.student_id": student_id}
    )
    if existing_issue_record:
        print("Book already issued to this student.")
        return

    # Handle dates
    issue_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    while True:
        return_date = input("Enter the return date (YYYY-MM-DD): ")
        if validate_return_date(return_date, issue_date):
            break

    try:
        book_collection.update_one(
            {"book_id": book_id},
            {
                "$inc": {"quantity": -1},
                "$push": {
                    "issued_to": {
                        "student_id": student_id,
                        "username": username,
                        "issue_date": issue_date,
                        "return_date": return_date,
                    }
                },
            },
        )
        print(f"Book '{book['book_name']}' issued successfully to {username}.")
        print(f"Issue Date: {issue_date} | Return Date: {return_date}")
    except Exception as e:
        print(f"An error occurred while issuing the book: {e}")


def return_book():
    book_id = input("Enter the book ID to return: ")

    if book_id is None or book_id == "":
        see_catalog()

    book = book_collection.find_one({"book_id": book_id})

    if book is None:
        print("Book not found.")
        return

    while True:
        student_id = input("Enter your student ID: ")
        if student_id.isdigit():
            break
        print("Invalid student ID. Please enter digits only.")

    while True:
        username = input("Enter your username: ")

        student = student_collection.find_one(
            {"student_id": student_id, "username": username}
        )
        if student is not None:
            break
        print("Invalid student ID or username. Please try again.")

    try:
        issued_record = book_collection.find_one(
            {
                "book_id": book_id,
                "issued_to.student_id": student_id,
                "issued_to.username": username,
            }
        )

        if issued_record is None:
            print("No issued record found for this student.")
            return

        book_collection.update_one(
            {"book_id": book_id},
            {
                "$inc": {"quantity": 1},
                "$pull": {
                    "issued_to": {
                        "student_id": student_id,
                        "username": username,
                    }
                },
            },
        )
        print(f"Book '{book['book_name']}' returned successfully by {username}.")
    except Exception as e:
        print(f"An error occurred while returning the book: {e}")


def validate_date(date_string):
    """Enhanced date validation with range checks"""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_string):
        print("Date format must be YYYY-MM-DD")
        return False

    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        today = datetime.now().date()

        # Validate date is not in distant past or future
        if date_obj < today - timedelta(days=365 * 10):  # Not older than 10 years
            print("Date is too far in the past")
            return False
        if date_obj > today + timedelta(
            days=365 * 10
        ):  # Not more than 10 years in future
            print("Date is too far in the future")
            return False

        return True
    except ValueError:
        print("Invalid date. Please enter a valid date.")
        return False


def validate_return_date(return_date_str, issue_date_str):
    """Validate that return date is after issue date and within reasonable timeframe"""
    if not validate_date(return_date_str):
        return False

    try:
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
        issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d").date()

        if return_date <= issue_date:
            print("Return date must be after the issue date")
            return False

        # Check if return date is within reasonable period (e.g., 60 days)
        if (return_date - issue_date).days > 60:
            print("Return period cannot exceed 60 days")
            return False

        return True
    except ValueError:
        print("Date comparison failed. Please check date formats.")
        return False


def validate_numeric(value, is_float=False, min_val=None, max_val=None):
    """Validate numeric input with optional min/max range"""
    try:
        if is_float:
            num_val = float(value)
        else:
            num_val = int(value)

        if min_val is not None and num_val < min_val:
            print(f"Value must be at least {min_val}")
            return False, None

        if max_val is not None and num_val > max_val:
            print(f"Value cannot exceed {max_val}")
            return False, None

        return True, num_val
    except ValueError:
        print(f"Please enter a valid {'decimal' if is_float else 'whole'} number")
        return False, None


def validate_phone_number(phone):
    """Validate phone number format and length"""
    # Remove any non-digit characters
    cleaned_phone = re.sub(r"\D", "", phone)

    if not cleaned_phone.isdigit():
        print("Phone number must contain only digits")
        return False

    # Check appropriate length (adjust for your country's standards)
    if len(cleaned_phone) < 10 or len(cleaned_phone) > 15:
        print("Phone number must be between 10 and 15 digits")
        return False

    return True


def validate_email(email):
    """Validate email using regex pattern"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email) is None:
        print("Invalid email format. Example: user@example.com")
        return False
    return True


def validate_password(password):
    """Validate password complexity requirements"""
    if len(password) < 8:
        print("Password must be at least 8 characters long")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter")
        return False
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter")
        return False
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one digit")
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        print("Password must contain at least one special character")
        return False
    return True


def add_book():
    try:
        book_name = input("Enter the book name: ").strip()
        if not book_name:
            print("Book name cannot be empty")
            return

        author = input("Enter the author name: ").strip()
        if not author:
            print("Author name cannot be empty")
            return

        while True:
            price = input("Enter the book price: ")
            valid, price_val = validate_numeric(price, is_float=True, min_val=0)
            if valid:
                price = price_val
                break

        while True:
            quantity = input("Enter the quantity: ")
            valid, quantity_val = validate_numeric(quantity, min_val=1, max_val=1000)
            if valid:
                quantity = quantity_val
                break

        publication = input("Enter the publication: ").strip()
        if not publication:
            print("Publication cannot be empty")
            return

        while True:
            publication_date = input("Enter the publication date (YYYY-MM-DD): ")
            if validate_date(publication_date):
                break

        book_id = str(uuid.uuid4())[:8]

        book_collection.insert_one(
            {
                "book_id": book_id,
                "book_name": book_name,
                "author": author,
                "price": price,
                "quantity": quantity,
                "publication": publication,
                "publication_date": publication_date,
            }
        )

        print(f"Book added successfully with ID: {book_id}")
    except Exception as e:
        print(f"An error occurred: {e}")


def view_issued_books():
    try:
        issued_books = list(
            book_collection.find({"issued_to": {"$exists": True, "$ne": []}})
        )

        if not issued_books:
            print("No books have been issued.")
            return

        print("\nIssued Books:")
        print("-" * 70)

        for book in issued_books:
            print(f"Book ID: {book['book_id']} | Title: {book['book_name']}")
            print("Issued To:")
            for issue in book["issued_to"]:
                print(
                    f"  Student ID: {issue['student_id']} | Username: {issue['username']} | "
                    f"Issue Date: {issue['issue_date']} | Return Date: {issue['return_date']}"
                )
            print("-" * 30)
        print("-" * 70)
    except Exception as e:
        print(f"An error occurred while fetching issued books: {e}")


def remove_book():
    book_id = input("Enter the book ID to remove: ")

    if not book_id.strip():
        see_catalog()
        book_id = input("Enter the book ID to remove: ")
        if not book_id.strip():
            print("Book ID cannot be empty")
            return

    book = book_collection.find_one({"book_id": book_id})
    if book is None:
        print("Book not found.")
        return

    # Check if the book is issued to any student
    if book.get("issued_to") and len(book["issued_to"]) > 0:
        print("Cannot remove book as it is currently issued to students.")
        print("Please ensure all copies are returned before removing.")
        return

    try:
        book_collection.delete_one({"book_id": book_id})
        print(f"Book '{book['book_name']}' removed successfully.")
    except Exception as e:
        print(f"An error occurred while removing the book: {e}")


def update_book():
    book_id = input("Enter the book ID to update: ")

    if not book_id.strip():
        see_catalog()
        book_id = input("Enter the book ID to update: ")
        if not book_id.strip():
            print("Book ID cannot be empty")
            return

    book = book_collection.find_one({"book_id": book_id})
    if book is None:
        print("Book not found.")
        return

    try:
        print(f"Current details of the book '{book['book_name']}':")
        print(format_book_display(book))

        print("Which field do you want to update?")
        print(
            "1. Book Name\n2. Author\n3. Price\n4. Quantity\n5. Publication\n6. Publication Date"
        )
        print(
            "Do you want to update a single field or multiple fields? (single/multiple)"
        )
        update_choice = input("Select one: ").strip().lower()

        # Create an empty update dictionary
        update_fields = {}

        if update_choice == "single":
            field_choice = input("Select the field to update: ")
            match field_choice:
                case "1":
                    new_book_name = input("Enter the new book name: ").strip()
                    if not new_book_name:
                        print("Book name cannot be empty")
                        return
                    update_fields["book_name"] = new_book_name
                case "2":
                    new_author = input("Enter the new author name: ").strip()
                    if not new_author:
                        print("Author name cannot be empty")
                        return
                    update_fields["author"] = new_author
                case "3":
                    new_price = input("Enter the new price: ")
                    valid, price_val = validate_numeric(
                        new_price, is_float=True, min_val=0
                    )
                    if not valid:
                        return
                    update_fields["price"] = price_val
                case "4":
                    new_quantity = input("Enter the new quantity: ")
                    valid, quantity_val = validate_numeric(
                        new_quantity, min_val=0, max_val=1000
                    )
                    if not valid:
                        return
                    update_fields["quantity"] = quantity_val
                case "5":
                    new_publication = input("Enter the new publication: ").strip()
                    if not new_publication:
                        print("Publication cannot be empty")
                        return
                    update_fields["publication"] = new_publication
                case "6":
                    new_publication_date = input(
                        "Enter the new publication date (YYYY-MM-DD): "
                    )
                    if not validate_date(new_publication_date):
                        return
                    update_fields["publication_date"] = new_publication_date
                case _:
                    print("Invalid choice. Please try again.")
                    return
        elif update_choice == "multiple":
            # Book name
            new_book_name = input(
                "Enter the new book name (leave empty to keep current): "
            ).strip()
            if new_book_name:
                update_fields["book_name"] = new_book_name

            # Author
            new_author = input(
                "Enter the new author name (leave empty to keep current): "
            ).strip()
            if new_author:
                update_fields["author"] = new_author

            # Price
            new_price = input("Enter the new price (leave empty to keep current): ")
            if new_price:
                valid, price_val = validate_numeric(new_price, is_float=True, min_val=0)
                if not valid:
                    return
                update_fields["price"] = price_val

            # Quantity
            new_quantity = input(
                "Enter the new quantity (leave empty to keep current): "
            )
            if new_quantity:
                valid, quantity_val = validate_numeric(
                    new_quantity, min_val=0, max_val=1000
                )
                if not valid:
                    return
                update_fields["quantity"] = quantity_val

            # Publication
            new_publication = input(
                "Enter the new publication (leave empty to keep current): "
            ).strip()
            if new_publication:
                update_fields["publication"] = new_publication

            # Publication date
            new_publication_date = input(
                "Enter the new publication date (YYYY-MM-DD, leave empty to keep current): "
            )
            if new_publication_date:
                if not validate_date(new_publication_date):
                    return
                update_fields["publication_date"] = new_publication_date

            # Check if any fields were updated
            if not update_fields:
                print("No fields were updated.")
                return
        else:
            print("Invalid choice. Please try again.")
            return

        # Apply the updates
        book_collection.update_one({"book_id": book_id}, {"$set": update_fields})
        print(f"Book '{book['book_name']}' updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the book: {e}")


def student_sign_up():
    try:
        while True:
            student_id = input("Enter your student ID: ")
            if student_id.strip() and student_id.isdigit():
                break
            print("Student ID must contain only digits and cannot be empty")

        username = input("Enter your username: ")
        if not username.strip():
            print("Username cannot be empty")
            return

        while True:
            email = input("Enter your email: ")
            if validate_email(email):
                break

        while True:
            password = input("Enter your password: ")
            if validate_password(password):
                break

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        while True:
            phone_num = input("Enter your phone number: ")
            if validate_phone_number(phone_num):
                break

        # Check if the user already exists
        existing_user = student_collection.find_one(
            {"$or": [{"email": email}, {"student_id": student_id}]}
        )
        if existing_user:
            if existing_user.get("email") == email:
                print("Email already registered. Please use a different email.")
            else:
                print("Student ID already registered. Please check your ID.")
            return

        student_collection.insert_one(
            {
                "student_id": student_id,
                "username": username,
                "email": email,
                "password": hashed_password,
                "phone_num": phone_num,
                "created_at": datetime.now(timezone.utc),
            }
        )
        print("Sign up successful!")

    except Exception as e:
        print(f"An error occurred: {e}")


def student_sign_in():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        # Check if the user exists in the database
        user = student_collection.find_one({"email": email})
        if user is not None and bcrypt.checkpw(
            password.encode("utf-8"), user["password"]
        ):
            while True:
                print("\nStudent Options")
                print(
                    "1. See the catalog\n2. Search for a book\n3. Issue a book\n4. Return a book\n5. Reset Password\n6. Return to Student Menu"
                )

                option = input("Select one: ")
                match option:
                    case "1":
                        see_catalog()
                    case "2":
                        search_book()
                    case "3":
                        issue_book()
                    case "4":
                        return_book()
                    case "5":
                        reset_password("student")
                    case "6":
                        return  # Return from the function instead of break
                    case _:
                        print("Invalid option. Please try again.")
        else:
            print("Invalid email or password. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


def librarian_sign_up():
    try:
        while True:
            librarian_id = input("Enter your librarian ID: ")
            if librarian_id.strip() and librarian_id.isdigit():
                break
            print("Librarian ID must contain only digits and cannot be empty")

        username = input("Enter your username: ")
        if not username.strip():
            print("Username cannot be empty")
            return

        while True:
            email = input("Enter your email: ")
            if validate_email(email):
                break

        while True:
            password = input("Enter your password: ")
            if validate_password(password):
                break

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        while True:
            phone_num = input("Enter your phone number: ")
            if validate_phone_number(phone_num):
                break

        # Check if the user already exists
        existing_user = librarian_collection.find_one(
            {"$or": [{"email": email}, {"librarian_id": librarian_id}]}
        )
        if existing_user:
            if existing_user.get("email") == email:
                print("Email already registered. Please use a different email.")
            else:
                print("Librarian ID already registered. Please check your ID.")
            return

        librarian_collection.insert_one(
            {
                "librarian_id": librarian_id,
                "username": username,
                "email": email,
                "password": hashed_password,
                "phone_num": phone_num,
                "created_at": datetime.now(timezone.utc),
            }
        )
        print("Sign up successful!")

    except Exception as e:
        print(f"An error occurred: {e}")


def librarian_sign_in():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        # Check if the user exists in the database
        user = librarian_collection.find_one({"email": email})
        if user is not None and bcrypt.checkpw(
            password.encode("utf-8"), user["password"]
        ):
            while True:
                print("\nLibrarian Options")
                print(
                    "1. View Catalog\n2. Search for a book\n3. Add New Book\n4. View Issued Books\n5. Remove Book\n6. Update Book\n7. Reset Password\n8. Return to Librarian Menu"
                )

                option = input("Select one: ")
                match option:
                    case "1":
                        see_catalog()
                    case "2":
                        search_book()
                    case "3":
                        add_book()
                    case "4":
                        view_issued_books()
                    case "5":
                        remove_book()
                    case "6":
                        update_book()
                    case "7":
                        reset_password("librarian")
                    case "8":
                        return  # Return from the function instead of break
                    case _:
                        print("Invalid option. Please try again.")
        else:
            print("Invalid email or password. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


def librarian_role():
    while True:
        print("\nLibrarian Menu")
        print("1. Sign in\n2. Sign up\n3. Reset Password\n4. Return to Main Menu")

        choice = input("Select one: ")

        match choice:
            case "1":
                librarian_sign_in()
            case "2":
                librarian_sign_up()
            case "3":
                reset_password("librarian")
            case "4":
                return
            case _:
                print("Invalid choice. Please try again.")


def student_role():
    while True:
        print("\nStudent Menu")
        print("1. Sign in\n2. Sign up\n3. Reset Password\n4. Return to Main Menu")

        choice = input("Select one: ")

        match choice:
            case "1":
                student_sign_in()
            case "2":
                student_sign_up()
            case "3":
                reset_password("student")
            case "4":
                return
            case _:
                print("Invalid choice. Please try again.")


def reset_password(collection_name):
    """Reset password function for both students and librarians"""
    email = input("Enter your email: ")

    # Determine which collection to use
    if collection_name == "student":
        collection = student_collection
    elif collection_name == "librarian":
        collection = librarian_collection
    else:
        print("Invalid collection type")
        return

    # Check if user exists
    user = collection.find_one({"email": email})
    if user is None:
        print("Email not found. Please check your email and try again.")
        return

    # Verify identity with current password
    current_password = input("Enter your current password: ")
    if not bcrypt.checkpw(current_password.encode("utf-8"), user["password"]):
        print("Incorrect password. Password reset failed.")
        return

    # Get and validate new password
    while True:
        new_password = input("Enter your new password: ")
        if validate_password(new_password):
            confirm_password = input("Confirm your new password: ")
            if new_password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")

    # Hash and update the new password
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    try:
        collection.update_one(
            {"email": email},
            {
                "$set": {
                    "password": hashed_password,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        print("Password reset successful!")
    except Exception as e:
        print(f"An error occurred while resetting password: {e}")


class LibraryManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)
        self.current_user = None
        self.user_type = None

        # Create the central widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main menu screen
        self.init_main_menu()

        # Create the student screens
        self.init_student_login_screen()
        self.init_student_signup_screen()

        # Create the librarian screens
        self.init_librarian_login_screen()
        self.init_librarian_signup_screen()

        # Display the main menu first
        self.central_widget.setCurrentIndex(0)

    def init_main_menu(self):
        main_menu = QWidget()
        layout = QVBoxLayout()

        # Add header
        header_label = QLabel("Library Management System")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(header_label)

        # Add role selection buttons
        student_btn = QPushButton("Student")
        librarian_btn = QPushButton("Librarian")
        exit_btn = QPushButton("Exit")

        # Connect buttons to functions
        student_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(1)
        )  # Student login screen
        librarian_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(3)
        )  # Librarian login screen
        exit_btn.clicked.connect(self.close)

        # Add buttons to layout
        layout.addStretch(1)
        layout.addWidget(student_btn)
        layout.addWidget(librarian_btn)
        layout.addWidget(exit_btn)
        layout.addStretch(1)

        main_menu.setLayout(layout)
        self.central_widget.addWidget(main_menu)

    def init_student_login_screen(self):
        student_login = QWidget()
        layout = QVBoxLayout()

        # Create header
        header_label = QLabel("Student Login")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header_label)

        # Create form
        form_layout = QFormLayout()
        self.student_email_input = QLineEdit()
        self.student_password_input = QLineEdit()
        self.student_password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Email:", self.student_email_input)
        form_layout.addRow("Password:", self.student_password_input)

        form_container = QWidget()
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        # Create buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        signup_btn = QPushButton("Sign Up")
        back_btn = QPushButton("Back")

        # Connect buttons
        login_btn.clicked.connect(self.student_login)
        signup_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(2)
        )  # Student signup screen
        back_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(0)
        )  # Main menu

        # Add buttons to layout
        button_layout.addWidget(login_btn)
        button_layout.addWidget(signup_btn)
        button_layout.addWidget(back_btn)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        student_login.setLayout(layout)
        self.central_widget.addWidget(student_login)

    def init_student_signup_screen(self):
        student_signup = QWidget()
        layout = QVBoxLayout()

        # Create header
        header_label = QLabel("Student Sign Up")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header_label)

        # Create form
        form_layout = QFormLayout()
        self.student_id_signup = QLineEdit()
        self.student_username_signup = QLineEdit()
        self.student_email_signup = QLineEdit()
        self.student_password_signup = QLineEdit()
        self.student_password_signup.setEchoMode(QLineEdit.Password)
        self.student_confirm_password_signup = QLineEdit()
        self.student_confirm_password_signup.setEchoMode(QLineEdit.Password)
        self.student_phone_signup = QLineEdit()

        form_layout.addRow("Student ID:", self.student_id_signup)
        form_layout.addRow("Username:", self.student_username_signup)
        form_layout.addRow("Email:", self.student_email_signup)
        form_layout.addRow("Password:", self.student_password_signup)
        form_layout.addRow("Confirm Password:", self.student_confirm_password_signup)
        form_layout.addRow("Phone Number:", self.student_phone_signup)

        form_container = QWidget()
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        # Create buttons
        button_layout = QHBoxLayout()
        signup_btn = QPushButton("Sign Up")
        back_btn = QPushButton("Back")

        # Connect buttons
        signup_btn.clicked.connect(self.student_signup)
        back_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(1)
        )  # Student login screen

        # Add buttons to layout
        button_layout.addWidget(signup_btn)
        button_layout.addWidget(back_btn)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        student_signup.setLayout(layout)
        self.central_widget.addWidget(student_signup)

    def init_librarian_login_screen(self):
        librarian_login = QWidget()
        layout = QVBoxLayout()

        # Create header
        header_label = QLabel("Librarian Login")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header_label)

        # Create form
        form_layout = QFormLayout()
        self.librarian_email_input = QLineEdit()
        self.librarian_password_input = QLineEdit()
        self.librarian_password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Email:", self.librarian_email_input)
        form_layout.addRow("Password:", self.librarian_password_input)

        form_container = QWidget()
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        # Create buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        signup_btn = QPushButton("Sign Up")
        back_btn = QPushButton("Back")

        # Connect buttons
        login_btn.clicked.connect(self.librarian_login)
        signup_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(4)
        )  # Librarian signup screen
        back_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(0)
        )  # Main menu

        # Add buttons to layout
        button_layout.addWidget(login_btn)
        button_layout.addWidget(signup_btn)
        button_layout.addWidget(back_btn)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        librarian_login.setLayout(layout)
        self.central_widget.addWidget(librarian_login)

    def init_librarian_signup_screen(self):
        librarian_signup = QWidget()
        layout = QVBoxLayout()

        # Create header
        header_label = QLabel("Librarian Sign Up")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header_label)

        # Create form
        form_layout = QFormLayout()
        self.librarian_id_signup = QLineEdit()
        self.librarian_username_signup = QLineEdit()
        self.librarian_email_signup = QLineEdit()
        self.librarian_password_signup = QLineEdit()
        self.librarian_password_signup.setEchoMode(QLineEdit.Password)
        self.librarian_confirm_password_signup = QLineEdit()
        self.librarian_confirm_password_signup.setEchoMode(QLineEdit.Password)
        self.librarian_phone_signup = QLineEdit()

        form_layout.addRow("Librarian ID:", self.librarian_id_signup)
        form_layout.addRow("Username:", self.librarian_username_signup)
        form_layout.addRow("Email:", self.librarian_email_signup)
        form_layout.addRow("Password:", self.librarian_password_signup)
        form_layout.addRow("Confirm Password:", self.librarian_confirm_password_signup)
        form_layout.addRow("Phone Number:", self.librarian_phone_signup)

        form_container = QWidget()
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        # Create buttons
        button_layout = QHBoxLayout()
        signup_btn = QPushButton("Sign Up")
        back_btn = QPushButton("Back")

        # Connect buttons
        signup_btn.clicked.connect(self.librarian_signup)
        back_btn.clicked.connect(
            lambda: self.central_widget.setCurrentIndex(3)
        )  # Librarian login screen

        # Add buttons to layout
        button_layout.addWidget(signup_btn)
        button_layout.addWidget(back_btn)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        librarian_signup.setLayout(layout)
        self.central_widget.addWidget(librarian_signup)

    # Authentication methods that connect to existing logic
    def student_login(self):
        email = self.student_email_input.text()
        password = self.student_password_input.text()

        try:
            user = student_collection.find_one({"email": email})
            if user is not None and bcrypt.checkpw(
                password.encode("utf-8"), user["password"]
            ):
                self.current_user = user
                self.user_type = "student"
                self.show_student_dashboard()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def student_signup(self):
        student_id = self.student_id_signup.text()
        username = self.student_username_signup.text()
        email = self.student_email_signup.text()
        password = self.student_password_signup.text()
        confirm_password = self.student_confirm_password_signup.text()
        phone_num = self.student_phone_signup.text()

        if not student_id.strip() or not student_id.isdigit():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Student ID must contain only digits and cannot be empty.",
            )
            return

        if not username.strip():
            QMessageBox.warning(self, "Validation Error", "Username cannot be empty.")
            return

        if not validate_email(email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            return

        if not validate_password(password):
            return  # validate_password already shows message

        if not validate_phone_number(phone_num):
            return  # validate_phone_number already shows message

        # Check if user already exists
        existing_user = student_collection.find_one(
            {"$or": [{"email": email}, {"student_id": student_id}]}
        )
        if existing_user:
            if existing_user.get("email") == email:
                QMessageBox.warning(
                    self, "Registration Error", "Email already registered."
                )
            else:
                QMessageBox.warning(
                    self, "Registration Error", "Student ID already registered."
                )
            return

        # Hash password and create user
        try:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            student_collection.insert_one(
                {
                    "student_id": student_id,
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                    "phone_num": phone_num,
                    "created_at": datetime.now(timezone.utc),
                }
            )
            QMessageBox.information(self, "Success", "Student registration successful!")
            self.central_widget.setCurrentIndex(1)  # Go back to login screen
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def librarian_login(self):
        email = self.librarian_email_input.text()
        password = self.librarian_password_input.text()

        try:
            user = librarian_collection.find_one({"email": email})
            if user is not None and bcrypt.checkpw(
                password.encode("utf-8"), user["password"]
            ):
                self.current_user = user
                self.user_type = "librarian"
                self.show_librarian_dashboard()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def librarian_signup(self):
        librarian_id = self.librarian_id_signup.text()
        username = self.librarian_username_signup.text()
        email = self.librarian_email_signup.text()
        password = self.librarian_password_signup.text()
        confirm_password = self.librarian_confirm_password_signup.text()
        phone_num = self.librarian_phone_signup.text()

        if not librarian_id.strip() or not librarian_id.isdigit():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Librarian ID must contain only digits and cannot be empty.",
            )
            return

        if not username.strip():
            QMessageBox.warning(self, "Validation Error", "Username cannot be empty.")
            return

        if not validate_email(email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            return

        if not validate_password(password):
            return  # validate_password already shows message

        if not validate_phone_number(phone_num):
            return  # validate_phone_number already shows message

        # Check if user already exists
        existing_user = librarian_collection.find_one(
            {"$or": [{"email": email}, {"librarian_id": librarian_id}]}
        )
        if existing_user:
            if existing_user.get("email") == email:
                QMessageBox.warning(
                    self, "Registration Error", "Email already registered."
                )
            else:
                QMessageBox.warning(
                    self, "Registration Error", "Librarian ID already registered."
                )
            return

        # Hash password and create user
        try:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            librarian_collection.insert_one(
                {
                    "librarian_id": librarian_id,
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                    "phone_num": phone_num,
                    "created_at": datetime.now(timezone.utc),
                }
            )
            QMessageBox.information(
                self, "Success", "Librarian registration successful!"
            )
            self.central_widget.setCurrentIndex(3)  # Go back to login screen
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    # These will be implemented in future code
    def show_student_dashboard(self):
        # We'll implement this in the next version
        QMessageBox.information(
            self,
            "Coming Soon",
            "Student Dashboard will be implemented in the next version",
        )

    def show_librarian_dashboard(self):
        # We'll implement this in the next version
        QMessageBox.information(
            self,
            "Coming Soon",
            "Librarian Dashboard will be implemented in the next version",
        )


# Replace the main function to use the GUI
def main():
    app = QApplication(sys.argv)
    window = LibraryManagementSystem()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
