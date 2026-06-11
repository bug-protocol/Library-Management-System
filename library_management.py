from datetime import date
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

def remove_book():

    book_id = int(input("Enter the book ID you want to remove!"))
    if book_id not in books:
        print("Book not found.")
        return

    collection_name = books[book_id]["collection"]

    if collection_name is not None:
        collections[collection_name].remove(book_id)

        if len(collections[collection_name]) == 0:
            del collections[collection_name]

    del books[book_id]

    print("Book removed successfully.")

def clear_entry():
    book_id = int(input("Enter your Book ID: "))
    if book_id not in books:
        print("There is no record for this Book!")
        return
    # gotta complete this function later

    remove_records = []
    for record in borrow_records:
        if book_id in record["book_ids"]:
            remove_records.append(record)

    for record in remove_records:
        borrow_records.remove(record)

    print("Book Entry Cleared!")

# User Side Functions

def receive_book():
    user_id = int(input("Enter the User ID"))

    if user_id not in users:
        user_name = input("Enter Name of the User")
        users[id] = {
            "id" : user_id,
            "name" : user_name,
            "blocked" :False
        }
    if users[user_name]["blocked"]:
        print("Sorry you are blocked from receiving any Book!")
        return
    
    print("Here is the list of all the Available Books!")

    if books:
        for book_id, book in books.items():
            if book["available"]:
                print(f"ID: {book_id}")
                print(f"Title: {book['title']}")
                print(f"Author: {book['author']}")
                print()
    
    else:
        print("No Available Books!")

    book_id = int(input("Enter the Book ID: "))

    if book_id not in books:
        print("Book not found.")
        return
    
    collection_name = books[book_id]["collction"]
    if collection_name is not None:
        book_collection = collections[collection_name]

        for find_book in book_collection:
            if not books[find_book]["available"]:
                print("Collection is not available.")
                return
            
        for find_book in book_collection:
            books[find_book]["available"] = False

        borrow_records.append({
            "user_id":user_id,
            "user": user_name,
            "book_ids": book_collection,
            "issue_date": date.today(),
            "return_date": None
        })

        print(f"Collection '{collection_name}' issued successfully.")
    
    else:

        if not books[book_id]["available"]:
            print("Book is not available.")
            return

        books[book_id]["available"] = False

        borrow_records.append({
            "user_id" : user_id,
            "user": user_name,
            "book_ids": [book_id],
            "issue_date": date.today(),
            "return_date": None
        })

        print("Book issued successfully.")

def view_issued_books():
    issued_books = []
    for record in borrow_records:
        if (record["return_date"] is None and (date.today() - record["issue_date"]).days > 14):
            issued_books.append(record)
    if not issued_books:
        print("No Book has been issued yet!")
    for all_book in issued_books:
        print(all_book)

def return_book():
    user_id = int(input("Enter the User ID"))
    if user_id not in users:
        print("User not Found!")
        return
    
    active_records = []
    for record in borrow_records:
        if (record["user_id"] == user_id and record["return_date"] is None):
           active_records.append(record)

    if not active_records:
        print("No issue record found for this user!")
        return
    
    print("\n Issued Books!")
    for record in active_records:
        for book_id in record["book_ids"]:
            print(f"{book_id} - {books[book_id]['title']}")

    selected_book_id = int(
        input("\nEnter Book ID to return: ")
    )

    target_record = None

    for record in active_records:
        if selected_book_id in record["book_ids"]:
            target_record = record
            break

    if target_record is None:
        print("This book is not issued to the user!")
        return
    
    borrow_days = (date.today() - target_record["issue_date"]).days

    target_record["return_date"] = date.today()

    if borrow_days > 14:
        users[user_id]["blocked"] = True
        print("User has returned late. Hence Blocked!")

    for book_id in target_record["book_ids"]:
        books[book_id]["available"] = True
    
def search_by_title():
    search_text = input("Enter title or substring!").lower()

    found_books = False

    for book_id, book in books.items():
        if search_text in book["title"].lower():
            found_books = True

            print(
                f"Book ID: {book_id}"
            )
            print(
                f"Title: {book['title']}"
            )
            print(
                f"Author: {book['author']}"
            )
            print()

    if found_books == False:
        print("No Matching Books Found!")

def search_by_author():
    author_search = input("Enter the name of the Author! ").lower()

    found_author = False

    for book_id, book in book.items():
        if author_search in book["author"].lower():
            found_author = True

            print(
                f"Book ID: {book_id}"
            )
            print(
                f"Title: {book['title']}"
            )
            print(
                f"Author: {book['author']}"
            )
            print()

    if found_author == False:
        print("No Matching Author Found!")


def user_menu():
    while True:
        print("\n User Menu")
        print("1. Receive Book")
        print("2. Return Book")
        print("3. Search Book By Title")
        print("4. Search Book By Author")
        print("5. Back")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            receive_book()
        elif choice == 2:
            return_book()
        elif choice == 3:
            search_by_title()
        elif choice == 4:
            search_by_author()
        elif choice == 5:
            break
        else:
            print("Invalid Choice")

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