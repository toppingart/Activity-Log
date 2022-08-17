from imports import *
import global_vars
import os
from others import destroy, create_frame



def options(*widgets):
    destroy(*widgets)

    frame1 = create_frame(0,1)

    options_label = Label(frame1, text="OPTIONS", font="Helvetica 18 bold")
    options_label.grid(row=0,column=1,padx=50,pady=10)    

    create_backup = Button(frame1, text = "Create backups of the collections", 
        command = lambda: ask_for_path("create", options_label, create_backup, restore_backup, frame1))
    create_backup.grid(row=1, column=1, padx = 50, pady=10)

    restore_backup = Button(frame1, text = "Restore backups of the collections", 
        command = lambda: ask_for_path("restore", options_label, create_backup, restore_backup, frame1))
    restore_backup.grid(row=2, column=1, padx = 50, pady=10)


def ask_for_path(selected_option, *widgets):
    from view import view_which_log

    destroy(*widgets)
    file_path = filedialog.askdirectory(title="Choose where you want to put these backups")
    if selected_option == "create":
        dump(file_path)
        view_which_log(None)
    else:
        restore(file_path)
        view_which_log(None)


# conn - client, db_name = db, collections - use list collection names
# https://gist.github.com/Lh4cKg/939ce683e2876b314a205b3f8c6e8e9d
def dump(path):

    collections_list = global_vars.db.list_collection_names()
    for collection in collections_list:
        with open(os.path.join(path, f'{collection}.bson'), 'wb+') as f:
            for doc in global_vars.db[collection].find():
                f.write(bson.BSON.encode(doc))


def restore(path):
    collections_list = global_vars.db.list_collection_names()
    for collection in os.listdir(path):
        collection_name = collection.split('.')[0]
        if collection.endswith('.bson') and collection_name not in collections_list:
            print(collection)
            with open(os.path.join(path, collection), 'rb+') as f:
                global_vars.db[collection_name].insert_many(bson.decode_all(f.read()))
      

#dump(path)

