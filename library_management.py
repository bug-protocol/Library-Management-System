books = {}
collections = {}
users = {}
borrow_records = []

# Admin Panel
def add_book():
    book_id = int(input("Enter Book Id: "))

    if books:
        new_id = max(books.keys()) + 1
        if book_id != new_id:
            print(f"Book id must be {new_id}")
            return
    
    title = input("Enter title of the Book: ")
    author = input("Enter the name of the Author: ")
    collection = int(input("Is it a collection? If Yes press 1 if No press 2"))

    if collection == 1:
        collection_name = input("Enter collection Name: ")
        volume = int(input("Enter Volume: "))

        books[book_id] = {
            "title": title,
            "author": author,
            "available": True,
            "collection": collection_name,
            "volume": volume
        }
        if collection_name not in collections:
            collections[collection_name] = []

        collections[collection_name].append(book_id)
    
    elif collection == 2:
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
    
    print("Book Added Successfully!")

    
def admin_menu():
    while True:
        print("\nADMIN MENU")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Clear Entry")
        print("4. View Borrowed Books")
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
            print("Invalid choice")

while True:
    print("\n LIBRARY MANAGEMENT SYSTEM")
    print("Press 1 for Admin")
    print("Press 2 for User")
    print("Press 3 for Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        admin_menu()
    elif choice == "2":
        pass
    elif choice == "3":
        break
    else:
        print("Invalid Choice: ")