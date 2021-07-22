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

def add_details(edited, details, keyword, *widgets):

    destroy(*widgets)
    frame1 = create_frame(0,0)
    frame2 = create_frame(0,1)
    frame3 = create_frame(1,1)

    details_text = Label(frame2, text="Give some details about the experience.")
    details_text.grid(row=0,column=0,padx=30,pady=10)   
    details_entry = Text(frame2, width=30, height=10, wrap=WORD)
    details_entry.grid(row=1, column=0)

    others_text = Label(frame2, text="Any additional notes? [OPTIONAL]")
    others_text.grid(row=0,column=1,padx=50,pady=10)   
    others_entry = Text(frame2, width=30, height=10, wrap=WORD)
    others_entry.grid(row=1, column=1)

    configure(3, 1)

    if not edited:
        go_back_button = Button(globals.root, text = "Go back", 
            command = lambda: menu(details_text, details_entry, submit_button, frame1, frame2, frame3, go_back_button))
        go_back_button.place(x=250, y=350)

        if isinstance(details, list):
            details_entry.insert(INSERT, details[0])
            others_entry.insert(INSERT, details[1])

        submit_button = Button(globals.root, text = "Submit All", 
           command = lambda: add_hours(details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), None, False, 
            details_text, details_entry, submit_button, frame1, frame2, frame3, go_back_button))
        submit_button.place(x=350, y=350)

    else: # if the user is making edits to their entry

        go_back_button = Button(globals.root, text = "Go back", 
            command = lambda: ask_entry_changes(details, keyword, go_back_button, details_text, details_entry, submit_button, frame1, frame2, frame3))
        go_back_button.place(x=300, y=350)

        details_entry.insert(INSERT, details['details'])
        others_entry.insert(INSERT, details['others'])


        submit_button = Button(globals.root, text = "Submit All", 
            command = lambda: types_of_changes(1, details_entry.get('1.0', 'end'), others_entry.get('1.0', 'end'), details, details_text, details_entry, submit_button, go_back_button, frame1, frame2, frame3))
        submit_button.place(x=400, y=350)



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
def add_hours(details, others, input_hours, edited, *widgets):

    # error handling
    if isinstance(details, str) and len(details.strip()) == 0:
        messagebox.showerror("Details Error", "Please enter some details.")
        return

    destroy(*widgets)
    frame1 = LabelFrame(globals.root)
    frame1.grid(row=0, column=1, padx=10, pady=10)

    hours_text = Label(frame1, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(frame1)
    hours_entry.grid(row=1, column=1,padx=50,pady=50)

    if edited == False:

        user_input_list = [details, others] # obtained from add_details()

        if input_hours != None:
            hours_entry.insert(INSERT, input_hours)

        submit_button = Button(globals.root, text = "Submit", 
            command = lambda: add_dates(user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button, frame1, go_back_button))

        # add_details(vol, edited, details, keyword, *widgets)
        go_back_button = Button(globals.root, text="Go back", command = lambda: add_details(False, user_input_list, None, hours_text,hours_entry,
            submit_button, frame1, go_back_button))

    else: # happens if the user wants to make edits to their entry (not a new entry)
        hours_entry.insert(INSERT, details['hours'])
        submit_button = Button(globals.root, text = "Submit",
            command = lambda: types_of_changes(2, hours_entry.get(), None, details, hours_text, hours_entry, submit_button, frame1, go_back_button))


        go_back_button = Button(globals.root, text="Go back", command = lambda: ask_entry_changes(details, None, hours_text,hours_entry,
            submit_button, frame1, go_back_button))

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
- user_list: a list of the user's inputs so far (which in this case, would be the details and the hours)
- hours: the user's input - ideally as an int, but will be checked if it is an integer
- *widgets

Output: None
Calls: one_day_option() or multiple_days_option()
"""
def add_dates(user_list, hours,*widgets):

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
        command = lambda: one_day_option(user_list, False, dates_text, one_day_button, m_days_button, frame1,
            go_back_button))
    one_day_button.grid(row=1, column=1, padx=50,pady=10)

    m_days_button = Button(frame1, text = "Multiple days", 
        command = lambda: multiple_days_option(user_list, False, dates_text, one_day_button, m_days_button, frame1,
            go_back_button))
    m_days_button.grid(row=2, column=1, padx=50, pady=10)

    go_back_button = Button(globals.root, text="Go back", command = lambda: add_hours(user_list[0], user_list[1], hours, False, 
        dates_text, one_day_button, m_days_button, frame1, go_back_button))
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

    frame1 = create_frame(0,1)
    configure(2, 1)

    day_text = Label(frame1, text = "What day did this take place (eg. 12/25/20) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(frame1) # textbox
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    if not edited:
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(user_list, day_text, day_entry, submit_button, frame1, go_back_button, date = day_entry.get()))
        submit_button.grid(row=2, column=1, padx=50,pady=10)

        go_back_button = Button(globals.root, text = "Go back", 
        command = lambda: add_dates(user_list, user_list[2], day_text, day_entry, submit_button, frame1, go_back_button))
    else:

        day_entry.insert(INSERT, user_list['date'].strftime('%m/%d/%y'))
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(3, day_entry.get(), None, user_list, day_text, day_entry, submit_button, frame1, go_back_button))
        submit_button.grid(row=2, column=1, padx=50,pady=10)

        go_back_button = Button(globals.root, text="Go back", command = lambda: ask_entry_changes(user_list, None, day_text, day_entry,
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
def multiple_days_option(user_list, edited, *widgets):

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
        command = lambda: all_user_inputs(user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1, go_back_button,
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))
        submit_button.grid(row=5, column=1, padx=50,pady=10)

        go_back_button = Button(globals.root, text = "Go back", 
        command = lambda: add_dates(user_list, user_list[2], start_day_entry, end_day_entry, submit_button, frame1, go_back_button))
        

    else:
        start_day_entry.insert(INSERT, user_list['startdate'].strftime('%m/%d/%y'))
        end_day_entry.insert(INSERT, user_list['enddate'].strftime('%m/%d/%y'))
        submit_button = Button(frame1, text = "Submit", 
        command = lambda: types_of_changes(4, [start_day_entry.get(), end_day_entry.get()], None, user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1, go_back_button))
        submit_button.grid(row=5, column=1, padx=50,pady=10)

        go_back_button = Button(globals.root, text="Go back", command = lambda: ask_entry_changes(user_list, None, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1, go_back_button))

    go_back_button.place(x=335, y=350)