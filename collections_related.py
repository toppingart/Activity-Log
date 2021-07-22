from interface2 import *
import others
import global_vars
from imports import *

"""
Now that a collection has been selected, the user will access that collection and continue with the menu options.

Input:
- list of buttons to be destroyed
- collection_name
- *widgets

Output: None
Calls: menu()
"""
def access_collection(collection_name, *widgets):
    destroy(*widgets)
    menu(collection_name)


"""
Called if the user wants to create a new collection.

Input: 
-list of buttons from "previous screen"
- *widgets

Output: None
Calls: adds_new_collection()
"""
def create_new_collection(*widgets): 
    from view import view_which_log


    frame1 = others.create_frame(0,1)
    destroy(*widgets)
    new_col = Label(global_vars.root, text = "What would you like the new collection to be called?", font="Helvetica 14 bold")
    new_col.place(x=100, y=100)

    new_col_entry = Entry(global_vars.root)
    new_col_entry.place(x=100, y=200)

    submit = Button(global_vars.root, text = "Submit", 
        command = lambda: adds_new_collection(new_col_entry.get(), new_col, new_col_entry, submit, frame1, go_back_button))
    submit.place(x=200, y=300)

    go_back_button = Button(global_vars.root, text = "Go back", 
        command = lambda: view_which_log(None, frame1, new_col, new_col_entry, submit, go_back_button))
    go_back_button.place(x=100, y=300)

    others.configure(3, 1)

"""
Adds the new collection.

Input:
- new_name: name of the new collection
_ *widgets

Output: None
Calls: view_which_log()

"""
def adds_new_collection(new_name, *widgets):



    if len(new_name.strip()) != 0:
        frame1 = others.create_frame(1,1)
        destroy(*widgets)
        success_message = Label(global_vars.root, text="A new collection has been added!", font="Helvetica 14 bold")
        success_message.place(x=100, y=100)

        col = global_vars.db[new_name]

        # a collection only appears if there is at least one document
        col.insert_one({"New": "new"})
        col.delete_one({"New": "new"})

        ok_button = Button(global_vars.root, text = "OK", command = lambda: view_which_log(None, None, success_message, ok_button, frame1))
        #ok_button.grid(row=2, column=1, padx=10, pady=10)
        ok_button.place(x=100, y=200)
    else:
        messagebox.showerror("Collection Name", "Please enter a collection name.")
        return

def delete_collection(collection, *widgets):
    answer = messagebox.askyesno('Delete Collection', 'Are you sure you want to delete this collection?')
    if answer == True:
        collection.drop()
        view_which_log(None, None, *widgets)
