from pymongo import MongoClient
from tkinter import messagebox, ttk
from tkinter import *
from datetime import datetime, date
import sys
from tkinter.font import BOLD
from PIL import Image, ImageTk

"""
The user enters one or more keywords to narrow down the results (when looking for a specific record).

Input: 
- vol: allows us to access the contents of the collection
- filter_col: True if we're searching for the purpose of filtering out collections, not records. False otherwise.
- *widgets: 0 or more widgets to be destroyed (cleared before displaying new widgets)
"""
def search_keywords(vol, filter_col, *widgets):

    destroy(*widgets)
    widget_list = []

    frame1 = create_frame(0,1)
    widget_list.append(frame1)

    search_label = Label(frame1, text="What would you like to search for?")
    search_label.grid(row=0, column=1, padx=10, pady=10)
    widget_list.append(search_label)

    search_entry = Entry(frame1)
    search_entry.grid(row=1, column=1, padx=10, pady=10)
    widget_list.append(search_entry)

    if filter_col == False:
        submit = Button(frame1, text = "Submit", 
        command = lambda: search_with_input(vol, search_entry.get(), widget_list))
        submit.grid(row=2, column=1, padx=10, pady=10)
        widget_list.append(submit)

        view_all = Button(frame1, text = "View all instead", 
        command = lambda: view_log(vol, False, None, search_label, search_entry, submit, view_all, frame1))
        view_all.grid(row=3, column=1, padx=10, pady=10)
        widget_list.append(view_all)

    else: # if filter_col is true
        submit = Button(frame1, text = "Submit", 
        command = lambda: filter_col_by_keyword(vol, search_entry.get(), search_label, search_entry, submit, frame1, back))
        submit.grid(row=2, column=1, padx=10, pady=10)

        back = Button(frame1, text = "Go back", command = lambda: view_which_log(None, search_label, 
            search_entry, submit, frame1, back))
        back.grid(row=3, column=1, padx=10, pady=10)

    configure(3,1)

"""
Adds wildcards (*) and allows for case-insensitive searches.

Input:
- vol
- entry: keyword used for searching
- *widgets

Output: None
Calls: view_log()
"""
def search_with_input(vol, entry, *widgets):

    print(*widgets)
    destroy(*widgets)


    # wildcards are used in between the entry
    keyword = '.*' + entry + '.*'
   
    # case insensitive is allowed
    results = vol.find({'details': {'$regex': keyword, '$options': 'i'}})
    
    # search is false since it has "already been searched"
    view_log(vol, False, keyword, *widgets)

"""
Used to change the date (as a string) to a datetime object.

Input: 
- vol
- the results (dictionaries in a list)
Output: None
"""
def to_datetime(vol, results):

    for result in results:
        date = result['date']
        if isinstance(date,str) and len(date.strip()) == 8:
            #12/02/20
            datetime_obj = datetime.strptime(date, "%m/%d/%y")
            vol.update_one({'_id': result['_id']}, {'$set': {'date': datetime_obj}})

        elif isinstance(date,str) and len(date.strip()) == 19:
            # 12/01/20 - 12/02/20
            start_date = result['date'][:8]
            end_date = result['date'][11:]
            start_datetime = datetime.strptime(start_date, "%m/%d/%y")
            end_datetime = datetime.strptime(end_date, "%m/%d/%y")
            vol.update_one({'_id': result['_id']}, {'$set': {'startdate': start_datetime}})
            vol.update_one({'_id': result['_id']}, {'$set': {'enddate': end_datetime}})

"""
The user enters some details about their experience, and any additional notes about that experience.

Input: 
- vol
- edited: True if the user is editing this entry. False if it is a new entry
- details: None if it's a new entry. Otherwise, it contains the information about the edited entry 
(eg. {'_id': ObjectId('60b4418688db9bce7b378c09'), 'date': datetime.datetime(2020, 12, 27, 0, 0), 'details': 'aa\n', 'hours': '1'})
- *widgets

Output: None
Calls: add_hours() or types_of_changes()
"""

def add_details(vol, edited, details, keyword, *widgets):

    destroy(*widgets)
    frame1 = create_frame(0,0)
    frame2 = create_frame(0,1)
    frame3 = create_frame(1,1)

    details_text = Label(frame2, text="Give some details about the experience.")
    details_text.grid(row=0,column=0,padx=30,pady=10)   
    details_entry = Text(frame2, width=30, height=10)
    details_entry.grid(row=1, column=0)

    others_text = Label(frame2, text="Any additional notes? [OPTIONAL]")
    others_text.grid(row=0,column=1,padx=50,pady=10)   
    others_entry = Text(frame2, width=30, height=10)
    others_entry.grid(row=1, column=1)

    configure(3, 1)

    if not edited:
        go_back_button = Button(root, text = "Go back", 
            command = lambda: menu(vol, details_text, details_entry, submit_button, frame1, frame2, frame3, go_back_button))
        go_back_button.place(x=250, y=350)

        if isinstance(details, list):
            details_entry.insert(INSERT, details[0])
            others_entry.insert(INSERT, details[1])

        submit_button = Button(root, text = "Submit All", 
           command = lambda: add_hours(vol, details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), None, False, 
            details_text, details_entry, submit_button, frame1, frame2, frame3, go_back_button))
        submit_button.place(x=350, y=350)

    else: # if the user is making edits to their entry

        go_back_button = Button(root, text = "Go back", 
            command = lambda: ask_entry_changes(vol, details, keyword, go_back_button, details_text, details_entry, submit_button, frame1, frame2, frame3))
        go_back_button.place(x=300, y=350)

        details_entry.insert(INSERT, details['details'])
        others_entry.insert(INSERT, details['others'])


        submit_button = Button(root, text = "Submit All", 
            command = lambda: types_of_changes(1, details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), vol, details, details_text, details_entry, submit_button, go_back_button, frame1, frame2, frame3))
        submit_button.place(x=400, y=350)

"""
The widgets are destroyed so that the other widgets can be placed on the screen.

Input: Any number of widgets (*args) which will be in a list (input can be a single widget or a list of widgets)
Output: None
"""
def destroy(*widgets):
    for item in widgets:

        if isinstance(item, list):

            for i in item[0]:
                i.destroy()
            continue
        item.destroy()

"""
The user is asked to enter the number of hours of their experience (how long did their volunteering/activity take?)

Input: 
- vol
- details: details of the experience (as a string)
- others: additional notes about that experience
- edited
- *widgets (NOTE: all the widgets are from the add_details())

Output: None
Calls: add_dates() or types_of_changes()
"""
def add_hours(vol, details, others, input_hours, edited, *widgets):

    # error handling
    if isinstance(details, str) and len(details.strip()) == 0:
        messagebox.showerror("Details Error", "Please enter some details.")
        return

    destroy(*widgets)
    frame1 = LabelFrame(root)
    frame1.grid(row=0, column=1, padx=10, pady=10)

    hours_text = Label(frame1, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(frame1)
    hours_entry.grid(row=1, column=1,padx=50,pady=50)

    if edited == False:

        user_input_list = [details, others] # obtained from add_details()

        if input_hours != None:
            hours_entry.insert(INSERT, input_hours)

        submit_button = Button(root, text = "Submit", 
            command = lambda: add_dates(vol, user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button, frame1, go_back_button))

        # add_details(vol, edited, details, keyword, *widgets)
        go_back_button = Button(root, text="Go back", command = lambda: add_details(vol, False, user_input_list, None, hours_text,hours_entry,
            submit_button, frame1, go_back_button))

    else: # happens if the user wants to make edits to their entry (not a new entry)
        hours_entry.insert(INSERT, details['hours'])
        submit_button = Button(root, text = "Submit",
            command = lambda: types_of_changes(2, hours_entry.get(), None, vol, details, hours_text, hours_entry, submit_button, frame1, go_back_button))


        go_back_button = Button(root, text="Go back", command = lambda: ask_entry_changes(vol, details, None, hours_text,hours_entry,
            submit_button, frame1, go_back_button))

    submit_button.place(x=380, y=300)
    go_back_button.place(x=280, y=300)

    configure(2, 1)

"""
Will take the appropiate action depending on what part ot the entry the user wants to make edits to

input:
- type_of_change:  details - 1, hours-2, date - 3, dates (start and end date) - 4 (int)
- edited_entry: edits made by the user (str)
- edited_entry_2: another edited entry (used for the additional notes)
- vol
- result: (eg. {'_id': ObjectId('60b4418688db9bce7b378c09'), 'date': datetime.datetime(2020, 12, 27, 0, 0), 'details': 'aa\n', 'hours': '1'})
- *widgets

Output: None
Calls: successful_message(), check_date(), to_datetime()
"""
def types_of_changes(type_of_change, edited_entry, edited_entry_2, vol, result, *widgets):

    destroy(*widgets)
    
    if type_of_change == 1:
        vol.update_one({'_id': result['_id']}, {'$set': {'details': edited_entry}})
        vol.update_one({'_id': result['_id']}, {'$set': {'others': edited_entry_2}})
        successful_message(vol, None, 2)
    elif type_of_change == 2:
        vol.update_one({'_id': result['_id']}, {'$set': {'hours': edited_entry}})
        successful_message(vol, None, 2)
    elif type_of_change == 3:
        check_date(edited_entry)
        vol.update_one({'_id': result['_id']}, {'$set': {'date': edited_entry}})
        to_datetime(vol, [result])
        successful_message(vol, None, 2)
    else:
        check_date(edited_entry[0])
        check_date(edited_entry[1])
        datetime_start = datetime.strptime(edited_entry[0], "%m/%d/%y")
        datetime_end = datetime.strptime(edited_entry[1], "%m/%d/%y")
        vol.update_one({'_id': result['_id']}, {'$set': {'startdate': datetime_start, 'enddate': datetime_end}})

"""
There are two purposes:
1. Checks if the hours that the user has entered is valid (is an integer), otherwise the user will 
be asked to enter their hours again.

2. If the hours that the user has entered is valid, then the user will be asked to select if their experience/activity
spans over a day or multiple days by clicking one of the buttons.

Input: 
- vol
- user_list: a list of the user's inputs so far (which in this case, would be the details and the hours)
- hours: the user's input - ideally as an int, but will be checked if it is an integer
- *widgets

Output: None
Calls: one_day_option() or multiple_days_option()
"""
def add_dates(vol, user_list, hours,*widgets):

    try:
        int(hours) # checks if an integer has been entered 
    except:
        messagebox.showerror("Hours Error", "Please enter a number for your hours.")
        return # exits the function (so that the user can enter the number of hours again)

    destroy(*widgets)

    if isinstance(user_list, list):
        user_list.append(int(hours)) # if hours is an int (is valid), it is added to the list of user inputs

    frame1 = create_frame(0,1)
  
    dates_text = Label(frame1, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    one_day_button = Button(frame1, text = "One day", 
        command = lambda: one_day_option(vol, user_list, False, dates_text, one_day_button, m_days_button, frame1,
            go_back_button))
    one_day_button.grid(row=1, column=1, padx=50,pady=10)

    m_days_button = Button(frame1, text = "Multiple days", 
        command = lambda: multiple_days_option(vol, user_list, False, dates_text, one_day_button, m_days_button, frame1,
            go_back_button))
    m_days_button.grid(row=2, column=1, padx=50, pady=10)

    go_back_button = Button(root, text="Go back", command = lambda: add_hours(vol, user_list[0], user_list[1], hours, False, 
        dates_text, one_day_button, m_days_button, frame1, go_back_button))
    go_back_button.place(x=330, y=300)

    configure(3, 1)


def configure(row, column):

    if row != None:
        for row_num in range(0, row+1):
            Grid.rowconfigure(root, index=row_num, weight=1)

    if column != None:
        for col_num in range(0,column+1):
            Grid.columnconfigure(root, index=col_num, weight=1)


def create_frame(row_num, col_num):
    frame1 = LabelFrame(root, padx=10, pady=10)
    frame1.grid(row=row_num, column=col_num)
    return frame1

"""
There are two purposes.
1. Destroys the widgets from add_dates()
2. Allows the user to enter the day that the experience/activity took place on (as a string)

Input: 
- vol
- user_list: a list of the user's inputs so far (in this case, the details, the additional notes, and hours). It will not be used in the function
itself, but will be used in the all_user_inputs()
- edited: True or False
- Any number of widgets to be destroyed

Output: None
Calls: all_user_inputs() or types_of_changes()
"""
def one_day_option(vol, user_list, edited, *widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    configure(2, 1)

    day_text = Label(frame1, text = "What day did this take place (eg. 12/25/20) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(frame1) # textbox
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    if not edited:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(vol, user_list, day_text, day_entry, submit_button, frame1, go_back_button, date = day_entry.get()))
        submit_button.grid(row=2, column=1, padx=50,pady=10)

        go_back_button = Button(root, text = "Go back", 
        command = lambda: add_dates(vol, user_list, user_list[2], day_text, day_entry, submit_button, frame1, go_back_button))
    else:

        day_entry.insert(INSERT, user_list['date'].strftime('%m/%d/%y'))
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(3, day_entry.get(), None, vol, user_list, day_text, day_entry, submit_button, frame1, go_back_button))
        submit_button.grid(row=2, column=1, padx=50,pady=10)

        go_back_button = Button(root, text="Go back", command = lambda: ask_entry_changes(vol, user_list, None, day_text, day_entry,
            submit_button, frame1, go_back_button))

    go_back_button.place(x=330, y=300)


"""
There are two purposes.
1. Destroys the widgets from add_dates()
2. Allows the user to enter the start date and the end date that the experience/activity took place on (as a string)

Input: 
- vol
- user_list: a list of the user's inputs so far (in this case, the details and hours). It will not be used in the function
itself, but will be used in the all_user_inputs()
- edited: True or False
- Any number of widgets to be destroyed

Output: None
Calls: all_user_inputs() or types_of_changes()
"""
def multiple_days_option(vol, user_list, edited, *widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    configure(5,1)

    days_text = Label(frame1, text = "What days did this take place (eg. 12/25/20 - 01/01/21)" )
    days_text.grid(row=0,column=1,padx=50,pady=10)

    start_day_text = Label(frame1, text = "Start date:")
    start_day_text.grid(row=1,column=1, padx=50, pady=10)

    start_day_entry = Entry(frame1)
    start_day_entry.grid(row=2,column=1,padx=50,pady=10)

    end_day_text = Label(frame1, text = "End date:")
    end_day_text.grid(row=3, column=1, padx=50, pady=10)

    end_day_entry = Entry(frame1)
    end_day_entry.grid(row=4, column=1, padx=50, pady=10)

    if not edited:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(vol, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1, go_back_button,
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))
        submit_button.grid(row=5, column=1, padx=50,pady=10)

        go_back_button = Button(root, text = "Go back", 
        command = lambda: add_dates(vol, user_list, user_list[2], start_day_entry, end_day_entry, submit_button, frame1, go_back_button))
        

    else:
        start_day_entry.insert(INSERT, user_list['startdate'].strftime('%m/%d/%y'))
        end_day_entry.insert(INSERT, user_list['enddate'].strftime('%m/%d/%y'))
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(4, [start_day_entry.get(), end_day_entry.get()], None, vol, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1, go_back_button))
        submit_button.grid(row=5, column=1, padx=50,pady=10)

        go_back_button = Button(root, text="Go back", command = lambda: ask_entry_changes(vol, user_list, None, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1, go_back_button))

    go_back_button.place(x=335, y=350)

"""
Checks if the date entered by the user is a valid date (valid day, month, and year).

Input: the date (as a string)
Output: None
"""
def check_date(date):
    if len(date.strip()) == 8:
        check_date = datetime.strptime(date, "%m/%d/%y") 
    else:
        raise ValueError

"""
There are two purposes.
1. Informs the user that the experience/activity record has been successfully added to the database. 
2. The user is then presented with two buttons: one that exits the program and the other takes them back to the menu screen.

Input: 
- vol
- The user list that contains the details, additional notes, hour(s), and date(s) 
(note that all have been checked to be valid already)
- type_of_success: 1 if it's a new entry being added successful, 2 if it's an entry being successfully edited
- Any number of widgets to be destroyed (these widgets are either from one_day_option() or multiple_days_option())
Output: None
Calls: to_datetime() and menu()

NOTE: [details, additional notes (others), hours, date(s)]
"""
def successful_message(vol, user_list, type_of_success, *widgets):

    try:
        destroy(*widgets)
        frame1 = create_frame(0,1)
        frame2 = create_frame(1,1)

        if type_of_success == 1: # new entry
            if len(user_list) == 4: # one date 
                vol_record = {"date": user_list[3], "details": user_list[0], "hours": user_list[2], "others": user_list[1] }
            else:
                vol_record = {"date": user_list[3] + " - " + user_list[4], "details": user_list[0], "hours": user_list[2], "others": user_list[1]}

            vol.insert_one(vol_record)
            to_datetime(vol, [vol_record])

            success_message = Label(frame1, text = "The record has been successfully added to the database!")
            success_message.grid(row=0, column=1)

        else: # edited entry
            success_message = Label(frame1, text = "The record has been successfully edited!")
            success_message.grid(row=0, column=1)


        # go back to menu option
        back_to_menu_button = Button(root, text = "Back to menu", 
        command = lambda: menu(vol, success_message, exit_button, back_to_menu_button, frame1, frame2))
       # back_to_menu_button.grid(row=1, column=1, padx=10, pady=10)
        back_to_menu_button.place(x=300, y=250)

        # exit option
        exit_button= Button(root, text = "Exit", command = lambda: sys.exit()) # if pressed, exits the program
        exit_button.place(x=400, y=250)

        configure(2,1)

    except Exception as e:
        print(e)

"""
There are two purposes.
1. If the date(s) are valid (which will be checked in this function), the date(s) will be added to the user_list 
(that contains the details and the hours)

2. Once the date is determined to be valid, the record is added to the database (using successful_message())

NOTE: the details and the hours are valid (as they have been checked before)

Calls: check_date() and successful_message()

"""
def all_user_inputs(vol, user_list, *widgets, **days):

    try:
        # add date(s)
        for key, value in days.items():
            if key == "date": # one date
                check_date(value)
                user_list.append(value)
                break # done checking, break out of for loop
            else: 
                check_date(days["startdate"])
                check_date(days["enddate"])

                if (datetime.strptime(day['startdate'], "%m/%d/%y") >= (datetime.strptime(day['enddate']))):
                    raise ValueError

                #['ad\n', '\n', 5]
                if len(user_list) == 3: # already contains the details, others, hours
                    user_list.append(days["startdate"]) # if statement prevents startdate from being added again



                if len(user_list) == 4: # already contains details, others, hours, and startdate
                    user_list.append(days["enddate"]) # if statement prevents enddate from being added again
                break

    except NameError as n:
        messagebox.showerror("Dates Error", "Please enter valid date(s)")

    except ValueError as v:
        messagebox.showerror("Dates Error", "Please enter valid date(s)")

    except Exception as e:
        messagebox.showerror("Dates Error", "Please fill in both the start date and end date.")

    else:
        successful_message(vol, user_list, 1, *widgets)

"""
Called if the user wants to create a new collection.

Input: 
-list of buttons from "previous screen"
- *widgets

Output: None
Calls: adds_new_collection()
"""
def create_new_collection(list_buttons, *widgets): 

    for button in list_buttons:
        destroy(button)

    frame1 = create_frame(0,1)
    destroy(*widgets)
    new_col = Label(root, text = "What would you like the new collection to be called?", font="Helvetica 14 bold")
    new_col.place(x=100, y=100)

    new_col_entry = Entry(root)
    new_col_entry.place(x=100, y=200)

    submit = Button(root, text = "Submit", 
        command = lambda: adds_new_collection(new_col_entry.get(), new_col, new_col_entry, submit, frame1, go_back_button))
    submit.place(x=200, y=300)

    go_back_button = Button(root, text = "Go back", 
        command = lambda: view_which_log(None, frame1, new_col, new_col_entry, submit, go_back_button))
    go_back_button.place(x=100, y=300)

    configure(3, 1)

"""
Adds the new collection.

Input:
- new_name: name of the new collection
_ *widgets

Output: None
Calls: view_which_log()

"""
def adds_new_collection(new_name, *widgets):
    destroy(*widgets)

    frame1 = create_frame(1,1)

    success_message = Label(root, text="A new collection has been added!", font="Helvetica 14 bold")
    success_message.place(x=100, y=100)

    col = db[new_name]

    # a collection only appears if there is at least one document
    col.insert_one({"New": "new"})
    col.delete_one({"New": "new"})

    ok_button = Button(root, text = "OK", command = lambda: view_which_log(None, None, success_message, ok_button, frame1))
    #ok_button.grid(row=2, column=1, padx=10, pady=10)
    ok_button.place(x=100, y=200)

def delete_collection(collection, *widgets):
    answer = messagebox.askyesno('Delete Collection', 'Are you sure you want to delete this collection?')
    if answer == True:
        collection.drop()
        view_which_log(None, None, *widgets)

"""
The date(s), details of the experience/activity, and the hour(s) are displayed on the screen.

Input: 
- Any number of widgets to be destroyed (from menu())

Output: None
Calls: access_collection() or create_new_collection()
"""

def view_which_log(filter_col, vol = None, *widgets):

    destroy(*widgets)
    widgets_list = []

    choose_col = Label(root, text = "Which collection would you like to look at?", font="Helvetica 18 bold")
    choose_col.place(relx=0.5, rely=0, anchor="n")
    widgets_list.append(choose_col)

    if filter_col == None:
        collection_list = list(db.list_collection_names())
        collection_list.sort()
    else:
        collection_list = filter_col

    selected_option = StringVar()

    combo_box = ttk.Combobox(root, values=collection_list, state="readonly")
    combo_box.config(height=5)
    combo_box.place(x=250, y=100)
    combo_box.current(0)
    widgets_list.append(combo_box)
  
    new_col = Button(root, text = "Add new collection instead", command = lambda: create_new_collection(widgets_list))
    new_col.place(x=150, y=330)
    widgets_list.append(new_col)

    search_col = Button(root, text = "Search for collections by keyword", 
        command = lambda: search_keywords(vol, True,choose_col, combo_box, new_col, search_col, access_button))
    search_col.place(x=380, y=330)
    widgets_list.append(search_col)

    access_button = Button(root, text = "Access this collection", command = lambda: access_collection(combo_box.get(), choose_col, combo_box, new_col,
        search_col, access_button))
    access_button.place(x=250, y=150)
    widgets_list.append(access_button)

    #configure(5,5)

def filter_col_by_keyword(vol, keyword, *widgets):
    collection_list = list(db.list_collection_names())
    filtered_list = []

    for collection in collection_list:
        vol = db[collection]

        document_num = vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}})

        if document_num != 0:
            filtered_list.append(collection)

    if len(filtered_list) !=0:
        destroy(*widgets)
        view_which_log(filtered_list, vol)
    else:
        messagebox.showerror("No collections", "No collections have been returned. Try searching something else.")
        return


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
Used to help with the "scrolling feature" when viewing the activity log
"""
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def no_entries(vol, search, *widgets):
    destroy(*widgets)
    frame1 = create_frame(0,1)

    if search == False:
        no_logs = Label(frame1, text = "There are currently no entries in this collection.")
        no_logs.grid(row=1, column=1)
    else: # search is true
        no_logs = Label(frame1, text = "No results have been returned based on your search.")
        no_logs.grid(row=1, column=1)

    # allows the user to go back to the menu
    menu_button = Button(root, text = "Back to Menu", 
    command = lambda: menu(vol, no_logs, menu_button, frame1))
    #menu_button.grid(row = 2, column = 1, padx=10, pady=10)
    menu_button.place(x=350, y=350)

    configure(2,1)

"""
Allows the user to see the entries displayed, and they are able to scroll through them and make edits, if necessary.

Input:
- vol
- search: True if we want to allow the user to search using keywords (display the search entrybox, etc), False otherwise.
- keyword: keyword used to search, otherwise None
- *widgets

Output: None
Calls: search_keywords() or menu()
"""

def view_log(vol, search, keyword=None, *widgets):

    destroy(*widgets)

    # if keyword is None and we want to allow the user to search
    if not isinstance(keyword,str) and search == True:
        search_keywords(vol, False, *widgets)

    # user has searched but no search results popped up
    elif search == True and vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}}) == 0:
        no_entries(vol, True)

    try:
        # if we don't want searching (or if the user has already searched before), then go ahead and display the results
        if not search:
            if isinstance(keyword, str): # if a keyword has been given by the user
                results = vol.find({'details': {'$regex': keyword, '$options': 'i'}}) # has all the results
                count = vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}}) # number of entries (documents)

                if count == 0: # no entries
                    no_entries(vol, True)

            elif keyword == None: # viewing all
                results = vol.find()
                count = vol.estimated_document_count()

                if count == 0: # no entries
                    no_entries(vol, False)

            if (count >= 1): # 1 or more entries

                results = results.sort([("date", 1), ("startdate", 1)])

                row_num = 0
                frame_main = Frame(my_canvas, width=800, height=400, bg='light pink')
                frame_main.grid(row=0, column=1, sticky='news')

                my_canvas.create_window((0,0), window=frame_main, anchor='nw')#, width=750)
        
                frame_main.grid_rowconfigure(0, weight=1)
                frame_main.grid_columnconfigure(0, weight=1)
                
                # Create a frame for the canvas with non-zero row&column weights
                frame_canvas = Frame(frame_main)
                frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
                frame_canvas.grid_rowconfigure(0, weight=1)
                frame_canvas.grid_columnconfigure(0, weight=1)
                # Set grid_propagate to False to allow 5-by-5 buttons resizing later
                frame_canvas.grid_propagate(False)

                # Add a canvas in that frame
                canvas = Canvas(frame_canvas, bg="lavender blush")
                canvas.grid(row=0, column=0, sticky="news")


                # Link a scrollbar to the canvas
                vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
                vsb.grid(row=0, column=1, sticky='ns')
                canvas.configure(yscrollcommand=vsb.set)
                bg=ImageTk.PhotoImage(file="394901.png")
                canvas.create_image(0,0, image=bg, tag='img', anchor='nw')

                # Create a frame to contain the buttons
                frame_buttons = Frame(canvas, bg='lavender blush')


                # Set image in canvas
                canvas.create_window((0,0), window=frame_buttons, anchor='nw')

                # allows you to use arrow keys
                canvas.bind("<Up>",    lambda event: canvas.yview_scroll(-1, "units"))
                canvas.bind("<Down>",  lambda event: canvas.yview_scroll( 1, "units"))
           
                canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int((event.delta / 120)), "units"))
                canvas.focus_set()
                canvas.bind("<1>", lambda event: self.canvas.focus_set())
                
                # Add 9-by-5 buttons to the frame
                rows = count 
                columns = 1
                buttons = [[Button() for j in range(columns)] for i in range(rows)]
                
                for i in range(0, rows):
                    if vol.count_documents({"startdate": {"$exists": True}, '_id': results[i]['_id']}) == 1 :
                        date_display = results[i]['startdate'].strftime('%m/%d/%y') + ' - ' + results[i]['enddate'].strftime('%m/%d/%y')
                    elif isinstance(results[i]['date'], str):
                        date_display = results[i]['date']
                    else:
                        date_display = results[i]['date'].strftime('%m/%d/%y')

                    for j in range(0, columns):
                        buttons[i][j] = Button(frame_buttons, bg = 'white', fg='black', font="Helvetica 9", height = 10, width=10, 
                            text= 'date: ' + date_display + '\n' + 
                            'details: ' + results[i]['details'].strip('\n') + '\n' + 'hours: ' + str(results[i]['hours']),
                            command = lambda i=i: ask_entry_changes(vol, results[i], keyword, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))
                        buttons[i][j].grid(row=i, column=j, ipadx=310, ipady=50,pady=50)

                # Update buttonsframes idle tasks to let tkinter calculate buttons sizes
                frame_buttons.update_idletasks()

                # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
                first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, columns)])
                first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, rows)])
                frame_canvas.config(width=buttons[0][j].winfo_width() + vsb.winfo_width(),
                                        height=buttons[0][j].winfo_height())

                # Set the canvas scrolling region
                canvas.config(scrollregion=canvas.bbox("all"))

                
                search_keywords_button = Button(root, text = "Search using keywords instead", 
                    command = lambda: search_keywords(vol, False, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))

                search_keywords_button.place(x=280, y=350)

                menu_button = Button(root, text = "Menu", 
                    command = lambda: menu(vol, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, menu_button, search_keywords_button))
                menu_button.place(x=350, y=300)
                
    except Exception as e:
        print(e)

def filter_by_date(results, *widgets):
    if var1.get() == 1:
        results.sort('date', pymongo.DESCENDING)
        return results

"""
Asks the user what part of their entry they would like to change.

Input:
- vol
- result: (eg. {'_id': ObjectId('60b4418688db9bce7b378c09'), 'date': datetime.datetime(2020, 12, 27, 0, 0), 'details': 'aa\n', 'hours': '1'})
- *widgets

Output: None
Calls: add_details() or add_hours() or make_date_changes() or view_log()
"""
def ask_entry_changes(vol, result, keyword, *widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    frame2 = create_frame(1,1)

    where_to_edit = Label(frame1, text="What part would you like to change?")
    where_to_edit.grid(row=1, column=1, padx=10, pady=10)

    details_button = Button(frame1, text = "Details", command = lambda: add_details(vol, True, result, keyword,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    details_button.grid(row=2, column=0, padx=10, pady=10)

    hours_button = Button(frame1, text = "Hours", command = lambda: add_hours(vol, result, True, None,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    hours_button.grid(row=2, column=1, padx=10, pady=10)

    dates_button = Button(frame1, text = "Date(s)", command = lambda: make_date_changes(vol, result,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    dates_button.grid(row=2, column=2, padx=10, pady=10)

    if keyword != None:
        search = True
    else:
        search = False

    go_back_button = Button(frame1, text = "Go back", 
        command = lambda: view_log(vol, search, keyword, where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    go_back_button.grid(row=3, column=1, padx=10, pady=10)

    additional = Button(root, text = "View Additional Notes", 
        command = lambda: view_additional_notes(vol, result, keyword, where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    additional.place(x=300, y=300)

def view_additional_notes(vol, result, keyword, *widgets):
    destroy(*widgets)

    if len(result['others'].strip()) == 0:
        additional_details = "There are no additional details added."
    else:
        additional_details = result['others']

    additional_notes = Label(root, text = "Additional notes:\n\n " + additional_details)
    additional_notes.place(x=root.winfo_width()/2 - 50, y=0)

    go_back_button = Button(root, text = "Go back", 
        command = lambda: ask_entry_changes(vol, result, keyword, additional_notes, go_back_button))
    go_back_button.place(x=root.winfo_width()/2 - 15, y=root.winfo_height() - 50)

    configure(3, 1)

"""
Takes the user to the appropiate method depending on if they want to edit one date or two dates (start and end date)

Input:
- vol
- result (all the details)
- *widgets

Output: None
Calls: one_day_option() or multiple_days_option()
"""
def make_date_changes(vol, result, *widgets):
    count = vol.count_documents({"startdate": {"$exists": True}, '_id': result['_id']})
    if count == 0: # one date
        one_day_option(vol, result, True, *widgets)
    else:
        multiple_days_option(vol, result, True, *widgets)

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

    destroy(*widgets)

    global string_collection
    global vol
    if isinstance(collection, str):
        vol = db[collection]
        string_collection = collection
    else:
        vol = collection

    db_label = Label(root, text="Collection Name: " + string_collection, font="Helvetica 18 bold")
    db_label.place(x=root.winfo_width()/3 - 10, y=0)


    frame1 = create_frame(0,1)
    
    global menu_label, add_record_1, view_act_log
    menu_label = Label(frame1, text="MENU", font="Helvetica 18 bold")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(frame1, text = "Add a new log record",
        command=lambda: add_details(vol, False, None, None, menu_label, add_record_1, view_act_log, frame1, db_label))
    add_record_1.grid(row=1, column=1, padx = 50, pady=10)

    view_act_log = Button(frame1, text = "View activity log", 
        command = lambda: view_log(vol, False,None, menu_label, add_record_1, view_act_log, frame1, db_label))
    view_act_log.grid(row=2, column=1, padx = 50, pady=10)

    another_collection_button = Button(frame1, text = "Choose another collection",
     command = lambda: view_which_log(None, menu_label, add_record_1, view_act_log, frame1, another_collection_button, db_label))
    another_collection_button.grid(row=3, column=1, padx=50, pady=10)

    delete_collection_button = Button(frame1, text = "Delete this collection", 
        command = lambda: delete_collection(vol, menu_label, add_record_1, view_act_log, frame1, 
            another_collection_button, delete_collection_button, db_label))
    delete_collection_button.grid(row=4, column=1, padx=50, pady=10)

    configure(4, 1)

"""
MAIN
"""
def main():

    global root, client, db, vol, my_canvas


    root = Tk()
    root.title("Activity Log")
    root.geometry("720x400")
    root.resizable(False, False)

    bg=ImageTk.PhotoImage(file="394901.png") # pink and light blue background

    my_canvas = Canvas(root, width=800, height=500)
    my_canvas.grid(row=0, column=1)

    # setting image in canvas
    my_canvas.create_image(0,0, image=bg, tag='img', anchor='nw')

    client = MongoClient('mongodb://localhost:27017') # connects to a specific port

    # open the database
    db = client["activities"]
    
    # starts off by making the user select a collection to view
    view_which_log(None)
    root.mainloop()

main()
       