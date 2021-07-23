import global_vars
from imports import *
from others import *
from view import *
from add import *


"""
Displays the menu where there are two buttons for the user to select from:
1. The user can add a new log record (they have a new experience/activity to add)
2. The user can view their current log (the records that they have at the moment)

Input: 
- collection (which would be the name of the collection if the menu is accessed for the first time, otherwise this is vol)
- *widgets

Output: None
Calls: add_details() or view_log() or view_which_log()
"""
def menu(collection, *widgets):
    from collections_related import delete_collection

    destroy(*widgets)

    global string_collection
    #global vol
    if isinstance(collection, str):
        global_vars.vol = global_vars.db[collection]
        string_collection = collection
    else:
        global_vars.vol = collection

    db_label = Label(global_vars.root, text="Collection Name: " + string_collection, font="Helvetica 18 bold")
    db_label.place(x=global_vars.root.winfo_width()/3 - 10, y=0)


    frame1 = create_frame(0,1)
    
    global menu_label, add_record_1, view_act_log
    menu_label = Label(frame1, text="MENU", font="Helvetica 18 bold")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(frame1, text = "Add a new log record",
        command=lambda: add_details(False, None, None, menu_label, add_record_1, view_act_log, frame1, db_label))
    add_record_1.grid(row=1, column=1, padx = 50, pady=10)

    view_act_log = Button(frame1, text = "View activity log", 
        command = lambda: view_log(False,None, menu_label, add_record_1, view_act_log, frame1, db_label))
    view_act_log.grid(row=2, column=1, padx = 50, pady=10)

    another_collection_button = Button(frame1, text = "Choose another collection",
     command = lambda: view_which_log(None, menu_label, add_record_1, view_act_log, frame1, another_collection_button, db_label))
    another_collection_button.grid(row=3, column=1, padx=50, pady=10)

    delete_collection_button = Button(frame1, text = "Delete this collection", 
        command = lambda: delete_collection(menu_label, add_record_1, view_act_log, frame1, 
            another_collection_button, delete_collection_button, db_label))
    delete_collection_button.grid(row=4, column=1, padx=50, pady=10)

    configure(4, 1)