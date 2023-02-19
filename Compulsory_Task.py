import sqlite3
from typing import Type
import PySimpleGUI as sg


def database_start():
    # Creates or opens a file called ebookstore with a SQLite3
    db = sqlite3.connect("ebookstore")
    cursor = db.cursor()
    # create the table and the headers
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY,Title VARCHAR(50), Author VARCHAR(50), Qty INTEGER)"""
    )
    # try/except in case the id already exist
    try:
        # books details
        books_list = [
            (3001, "A Tale of Two Cities", "Charles Dickens", 61),
            (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
            (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
            (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
            (3005, "Alice in Wonderland", "Lewis Carroll", 12),
        ]
        # add the books details above to the table
        cursor.executemany(
            """INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)""",
            books_list,
        )
        db.commit()
    # error catching incase the id already exist
    except Exception as e:
        print(e)
    # close the connection
    finally:
        db.close()


database_start()


def main_menu():
    layout = [
        [sg.Text("Welcome to the book database.")],
        [sg.Text("Please enter the operation :")],
        [sg.Button("1"), sg.Text("Add a book")],
        [sg.Button("2"), sg.Text("Update a book")],
        [sg.Button("3"), sg.Text("Delete a book")],
        [sg.Button("4"), sg.Text("Search a book")],
        [sg.Button("Exit")],
    ]
    return sg.Window("Main Menu", layout, finalize=True)


def add_book_view():
    db = sqlite3.connect("ebookstore")
    cursor = db.cursor()
    cursor.execute("""Select * FROM books""")
    global lastId
    # print all the books in the database
    books_text = ""
    for row in cursor:
        books_text = books_text + "ID: {0} Title: {1} ".format(row[0], row[1]) + "\n"
        # this will get the last id number
        lastId = row[0]
    db.close()
    layout = [
        [sg.Text("You have selected option 1")],
        [sg.Text(books_text)],
        [sg.Text("Please enter the title you like to add: ")],
        [sg.Text("Title", size=(15, 1)), sg.InputText(key="title")],
        [sg.Text("Author", size=(15, 1)), sg.InputText(key="author")],
        [sg.Text("Quantity", size=(15, 1)), sg.InputText(key="qnty")],
        [sg.Button("Add"), sg.Button("Cancel")],
    ]

    return sg.Window("Add a book", layout, modal=True, finalize=True)


def update_book_view():
    db = sqlite3.connect("ebookstore")
    cursor = db.cursor()
    cursor.execute("""Select * FROM books""")
    books_text = ""
    for row in cursor:
        books_text = books_text + "ID: {0} Title: {1} ".format(row[0], row[1]) + "\n"
    db.close()
    layout = [
        [sg.Text("You have selected option 2")],
        [sg.Text(books_text)],
        [sg.Text("Please enter the id of the title you wish to update: ")],
        [sg.Text("ID", size=(15, 1)), sg.InputText(key="update_id")],
        [sg.Button("Update"), sg.Button("Cancel")],
    ]
    return sg.Window("Update a book", layout, modal=True, finalize=True)


def delete_book_view():
    db = sqlite3.connect("ebookstore")
    cursor = db.cursor()
    cursor.execute("""Select * FROM books""")
    books_text = ""
    for row in cursor:
        books_text = books_text + "ID: {0} Title: {1} ".format(row[0], row[1]) + "\n"
    db.close()
    layout = [
        [sg.Text("You have selected option 3")],
        [sg.Text(books_text)],
        [sg.Text("Please enter the id of the title you wish to delete: ")],
        [sg.Text("ID", size=(15, 1)), sg.InputText(key="delete_id")],
        [sg.Button("Delete"), sg.Button("Cancel")],
    ]
    return sg.Window("Delete a book", layout, modal=True, finalize=True)


def detail_book_view():
    db = sqlite3.connect("ebookstore")
    cursor = db.cursor()
    cursor.execute("""Select * FROM books""")
    global lastId
    # print all the books in the database
    books_text = ""
    for row in cursor:
        books_text = books_text + "ID: {0} Title: {1} ".format(row[0], row[1]) + "\n"
        # this will get the last id number
        lastId = row[0]
    db.close()
    layout = [
        [sg.Text("You have selected option 4")],
        [sg.Text(books_text)],
        [sg.Text("Please enter the name of the title: ")],
        [sg.Text("Title", size=(15, 1)), sg.InputText(key="detail_title")],
        [sg.Button("View"), sg.Button("Cancel")],
    ]

    return sg.Window("Detail view", layout, modal=True, finalize=True)


# Create the window
window1, window2 = main_menu(), None  # start off with 1 window open

while True:
    window, event, values = sg.read_all_windows()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "Exit" or event == "Cancel":
        window.close()
        if window == window2:  # if closing win 2, mark as closed
            window2 = None
        elif window == window1:  # if closing win 1, exit program
            break
    if event == "1":
        window2 = add_book_view()
    # add logic to the database
    if event == "Add":
        ready_to_commit = True
        title = values["title"]
        author = values["author"]
        qnty = values["qnty"]
        # check for blank
        if title == "" or author == "" or qnty == "":
            sg.Popup("Empty field detected, Please populate every field.")
            ready_to_commit = False
        else:
            # check if the qnty entered is an interger
            try:
                int(values["qnty"])
            except:
                sg.Popup("Quantity is not an interger.")
                ready_to_commit = False
        # write to database if all data is correct
        if ready_to_commit:
            try:
                db = sqlite3.connect("ebookstore")
                cursor = db.cursor()
                # new id
                id = lastId + 1
                cursor.execute(
                    """INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)""",
                    (id, title, author, qnty),
                )
                db.commit()
                sg.Popup("Entry has been added")
                window.close()
            except Exception as e:
                sg.Popup(e)
            finally:
                db.close()

    if event == "3":
        window2 = delete_book_view()
    if event == "Delete":
        ready_to_commit = True
        delete_id = values["delete_id"]
        if delete_id == "":
            sg.Popup("Empty field detected, Please populate every field.")
            ready_to_commit = False
        else:
            # check if the id entered is an interger
            try:
                int_test = int(delete_id)
            except:
                sg.Popup("ID entered is not an interger.")
                ready_to_commit = False
        db = sqlite3.connect("ebookstore")
        cursor = db.cursor()
        print(type(int_test))
        # check if the Id exist
        if delete_id != "" and isinstance(int_test, int):
            cursor.execute("""SELECT id FROM books WHERE id = ?""", (delete_id,))
            data = cursor.fetchall()
            if len(data) == 0:
                sg.Popup("ID entered deos not exist.")
                ready_to_commit = False
        if ready_to_commit:
            try:
                cursor.execute("""DELETE FROM books WHERE id = ?""", (delete_id,))
                db.commit()
                sg.Popup("Request has been send succesfully")
                window.close()
            except Exception as e:
                sg.Popup(e)
        db.close()

    if event == "4":
        window2 = detail_book_view()
    if event == "View":
        sg.Popup("view")

window.close()


# # main menu
user_input = None

while user_input != 0:
    try:
        # user_input = int(
        #     input(
        #         """Please enter the operation number:
        #                 1 - Enter book
        #                 2 - Update book
        #                 3 - Delete book
        #                 4 - Search books
        #                 0 - Exit
        #                 :"""
        #     )
        # )

        # if user_input > 4 or user_input < 0:
        #     print("Invalid input please enter a number from 0 to 4")
        # else:
        # add a book to the database
        # if user_input == 1:
        #     db = sqlite3.connect("ebookstore")
        #     cursor = db.cursor()
        #     cursor.execute("""Select * FROM books""")
        #     # print all the books in the database
        #     for row in cursor:
        #         print("ID: {0} Title: {1} ".format(row[0], row[1]))
        #         # this will get the last id number
        #         id = row[0]
        #     print("\n")
        #     # new id
        #     id = id + 1
        #     title_to_add = input("Please enter the title you like to add: ")
        #     author_to_add = input("Please enter the Author of the title: ")
        #     try:
        #         qnty_to_add = int(input("Please enter the quantity of the book: "))
        #         cursor.execute(
        #             """INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)""",
        #             (id, title_to_add, author_to_add, qnty_to_add),
        #         )
        #         db.commit()
        #         print("Entry has been added")
        #     except Exception as e:
        #         print(e)
        #     db.close()
        # update a book in the database
        if user_input == 2:
            db = sqlite3.connect("ebookstore")
            cursor = db.cursor()
            # print all books id and title for the user to choose from
            cursor.execute("""Select * FROM books""")
            for row in cursor:
                print("ID: {0} Title: {1} ".format(row[0], row[1]))
            print("\n")

            # get id input from the user
            try:
                query_id = int(
                    input(
                        "Please enter the id of the title you wish to update: "
                    ).strip()
                )

                # check if this id exist in the database
                cursor.execute("""SELECT id FROM books WHERE id = ?""", (query_id,))
                data = cursor.fetchall()
                if len(data) == 0:
                    print("There is no records in the database with that id.")
                else:
                    # ask the user which info they want to update
                    option_isValid = False
                    while not option_isValid:
                        try:
                            user_option = int(
                                input(
                                    "Please enter the number below that corresponded to what you would like to update:\n1 - Title \n2 - Author \n3 - Quantity \n0 - Back to Main menu\n:"
                                )
                            )
                            # title update
                            if user_option == 1:
                                option_isValid = True
                                updated_title = input("Please enter a new title: ")
                                cursor.execute(
                                    """UPDATE books SET Title = ? WHERE id = ?""",
                                    (updated_title, query_id),
                                )
                                db.commit()
                                print("Title has been updated")
                                break
                            # author update
                            if user_option == 2:
                                option_isValid = True
                                updated_author = input("Please enter a new author: ")
                                cursor.execute(
                                    """UPDATE books SET Author = ? WHERE id = ?""",
                                    (updated_author, query_id),
                                )
                                db.commit()
                                print("Author has been updated")
                                break
                            # qnty update
                            if user_option == 3:
                                option_isValid = True
                                try:
                                    updated_qty = int(
                                        input("Please enter a new quantity: ")
                                    )
                                    cursor.execute(
                                        """UPDATE books SET Qty = ? WHERE id = ?""",
                                        (updated_qty, query_id),
                                    )
                                    db.commit()
                                    print("Quantity has been updated")
                                    break
                                except Exception as e:
                                    print(e)
                            # Back to the main menu
                            if user_option == 0:
                                break
                            else:
                                print(
                                    "Invalid input. Please enter a number from 0 to 3"
                                )
                        except:
                            print("Invalid input")
            except Exception as e:
                print(e)
            # close db connection
            db.close()
        # delete a book in the database
        # if user_input == 3:
        #     db = sqlite3.connect("ebookstore")
        #     cursor = db.cursor()
        #     # print all books id and title for the user to choose from
        #     cursor.execute("""Select * FROM books""")
        #     for row in cursor:
        #         print("ID: {0} Title: {1} ".format(row[0], row[1]))
        #     print("\n")
        #     # ask user the id of the book they want to delete
        #     try:
        #         id_to_delete = int(
        #             input(
        #                 "Please enter they id of the book you wish to delete from the database: "
        #             )
        #         )
        #         cursor.execute("""DELETE FROM books WHERE id = ?""", (id_to_delete,))
        #         db.commit()
        #         print("Entry has been deleted")
        #     except Exception as e:
        #         print(e)
        #     # close db connection
        #     db.close()
        # search a specific book detail in the database
        if user_input == 4:
            db = sqlite3.connect("ebookstore")
            cursor = db.cursor()
            # show all the books title in the database
            cursor.execute("""Select * FROM books""")
            for row in cursor:
                print("ID: {0} Title: {1} ".format(row[0], row[1]))
            print("\n")
            # ask the user for the title to look for
            query_title = input("Please enter the name of the title: ").strip()
            # check if the query exist in the database
            cursor.execute(
                """SELECT Title FROM books WHERE Title = ?""", (query_title,)
            )
            data = cursor.fetchall()
            if len(data) == 0:
                print("There is no records in the database with that title.")
            # print the book detail
            else:
                cursor.execute(
                    """SELECT * FROM books WHERE Title = ?""", (query_title,)
                )
                for row in cursor:
                    print(
                        "ID: {0} Title: {1} \tAuthor: {2} Qty: {3}".format(
                            row[0], row[1], row[2], row[3]
                        )
                    )
            db.close()
        # quit program
        if user_input == 0:
            break
    except Exception as e:
        print(e)
