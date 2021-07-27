from imports import *
from others import create_frame, configure, destroy
import global_vars
"""
The user enters one or more keywords to narrow down the results (when looking for a specific record).

Input: 
- filter_col: True if we're searching for the purpose of filtering out collections, not records. False otherwise.
- *widgets: 0 or more widgets to be destroyed (cleared before displaying new widgets)

Calls: search_with_input(), view_log(), filter_col_by_keyword(), view_which_log()
"""
def search_keywords(filter_col, *widgets):
    from view import view_which_log, view_log

    destroy(*widgets)
    frame1 = create_frame(0,1)

    search_label = Label(frame1, text="What would you like to search for?")
    search_label.grid(row=0, column=1, padx=10, pady=10)

    search_entry = Entry(frame1)
    search_entry.grid(row=1, column=1, padx=10, pady=10)

    if filter_col == False:
        submit = Button(frame1, text = "Submit", 
        command = lambda: search_with_input(search_entry.get(), search_label, search_entry, submit, view_all, frame1))
        submit.grid(row=2, column=1, padx=10, pady=10)

        view_all = Button(frame1, text = "View all instead", 
        command = lambda: view_log(False, None, search_label, search_entry, submit, view_all, frame1))
        view_all.grid(row=3, column=1, padx=10, pady=10)

    else: # if filter_col is true
        submit = Button(frame1, text = "Submit", 
        command = lambda: filter_col_by_keyword(search_entry.get(), search_label, search_entry, submit, frame1, back))
        submit.grid(row=2, column=1, padx=10, pady=10)

        back = Button(frame1, text = "Go back", command = lambda: view_which_log(None, search_label, 
            search_entry, submit, frame1, back))
        back.grid(row=3, column=1, padx=10, pady=10)

    configure(3,1)

"""
Adds wildcards (*) and allows for case-insensitive searches.

Input:
- entry: keyword used for searching
- *widgets

Calls: view_which_log()
"""
def search_with_input(entry, *widgets):

    # if the user did not enter anything
    if len(entry.strip()) == 0:
        messagebox.showerror("Searching", "Please type something in the given space.")
        return

    from view import view_log
    destroy(*widgets)

    # wildcards are used in between the entry
    keyword = '.*' + entry + '.*'
       
    # search is false since it has "already been searched"
    view_log(False, keyword)

def filter_col_by_keyword(keyword, *widgets):

    from view import view_which_log

    # if the user did not enter anything
    if len(keyword.strip()) == 0:
        messagebox.showerror("Searching", "Please type something in the given space.")
        return

    collection_list = list(global_vars.db.list_collection_names())
    filtered_list = []

    for collection in collection_list:
        global_vars.vol = global_vars.db[collection]
        document_num = global_vars.vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}})

        if document_num != 0: # if a keyword can be found in a certain collection
            filtered_list.append(collection)

    if len(filtered_list) !=0:
        destroy(*widgets)
        view_which_log(filtered_list)
    else: # even after searching, no collections have been returned (no collections contain that keyword)
        messagebox.showerror("No Collections", "No collections have been returned. Try searching something else.")
        return


