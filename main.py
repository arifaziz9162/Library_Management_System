import logging

# File handler and stream handler setup
logger = logging.getLogger("Library_Management_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("library_management.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# Custom Exception
class LibraryError(Exception):
    """Base exception for all library-related errors."""
    pass

class BookNotFoundError(LibraryError):
    """Raised when the requested book is not found in the library."""
    def __init__(self, requested_book):
        super().__init__(f"The book {requested_book} was not found in the library.")

class BookAlreadyBorrowedError(LibraryError):
    """Raised when the requested book is already borrowed by another user."""
    def __init__(self, book, borrower):
        super().__init__(f"The book {book} is already borrowed by {borrower}.")

class InvalidBookNameError(LibraryError):
    """Raised when the book name provided is empty or invalid."""
    def __init__(self):
        super().__init__("Invalid or empty book name provided.")


class Library:
    def __init__(self, books):
        self.books = books

    def show_available_books(self):
        try:
            print("\nAvailable books:")
            print("+" * 40)
            available = False
            for book, borrower in self.books.items():
                if borrower == "Free":
                    print(f"- {book}")
                    available = True
            if not available:
                print("No books are currently available.")
                logger.info("No books available at this time.")
            else:
                logger.info("Displayed available books.")
        except LibraryError as le:
            logger.error("Error occurred during showing available books", exc_info=True)
            print(str(le))

    def lend_book(self, requested_book, name):
        try:
            if not requested_book.strip():
                raise InvalidBookNameError()
            
            matched_book = None
            for book in self.books:
                if book.lower() == requested_book.lower():
                    matched_book = book
                    break

            if not matched_book:
                raise BookNotFoundError(requested_book)

            if self.books[matched_book] == "Free":
                self.books[matched_book] = name
                logger.info(f"Book lend: '{matched_book}' to {name}")
                print(f"'{matched_book}' has been borrowed by {name}")
                return True
            else:
                borrower = self.books[matched_book]
                raise BookAlreadyBorrowedError(matched_book, borrower)
            
        except LibraryError as le:
            logger.error("Error occured during lending book", exc_info=True)
            print(str(le))

    def return_book(self, returned_book):
        try:
            matched_book = None
            for book in self.books:
                if book.lower() == returned_book.lower():
                    matched_book = book
                    break

            if matched_book:
                self.books[matched_book] = "Free"
                logger.info(f"Book returned: '{matched_book}'")
                print(f"Thank you for returning '{matched_book}'.")
            else:
                raise LibraryError(f"'{returned_book}' does not belong to this library.")
            
        except LibraryError as le:
            logger.error("Error occurred during return book", exc_info=True)
            print(str(le))

class Student:
    def __init__(self, name, library):
        self.name = name
        self.library = library
        self.books = []
        logger.info(f"Student '{name}' logged into the library successfully.")

    def view_borrowed(self):
        print(f"\nBooks borrowed by {self.name}:")
        if not self.books:
            print("You haven't borrowed any books.")
        else:
            for book in self.books:
                print(f"- {book}")

    def request_book(self):
        book = input("Enter book to borrow = ").strip()
        if not book:
            print("Book name cannot be empty.")
            logger.warning(f"{self.name} entered an empty book name.")
            return
    
        if self.library.lend_book(book, self.name):
            for b in self.library.books:
                if b.lower() == book.lower():
                    self.books.append(b)
                    logger.debug(f"{self.name} borrowed {b}")
                    break

    def return_book(self):
        book = input("Enter book to return = ").strip()
        matched_book = None
        for b in self.books:
            if b.lower() == book.lower():
                matched_book = b
                break

        if matched_book:
            self.library.return_book(matched_book)
            self.books.remove(matched_book)
            logger.debug(f"{self.name} returned {matched_book}")
        else:
            logger.warning(f"{self.name} tried to return unborrowed book.")
            print("You haven't borrowed that book.")
            
def library_management_system():
    books = {
        "Python Coding": "Free",
        "Data Science": "Free",
        "Machine Learning": "Free"
    }

    library = Library(books)

    student_name = input("Enter your name = ").strip()
    student = Student(student_name, library)

    while True:
        print("\n********** Library Menu **********")
        print("1. Display Available Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. View Your Borrowed Books")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice = "))
            
            if choice == 1:
                library.show_available_books()

            elif choice == 2:
                student.request_book()

            elif choice == 3:
                student.return_book()

            elif choice == 4:
                student.view_borrowed()

            elif choice == 5:
                logger.info("Program exited by user.")
                print("Thank you for using the library. Goodbye!")
                break

            else:
                print("Invalid choice. Please select from the menu options.")

        except ValueError as ve:
            logger.warning("Invalid choice! Please choose a number between 1 to 5.", exc_info=True)
            print(str(ve))
            continue


if __name__ == "__main__":
    library_management_system()
