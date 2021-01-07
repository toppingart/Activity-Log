from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import sys


print("=======================================================================")
print("ACTIVITY LOG")
print("=======================================================================")

print("MENU:")


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
def search_keywords():
    keyword = '.*stu.*' # wildcard characters in between
    #user_keyword = input('What keyword would you like to search? ')
   # results = vol.find({'details': {'$regex': keyword, '$options': 'i'}})
    results = vol.find({'hours': 0.5, 'details': 'Interact Club Meeting'})
    display_results(results)

def alter_date_format():
    pass
    # https://www.programiz.com/python-programming/datetime/strptime


"""
Used to change the date (as a string) to a datetime object.

Input: the results (dictionaries in a list)
Output: None

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

def add_details():

    menu_label.destroy()
    add_record_1.destroy()
    view_2.destroy()


    details_text = Label(root, text="Give some details about the experience.")
    details_text.grid(row=0,column=1,padx=50,pady=10)   
    details_entry = Entry(root)
    details_entry.grid(row=1, column=1,ipadx=70, ipady = 70,padx=50,pady=50)

    submit_button = Button(root, text = "Submit", command = lambda: add_hours(details_entry.get(), details_text, details_entry, submit_button))
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

    hours_text = Label(root, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(root)
    hours_entry.grid(row=1, column=1,ipadx=10, ipady = 10,padx=50,pady=50)

    submit_button = Button(root, text = "Submit", 
        command = lambda: add_dates(user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button))
    submit_button.grid(row=2, column=1, padx=50,pady=50)


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
  
    dates_text = Label(root, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    # first option the user can select 
    one_day_button = Button(root, text = "One day", 
        command = lambda: one_day_option(user_list, dates_text, one_day_button, m_days_button))

    one_day_button.grid(row=2, column=1, padx=50,pady=50)

    # second option the user can select 
    m_days_button = Button(root, text = "Multiple days", 
        command = lambda: multiple_days_option(user_list, dates_text, one_day_button, m_days_button))

    m_days_button.grid(row=3, column=1, padx=50, pady=50)



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

    day_text = Label(root, text = "What day did this take place (eg. 25/12/2020) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(root) # textbox
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    submit_button = Button(root, text = "Submit", 
        command = lambda: all_user_inputs(user_list, day_text, day_entry, submit_button, date = day_entry.get()))
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

def multiple_days_option(user_list, *widgets):

    destroy(*widgets)

    days_text = Label(root, text = "What days did this take place (eg. 25/12/2020 - 01/01/2021)" )
    days_text.grid(row=0,column=1,padx=50,pady=10)

    start_day_text = Label(root, text = "Start date:")
    start_day_text.grid(row=1,column=1, padx=50, pady=10)

    start_day_entry = Entry(root)
    start_day_entry.grid(row=2,column=1,padx=50,pady=10)

    end_day_text = Label(root, text = "End date:")
    end_day_text.grid(row=3, column=1, padx=50, pady=10)

    end_day_entry = Entry(root)
    end_day_entry.grid(row=4, column=1, padx=50, pady=10)


    submit_button = Button(root, text = "Submit", 
        command = lambda: all_user_inputs(user_list, days_text, start_day_text, end_day_text, 
            start_day_entry, end_day_entry, submit_button, 
            startdate = start_day_entry.get(), enddate = end_day_entry.get()))


    submit_button.grid(row=5, column=1, padx=50,pady=50)

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
2. The user is then presented with two buttons: one that exists the program and the other takes them back to the menu screen.

Input: Any number of widgets to be destroyed (these widgets are either from one_day_option() or multiple_days_options() )
Output: None

"""

def successful_message(*widgets):

    destroy(*widgets)

    success_message = Label(root, text = "The record has been successfully added to the database!")
    success_message.grid(row=1, column=1)

    # exit option
    exit_button= Button(root, text = "Exit", command = lambda: sys.exit()) # if pressed, exits the program
    exit_button.grid(row=2, column = 1)

    # go back to menu option
    back_to_menu_button = Button(root, text = "Back to menu", 
        command = lambda: menu(success_message, exit_button, back_to_menu_button))
    back_to_menu_button.grid(row=3, column=1)


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
        successful_message(*widgets)

    #except NameError:
      #  messagebox.showerror("Dates Error", "Please enter a valid date.")

    except Exception:
        # messagebox.showerror("Dates Error", "Please fill in both the start date and end date.")
        return

  #  except Exception as e:
   #     print(e)
    #    messagebox.showerror("Dates Error", "Please fill in both the start date and end date.")
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

"""
**NEEDS TO BE CHANGED. CURRENTLY DISPLAYS ONE RECORD (AND OTHER CHANGES...SEE BELOW)

The date(s), details of the experience/activity, and the hour(s) are displayed on the screen.
The user can click on the PREVIOUS and NEXT buttons to look through their records. 

Input: 
- Any number of widgets to be destroyed (from menu())
- skip_num: the record that will be displayed

Output: None

"""

def view_log(*widgets, skip_num=0):

    destroy(*widgets)


    # **ADD PREVIOUS BUTTON
    # ** ADD SEARCH KEYWORDS (maybe in different function?)
   
    try:
        #results = vol.find().skip(skip_num).limit(1)
        results = vol.find({'hours': 0.5, 'details': 'Interact Club Meeting'}).skip(skip_num).limit(1)
        row_num = 0

        for result in results:
            skip_num +=1

            date = Label(root, text = result['date'] if isinstance(result['date'], str) else result['date'].strftime("%d/%m/%Y"))
            date.grid(row=row_num, column=1, padx=10, pady=10)
            row_num +=1

            details = Label(root, text = "Details: " + result['details'])
            details.grid(row = row_num, column =1, padx=10, pady=10)
            row_num +=1

            hours = Label(root, text = "Hours: " + str(result['hours']))
            hours.grid(row = row_num, column=1, padx=10, pady=10)
            row_num +=1

        # ** HANDLE ERROR ONCE USER REACHES THE END
        next_button = Button(root, text = "Next", command = lambda: view_log(date, details, hours, next_button, skip_num = skip_num))
        next_button.grid(row = row_num, column=2, padx=10, pady=10)

        # ValueError: skip must be >= 0
        previous_button = Button(root, text = "Previous", 
        command = lambda: view_log(date, details, hours, previous_button, next_button, skip_num = skip_num - 2))
        previous_button.grid(row = row_num, column=1, padx=10, pady=10)


    except ValueError: # there are no "previous" posts to display (the user is currently viewing the first post)

        # widgets have already been destroyed when the button is clicked (does not need to be added again)
        # the default value of skip_num is 0
        view_log() 


    # {'_id': ObjectId('5fe2adc955957e2ab04be27c'), 'date': datetime.datetime(2017, 8, 24, 0, 0), 'details': 'Principal Breakfast Volunteer', 'hours': 3}

"""
Displays the menu where there are two buttons for the user to select from:
1. The user can add a new log record (they have a new experience/activity to add)
2. The user can view their current log (the records that they have at the moment)
"""
def menu(*widgets):

    destroy(*widgets)
    
    global menu_label, add_record_1, view_2
    menu_label = Label(root, text="MENU")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(root, text = "Add a new log record", padx = 50, pady=10, command=lambda: add_details())
    add_record_1.grid(row=2, column=1)

    #search_keywords()

    view_2 = Button(root, text = "View activity log", padx = 50, pady=10, 
        command = lambda: view_log(menu_label, add_record_1, view_2))
    view_2.grid(row=3, column=1)



def main():


    global root, test_label, client, db, vol

    root = Tk()
    root.title("Activity Log")
    root.geometry("700x400")

 
    client = MongoClient('mongodb://localhost:27017') # connects to a specific port
    # open the database
    db = client["sheets"]

    # opens the collection that is in the database
    vol = db["volunteer"]


    results = vol.find()

    menu()
    #test_label.pack()
    root.mainloop()

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


