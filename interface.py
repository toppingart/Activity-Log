from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, date
import sys

"""
The user enters one or more keywords to narrow down the results (when looking for a specific record).

Input: 
- vol: allows us to access the contents of the collection
- *widgets: 0 or more widgets to be destroyed (cleared before displaying new widgets)

Output: None
Calls: search_with_input() or view_log()
"""
def search_keywords(vol, *widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)

    search_label = Label(frame1, text="What would you like to search for?")
    search_label.grid(row=0, column=1, padx=10, pady=10)

    search_entry = Entry(frame1)
    search_entry.grid(row=1, column=1, padx=10, pady=10)

    submit = Button(frame1, text = "Submit", 
        command = lambda: search_with_input(vol, search_entry.get(), search_label, search_entry, submit, view_all, frame1))
    submit.grid(row=2, column=1, padx=10, pady=10)

    view_all = Button(frame1, text = "View all instead", 
        command = lambda: view_log(vol, False, None, search_label, search_entry, submit, view_all, frame1))
    view_all.grid(row=3, column=1, padx=10, pady=10)

    configure(3,1)

"""
Adds wildcards (*) and allows for case-insenstive searches.

Input:
- vol
- entry: keyword used for searching
- *widgets

Output: None
Calls: view_log()
"""
def search_with_input(vol, entry, *widgets):

    destroy(*widgets)

    # wildcards are used in between the entry
    keyword = '.*' + entry + '.*'
   
    # case insensitive is allowed
    results = vol.find({'details': {'$regex': keyword, '$options': 'i'}})

    view_log(vol, True, keyword, *widgets)

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

        elif isinstance(date,str) and len(date.strip()) == 17:
            # 12/01/20-12/02/20
            start_date = result['date'][:8]
            end_date = result['date'][9:]
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

def add_details(vol, edited, details, *widgets):

    destroy(*widgets)
    frame1 = create_frame(0,0)
    frame2 = create_frame(0,1)
    frame3 = create_frame(1,1)

    details_text = Label(frame1, text="Give some details about the experience.")
    details_text.grid(row=0,column=0,padx=30,pady=10)   
    details_entry = Text(frame1, width=30, height=10)
    details_entry.grid(row=1, column=0)

    others_text = Label(frame2, text="Any additional notes? [OPTIONAL]")
    others_text.grid(row=0,column=1,padx=50,pady=10)   
    others_entry = Text(frame2, width=30, height=10)
    others_entry.grid(row=1, column=1)

    configure(3, 1)

    if not edited:

        go_back_button = Button(frame3, text = "Go back", 
            command = lambda: menu(vol, details_text, details_entry, submit_button, frame1))
        go_back_button.grid(row=1, column=1, padx=10, pady=10)

        submit_button = Button(frame3, text = "Submit All", 
            command = lambda: add_hours(vol, details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), False, details_text, details_entry, submit_button, frame1, frame2, frame3))
        submit_button.grid(row=1, column=2, padx=10,pady=10)

    else: # if the user is making edits to their entry
        submit_button = Button(frame3, text = "Submit All", 
            command = lambda: types_of_changes(1, details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), vol, details, details_text, details_entry, submit_button, frame1, frame2, frame3))
        submit_button.grid(row=1, column=1, padx=10,pady=10)

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
def add_hours(vol, details, others, edited, *widgets):

    # error handling
    if len(details.strip()) == 0:
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

        submit_button = Button(frame1, text = "Submit", 
            command = lambda: add_dates(vol, user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)

    else: # happens if the user wants to make edits to their entry (not a new entry)
        submit_button = Button(frame1, text = "Submit",
            command = lambda: types_of_changes(2, hours_entry.get(), None, vol, details, hours_text, hours_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)

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
    user_list.append(int(hours)) # if hours is an int (is valid), it is added to the list of user inputs

    frame1 = create_frame(0,1)
  
    dates_text = Label(frame1, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    one_day_button = Button(frame1, text = "One day", 
        command = lambda: one_day_option(vol, user_list, False, dates_text, one_day_button, m_days_button, frame1))
    one_day_button.grid(row=1, column=1, padx=50,pady=50)

    m_days_button = Button(frame1, text = "Multiple days", 
        command = lambda: multiple_days_option(vol, user_list, dates_text, one_day_button, m_days_button, frame1))
    m_days_button.grid(row=2, column=1, padx=50, pady=50)

    configure(2, 1)


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
        command = lambda: all_user_inputs(vol, user_list, day_text, day_entry, submit_button, frame1, date = day_entry.get()))
        submit_button.grid(row=2, column=1, padx=50,pady=50)
    else:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(3, day_entry.get(), None, vol, user_list, day_text, day_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)


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

    days_text = Label(frame1, text = "What days did this take place (eg. 12/25/2020 - 01/01/2021)" )
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
            start_day_entry, end_day_entry, submit_button, frame1,
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))
        submit_button.grid(row=5, column=1, padx=50,pady=50)

    else:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(4, [start_day_entry.get(), end_day_entry.get()], None, vol, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1))
        submit_button.grid(row=5, column=1, padx=50,pady=50)

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
- Any number of widgets to be destroyed (these widgets are either from one_day_option() or multiple_days_options())
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
        back_to_menu_button = Button(frame2, text = "Back to menu", 
        command = lambda: menu(vol, success_message, exit_button, back_to_menu_button, frame1, frame2))
        back_to_menu_button.grid(row=1, column=1, padx=10, pady=10)

        # exit option
        exit_button= Button(frame2, text = "Exit", command = lambda: sys.exit()) # if pressed, exits the program
        exit_button.grid(row=2, column = 1)

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

                if len(user_list) == 2: # already contains the details, hours
                    user_list.append(days["startdate"]) # if statement prevents startdate from being added again

                check_date(days["enddate"])

                if len(user_list) == 3: # already contains details, hours, and startdate
                    user_list.append(days["enddate"]) # if statement prevents enddate from being added again
                break

    except NameError as n:
        messagebox.showerror("Dates Error", "Please enter a valid date.")

    except ValueError as v:
        messagebox.showerror("Dates Error", "Please enter a valid date.")

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

    frame1 = create_frame(1,1)

    destroy(*widgets)
    new_col = Label(frame1, text = "What would you like the new collection to be called?")
    new_col.grid(row=1, column=1, padx=10, pady=10)

    new_col_entry = Entry(frame1)
    new_col_entry.grid(row=2, column=1, padx=10, pady=10)

    submit = Button(frame1, text = "Submit", 
        command = lambda: adds_new_collection(new_col_entry.get(), new_col, new_col_entry, submit, frame1))
    submit.grid(row=3, column=1, padx=10, pady=10)

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

    success_message = Label(frame1, text="A new collection has been added!")
    success_message.grid(row=1, column=1, padx=10, pady=10)

    col = db[new_name]

    # a collection only appears if there is at least one document
    col.insert_one({"New": "new"})
    col.delete_one({"New": "new"})

    ok_button = Button(frame1, text = "Ok", command = lambda: view_which_log(success_message, ok_button, frame1))
    ok_button.grid(row=2, column=1, padx=10, pady=10)

def delete_collection(collection, *widgets):
    answer = messagebox.askyesno('Delete Collection', 'Are you sure you want to delete this collection?')
    if answer == True:
        collection.drop()
        view_which_log(*widgets)

"""
The date(s), details of the experience/activity, and the hour(s) are displayed on the screen.

Input: 
- Any number of widgets to be destroyed (from menu())

Output: None
Calls: access_collection() or create_new_collection()
"""

def view_which_log(*widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    frame2 = create_frame(1,1)
    frame3 = create_frame(2,1)


    choose_col = Label(frame1, text = "Which collection would you like to look at?")
    choose_col.grid(row = 0, column =1)

    col_buttons = [] # keeps track of all the collection buttons
    button_num = 0
    row_num = 1
    for collection in db.list_collection_names():
        # command= lambda s=somevariable: printout(s)) 
        # https://stackoverflow.com/questions/49082862/create-multiple-tkinter-button-with-different-command-but-external-variable
        b = Button(frame2, text = collection, 
            command = lambda collection_name = collection: access_collection(col_buttons, collection_name, choose_col, new_col, frame1, frame2, frame3))
        b.grid(row=row_num, column=button_num, padx=10, pady=10)
        col_buttons.append(b)
        button_num +=1

        if button_num % 5 == 0:
            row_num +=1
            button_num = 0

    new_col = Button(frame3, text = "Add new collection instead", command = lambda: create_new_collection(col_buttons, choose_col, new_col, frame1, frame2, frame3))
    new_col.grid(row=row_num+1, column=1, padx=10, pady=10)

    configure(row_num+1, button_num)

"""
Now that a collection has been selected, the user will access that collection and continue with the menu options.

Input:
- list of buttons to be destroyed
- collection_name
- *widgets

Output: None
Calls: menu()
"""
def access_collection(button_list, collection_name, *widgets):

    for button in button_list:
        destroy(button)

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
    else:
        no_logs = Label(frame1, text = "No results have been returned based on your search.")
        no_logs.grid(row=1, column=1)

    # allows the user to go back to the menu
    menu_button = Button(root, text = "Menu", 
    command = lambda: menu(vol, no_logs, menu_button, frame1))
    menu_button.grid(row = 2, column = 1, padx=10, pady=10)

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
        search_keywords(vol, *widgets)
    
    try:
        # if we don't want searching (or if the user has already searched before), then go ahead and display the results
        if not search:
            if isinstance(keyword, str): # if a keyword has been given by the user
                results = vol.find({'details': {'$regex': keyword, '$options': 'i'}}) # has all the results
                count = vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}}) # number of entries (documents)

            elif keyword == None: # viewing all
                results = vol.find()
                count = vol.estimated_document_count()

            if count == 0: # no entries
                no_entries(vol, search)

            else: # 1 or more entries
                row_num = 0
                frame_main = Frame(root, bg="gray")
                frame_main.grid(sticky='news')

                root.grid_rowconfigure(0, weight=1)
                root.grid_columnconfigure(0, weight=1)

                # Create a frame for the canvas with non-zero row&column weights
                frame_canvas = Frame(frame_main)
                frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
                frame_canvas.grid_rowconfigure(0, weight=1)
                frame_canvas.grid_columnconfigure(0, weight=1)
                # Set grid_propagate to False to allow 5-by-5 buttons resizing later
                frame_canvas.grid_propagate(False)

                # Add a canvas in that frame
                canvas = Canvas(frame_canvas, bg="yellow")
                canvas.grid(row=0, column=0, sticky="news")


                # Link a scrollbar to the canvas
                vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
                vsb.grid(row=0, column=1, sticky='ns')
                canvas.configure(yscrollcommand=vsb.set)

                # Create a frame to contain the buttons
                frame_buttons = Frame(canvas, bg="pink")
                canvas.create_window((0,0), window=frame_buttons, anchor='nw')

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
                        buttons[i][j] = Button(frame_buttons, height = 10, width=10,  text= 'date: ' + date_display + '\n' + 
                            'details: ' + results[i]['details'] + '\n' + 'hours: ' + str(results[i]['hours']),
                            command = lambda i=i: ask_entry_changes(vol, results[i], keyword, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))
                        buttons[i][j].grid(row=i, column=j, ipadx=300, ipady=50,pady=50)

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
                    command = lambda: search_keywords(vol, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))
                search_keywords_button.grid(row=1, column=0, padx=10, pady=10)

                menu_button = Button(root, text = "Menu", 
                    command = lambda: menu(vol, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, menu_button, search_keywords_button))
                menu_button.grid(row = 2, column = 0, padx=10, pady=10)

    except Exception as e:
        print(e)

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

    where_to_edit = Label(text="What part would you like to change?")
    where_to_edit.grid(row=1, column=1, padx=10, pady=10)

    details_button = Button(root, text = "Details", command = lambda: add_details(vol, True, result, 
        where_to_edit, details_button, hours_button, dates_button, go_back_button))
    details_button.grid(row=2, column=0, padx=10, pady=10)

    hours_button = Button(root, text = "Hours", command = lambda: add_hours(vol, result, True, 
        where_to_edit, details_button, hours_button, dates_button, go_back_button))
    hours_button.grid(row=2, column=1, padx=10, pady=10)

    dates_button = Button(root, text = "Date(s)", command = lambda: make_date_changes(vol, result,
        where_to_edit, details_button, hours_button, dates_button, go_back_button))
    dates_button.grid(row=2, column=2, padx=10, pady=10)

    go_back_button = Button(root, text = "Go back", 
        command = lambda: view_log(vol, False, keyword, where_to_edit, details_button, hours_button, dates_button, go_back_button))
    go_back_button.grid(row=3, column=1, padx=10, pady=10)


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

    if isinstance(collection, str):
        vol = db[collection]
    else:
        vol = collection

    frame1 = create_frame(0,1)
    
    global menu_label, add_record_1, view_act_log
    menu_label = Label(frame1, text="MENU")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(frame1, text = "Add a new log record",
        command=lambda: add_details(vol, False, None, menu_label, add_record_1, view_act_log, frame1))
    add_record_1.grid(row=1, column=1, padx = 50, pady=10)

    view_act_log = Button(frame1, text = "View activity log", 
        command = lambda: view_log(vol, False,None, menu_label, add_record_1, view_act_log, frame1))
    view_act_log.grid(row=2, column=1, padx = 50, pady=10)

    another_collection_button = Button(frame1, text = "Choose another collection",
     command = lambda: view_which_log(menu_label, add_record_1, view_act_log, frame1, another_collection_button))
    another_collection_button.grid(row=3, column=1, padx=50, pady=10)

    delete_collection_button = Button(frame1, text = "Delete this collection", 
        command = lambda: delete_collection(vol, menu_label, add_record_1, view_act_log, frame1, another_collection_button, delete_collection_button))
    delete_collection_button.grid(row=4, column=1, padx=50, pady=10)

    configure(4, 1)

"""
MAIN
"""
def main():

    global root, client, db, vol

    root = Tk()
    root.title("Activity Log")
    root.geometry("700x400")

    client = MongoClient('mongodb://localhost:27017') # connects to a specific port

    today = date.today()

    current_year = today.strftime("%Y")

    # open the database (depends on year)
    db = client["sheets"]
    
    # starts off by making the user select a log (or collection) to view
    view_which_log()
    root.mainloop()

main()
       