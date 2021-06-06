from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import sys
import globals

# maybe do data visualization?

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
        command = lambda: view_log(vol, None, search_label, search_entry, submit, view_all, frame1))
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

    view_log(vol, keyword, *widgets)

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
The user enters some details about their experience.

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
    frame1 = create_frame(0,1)

    details_text = Label(frame1, text="Give some details about the experience.")
    details_text.grid(row=0,column=1,padx=50,pady=10)   
    details_entry = Text(frame1, width=30, height=10)
    details_entry.grid(row=1, column=1)

    configure(2, 1)

    if not edited:

        go_back_button = Button(frame1, text = "Go back", 
            command = lambda: menu(vol, details_text, details_entry, submit_button, frame1))
        go_back_button.grid(row=3, column=1, padx=10, pady=10)

        submit_button = Button(frame1, text = "Submit", command = lambda: add_hours(vol, details_entry.get('1.0', 'end'), False, details_text, details_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)

    else: # if the user is making edits to their entry
        submit_button = Button(frame1, text = "Submit", command = lambda: types_of_changes(1, details_entry.get('1.0', 'end'), vol, details, details_text, details_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)

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
- edited
- *widgets (NOTE: all the widgets are from the add_details())

Output: None
"""
def add_hours(vol, details, edited, *widgets):

    destroy(*widgets)

    frame1 = LabelFrame(root)
    frame1.grid(row=0, column=1, padx=10, pady=10)

    hours_text = Label(frame1, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(frame1)
    hours_entry.grid(row=1, column=1,padx=50,pady=50)

    if edited == False:
        # error handling
        if len(details.strip()) == 0:
            messagebox.showerror("Details Error", "Please enter some details.")
            return

        user_input_list = [details] # obtained from add_details()

        submit_button = Button(frame1, text = "Submit", 
            command = lambda: add_dates(vol, user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)

    else: # happens if the user wants to make edits to their entry (not a new entry)
        submit_button = Button(frame1, text = "Submit",
            command = lambda: types_of_changes(2, hours_entry.get(), vol, details, hours_text, hours_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)

    configure(2, 1)

"""
Will take the appropiate action depending on what part ot the entry the user wants to make edits to

input:
- type_of_change:  details - 1, hours-2, date - 3, dates (start and end date) - 4 (int)
- edited_entry: edits made by the user (str)
- vol
- result: (eg. {'_id': ObjectId('60b4418688db9bce7b378c09'), 'date': datetime.datetime(2020, 12, 27, 0, 0), 'details': 'aa\n', 'hours': '1'})
- *widgets

Calls: successful_message(), check_date(), to_datetime()
"""
def types_of_changes(type_of_change, edited_entry, vol, result, *widgets):

    destroy(*widgets)
    
    if type_of_change == 1:
        vol.update_one({'_id': result['_id']}, {'$set': {'details': edited_entry}})
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
       # vol.update_one({'_id': result['_id']}, {'$set': {'startdate': edited_entry[0], 
         #   'enddate': edited_entry[1]}})

        datetime_start = datetime.strptime(edited_entry[0], "%m/%d/%y")
        datetime_end = datetime.strptime(edited_entry[1], "%m/%d/%y")
        vol.update_one({'_id': result['_id']}, {'$set': {'startdate': datetime_start, 'enddate': datetime_end}})
        #to_datetime(vol, [result])
        #successful_message(vol, None, 2)



"""
There are two purposes:
1. Checks if the hours that the user has entered is valid (is an integer), otherwise the user will 
be asked to enter their hours again.

2. If the hours that the user has entered is valid, then the user will be asked to select if their experience/activity
spans over a day or multiple days by clicking one of the buttons.

Input: 
- user_list: a list of the user's inputs so far (which in this case, would be the details and the hours)
- hours: the user's input - ideally as an int, but will be checked if it is an integer
- Any number of widgets from add_hours() to be destroyed 

Output: None

"""

def add_dates(vol, user_list, hours,*widgets):

    try:
        int(hours) # checks if an integer has been entered 
    except:
        messagebox.showerror("Hours Error", "Please enter a number for your hours.")
        return # exits the function (so that the user can enter the number of hours again)

    destroy(*widgets)
    user_list.append(hours) # if hours is an int (is valid), it is added to the list of user inputs

    frame1 = create_frame(0,1)
  
    dates_text = Label(frame1, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    # first option the user can select 
    one_day_button = Button(frame1, text = "One day", 
        command = lambda: one_day_option(vol, user_list, False, dates_text, one_day_button, m_days_button, frame1))

    one_day_button.grid(row=1, column=1, padx=50,pady=50)

    # second option the user can select 
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
- user_list: a list of the user's inputs so far (in this case, the details and hours). It will not be used in the function
itself, but will be used in the all_user_inputs()
- Any number of widgets to be destroyed

Output: None

"""
def one_day_option(vol, user_list, done, *widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    configure(2, 1)

    # DATE CHANGED
    day_text = Label(frame1, text = "What day did this take place (eg. 12/25/2020) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(frame1) # textbox
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    if not done:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(vol, user_list, day_text, day_entry, submit_button, frame1, date = day_entry.get()))
        submit_button.grid(row=2, column=1, padx=50,pady=50)
    else:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(3, day_entry.get(), vol, user_list, day_text, day_entry, submit_button, frame1))
        submit_button.grid(row=2, column=1, padx=50,pady=50)





"""
There are two purposes.
1. Destroys the widgets from add_dates()
2. Allows the user to enter the start date and the end date that the experience/activity took place on (as a string)

Input: 
- user_list: a list of the user's inputs so far (in this case, the details and hours). It will not be used in the function
itself, but will be used in the all_user_inputs()
- Any number of widgets to be destroyed

Output: None

"""

def multiple_days_option(vol, user_list, done, *widgets):

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

    if not done:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(vol, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1,
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))


        submit_button.grid(row=5, column=1, padx=50,pady=50)

    else:


        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(4, [start_day_entry.get(), end_day_entry.get()], vol, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1))


        submit_button.grid(row=5, column=1, padx=50,pady=50)


"""
Checks if the date entered by the user is a valid date (valid day, month, and year).

Input: the date (as a string)
Output: None

"""

def check_date(date):
    try:
        print(len(date.strip()))
        if len(date.strip()) == 8:
            check_date = datetime.strptime(date, "%m/%d/%y") 
          
        else:
            raise ValueError
    except Exception as e:
        print(e)
        messagebox.showerror("Date(s) Error", "Check that the date(s) you have entered are valid.")
        #raise Exception

"""
There are two purposes.
1. Informs the user that the experience/activity record has been successfully added to the database. 
2. The user is then presented with two buttons: one that exits the program and the other takes them back to the menu screen.

Input: 
- The user list that contains the details, hour(s), and date(s) (note that all have been checked to be valid already)
- Any number of widgets to be destroyed (these widgets are either from one_day_option() or multiple_days_options())
Output: None

"""

def successful_message(vol, user_list, type_of_success, *widgets):

    
    try:

        destroy(*widgets)
        frame1 = create_frame(0,1)
        frame2 = create_frame(1,1)

        if type_of_success == 1:
            if len(user_list) == 3: # date (2017-07-31T00:00:00.000+00:00), detail, hours
                vol_record = {"date": user_list[2], "details": user_list[0], "hours": user_list[1] }
            else: # date ("02/08/2017 - 04/08/2017"), detail, hours, startdate, enddate
                vol_record = {"date": user_list[2] + " - " + user_list[3], "details": user_list[0], "hours": user_list[1]}

   # vol_record = {"details"}
            vol.insert_one(vol_record)
            to_datetime(vol, [vol_record])

            success_message = Label(frame1, text = "The record has been successfully added to the database!")
            success_message.grid(row=0, column=1)

        else:

            success_message = Label(frame1, text = "The record has been successfully edited!")
            success_message.grid(row=0, column=1)

    # ['a', '1', '25/12/2020']
    # ['a', '1', '25/12/2020', '01/01/2021']
    # rental = {"member_renting": ("Saeed", "7806808181"), "movie_rented": movie_ids[1]}


        # exit option
        exit_button= Button(frame2, text = "Exit", command = lambda: sys.exit()) # if pressed, exits the program
        exit_button.grid(row=1, column = 1)

        # go back to menu option
        back_to_menu_button = Button(frame2, text = "Back to menu", 
        command = lambda: menu(vol, success_message, exit_button, back_to_menu_button, frame1, frame2))
        back_to_menu_button.grid(row=2, column=1, padx=10, pady=10)

        configure(2,1)

    except Exception as e:
        print(e)


"""
There are two purposes.
1. If the date(s) are valid (which will be checked in this function), the date(s) will be added to the user_list 
(that contains the details and the hours)

2. Once the date is determined to be valid, the record is added to the database. (**INCORPORATE)

REMINDER: the details and the hours are valid (as they have been checked before)

"""

def all_user_inputs(vol, user_list, *widgets, **days):

    try:

        # add date(s)
        for key, value in days.items():
            if key == "date":
                check_date(value)
                user_list.append(value)
                break

            else: 
                check_date(days["startdate"])

                if len(user_list) == 2: # already contains the details, hours
                    user_list.append(days["startdate"]) # if statement prevents startdate from being added again

                check_date(days["enddate"])

                if len(user_list) == 3: # already contains details, hours, and startdate
                    user_list.append(days["enddate"]) # if statement prevents enddate from being added again
                
                break


           # destroy(*widgets)
        print(user_list)
        successful_message(vol, user_list, 1, *widgets)

    except NameError as n:
        print(n)
        messagebox.showerror("Dates Error", "Please enter a valid date.")

   # except Exception:
        # messagebox.showerror("Dates Error", "Please fill in both the start date and end date.")
    #    return

    except Exception as e:
        print(e)
        messagebox.showerror("Dates Error", "Please fill in both the start date and end date.")
     #   return # exit the function


    #return user_list


def print_value(e):
    print(e.get())

def delete_test():
    pass

def add_test(user_list):
    record = {"details": user_list[0]}
    vol.insert(record)

def modify_log():
    pass

def create_new_collection(year_buttons, *widgets): #DOO

    for button in year_buttons:
        destroy(button)

    destroy(*widgets)
    new_year = Label(root, text = "What would you like the new year to be called?")
    new_year.grid(row=1, column=1, padx=10, pady=10)

    new_year_entry = Entry(root)
    new_year_entry.grid(row=2, column=1, padx=10, pady=10)

    submit = Button(root, text = "Submit", command = lambda: new_collection(new_year_entry.get(), new_year, new_year_entry, submit))
    submit.grid(row=3, column=1, padx=10, pady=10)

  

def new_collection(new_name, *widgets):
    destroy(*widgets)
    success_message = Label(root, text="A new collection has been added!")
    success_message.grid(row=1, column=1, padx=10, pady=10)



    ok_button = Button(root, text = "ok", command = lambda: view_which_log(success_message, ok_button))
    ok_button.grid(row=2, column=1, padx=10, pady=10)


"""
**NEEDS TO BE CHANGED. CURRENTLY DISPLAYS ONE RECORD (AND OTHER CHANGES...SEE BELOW)

The date(s), details of the experience/activity, and the hour(s) are displayed on the screen.
The user can click on the PREVIOUS and NEXT buttons to look through their records. 

Input: 
- Any number of widgets to be destroyed (from menu())
- skip_num: the record that will be displayed

Output: None

"""

def view_which_log(*widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    frame2 = create_frame(1,1)

   # frame1['bg'] = 'azure'

    choose_years = Label(frame1, text = "Which year would you like to look at?")
    choose_years.grid(row = 0, column =1)

    # show the collections that are available 
    row_num = 2;
    col_names = ""

    year_buttons = []
    button_num = 0
    for collection in db.list_collection_names():
        # command= lambda s=somevariable: printout(s)) 
        # https://stackoverflow.com/questions/49082862/create-multiple-tkinter-button-with-different-command-but-external-variable
        b = Button(frame2, text = collection, command = lambda collection_name = collection: access_collection(year_buttons, collection_name, choose_years, new_year, frame1, frame2))
        b.grid(row=1, column=button_num, padx=10, pady=10)
        year_buttons.append(b)
        button_num +=1



    #display_cols = Label(root, text = col_names)
    #display_cols.grid(row=row_num, column=2, padx=10, pady=10)
        

    #collection_input = Entry(root)
    #collection_input.grid(row=row_num+1, column=2, padx=10, pady=10)
   

    new_year = Button(frame2, text = "Add new year instead", command = lambda: create_new_collection(year_buttons, choose_years, new_year, frame1, frame2))
    new_year.grid(row=1, column=button_num, padx=10, pady=10)

    configure(1, button_num)

def access_collection(button_list, collection_name, *widgets):

    for button in button_list:
        destroy(button)

    destroy(*widgets)
    menu(collection_name)
    
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def no_entries(vol, *widgets):
    destroy(*widgets)
    no_logs = Label(root, text = "There are currently no entries in this collection")
    no_logs.grid(row=1, column=1)



def view_log(vol, keyword=None, *widgets, skip_num=0):

    # otherwise !label
    
    destroy(*widgets)
    destroy(menu_label)

    if keyword == None:
        pass
    elif not isinstance(keyword,str):
        search_keywords(vol, *widgets)

    
    

   # frame1 = create_frame(0,1)
    #frame2 = create_frame(1,1)




    # **ADD PREVIOUS BUTTON [DONE]
    # ** ADD SEARCH KEYWORDS (maybe in different function?)
    
    try:
        #results = vol.find().skip(skip_num).limit(1)

        if isinstance(keyword, str) or keyword == None:


            if isinstance(keyword, str):
                results = vol.find({'details': {'$regex': keyword, '$options': 'i'}}).skip(skip_num).limit(1)
                count = vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}})

            elif keyword == None:
                results = vol.find().skip(skip_num).limit(1)
                count = vol.estimated_document_count()

            row_num = 0

            if count == 0:
                print('heres')
                no_entries(vol)

            # ---------------------------
            # creating a scrollbar...

            # create a main frame
           # main_frame = Frame(root)
           # main_frame.grid(row=0, column=2)
           # frame1.grid(sticky = 'news')

          #  frame_canvas = Frame(frame1)
          #  frame_canvas.grid(row=0, column=1)
           # frame_canvas.grid_rowconfigure(0, weight=1)
           # frame_canvas.grid_columnconfigure(1, weight=1)
            else:
                frame_main = Frame(root, bg="gray")
                frame_main.grid(sticky='news')

                root.grid_rowconfigure(0, weight=1)
                root.columnconfigure(0, weight=1)

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
                frame_buttons = Frame(canvas, bg="white")
                canvas.create_window((0,0), window=frame_buttons, anchor='nw')

                # Add 9-by-5 buttons to the frame
                rows = count 
                columns = 1
                buttons = [[Button() for j in range(columns)] for i in range(rows)]
                
                for i in range(0, rows):
                    #print(results[i])
                    if vol.count_documents({"startdate": {"$exists": True}, '_id': results[i]['_id']}) == 1 :
                        #date_display = results[i]['startdate']+ '- ' + results[i]['enddate']
                        date_display = results[i]['startdate'].strftime('%m/%d/%y') + ' - ' + results[i]['enddate'].strftime('%m/%d/%y')
                    elif isinstance(results[i]['date'], str):
                        date_display = results[i]['date']
                    else:
                        date_display = results[i]['date'].strftime('%m/%d/%y')


                    for j in range(0, columns):
                        buttons[i][j] = Button(frame_buttons, height = 10, width=10,  text= 'date: ' + date_display + '\n' + 
                            'details: ' + results[i]['details'] + '\n' + 'hours: ' + str(results[i]['hours']),
                            command = lambda i=i: make_entry_changes(vol, results[i], buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))
                        buttons[i][j].grid(row=i, column=j, ipadx=300, ipady=50,pady=50)

                    #i +=1

                    # Update buttonsframes idle tasks to let tkinter calculate buttons sizes
                frame_buttons.update_idletasks()

                # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
                first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, columns)])
                first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, rows)])
                frame_canvas.config(width=buttons[0][j].winfo_width() + vsb.winfo_width(),
                                        height=buttons[0][j].winfo_height())

                #configure(10,10)

                # Set the canvas scrolling region
                canvas.config(scrollregion=canvas.bbox("all"))

                search_keywords_button = Button(root, text = "Search using keywords instead", 
                    command = lambda: search_keywords(vol, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))
                search_keywords_button.grid(row=1, column=0, padx=10, pady=10)

                menu_button = Button(root, text = "Menu", 
                    command = lambda: menu(vol, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, menu_button, search_keywords_button))
                menu_button.grid(row = 2, column = 0, padx=10, pady=10)

           
            # create a canvas
           # canvas_1 = Canvas(frame1)
            #canvas_1.grid(row=2, column=0, pady = (5,0), sticky = 'nw')
            #Grid.rowconfigure(canvas_1, 0, weight=1)
            #Grid.columnconfigure(canvas_1, 0, weight =1)


            # add scrollbar to the canvas
           # v_scrollbar = ttk.Scrollbar(frame1, orient = VERTICAL, command = canvas_1.yview)
            #v_scrollbar.grid(row=0, column=15)

            # configure the canvas
            #canvas_1.configure(yscrollcommand = v_scrollbar.set)
            #canvas_1.bind('<Configure>', lambda e: canvas_1.configure(scrollregion = canvas_1.bbox("all")))

            # Create ANOTHER Frame INSIDE the Canvas
            #frame_2 = Frame(canvas_1)

            # Add that New frame To a Window In The Canvas
            #canvas_1.create_window((0,0), window=frame_2, anchor="nw")

            # -----------------------------
            
           # for result in results:
               # print(result)

               # info_label = Label(frame_canvas, text = date_display + '\n' + result['details'] + '\n' + str(result['hours']))
                #date = Label(root, text = result['date'] if isinstance(result['date'], str) else result['date'].strftime("%d/%m/%Y"))
 
            """

            #print("Count is",count)
 
    """
    except NameError as f:
        print(f)

    except ValueError as v: # there are no "previous" posts to display (the user is currently viewing the first post)
        # widgets have already been destroyed when the button is clicked (does not need to be added again)
        # the default value of skip_num is 0
       # view_log() 
        print(v)
    except Exception as e:
        print(e)


def make_entry_changes(vol, result, *widgets):

    destroy(*widgets)

    where_to_edit = Label(text="What part would you like to change?")
    where_to_edit.grid(row=1, column=1, padx=10, pady=10)

    details_button = Button(root, text = "Details", command = lambda: add_details(vol, True, result, 
        where_to_edit, details_button, hours_button, dates_button))
    details_button.grid(row=2, column=0, padx=10, pady=10)

    hours_button = Button(root, text = "Hours", command = lambda: add_hours(vol, result, True, 
        where_to_edit, details_button, hours_button, dates_button))
    hours_button.grid(row=2, column=1, padx=10, pady=10)

    dates_button = Button(root, text = "Date(s)", command = lambda: make_date_changes(vol, result,
        where_to_edit, details_button, hours_button, dates_button, go_back_button))
    dates_button.grid(row=2, column=2, padx=10, pady=10)

    go_back_button = Button(root, text = "Go back", 
        command = lambda: view_log(vol, None, where_to_edit, details_button, hours_button, dates_button, go_back_button))
    go_back_button.grid(row=3, column=1, padx=10, pady=10)

def make_date_changes(vol, result, *widgets):
    #results = vol.find({"startdate": {"$exists": True}, '_id': result['_id']})
    count = vol.count_documents({"startdate": {"$exists": True}, '_id': result['_id']})
    if count == 0:
        one_day_option(vol, result, True, *widgets)
    else:
        multiple_days_option(vol, result, True, *widgets)

    
"""
Displays the menu where there are two buttons for the user to select from:
1. The user can add a new log record (they have a new experience/activity to add)
2. The user can view their current log (the records that they have at the moment)
"""
def menu(collection, *widgets):

    destroy(*widgets)

    if isinstance(collection, str):
        vol = db[collection]
    else:
        vol = collection

    frame1 = create_frame(0,1)
    
    global menu_label, add_record_1, view_2
    menu_label = Label(frame1, text="MENU")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(frame1, text = "Add a new log record", padx = 50, pady=10, command=lambda: add_details(vol, False, None, menu_label, add_record_1, view_2, frame1))


    add_record_1.grid(row=1, column=1)

    #search_keywords()

    view_2 = Button(frame1, text = "View activity log", padx = 50, pady=10, 
        command = lambda: view_log(vol, menu_label, add_record_1, view_2, frame1))
    view_2.grid(row=2, column=1)


    another_collection_button = Button(frame1, text = "Choose another collection",
     command = lambda: view_which_log(menu_label, add_record_1, view_2, frame1, another_collection_button))
    another_collection_button.grid(row=3, column=1, padx=50, pady=10)

    configure(3, 1)

def main():

    global root, test_label, client, db, vol

    root = Tk()
    root.title("Activity Log")
    root.geometry("700x400")

    #root['bg'] = 'lavender blush'

    client = MongoClient('mongodb://localhost:27017') # connects to a specific port

    # open the database
    db = client["sheets"]
    
    view_which_log()

    root.mainloop()

# calls main
main()
       




#https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
