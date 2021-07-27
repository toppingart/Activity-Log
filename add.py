from imports import *
from others import *
from changes import *
"""
The user enters some details about their experience, and any additional notes about that experience.

Input: 
- edited: True if the user is editing this entry. False if it is a new entry.
- details: None if it's a new entry. Otherwise, it contains the information about the edited entry 
(eg. {'_id': ObjectId('60ceae4fb431e4027d400b1d'), 'date': datetime.datetime(2018, 1, 12, 0, 0), 
'details': 'Green Team (Collected bottles in the social department))', 'hours': 0.5, 'others': ''})
- *widgets

Calls: add_hours() or types_of_changes()
"""
def add_details(edited, details, keyword, *widgets):

    from menu_screen import menu

    destroy(*widgets)
    frame = create_frame(0,1)

    details_text = Label(frame, text="Give some details about the experience.")
    details_text.grid(row=0,column=0,padx=30,pady=10)   
    details_entry = Text(frame, width=30, height=10, wrap=WORD)
    details_entry.grid(row=1, column=0)

    others_text = Label(frame, text="Any additional notes? [OPTIONAL]")
    others_text.grid(row=0,column=1,padx=50,pady=10)   
    others_entry = Text(frame, width=30, height=10, wrap=WORD)
    others_entry.grid(row=1, column=1)

    configure(1, 1)

    if not edited:
        go_back_button = Button(global_vars.root, text = "Go back", 
            command = lambda: menu(details_text, details_entry, submit_button, frame, go_back_button))
        go_back_button.place(x=250, y=350)

        # if the user decides to go back from adding hours to adding details, 
        # we can insert what was written in the details before.
        if isinstance(details, list): 
            details_entry.insert(INSERT, details[0])
            others_entry.insert(INSERT, details[1])

        submit_button = Button(global_vars.root, text = "Submit All", 
           command = lambda: add_hours(details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), None, False, 
            details_text, details_entry, submit_button, frame, go_back_button))
        submit_button.place(x=350, y=350)

    else: # if the user is making edits to their entry

        go_back_button = Button(global_vars.root, text = "Go back", 
            command = lambda: ask_entry_changes(details, keyword, go_back_button, details_text, details_entry, submit_button, frame))
        go_back_button.place(x=300, y=350)

        # inserts what was previously written into the entry box
        details_entry.insert(INSERT, details['details'])
        others_entry.insert(INSERT, details['others'])

        submit_button = Button(global_vars.root, text = "Submit All", 
            command = lambda: types_of_changes(1, details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), details, 
                details_text, details_entry, submit_button, go_back_button, frame))
        submit_button.place(x=400, y=350)

"""
The user is asked to enter the number of hours of their experience (how long did their volunteering/activity take?)

Input: 
- details: details of the experience (as a string) OR a dictionary with all stored information (eg. {details: ..., hours: ...})
- others: additional notes about that experience (as a string)
- input_hours (int): used to save the number of hours entered (if the user goes back from adding dates to adding hours). 
None otherwise.
- edited: False if it is a new entry. True otherwise.
- *widgets (NOTE: all the widgets are from the add_details())

Calls: add_dates() or types_of_changes()
"""
def add_hours(details, others, input_hours, edited, *widgets):

    # error handling
    if isinstance(details, str) and len(details.strip()) == 0:
        messagebox.showerror("Details Error", "Please enter some details.")
        return

    destroy(*widgets)

    frame = LabelFrame(global_vars.root)
    frame.grid(row=0, column=1, padx=10, pady=10)

    hours_text = Label(frame, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(frame)
    hours_entry.grid(row=1, column=1,padx=50,pady=50)

    if edited == False:

        user_input_list = [details, others] # obtained from add_details()

        if input_hours != None:
            hours_entry.insert(INSERT, input_hours)

        submit_button = Button(global_vars.root, text = "Submit", 
            command = lambda: add_dates(user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button, frame, go_back_button))

        # add_details(vol, edited, details, keyword, *widgets)
        go_back_button = Button(global_vars.root, text="Go back", command = lambda: add_details(False, user_input_list, None, hours_text,hours_entry,
            submit_button, frame, go_back_button))

    else: # happens if the user wants to make edits to their entry (not a new entry)
        hours_entry.insert(INSERT, details['hours'])
        submit_button = Button(global_vars.root, text = "Submit",
            command = lambda: types_of_changes(2, hours_entry.get(), None, details, hours_text, hours_entry, submit_button, frame, go_back_button))

        go_back_button = Button(global_vars.root, text="Go back", command = lambda: ask_entry_changes(details, None, hours_text,hours_entry,
            submit_button, frame, go_back_button))

    submit_button.place(x=380, y=300)
    go_back_button.place(x=280, y=300)

    configure(2, 1)

"""
There are two purposes:
1. Checks if the hours that the user has entered is valid (is an integer), otherwise the user will 
be asked to enter their hours again.

2. If the hours that the user has entered is valid, then the user will be asked to select if their experience/activity
spans over a day or multiple days by clicking one of the buttons.

Input: 
- vol
- user_list: a list of the user's inputs so far (which in this case, 
would be [details, additional notes]
- hours: the user's input - ideally as an int, but will be checked if it is an integer
- *widgets

Calls: one_day_option() or multiple_days_option()
"""
def add_dates(user_list, hours,*widgets):
    try:
        if '.' in hours: # checks if hours is an int or a float
            convert_hours = float(hours)
        else:
            convert_hours = int(hours)
    except:
        messagebox.showerror("Hours Error", "Please enter a number for your hours.")
        return # exits the function (so that the user can enter the number of hours again)

    destroy(*widgets)

    user_list.append(convert_hours) # if hours is an int or a float (is valid), it is added to the list of user inputs

    frame = create_frame(0,1)
  
    dates_text = Label(frame, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    one_day_button = Button(frame, text = "One day", 
        command = lambda: one_day_option(user_list, False, dates_text, one_day_button, m_days_button, frame,
            go_back_button))
    one_day_button.grid(row=1, column=1, padx=50,pady=10)

    m_days_button = Button(frame, text = "Multiple days", 
        command = lambda: multiple_days_option(user_list, False, dates_text, one_day_button, m_days_button, frame,
            go_back_button))
    m_days_button.grid(row=2, column=1, padx=50, pady=10)

    go_back_button = Button(global_vars.root, text="Go back", command = lambda: add_hours(user_list[0], user_list[1], hours, False, 
        dates_text, one_day_button, m_days_button, frame, go_back_button))
    go_back_button.place(x=330, y=300)

    configure(3, 1)

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
def one_day_option(user_list, edited, *widgets):

    destroy(*widgets)

    frame = create_frame(0,1)
    configure(2, 1)

    day_text = Label(frame, text = "What day did this take place (eg. 12/25/20) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(frame) # textbox
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    if not edited:
        submit_button = Button(frame, text = "Submit", 
        command = lambda: all_user_inputs(user_list, day_text, day_entry, submit_button, frame, go_back_button, date = day_entry.get()))
        submit_button.grid(row=2, column=1, padx=50,pady=10)

        go_back_button = Button(global_vars.root, text = "Go back", 
        command = lambda: add_dates(user_list, user_list[2], day_text, day_entry, submit_button, frame, go_back_button))
    else:

        day_entry.insert(INSERT, user_list['date'].strftime('%m/%d/%y'))
        submit_button = Button(frame, text = "Submit", 
        command = lambda: types_of_changes(3, day_entry.get(), None, user_list, day_text, day_entry, submit_button, frame, go_back_button))
        submit_button.grid(row=2, column=1, padx=50,pady=10)

        go_back_button = Button(global_vars.root, text="Go back", command = lambda: ask_entry_changes(user_list, None, day_text, day_entry,
            submit_button, frame, go_back_button))

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
def multiple_days_option(user_list, edited, *widgets):

    destroy(*widgets)

    frame = create_frame(0,1)
    configure(5,1)

    days_text = Label(frame, text = "What days did this take place (eg. 12/25/20 - 01/01/21)" )
    days_text.grid(row=0,column=1,padx=50,pady=10)

    start_day_text = Label(frame, text = "Start date:")
    start_day_text.grid(row=1,column=1, padx=50, pady=10)

    start_day_entry = Entry(frame)
    start_day_entry.grid(row=2,column=1,padx=50,pady=10)

    end_day_text = Label(frame, text = "End date:")
    end_day_text.grid(row=3, column=1, padx=50, pady=10)

    end_day_entry = Entry(frame)
    end_day_entry.grid(row=4, column=1, padx=50, pady=10)

    if not edited:
        submit_button = Button(frame, text = "Submit", 
        command = lambda: all_user_inputs(user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame, go_back_button,
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))
        submit_button.grid(row=5, column=1, padx=50,pady=10)

        go_back_button = Button(global_vars.root, text = "Go back", 
        command = lambda: add_dates(user_list, user_list[2], start_day_entry, end_day_entry, submit_button, frame, go_back_button))
        

    else:
        start_day_entry.insert(INSERT, user_list['startdate'].strftime('%m/%d/%y'))
        end_day_entry.insert(INSERT, user_list['enddate'].strftime('%m/%d/%y'))
        submit_button = Button(frame, text = "Submit", 
        command = lambda: types_of_changes(4, [start_day_entry.get(), end_day_entry.get()], None, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame, go_back_button))
        submit_button.grid(row=5, column=1, padx=50,pady=10)

        go_back_button = Button(global_vars.root, text="Go back", command = lambda: ask_entry_changes(user_list, None, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame, go_back_button))

    go_back_button.place(x=335, y=350)



"""
There are two purposes.
1. If the date(s) are valid (which will be checked in this function), the date(s) will be added to the user_list 
(that contains the details and the hours)

2. Once the date is determined to be valid, the record is added to the database (using successful_message())

NOTE: the details and the hours are valid (as they have been checked before)

Calls: check_date() and successful_message()

"""
def all_user_inputs(user_list, *widgets, **days):
    from dates import check_date
    from others import successful_message

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

                if (datetime.strptime(days['startdate'], "%m/%d/%y") >= (datetime.strptime(days['enddate'], "%m/%d/%y"))):
                    raise ValueError

                #['ad\n', '\n', 5]
                if len(user_list) == 3: # already contains the details, others, hours
                    user_list.append(days["startdate"]) # if statement prevents startdate from being added again



                if len(user_list) == 4: # already contains details, others, hours, and startdate
                    user_list.append(days["enddate"]) # if statement prevents enddate from being added again
                break

    except ValueError as v:
        print(v)
        messagebox.showerror("Dates Error", "Please enter valid date(s)")

    except Exception as e:
        print(e)
        messagebox.showerror("Dates Error", "Please fill in both the start date and end date.")

    else:
        successful_message(user_list, 1, *widgets)


