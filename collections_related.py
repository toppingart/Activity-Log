import global_vars
from imports import *
from others import create_frame, configure, destroy

"""
Now that a collection has been selected, the user will access that collection and continue with the menu options.

Input:
- collection_name (str)
- *widgets

Calls: menu()
"""
def access_collection(collection_name, *widgets):
    from menu_screen import menu

    destroy(*widgets)
    menu(collection_name) # goes to the menu


"""
Called if the user wants to create a new collection.

Input: 
- *widgets

Calls: adds_new_collection(), view_which_log()
"""
def create_new_collection(*widgets): 
    from view import view_which_log
   
    frame1 = create_frame(0,1)
    destroy(*widgets)

    new_col = Label(global_vars.root, text = "What would you like the new collection to be called?", 
        font="Helvetica 14 bold")
    new_col.place(x=100, y=100)

    # entry box
    new_col_entry = Entry(global_vars.root)
    new_col_entry.place(x=100, y=200)

    submit = Button(global_vars.root, text = "Submit", 
        command = lambda: adds_new_collection(new_col_entry.get(), new_col, new_col_entry, submit, 
            frame1, go_back_button))
    submit.place(x=200, y=300)

    go_back_button = Button(global_vars.root, text = "Go back", 
        command = lambda: view_which_log(None, frame1, new_col, new_col_entry, submit, go_back_button))
    go_back_button.place(x=100, y=300)

    configure(3, 1)

"""
Adds the new collection.

Input:
- new_name: name of the new collection (str)
- *widgets

Calls: view_which_log()
"""
def adds_new_collection(new_name, *widgets):
    from view import view_which_log

    if new_name in global_vars.db.list_collection_names():
        messagebox.showerror("Collection Name", "This name already exists.")
        return

    # if the new collection name is not empty
    if len(new_name.strip()) != 0:
        frame = create_frame(1,1)
        destroy(*widgets)

        success_message = Label(global_vars.root, text="A new collection has been added!", font="Helvetica 14 bold")
        success_message.place(x=100, y=100)

        col = global_vars.db[new_name]

        # a collection only appears if there is at least one document
        col.insert_one({"New": "new"})
        col.delete_one({"New": "new"})

        ok_button = Button(global_vars.root, text = "OK", 
            command = lambda: view_which_log(None, success_message, ok_button, frame))
        ok_button.place(x=100, y=200)

    else: # the new collection is empty
        messagebox.showerror("Collection Name", "Please enter a collection name.")
        return

def delete_collection(collection, *widgets):
    from view import view_which_log

    answer = messagebox.askyesno('Delete Collection', 'Are you sure you want to delete this collection?')
    if answer == True:
        collection.drop()
        view_which_log(None, *widgets) # user is prompted to select another collection
