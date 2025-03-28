import os
import re
import uuid
import bcrypt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, Any, Optional


class LibraryManagementSystem:
    def __init__(self):
        """Initialize the Library Management System"""
        load_dotenv()
        self.uri = os.getenv("MONGODB_URI")
        if not self.uri:
            raise ValueError("MONGODB_URI environment variable not set")

        try:
            self.client = MongoClient(self.uri, server_api=ServerApi("1"))
            self.db = self.client["library_management_system"]
            self.student_collection = self.db["student"]
            self.librarian_collection = self.db["librarian"]
            self.book_collection = self.db["book"]
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def validate_input(self, input_type: str, value: str) -> bool:
        """Centralized input validation method"""
        validations = {
            "email": self._validate_email,
            "password": self._validate_password,
            "phone": self._validate_phone_number,
            "student_id": self._validate_student_id,
            "librarian_id": self._validate_librarian_id,
            "book_name": self._validate_book_name,
            "author": self._validate_author,
            "price": self._validate_price,
            "quantity": self._validate_quantity,
            "publication_date": self._validate_publication_date,
        }

        validator = validations.get(input_type)
        return validator(value) if validator else False

    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def _validate_password(self, password: str) -> bool:
        """Validate password complexity"""
        return (
            len(password) >= 8
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
            and re.search(r"[0-9]", password)
            and re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        )

    def _validate_phone_number(self, phone: str) -> bool:
        """Validate phone number"""
        cleaned_phone = re.sub(r"\D", "", phone)
        return len(cleaned_phone) >= 10 and len(cleaned_phone) <= 15

    def _validate_student_id(self, student_id: str) -> bool:
        """Validate student ID"""
        return student_id.isdigit() and len(student_id) > 0

    def _validate_librarian_id(self, librarian_id: str) -> bool:
        """Validate librarian ID"""
        return librarian_id.isdigit() and len(librarian_id) > 0

    def _validate_book_name(self, book_name: str) -> bool:
        """Validate book name"""
        return bool(book_name.strip())

    def _validate_author(self, author: str) -> bool:
        """Validate author name"""
        return bool(author.strip())

    def _validate_price(self, price: str) -> bool:
        """Validate book price"""
        try:
            price_val = float(price)
            return price_val >= 0
        except ValueError:
            return False

    def _validate_quantity(self, quantity: str) -> bool:
        """Validate book quantity"""
        try:
            quantity_val = int(quantity)
            return 0 <= quantity_val <= 1000
        except ValueError:
            return False

    def _validate_publication_date(self, publication_date: str) -> bool:
        """Validate publication date"""
        try:
            date_obj = datetime.strptime(publication_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            return date_obj <= today and date_obj >= today - timedelta(days=365 * 200)
        except ValueError:
            return False

    def format_book_display(self, book: Dict[str, Any]) -> str:
        """Format book details consistently for display"""
        return (
            f"Book ID: {book['book_id']} | Title: {book['book_name']} | "
            f"Author: {book['author']} | Price: {book['price']} | "
            f"Quantity: {book['quantity']} | Publication: {book['publication']} | "
            f"Publication Date: {book['publication_date']}"
        )

    def see_catalog(self) -> None:
        """Display the catalog of books"""
        try:
            books = list(self.book_collection.find())

            if not books:
                print("No books available in the catalog.")
                return

            print("\nCatalog of Books:")
            print("-" * 70)

            for book in books:
                print(self.format_book_display(book))
            print("-" * 70)
        except Exception as e:
            print(f"An error occurred while fetching the catalog: {e}")

    def search_book(self) -> None:
        """Search for books by name or author"""
        search_query = input("Enter the book name or author to search: ")

        try:
            books = list(
                self.book_collection.find(
                    {
                        "$or": [
                            {"book_name": {"$regex": search_query, "$options": "i"}},
                            {"author": {"$regex": search_query, "$options": "i"}},
                        ]
                    }
                )
            )

            if not books:
                print("No books found matching your search.")
                return

            print("\nSearch Results:")
            print("-" * 70)

            for book in books:
                print(self.format_book_display(book))
            print("-" * 70)

            choice = input("Do you want to issue this book? (yes/no): ").strip().lower()
            if choice == "yes":
                self.issue_book()
        except Exception as e:
            print(f"An error occurred while searching for the book: {e}")

    def issue_book(self) -> None:
        """Issue a book to a student"""
        # Validate book ID
        while True:
            book_id = input("Enter the book ID to issue: ")
            if book_id.strip():
                break
            self.see_catalog()

        # Validate student
        while True:
            student_id = input("Enter your student ID: ")
            if self.validate_input("student_id", student_id):
                break
            print("Invalid student ID. Please enter digits only.")

        username = input("Enter your username: ")
        if not username.strip():
            print("Username cannot be empty")
            return

        student = self.student_collection.find_one(
            {"student_id": student_id, "username": username}
        )
        if student is None:
            print("Invalid student credentials.")
            return

        # Check book availability
        book = self.book_collection.find_one(
            {"book_id": book_id, "quantity": {"$gt": 0}}
        )
        if book is None:
            print("Book not found or not available.")
            return

        # Check if book is already issued to this student
        existing_issue_record = self.book_collection.find_one(
            {"book_id": book_id, "issued_to.student_id": student_id}
        )
        if existing_issue_record:
            print("Book already issued to this student.")
            return

        # Handle dates
        issue_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        while True:
            return_date = input("Enter the return date (YYYY-MM-DD): ")
            if self.validate_input("publication_date", return_date):
                break

        try:
            self.book_collection.update_one(
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

    def return_book(self) -> None:
        """Return a book to the library"""
        book_id = input("Enter the book ID to return: ")

        if not book_id:
            self.see_catalog()
            return

        book = self.book_collection.find_one({"book_id": book_id})
        if book is None:
            print("Book not found.")
            return

        student_id = input("Enter your student ID: ")
        username = input("Enter your username: ")

        student = self.student_collection.find_one(
            {"student_id": student_id, "username": username}
        )
        if student is None:
            print("Invalid student credentials.")
            return

        try:
            issued_record = self.book_collection.find_one(
                {
                    "book_id": book_id,
                    "issued_to.student_id": student_id,
                    "issued_to.username": username,
                }
            )

            if issued_record is None:
                print("No issued record found for this student.")
                return

            self.book_collection.update_one(
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

    def add_book(self) -> Optional[str]:
        """Add a new book to the library"""
        try:
            book_details = {}

            while True:
                book_name = input("Enter book name: ")
                if self.validate_input("book_name", book_name):
                    book_details["book_name"] = book_name
                    break
                print("Invalid book name")

            while True:
                author = input("Enter author name: ")
                if self.validate_input("author", author):
                    book_details["author"] = author
                    break
                print("Invalid author name")

            while True:
                price = input("Enter book price: ")
                if self.validate_input("price", price):
                    book_details["price"] = float(price)
                    break
                print("Invalid price")

            while True:
                quantity = input("Enter book quantity: ")
                if self.validate_input("quantity", quantity):
                    book_details["quantity"] = int(quantity)
                    break
                print("Invalid quantity")

            while True:
                publication = input("Enter publication: ")
                if publication.strip():
                    book_details["publication"] = publication
                    break
                print("Publication cannot be empty")

            while True:
                publication_date = input("Enter publication date (YYYY-MM-DD): ")
                if self.validate_input("publication_date", publication_date):
                    book_details["publication_date"] = publication_date
                    break
                print("Invalid publication date")

            # Generate unique book ID
            book_details["book_id"] = str(uuid.uuid4())[:8]

            # Insert book
            self.book_collection.insert_one(book_details)
            print(f"Book added successfully. Book ID: {book_details['book_id']}")
            return book_details["book_id"]

        except Exception as e:
            print(f"Book addition error: {e}")
            return None

    def view_issued_books(self) -> None:
        """View all issued books"""
        try:
            issued_books = list(
                self.book_collection.find({"issued_to": {"$exists": True, "$ne": []}})
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

    def remove_book(self) -> None:
        """Remove a book from the library"""
        book_id = input("Enter the book ID to remove: ")

        if not book_id.strip():
            self.see_catalog()
            book_id = input("Enter the book ID to remove: ")
            if not book_id.strip():
                print("Book ID cannot be empty")
                return

        book = self.book_collection.find_one({"book_id": book_id})
        if book is None:
            print("Book not found.")
            return

        # Check if the book is issued to any student
        if book.get("issued_to") and len(book["issued_to"]) > 0:
            print("Cannot remove book as it is currently issued to students.")
            print("Please ensure all copies are returned before removing.")
            return

        try:
            self.book_collection.delete_one({"book_id": book_id})
            print(f"Book '{book['book_name']}' removed successfully.")
        except Exception as e:
            print(f"An error occurred while removing the book: {e}")

    def update_book(self) -> None:
        """Update book details"""
        book_id = input("Enter the book ID to update: ")

        if not book_id.strip():
            self.see_catalog()
            book_id = input("Enter the book ID to update: ")
            if not book_id.strip():
                print("Book ID cannot be empty")
                return

        book = self.book_collection.find_one({"book_id": book_id})
        if book is None:
            print("Book not found.")
            return

        update_fields = {}
        print(f"Current details of the book '{book['book_name']}':")
        print(self.format_book_display(book))

        # Book name
        book_name = input(
            "Enter the new book name (leave empty to keep current): "
        ).strip()
        if book_name and self.validate_input("book_name", book_name):
            update_fields["book_name"] = book_name

        # Author
        author = input(
            "Enter the new author name (leave empty to keep current): "
        ).strip()
        if author and self.validate_input("author", author):
            update_fields["author"] = author

        # Price
        price = input("Enter the new price (leave empty to keep current): ")
        if price and self.validate_input("price", price):
            update_fields["price"] = float(price)

        # Quantity
        quantity = input("Enter the new quantity (leave empty to keep current): ")
        if quantity and self.validate_input("quantity", quantity):
            update_fields["quantity"] = int(quantity)

        # Publication
        publication = input(
            "Enter the new publication (leave empty to keep current): "
        ).strip()
        if publication:
            update_fields["publication"] = publication

        # Publication date
        publication_date = input(
            "Enter the new publication date (YYYY-MM-DD, leave empty to keep current): "
        )
        if publication_date and self.validate_input(
            "publication_date", publication_date
        ):
            update_fields["publication_date"] = publication_date

        if not update_fields:
            print("No fields were updated.")
            return

        try:
            self.book_collection.update_one(
                {"book_id": book_id}, {"$set": update_fields}
            )
            print(f"Book '{book['book_name']}' updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating the book: {e}")

    # User registration and authentication methods remain largely the same as in the first implementation

    def register_user(self, user_type: str) -> Optional[Dict[str, Any]]:
        """Generic user registration method"""
        collection = (
            self.student_collection
            if user_type == "student"
            else self.librarian_collection
        )

        try:
            details = {}

            # ID validation
            while True:
                user_id = input(f"Enter {user_type} ID: ")
                validation_field = f"{user_type}_id"
                if self.validate_input(validation_field, user_id):
                    details[validation_field] = user_id
                    break
                print(f"Invalid {user_type} ID")

            # Username validation
            while True:
                username = input("Enter username: ")
                if username.strip():
                    details["username"] = username
                    break
                print("Username cannot be empty")

            # Email validation
            while True:
                email = input("Enter email: ")
                if self.validate_input("email", email):
                    # Check for existing email
                    if collection.find_one({"email": email}):
                        print("Email already registered")
                        continue
                    details["email"] = email
                    break
                print("Invalid email format")

            # Password validation
            while True:
                password = input("Enter password: ")
                if self.validate_input("password", password):
                    confirm_password = input("Confirm password: ")
                    if password == confirm_password:
                        details["password"] = bcrypt.hashpw(
                            password.encode("utf-8"), bcrypt.gensalt()
                        )
                        break
                    print("Passwords do not match")
                print("Password does not meet complexity requirements")

            # Phone number validation
            while True:
                phone_num = input("Enter phone number: ")
                if self.validate_input("phone", phone_num):
                    details["phone_num"] = phone_num
                    break
                print("Invalid phone number")

            # Add timestamp
            details["created_at"] = datetime.now(timezone.utc)

            # Insert user
            result = collection.insert_one(details)
            print(f"{user_type.capitalize()} registration successful!")
            return details

        except Exception as e:
            print(f"Registration error: {e}")
            return None

    def user_login(self, user_type: str) -> Optional[Dict[str, Any]]:
        """Generic user login method"""
        collection = (
            self.student_collection
            if user_type == "student"
            else self.librarian_collection
        )

        try:
            email = input("Enter email: ")
            password = input("Enter password: ")

            user = collection.find_one({"email": email})

            if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                print(f"{user_type.capitalize()} login successful!")
                return user

            print("Invalid credentials")
            return None

        except Exception as e:
            print(f"Login error: {e}")
            return None

    def reset_password(self, user_type: str) -> bool:
        """Password reset method"""
        collection = (
            self.student_collection
            if user_type == "student"
            else self.librarian_collection
        )

        try:
            email = input("Enter email: ")
            user = collection.find_one({"email": email})

            if not user:
                print("Email not found")
                return False

            # Verify current password
            current_password = input("Enter current password: ")
            if not bcrypt.checkpw(current_password.encode("utf-8"), user["password"]):
                print("Incorrect current password")
                return False

            # New password validation
            while True:
                new_password = input("Enter new password: ")
                if self.validate_input("password", new_password):
                    confirm_password = input("Confirm new password: ")
                    if new_password == confirm_password:
                        # Update password
                        hashed_password = bcrypt.hashpw(
                            new_password.encode("utf-8"), bcrypt.gensalt()
                        )
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
                        return True
                    print("Passwords do not match")
                print("Password does not meet complexity requirements")

        except Exception as e:
            print(f"Password reset error: {e}")
            return False

    def student_role(self) -> None:
        """Dedicated student role menu"""
        while True:
            print("\nStudent Menu")
            print("1. Sign in\n2. Sign up\n3. Reset Password\n4. Return to Main Menu")

            choice = input("Select one: ")

            match choice:
                case "1":
                    user = self.user_login("student")
                    if user:
                        self.student_dashboard(user)
                case "2":
                    self.register_user("student")
                case "3":
                    self.reset_password("student")
                case "4":
                    return
                case _:
                    print("Invalid choice. Please try again.")

    def librarian_role(self) -> None:
        """Dedicated librarian role menu"""
        while True:
            print("\nLibrarian Menu")
            print("1. Sign in\n2. Sign up\n3. Reset Password\n4. Return to Main Menu")

            choice = input("Select one: ")

            match choice:
                case "1":
                    user = self.user_login("librarian")
                    if user:
                        self.librarian_dashboard(user)
                case "2":
                    self.register_user("librarian")
                case "3":
                    self.reset_password("librarian")
                case "4":
                    return
                case _:
                    print("Invalid choice. Please try again.")

    def student_dashboard(self, student) -> None:
        """Student dashboard with available actions"""
        while True:
            print(f"\nWelcome, {student['username']}!")
            print(
                "1. See the catalog\n2. Search for a book\n3. Issue a book\n4. Return a book\n5. Reset Password\n6. Logout"
            )

            option = input("Select one: ")
            match option:
                case "1":
                    self.see_catalog()
                case "2":
                    self.search_book()
                case "3":
                    self.issue_book()
                case "4":
                    self.return_book()
                case "5":
                    self.reset_password("student")
                case "6":
                    return
                case _:
                    print("Invalid option. Please try again.")

    def librarian_dashboard(self, librarian) -> None:
        """Librarian dashboard with available actions"""
        while True:
            print(f"\nWelcome, {librarian['username']}!")
            print(
                "1. View Catalog\n2. Search for a book\n3. Add New Book\n4. View Issued Books\n5. Remove Book\n6. Update Book\n7. Reset Password\n8. Logout"
            )

            option = input("Select one: ")
            match option:
                case "1":
                    self.see_catalog()
                case "2":
                    self.search_book()
                case "3":
                    self.add_book()
                case "4":
                    self.view_issued_books()
                case "5":
                    self.remove_book()
                case "6":
                    self.update_book()
                case "7":
                    self.reset_password("librarian")
                case "8":
                    return
                case _:
                    print("Invalid option. Please try again.")

    def main_menu(self) -> None:
        """Main application menu"""
        while True:
            print("\n")
            print("-" * 70)
            print("Library Management System")
            print("1. Student\n2. Librarian\n3. Exit")

            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    self.student_role()
                case "2":
                    self.librarian_role()
                case "3":
                    break
                case _:
                    print("Invalid choice. Please try again.")


def main():
    """Main application entry point"""
    try:
        library_system = LibraryManagementSystem()
        library_system.main_menu()
    except Exception as e:
        print(f"Application initialization error: {e}")


if __name__ == "__main__":
    main()
