import datetime
import pymongo
import tkinter as tk
from tkinter import *


def searchHandler(type, data='none'):
    try:
        # Connecting to server
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = pymongo.MongoClient(CONNECTION_STRING)

        # Selecting db
        mydb = client['MoviesDB']

        # Selecting collection
        col = mydb['Movies']

        if type == 'all':
            records = list(col.find())
            return records
        if type == 'director':
            agg_result = col.aggregate(
                [{
                    "$group":
                    {"_id": "$Director",
                     "numPelis": {"$sum": 1}
                     },
                },
                    {
                    "$sort": {"numPelis": -1}
                }
                ])
            # for i in agg_result:
            # print(i)
            return agg_result
        if type == 'year':
            agg_result = col.aggregate([
                {
                    "$group": {
                        "_id": {"$year": "$Premiere"},
                        "numPelis": {"$sum": 1},
                    }
                },
                {
                    "$sort": {"numPelis": -1}
                }
            ])
            # for i in agg_result:
            #     print(i)
            return agg_result
        if type == 'one-id':
            records = col.find_one({'Id': data})
            # print(records)
            return records
        if type == 'one-title':
            records = col.find_one({'Title': data})
            # print(records)
            return records

    except Exception as e:
        print("Database not created and Failed to Connect")
    finally:
        print("Program executed successfully")


def modifyHandler(type, data, check=""):
    try:
        # Connecting to server
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = pymongo.MongoClient(CONNECTION_STRING)

        # Selecting db
        mydb = client['MoviesDB']

        # Selecting collection
        col = mydb['Movies']

        # print("Data = " + str(data))

        if (type == 'insert'):
            r = col.insert_one(data)
            return r
        if (type == 'update'):
            pass
        if (type == 'delete-id'):
            r = col.delete_many({'Id': data})
            if r.deleted_count > 0:
                return True
            else:
                return False
        if (type == 'delete-title'):
            r = col.delete_many({'Title': data})
            if r.deleted_count > 0:
                return True
            else:
                return False
        if(type == 'update-id'):
            r = col.update_many({'Id': check}, {'$set': data})
            return r
        if(type == 'update-title'):
            r = col.update_many({'Title': check}, {'$set': data})
            return r

    except Exception as e:
        print("Database not created and Failed to Connect" + e)
    finally:
        print("Program executed successfully")


def main():
    # Cleaning window
    for widget in root.winfo_children():
        widget.destroy()

    # Labels and buttons
    lbl_title = tk.Label(text="Main Menu", height=4, width=30)
    lbl_title.grid(column=2, row=1)

    btn_create = tk.Button(text="Create", height=2,
                           width=14, command=lambda: CGUI())
    btn_create.grid(column=2, row=2, pady=5, padx=40)

    btn_read = tk.Button(text="Read", height=2,
                         width=14, command=lambda: RGUI())
    btn_read.grid(column=2, row=3, pady=5, padx=40)

    btn_update = tk.Button(text="Update", height=2,
                           width=14, command=lambda: UGUI())
    btn_update.grid(column=2, row=4, pady=5, padx=40)

    btn_delete = tk.Button(text="Delete", height=2,
                           width=14, command=lambda: DGUI())
    btn_delete.grid(column=2, row=5, pady=5, padx=40)


def CGUI():
    # Cleaning window
    for widget in root.winfo_children():
        widget.destroy()

    # Labels and entries
    btn_back = tk.Button(text="<", height=1, width=1, command=lambda: main())
    btn_back.grid(column=0, row=0)

    lbl_title = tk.Label(text="Create new Movie", height=4, width=30)
    lbl_title.grid(column=0, row=1, columnspan=2)

    lbl_checker = tk.Label(text="∆")
    lbl_checker.grid(column=1, row=0, sticky="e")

    lbl_id = tk.Label(text="Id", height=2, width=10)
    lbl_id.grid(column=0, row=2, padx=10)
    ent_id = tk.Entry(width=3)
    ent_id.grid(column=1, row=2, padx=10, sticky="w")

    lbl_title = tk.Label(text="Title", height=2, width=10)
    lbl_title.grid(column=0, row=3, padx=10)
    ent_title = tk.Entry()
    ent_title.grid(column=1, row=3, padx=10, sticky="w")

    lbl_character = tk.Label(text="Character", height=2, width=10)
    lbl_character.grid(column=0, row=4)
    ent_character = tk.Entry()
    ent_character.grid(column=1, row=4, padx=10, sticky="w")

    lbl_premiere = tk.Label(text="Premiere", height=2, width=10)
    lbl_premiere.grid(column=0, row=5)
    ent_premiere = tk.Entry()
    ent_premiere.grid(column=1, row=5, padx=10, sticky="w")

    lbl_director = tk.Label(text="Director", height=2, width=10)
    lbl_director.grid(column=0, row=6)
    ent_director = tk.Entry()
    ent_director.grid(column=1, row=6, padx=10, sticky="w")

    # Create new Movie button
    btn_create = tk.Button(text="Create", command=lambda: [newMovie(), ent_id.delete(0, END), ent_title.delete(
        0, END), ent_character.delete(0, END), ent_premiere.delete(0, END), ent_director.delete(0, END)])
    btn_create.grid(column=0, row=7, columnspan=2)

    # New movie function, checker color updated
    def newMovie():
        d = datetime.datetime.strptime(
            ent_premiere.get(), "%Y-%m-%d")
        newDocument = {"Id": int(ent_id.get()), "Title": ent_title.get(
        ), "Character": ent_character.get(), "Premiere": d, "Director": ent_director.get()}

        if (modifyHandler("insert", newDocument)):
            lbl_checker.configure(fg="green")
        else:
            lbl_checker.configure(fg="red")


def RGUI():
    # Cleaning window
    for widget in root.winfo_children():
        widget.destroy()

    # Labels and buttons
    btn_back = tk.Button(text="<", height=1, width=1, command=lambda: main())
    btn_back.grid(column=0, row=0)

    lbl_title = tk.Label(text="Reading options", height=4, width=30)
    lbl_title.grid(column=0, row=1, columnspan=2)

    btn_detailed = tk.Button(text="Detailed View",
                             height=2, width=14, command=lambda: detailedView())
    btn_detailed.grid(column=0, row=2, pady=5, padx=40, columnspan=2)

    btn_year = tk.Button(text="Movies by Year", height=2,
                         width=14, command=lambda: yearView())
    btn_year.grid(column=0, row=3, pady=5, padx=40, columnspan=2)

    btn_director = tk.Button(text="Movies by Director",
                             height=2, width=14, command=lambda: directorView())
    btn_director.grid(column=0, row=4, pady=5, padx=40, columnspan=2)

    # Functions for each button/view
    def detailedView():
        # Clears possible listbox and scrollbar
        lista = []
        for widget in root.winfo_children():
            lista.append(widget)
        if(len(lista) > 5):
            lista[5].destroy()
            lista[6].destroy()
        # Creating a Listbox and
        # attaching it to root window
        listbox = Listbox(root, width=60, height=40)

        # Adding Listbox to the left
        # side of root window
        listbox.grid(row=2, column=2, rowspan=5)

        # Creating a Scrollbar and
        # attaching it to root window
        scrollbar = Scrollbar(root)

        # Adding Scrollbar to the right
        # side of root window
        scrollbar.grid(row=2, column=3, sticky="ns", rowspan=5)

        # Fetch results from DB
        results = searchHandler("all")

        # Insert elements into the listbox
        # for doc in results:
        #     item = f"'id': {doc['Id']}, \n'Title': {doc['Title']}, \n\n\n'Character': {doc['Character']}, \n'Premier': {doc['Premiere']}, \n'Director': {doc['Director']}"
        #     listbox.insert(END, item)
        for doc in results:
            data = [['Id', doc['Id']], ['Title', doc['Title']], ['Character', doc['Character']], [
                'Premiere', doc['Premiere']], ['Director', doc['Director']]]
            # print(data)
            listbox.insert(END, " {")

            for value in data:
                listbox.insert(END, f"{' '*5}'{value[0]}': '{value[1]}'")

            listbox.insert(END, " }")

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        listbox.config(yscrollcommand=scrollbar.set, font='TkFixedFont')

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        scrollbar.config(command=listbox.yview)

    def yearView():
        # Clears possible listbox and scrollbar
        lista = []
        for widget in root.winfo_children():
            lista.append(widget)
        if(len(lista) > 5):
            lista[5].destroy()
            lista[6].destroy()
        # Creating a Listbox and
        # attaching it to root window
        listbox = Listbox(root, width=60, height=40)

        # Adding Listbox to the left
        # side of root window
        listbox.grid(row=2, column=2, rowspan=10)

        # Creating a Scrollbar and
        # attaching it to root window
        scrollbar = Scrollbar(root)

        # Adding Scrollbar to the right
        # side of root window

        scrollbar.grid(row=2, column=3, sticky="ns", rowspan=10)

        # Fetch results from DB
        # Fetch results from DB
        results = searchHandler("year")

        # Insert elements into the listbox
        for doc in results:
            data = [['Premiere', doc['_id']], ['Peliculas', doc['numPelis']]]
            # print(data)
            listbox.insert(END, " {")

            for value in data:
                listbox.insert(END, f"{' '*5}'{value[0]}': '{value[1]}'")

            listbox.insert(END, " }")

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        listbox.config(yscrollcommand=scrollbar.set, font='TkFixedFont')

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        scrollbar.config(command=listbox.yview)

    def directorView():
        # Clears possible listbox and scrollbar
        lista = []
        for widget in root.winfo_children():
            lista.append(widget)
        if(len(lista) > 5):
            lista[5].destroy()
            lista[6].destroy()
        # Creating a Listbox and
        # attaching it to root window
        listbox = Listbox(root, width=60, height=40)

        # Adding Listbox to the left
        # side of root window
        listbox.grid(row=2, column=2, rowspan=5)

        # Creating a Scrollbar and
        # attaching it to root window
        scrollbar = Scrollbar(root)

        # Adding Scrollbar to the right
        # side of root window
        scrollbar.grid(row=2, column=3, sticky="ns", rowspan=5)

        # Fetch results from DB
        results = searchHandler("director")

        # Insert elements into the listbox
        for doc in results:
            data = [['Director', doc['_id']], ['Peliculas', doc['numPelis']]]
            # print(data)
            listbox.insert(END, " {")

            for value in data:
                listbox.insert(END, f"{' '*5}'{value[0]}': '{value[1]}'")

            listbox.insert(END, " }")

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        listbox.config(yscrollcommand=scrollbar.set, font='TkFixedFont')

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        scrollbar.config(command=listbox.yview)


def UGUI():
    # Cleaning window
    for widget in root.winfo_children():
        widget.destroy()

    # Labels entries and buttons
    btn_back = tk.Button(text="<", height=1, width=1, command=lambda: main())
    btn_back.grid(column=0, row=0)

    lbl_title = tk.Label(
        text="Update Movie\nFirst, select a movie to update", height=4, width=30)
    lbl_title.grid(column=0, row=1, columnspan=2)

    lbl_checker = tk.Label(text="∆")
    lbl_checker.grid(column=1, row=0, sticky="e")

    lbl_id = tk.Label(text="Id", height=2, width=10)
    lbl_id.grid(column=0, row=2, padx=10)
    ent_id = tk.Entry()
    ent_id.grid(column=1, row=2, padx=10, sticky="w")

    btn_create = tk.Button(text="Select by Id",
                           command=lambda: verify("Id"))
    btn_create.grid(column=0, row=3, columnspan=2)

    lbl_title = tk.Label(text="Title", height=2, width=10)
    lbl_title.grid(column=0, row=4, padx=10)
    ent_title = tk.Entry()
    ent_title.grid(column=1, row=4, padx=10, sticky="w")

    btn_create = tk.Button(text="Select by Title",
                           command=lambda: verify("Title"))
    btn_create.grid(column=0, row=5, columnspan=2)

    # verify function, searches for row with Id or Title
    # runs update function if exists
    # else clears entries and updates checker color
    def verify(type):
        if type == "Title":
            search = searchHandler('one-title', ent_title.get())
            if (len(search) > 0):
                lbl_checker.configure(fg="green")
                update(search, type, ent_title.get())
            else:
                ent_title.delete(0, END)
                lbl_checker.configure(fg="red")
        if type == "Id":
            search = searchHandler('one-id', int(ent_id.get()))
            if (len(search) > 0):
                lbl_checker.configure(fg="green")
                update(search, type, int(ent_id.get()))
            else:
                ent_id.delete(0, END)
                lbl_checker.configure(fg="red")

    # Creates new window
    def update(search, type, check):
        # Cleaning window
        for widget in root.winfo_children():
            widget.destroy()

        # Labels and entries
        btn_back = tk.Button(text="<", height=1, width=1,
                             command=lambda: UGUI())
        btn_back.grid(column=0, row=0)
        lbl_title = tk.Label(text="Updating Movie", height=4, width=30)
        lbl_title.grid(column=0, row=1, columnspan=2)

        lbl_checker = tk.Label(text="∆")
        lbl_checker.grid(column=1, row=0, sticky="e")

        lbl_id = tk.Label(text="Id", height=2, width=10)
        lbl_id.grid(column=0, row=2, padx=10)
        lbl_idHolder = tk.Label(text=search['Id'], height=2)
        lbl_idHolder.grid(column=1, row=2, padx=10, sticky="w")

        lbl_title = tk.Label(text="Title", height=2, width=10)
        lbl_title.grid(column=0, row=3, padx=10)
        ent_title = tk.Entry()
        ent_title.insert(END, search['Title'])
        ent_title.grid(column=1, row=3, padx=10, sticky="w")

        lbl_character = tk.Label(text="Character", height=2, width=10)
        lbl_character.grid(column=0, row=4)
        ent_character = tk.Entry()
        ent_character.insert(END, search['Character'])
        ent_character.grid(column=1, row=4, padx=10, sticky="w")

        lbl_premiere = tk.Label(text="Premiere", height=2, width=10)
        lbl_premiere.grid(column=0, row=5)
        ent_premiere = tk.Entry()
        ent_premiere.insert(END, str(search['Premiere'])[:10])
        ent_premiere.grid(column=1, row=5, padx=10, sticky="w")

        lbl_director = tk.Label(text="Director", height=2, width=10)
        lbl_director.grid(column=0, row=6)
        ent_director = tk.Entry()
        ent_director.insert(END, search['Director'])
        ent_director.grid(column=1, row=6, padx=10, sticky="w")

        # Update button, throws updateMovie function
        btn_update = tk.Button(text="Update", command=lambda: updateMovie())
        btn_update.grid(column=0, row=7, columnspan=2)

        # Movie exists, so no further check is necessary
        # Updates row(s) and updates checker color if error is found
        # Else goes back to Update view
        def updateMovie():
            d = datetime.datetime.strptime(ent_premiere.get(), "%Y-%m-%d")
            newDocument = {"Id": search['Id'], "Title": ent_title.get(
            ), "Character": ent_character.get(), "Premiere": d, "Director": ent_director.get()}
            if (type == "Title"):
                if (modifyHandler("update-title", newDocument, check)):
                    UGUI()
                else:
                    lbl_checker.configure(fg="red")
            if (type == "Id"):
                if (modifyHandler("update-id", newDocument, check)):
                    UGUI()
                else:
                    lbl_checker.configure(fg="red")


def DGUI():
    # Cleaning window
    for widget in root.winfo_children():
        widget.destroy()

    # Labels entries and buttons
    btn_back = tk.Button(text="<", height=1, width=1,
                         command=lambda: main())
    btn_back.grid(column=0, row=0)

    lbl_title = tk.Label(text="Delete Movie", height=4, width=30)
    lbl_title.grid(column=0, row=1, columnspan=2)

    lbl_checker = tk.Label(text="∆")
    lbl_checker.grid(column=1, row=0, sticky="e")

    lbl_id = tk.Label(text="Id", height=2, width=10)
    lbl_id.grid(column=0, row=2, padx=10)
    ent_id = tk.Entry()
    ent_id.grid(column=1, row=2, padx=10, sticky="w")

    btn_delId = tk.Button(text="Delete by Id", command=lambda: [
        deleteMovie("Id"), ent_id.delete(0, END)])
    btn_delId.grid(column=0, row=3, columnspan=2)

    lbl_title = tk.Label(text="Title", height=2, width=10)
    lbl_title.grid(column=0, row=4, padx=10)
    ent_title = tk.Entry()
    ent_title.grid(column=1, row=4, padx=10, sticky="w")

    # Delete button throws deleteMovie function and clears entries
    btn_delTitle = tk.Button(text="Delete by Title", command=lambda: [
        deleteMovie("Title"), ent_title.delete(0, END)])
    btn_delTitle.grid(column=0, row=5, columnspan=2)

    # Executes req and updates checker color
    def deleteMovie(type):
        if type == "Title":
            if (modifyHandler('delete-title', ent_title.get())):
                lbl_checker.configure(fg="green")
            else:
                lbl_checker.configure(fg="red")
        if type == "Id":
            if (modifyHandler('delete-id', int(ent_id.get()))):
                lbl_checker.configure(fg="green")
            else:
                lbl_checker.configure(fg="red")


if __name__ == '__main__':
    root = tk.Tk(className='Sqlite CRUD')
    main()
    root.mainloop()
