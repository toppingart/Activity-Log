from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import sys

# maybe do data visualization stuff with this later? see how much you volunteer over time or on certain periods


"""
The results of the database is displayed (when the user chooses to view the activity log)

Input: a list of the result(s)
Output: None

"""
def display_results(results):
    for index, result in enumerate(results, start = 1):
        print('Result', index)

        date = result['date']
        print('DATE: ', date[:10]) if isinstance(date, str) and len(date) == 24 else print('DATE: ', date)
        print('DETAILS: ', result['details'])
        print('NUMBER OF HOURS: ', result['hours'], '\n')

def sort_by_factor():
    pass

"""
The user enters one or more keywords to narrow down the results (when looking for a specific record).

Input: None
Output: None

"""
def search_keywords(vol, *widgets):
    destroy(*widgets)

    frame1 = create_frame()

    search_label = Label(frame1, text="What would you like to search for?")
    search_label.grid(row=0, column=1, padx=10, pady=10)

    search_entry = Entry(frame1)
    search_entry.grid(row=1, column=1, padx=10, pady=10)

    submit = Button(frame1, text = "Submit", command = lambda: search_with_input(vol, search_entry.get(), search_label, search_entry, submit, view_all, frame1))
    submit.grid(row=2, column=1, padx=10, pady=10)

    view_all = Button(frame1, text = "View all instead", command = lambda: view_log(vol, None, search_label, search_entry, submit, view_all, frame1))
    view_all.grid(row=3, column=1, padx=10, pady=10)

    configure(3,1)
   # keyword = '.*stu.*' # wildcard characters in between
   # keyword = '*'+ search_entry.get() + '*'
    #print(keyword)
    #user_keyword = input('What keyword would you like to search? ')
   # results = vol.find({'details': {'$regex': keyword, '$options': 'i'}})
   # results = vol.find({'hours': 0.5, 'details': 'Interact Club Meeting'})
    #display_results(results)

def search_with_input(vol, entry, *widgets):
    destroy(*widgets)

    # example: results = db.collections.find({'my_key': {'$regex': '.*2019.*'}})
    keyword = '.*' + entry + '.*'
   
    #results = vol.find({'hours': 0.5})
    results = vol.find({'details': {'$regex': keyword, '$options': 'i'}})
    view_log(vol, keyword, *widgets)
   # display_results(results)

def alter_date_format():
    pass
    # https://www.programiz.com/python-programming/datetime/strptime


"""
Used to change the date (as a string) to a datetime object.

Input: the results (dictionaries in a list)
Output: None

# ** CHANGE TO USE FOR CURRENT TASK (changing the strings to datetime before adding it into the database in successful_message())

"""
def to_datetime(results):
    for result in results:
        date = result['date']
        if isinstance(date,str) and len(date) == 10:
            datetime_obj = datetime.strptime(date, "%d/%m/%Y")
            vol.update_one({'_id': result['_id']}, {'$set': {'date': datetime_obj}})

        elif isinstance(date,str) and len(date) == 23:
            start_date = result['date'][:10]
            end_date = result['date'][14:]
            start_datetime = datetime.strptime(start_date, "%d/%m/%Y")
            end_datetime = datetime.strptime(end_date, "%d/%m/%Y")
            vol.update_one({'_id': result['_id']}, {'$set': {'startdate': start_datetime}})
            vol.update_one({'_id': result['_id']}, {'$set': {'enddate': end_datetime}})


"""
The user enters some details about their experience.

Input: None
Output: None

Note: The user exits this function when the SUBMIT button is pressed (the user is then sent to add_hours())
"""

def add_details(*widgets):

    for widget in widgets:
        destroy(widget)

    frame1 = LabelFrame(root, padx=10, pady=10)
    frame1.grid(row=0, column=0)

    details_text = Label(frame1, text="Give some details about the experience.")
    details_text.grid(row=0,column=1,padx=50,pady=10)   
    details_entry = Text(frame1, width=30, height=10)
    details_entry.grid(row=1, column=1)

    submit_button = Button(frame1, text = "Submit", command = lambda: add_hours(details_entry.get('1.0', 'end'), details_text, details_entry, submit_button, frame1))
    submit_button.grid(row=2, column=1, padx=50,pady=50)

    #add_hours(details_text, submit_button)
    # add_dates()


"""
The widgets are destroyed so that the other widgets can be placed on the screen.

Input: Any number of widgets (*args) which will be in a list
Output: None

"""
def destroy(*widgets):
    for item in widgets:
        item.destroy()


"""
The user is asked to enter the number of hours of their experience (how long did their volunteering/activity take?)

Input: the details of the experience (as a string), any number of widgets that was on the screen when the user 
was asked to enter the details (all the widgets from the add_details())

Output: None

"""

def add_hours(details, *widgets):


    if len(details.strip()) == 0:
        messagebox.showerror("Details Error", "Please enter some details.")
        return

    user_input_list = [details] # obtained from add_details()
    destroy(*widgets)

    frame1 = LabelFrame(root)
    frame1.grid(row=0, column=1, padx=10, pady=10)

    hours_text = Label(frame1, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(frame1)
    hours_entry.grid(row=1, column=1,padx=50,pady=50)

    submit_button = Button(frame1, text = "Submit", 
        command = lambda: add_dates(user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button, frame1))
    submit_button.grid(row=2, column=1, padx=50,pady=50)

    Grid.columnconfigure(root, index=1, weight=1)

    Grid.rowconfigure(root, index=0, weight=1)
    Grid.rowconfigure(root, index=1, weight=1)
    Grid.rowconfigure(root, index=2, weight=1)


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

def add_dates(user_list, hours,*widgets):

    try:
        int(hours) # checks if an integer has been entered 
    except:
        messagebox.showerror("Hours Error", "Please enter a number for your hours.")
        return # exits the function (so that the user can enter the number of hours again)

    destroy(*widgets)
    user_list.append(hours) # if hours is an int (is valid), it is added to the list of user inputs

    frame1 = create_frame()
  
    dates_text = Label(frame1, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    # first option the user can select 
    one_day_button = Button(frame1, text = "One day", 
        command = lambda: one_day_option(user_list, dates_text, one_day_button, m_days_button, frame1))

    one_day_button.grid(row=1, column=1, padx=50,pady=50)

    # second option the user can select 
    m_days_button = Button(frame1, text = "Multiple days", 
        command = lambda: multiple_days_option(user_list, dates_text, one_day_button, m_days_button, frame1))

    m_days_button.grid(row=2, column=1, padx=50, pady=50)

    configure(2, 1)


def configure(row, column):

    if row != None:
        for row_num in range(0, row+1):
            Grid.rowconfigure(root, index=row_num, weight=1)

    if column != None:
        for col_num in range(0,column+1):
            Grid.columnconfigure(root, index=col_num, weight=1)


def create_frame():
    frame1 = LabelFrame(root, padx=10, pady=10)
    frame1.grid(row=0, column=1)
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
def one_day_option(user_list, *widgets):

    destroy(*widgets)

    frame1 = create_frame()

    day_text = Label(frame1, text = "What day did this take place (eg. 25/12/2020) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(frame1) # textbox
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(user_list, day_text, day_entry, submit_button, frame1, date = day_entry.get()))
    submit_button.grid(row=2, column=1, padx=50,pady=50)

    configure(2, 1)


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

def multiple_days_option(user_list, *widgets):

    destroy(*widgets)

    frame1 = create_frame()

    days_text = Label(frame1, text = "What days did this take place (eg. 25/12/2020 - 01/01/2021)" )
    days_text.grid(row=0,column=1,padx=50,pady=10)

    start_day_text = Label(frame1, text = "Start date:")
    start_day_text.grid(row=1,column=1, padx=50, pady=10)

    start_day_entry = Entry(frame1)
    start_day_entry.grid(row=2,column=1,padx=50,pady=10)

    end_day_text = Label(frame1, text = "End date:")
    end_day_text.grid(row=3, column=1, padx=50, pady=10)

    end_day_entry = Entry(frame1)
    end_day_entry.grid(row=4, column=1, padx=50, pady=10)


    submit_button = Button(frame1, text = "Submit", 
        command = lambda: all_user_inputs(user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, frame1,
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))


    submit_button.grid(row=5, column=1, padx=50,pady=50)

    configure(5,1)

"""
Checks if the date entered by the user is a valid date (valid day, month, and year).

Input: the date (as a string)
Output: None

"""

def check_date(date):
    try:
        if len(date.strip()) == 10:
            check_date = datetime.strptime(date, "%d/%m/%Y") 
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Date(s) Error", "Check that the date(s) you have entered are valid.")
        raise Exception

"""
There are two purposes.
1. Informs the user that the experience/activity record has been successfully added to the database. 
2. The user is then presented with two buttons: one that exits the program and the other takes them back to the menu screen.

Input: 
- The user list that contains the details, hour(s), and date(s) (note that all have been checked to be valid already)
- Any number of widgets to be destroyed (these widgets are either from one_day_option() or multiple_days_options())
Output: None

"""

def successful_message(user_list, *widgets):

  

    if len(user_list) == 3: # date (2017-07-31T00:00:00.000+00:00), detail, hours
        vol_record = {"date": user_list[2], "details": user_list[0], "hours": user_list[1] }
    else: # date ("02/08/2017 - 04/08/2017"), detail, hours, startdate, enddate
        pass

   # vol_record = {"details"}
    vol.insert_one(vol_record)
    # ['a', '1', '25/12/2020']
    # ['a', '1', '25/12/2020', '01/01/2021']
    # rental = {"member_renting": ("Saeed", "7806808181"), "movie_rented": movie_ids[1]}

    destroy(*widgets)

    frame1 = create_frame()


    success_message = Label(frame1, text = "The record has been successfully added to the database!")
    success_message.grid(row=0, column=1)

    # exit option
    exit_button= Button(frame1, text = "Exit", command = lambda: sys.exit()) # if pressed, exits the program
    exit_button.grid(row=1, column = 1)

    # go back to menu option
    back_to_menu_button = Button(root, text = "Back to menu", 
        command = lambda: menu(success_message, exit_button, back_to_menu_button))
    back_to_menu_button.grid(row=2, column=1)

    configure(2,1)


"""
There are two purposes.
1. If the date(s) are valid (which will be checked in this function), the date(s) will be added to the user_list 
(that contains the details and the hours)

2. Once the date is determined to be valid, the record is added to the database. (**INCORPORATE)

REMINDER: the details and the hours are valid (as they have been checked before)

"""

def all_user_inputs(user_list, *widgets, **days):

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
        successful_message(user_list, *widgets)

    except NameError:
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

    frame1 = LabelFrame(root, padx=5, pady=5)
    frame1.grid(row=0, padx=10, pady=10)

    frame2 = LabelFrame(root, padx=5, pady=5)
    frame2.grid(row=1, padx=10, pady=10)

    choose_years = Label(frame1, text = "Which year would you like to look at? \n Enter your option by typing in the number")
    choose_years.grid(row = 1, column =1, padx=10, pady=10)

    # show the collections that are available 
    row_num = 2;
    col_names = ""

    year_buttons = []
    button_num = 0
    for collection in db.list_collection_names():
        # command= lambda s=somevariable: printout(s)) 
        # https://stackoverflow.com/questions/49082862/create-multiple-tkinter-button-with-different-command-but-external-variable
        b = Button(frame2, text = collection, command = lambda collection_name = collection: access_collection(year_buttons, collection_name, choose_years, new_year, frame1, frame2))
        b.grid(row=2, column=button_num, padx=10, pady=10)
        year_buttons.append(b)
        Grid.columnconfigure(root, index=button_num, weight=1)
        button_num +=1



    #display_cols = Label(root, text = col_names)
    #display_cols.grid(row=row_num, column=2, padx=10, pady=10)
        

    #collection_input = Entry(root)
    #collection_input.grid(row=row_num+1, column=2, padx=10, pady=10)
   

    new_year = Button(frame2, text = "Add new year instead", command = lambda: create_new_collection(year_buttons, choose_years, new_year, frame1, frame2))
    new_year.grid(row=2, column=button_num, padx=10, pady=10)

    Grid.rowconfigure(root, index=0, weight=1)
    Grid.rowconfigure(root, index=1, weight=1)
    Grid.rowconfigure(root, index=2, weight=1)

def access_collection(button_list, collection_name, *widgets):

    for button in button_list:
        destroy(button)

    destroy(*widgets)
    menu(collection_name)
    


def view_log(vol, keyword=None, *widgets, skip_num=0):

    # otherwise !label
    
    destroy(*widgets)
    destroy(menu_label)

    if keyword == None:
        pass
    elif not isinstance(keyword,str):
        search_keywords(vol, *widgets)

    
    

    frame1 = create_frame()
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

            for result in results:
               # print(result)


                skip_num +=1

                if isinstance(result['date'], str):
                    date_display = result['date']
                elif isinstance(result['date'], datetime):
                    date_display = result['date'].strftime("%d/%m/%Y")
                else:
                    print('LOL')
                    date_display = ''

                date = Label(frame1, text = date_display)
                #date = Label(root, text = result['date'] if isinstance(result['date'], str) else result['date'].strftime("%d/%m/%Y"))
                date.grid(row=row_num, column=1, padx=10, pady=10)
                row_num +=1

                details = Label(frame1, text = "Details: " + result['details'])
                details.grid(row = row_num, column =1, padx=10, pady=10)
                row_num +=1

                hours = Label(frame1, text = "Hours: " + str(result['hours']))
                hours.grid(row = row_num, column=1, padx=10, pady=10)
                row_num +=1

            #print(date)
            # ** HANDLE ERROR ONCE USER REACHES THE END NameError: free variable 'date' referenced before assignment in enclosing scope
            next_button = Button(frame1, text = "Next", command = lambda: view_log(vol, keyword, date, details, hours, previous_button, next_button, skip_num = skip_num))
            next_button.grid(row = row_num, column=2, padx=10, pady=10)

            # ValueError: skip must be >= 0
            previous_button = Button(frame1, text = "Previous", 
            command = lambda: view_log(vol, keyword, date, details, hours, previous_button, next_button, skip_num = skip_num - 2))
            previous_button.grid(row = row_num, column=1, padx=10, pady=10)


            edit_entry_button = Button(frame1, text = "Edit Entry")
            edit_entry_button.grid(row=6, column=7, padx=10, pady=10)

            # if the user changes their mind and wants to return to menu
            menu_button = Button(frame1, text = "Menu", 
                command = lambda: menu(date, details, hours, previous_button, next_button, menu_button, edit_entry_button))
            menu_button.grid(row = 5, column = 5, padx=10, pady=10)

            search_keywords_button = Button(frame1, text = "Search log", command = lambda: search_keywords(vol, next_button, previous_button, edit_entry_button, search_keywords_button, date, details, hours))
            search_keywords_button.grid(row=6, column=5, padx=10, pady=10)

            if count == 0:
                no_logs = Label(root, text="No search results have appeared. Try something else.") 
                destroy(previous_button, menu_button, edit_entry_button, search_keywords_button)
                no_logs.grid(row=1, column=1, padx=10, pady=10)

                search_again = Button(root, text="Search again", command = lambda: search_keywords(vol, no_logs, search_again))
                search_again.grid(row=2, column=1, padx=10,pady=10)


            if skip_num == count:
                destroy(next_button)
            elif skip_num == 1:
                destroy(previous_button)

    except NameError as f:
        print(f)

    except ValueError: # there are no "previous" posts to display (the user is currently viewing the first post)
        # widgets have already been destroyed when the button is clicked (does not need to be added again)
        # the default value of skip_num is 0
        view_log() 
    #  except Exception as e:
    #     print(e)
    
# {'_id': ObjectId('5fe2adc955957e2ab04be27c'), 'date': datetime.datetime(2017, 8, 24, 0, 0), 'details': 'Principal Breakfast Volunteer', 'hours': 3}
    
"""
Displays the menu where there are two buttons for the user to select from:
1. The user can add a new log record (they have a new experience/activity to add)
2. The user can view their current log (the records that they have at the moment)
"""
def menu(collection, *widgets):

    destroy(*widgets)

    vol = db[collection]

    frame1 = create_frame()
    
    global menu_label, add_record_1, view_2
    menu_label = Label(frame1, text="MENU")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(frame1, text = "Add a new log record", padx = 50, pady=10, command=lambda: add_details(menu_label, add_record_1, view_2, frame1))


    add_record_1.grid(row=1, column=1)

    #search_keywords()

    view_2 = Button(frame1, text = "View activity log", padx = 50, pady=10, 
        command = lambda: view_log(vol, menu_label, add_record_1, view_2, frame1))
    view_2.grid(row=2, column=1)

    configure(2, 1)

def main():

    global root, test_label, client, db, vol
    

    root = Tk()
    root.title("Activity Log")
    root.geometry("700x400")

   # root.columnconfigure(0,weight=1)    #confiugures column 0 to stretch with a scaler of 1.
   # root.rowconfigure(0,weight=1)

 
    client = MongoClient('mongodb://localhost:27017') # connects to a specific port
    # open the database
    db = client["sheets"]
    
   # while view_which_log() != None:
    view_which_log()
   #     print(a)

    # opens the collection that is in the database
    #vol = db["volunteer"]
   # menu()
   # results = vol.find()
    
    #menu()
    #test_label.pack()

    root.mainloop()

# calls main
main()
       
#start = datetime(2016, 12, 20)
#a = vol.find_one({'startdate': {'$gt': start}})
#print(a)
#display_results(a)

# 5fe2adc955957e2ab04be289
# 22/09/2017

#print(len("04/09/2017 - 05/09/2017"))
# 23
# test(results)
