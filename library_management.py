from datetime import date

books = {}
collections = {}
users = {}
borrow_records = []


def get_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid input. Numbers only.")
        return None


def display_book(book_id, book):
    print(f"Book ID    : {book_id}")
    print(f"Title      : {book['title']}")
    print(f"Author     : {book['author']}")
    print(f"Available  : {book['available']}")

    if book["collection"]:
        print(f"Collection : {book['collection']}")
        print(f"Volume     : {book['volume']}")


def add_book():

    book_id = get_int("Enter Book ID: ")
    if book_id is None:
        return

    if not books:
        if book_id != 1:
            print("First Book ID must be 1.")
            return
    else:
        expected_id = max(books.keys()) + 1

        if book_id != expected_id:
            print(f"Book ID must be {expected_id}")
            return

    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    collection_choice = get_int(
        "Is this part of a collection?\n1. Yes\n2. No\nChoice: "
    )

    if collection_choice == 1:

        collection_name = input("Enter Collection Name: ").strip()
        volume = get_int("Enter Volume Number: ")

        if volume is None:
            return

        books[book_id] = {
            "title": title,
            "author": author,
            "available": True,
            "collection": collection_name,
            "volume": volume
        }

        collections.setdefault(collection_name, [])
        collections[collection_name].append(book_id)

    elif collection_choice == 2:

        books[book_id] = {
            "title": title,
            "author": author,
            "available": True,
            "collection": None,
            "volume": None
        }

    else:
        print("Invalid choice.")
        return

    print("Book added successfully.")


def remove_book():

    book_id = get_int("Enter Book ID to remove: ")

    if book_id is None:
        return

    if book_id not in books:
        print("Book not found.")
        return

    if not books[book_id]["available"]:
        print("Cannot remove an issued book.")
        return

    collection_name = books[book_id]["collection"]

    if collection_name:

        collections[collection_name].remove(book_id)

        if not collections[collection_name]:
            del collections[collection_name]

    del books[book_id]

    print("Book removed successfully.")


def clear_entry():

    book_id = get_int("Enter Book ID: ")

    if book_id is None:
        return

    if book_id not in books:
        print("Book not found.")
        return

    records_to_remove = []

    for record in borrow_records:
        if book_id in record["book_ids"]:
            records_to_remove.append(record)

    for record in records_to_remove:

        for issued_book in record["book_ids"]:
            if issued_book in books:
                books[issued_book]["available"] = True

        borrow_records.remove(record)

    print("Entry cleared successfully.")


def view_issued_books():

    active_records = [
        record
        for record in borrow_records
        if record["return_date"] is None
    ]

    if not active_records:
        print("No books currently issued.")
        return

    print("\nCURRENTLY ISSUED BOOKS\n")

    for record in active_records:
        print(f"User ID    : {record['user_id']}")
        print(f"User Name  : {record['user']}")
        print(f"Books      : {record['book_ids']}")
        print(f"Issue Date : {record['issue_date']}")


def receive_book():

    user_id = get_int("Enter User ID: ")

    if user_id is None:
        return

    if user_id not in users:

        name = input("Enter User Name: ")

        users[user_id] = {
            "id": user_id,
            "name": name,
            "blocked": False
        }

    user = users[user_id]

    if user["blocked"]:
        print("You are blocked from borrowing books.")
        return

    print("\nAVAILABLE BOOKS\n")

    available_found = False

    for book_id, book in books.items():
        if book["available"]:
            available_found = True
            display_book(book_id, book)

    if not available_found:
        print("No books available.")
        return

    selected_book = get_int("Enter Book ID: ")

    if selected_book is None:
        return

    if selected_book not in books:
        print("Book not found.")
        return

    collection_name = books[selected_book]["collection"]

    if collection_name:

        collection_books = sorted(
            collections[collection_name],
            key=lambda x: books[x]["volume"]
        )

        for book_id in collection_books:
            if not books[book_id]["available"]:
                print("Entire collection is not available.")
                return

        for book_id in collection_books:
            books[book_id]["available"] = False

        borrow_records.append({
            "user_id": user_id,
            "user": user["name"],
            "book_ids": collection_books.copy(),
            "issue_date": date.today(),
            "return_date": None
        })

        print(f"Collection '{collection_name}' issued successfully.")

    else:

        if not books[selected_book]["available"]:
            print("Book is not available.")
            return

        books[selected_book]["available"] = False

        borrow_records.append({
            "user_id": user_id,
            "user": user["name"],
            "book_ids": [selected_book],
            "issue_date": date.today(),
            "return_date": None
        })

        print("Book issued successfully.")


def return_book():

    user_id = get_int("Enter User ID: ")

    if user_id is None:
        return

    if user_id not in users:
        print("User not found.")
        return

    active_records = []

    for record in borrow_records:
        if (
            record["user_id"] == user_id
            and record["return_date"] is None
        ):
            active_records.append(record)

    if not active_records:
        print("No issued books found.")
        return

    print("\nISSUED BOOKS\n")

    for record in active_records:
        for book_id in record["book_ids"]:
            print(f"{book_id} - {books[book_id]['title']}")

    selected_book = get_int(
        "\nEnter Book ID to return: "
    )

    if selected_book is None:
        return

    target_record = None

    for record in active_records:
        if selected_book in record["book_ids"]:
            target_record = record
            break

    if target_record is None:
        print("This book is not issued to the user.")
        return

    borrow_days = (
        date.today() - target_record["issue_date"]
    ).days

    target_record["return_date"] = date.today()

    for book_id in target_record["book_ids"]:
        books[book_id]["available"] = True

    if borrow_days > 14:
        users[user_id]["blocked"] = True
        print("Returned late. User has been blocked.")

    print("Book returned successfully.")


def search_by_title():

    title = input(
        "Enter title or partial title: "
    ).lower()

    found = False

    for book_id, book in books.items():

        if title in book["title"].lower():
            display_book(book_id, book)
            found = True

    if not found:
        print("No matching books found.")


def search_by_author():

    author = input(
        "Enter author name: "
    ).lower()

    found = False

    for book_id, book in books.items():

        if author in book["author"].lower():
            display_book(book_id, book)
            found = True

    if not found:
        print("No matching authors found.")

def user_menu():

    while True:

        print("\nUSER MENU")
        print("1. Receive Book")
        print("2. Return Book")
        print("3. Search By Title")
        print("4. Search By Author")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            receive_book()

        elif choice == "2":
            return_book()

        elif choice == "3":
            search_by_title()

        elif choice == "4":
            search_by_author()

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def admin_menu():

    while True:

        print("\nADMIN MENU")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Clear Entry")
        print("4. View Issued Books")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            remove_book()

        elif choice == "3":
            clear_entry()

        elif choice == "4":
            view_issued_books()

        elif choice == "5":
            break

        else:
            print("Invalid choice.")

def main():

    while True:


        print("LIBRARY MANAGEMENT SYSTEM")

        print("1. Admin")
        print("2. User")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_menu()

        elif choice == "2":
            user_menu()

        elif choice == "3":
            print("Thank you for using LMS.")
            break

        else:
            print("Invalid choice.")

main()