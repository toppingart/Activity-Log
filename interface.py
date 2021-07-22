from imports import *
from interface2 import *
from searching import search_keywords, search_with_input
from others import create_frame
import global_vars
from view import view_which_log
#import collections_related


"""
Used to change the date (as a string) to a datetime object.

Input: 
- vol
- the results (dictionaries in a list)
Output: None
"""
def to_datetime(results):

    for result in results:
        date = result['date']
        if isinstance(date,str) and len(date.strip()) == 8:
            #12/02/20
            datetime_obj = datetime.strptime(date, "%m/%d/%y")
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'date': datetime_obj}})

        elif isinstance(date,str) and len(date.strip()) == 19:
            # 12/01/20 - 12/02/20
            start_date = result['date'][:8]
            end_date = result['date'][11:]
            start_datetime = datetime.strptime(start_date, "%m/%d/%y")
            end_datetime = datetime.strptime(end_date, "%m/%d/%y")
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'startdate': start_datetime}})
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'enddate': end_datetime}})



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
def types_of_changes(type_of_change, edited_entry, edited_entry_2, result, *widgets):

    destroy(*widgets)
    
    if type_of_change == 1:
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'details': edited_entry}})
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'others': edited_entry_2}})
        successful_message(None, 2)
    elif type_of_change == 2:
        vol.update_one({'_id': result['_id']}, {'$set': {'hours': edited_entry}})
        successful_message(None, 2)
    elif type_of_change == 3:
        check_date(edited_entry)
        vol.update_one({'_id': result['_id']}, {'$set': {'date': edited_entry}})
        to_datetime([result])
        successful_message(None, 2)
    else:
        check_date(edited_entry[0])
        check_date(edited_entry[1])
        datetime_start = datetime.strptime(edited_entry[0], "%m/%d/%y")
        datetime_end = datetime.strptime(edited_entry[1], "%m/%d/%y")
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'startdate': datetime_start, 'enddate': datetime_end}})



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
def successful_message(user_list, type_of_success, *widgets):

    try:
        destroy(*widgets)
        frame1 = create_frame(0,1)
        frame2 = create_frame(1,1)

        if type_of_success == 1: # new entry
            if len(user_list) == 4: # one date 
                vol_record = {"date": user_list[3], "details": user_list[0], "hours": user_list[2], "others": user_list[1] }
            else:
                vol_record = {"date": user_list[3] + " - " + user_list[4], "details": user_list[0], "hours": user_list[2], "others": user_list[1]}

            global_vars.vol.insert_one(vol_record)
            to_datetime([vol_record])

            success_message = Label(frame1, text = "The record has been successfully added to the database!")
            success_message.grid(row=0, column=1)

        else: # edited entry
            success_message = Label(frame1, text = "The record has been successfully edited!")
            success_message.grid(row=0, column=1)


        # go back to menu option
        back_to_menu_button = Button(global_vars.root, text = "Back to menu", 
        command = lambda: menu(success_message, exit_button, back_to_menu_button, frame1, frame2))
       # back_to_menu_button.grid(row=1, column=1, padx=10, pady=10)
        back_to_menu_button.place(x=300, y=250)

        # exit option
        exit_button= Button(global_vars.root, text = "Exit", command = lambda: sys.exit()) # if pressed, exits the program
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
def all_user_inputs(user_list, *widgets, **days):

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
        successful_message(user_list, 1, *widgets)







def no_entries(search, *widgets):
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
    command = lambda: menu(no_logs, menu_button, frame1))
    #menu_button.grid(row = 2, column = 1, padx=10, pady=10)
    menu_button.place(x=350, y=350)

    configure(2,1)



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
def ask_entry_changes(result, keyword, *widgets):

    destroy(*widgets)

    frame1 = create_frame(0,1)
    frame2 = create_frame(1,1)

    where_to_edit = Label(frame1, text="What part would you like to change?")
    where_to_edit.grid(row=1, column=1, padx=10, pady=10)

    details_button = Button(frame1, text = "Details", command = lambda: add_details(True, result, keyword,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    details_button.grid(row=2, column=0, padx=10, pady=10)

    hours_button = Button(frame1, text = "Hours", command = lambda: add_hours(result, True, None,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    hours_button.grid(row=2, column=1, padx=10, pady=10)

    dates_button = Button(frame1, text = "Date(s)", command = lambda: make_date_changes(result,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    dates_button.grid(row=2, column=2, padx=10, pady=10)

    if keyword != None:
        search = True
    else:
        search = False

    go_back_button = Button(frame1, text = "Go back", 
        command = lambda: view_log(search, keyword, where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    go_back_button.grid(row=3, column=1, padx=10, pady=10)

    additional = Button(global_vars.root, text = "View Additional Notes", 
        command = lambda: view_additional_notes(result, keyword, where_to_edit, details_button, hours_button, dates_button, go_back_button, frame1, frame2, additional))
    additional.place(x=300, y=300)

def view_additional_notes(result, keyword, *widgets):
    destroy(*widgets)

    if len(result['others'].strip()) == 0:
        additional_details = "There are no additional details added."
    else:
        additional_details = result['others']

    additional_notes = Label(global_vars.root, text = "Additional notes:\n\n " + additional_details)
    additional_notes.place(x=global_vars.root.winfo_width()/2 - 50, y=0)

    go_back_button = Button(root, text = "Go back", 
        command = lambda: ask_entry_changes(result, keyword, additional_notes, go_back_button))
    go_back_button.place(x=global_vars.root.winfo_width()/2 - 15, y=global_vars.root.winfo_height() - 50)

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
def make_date_changes(result, *widgets):
    count = global_vars.vol.count_documents({"startdate": {"$exists": True}, '_id': result['_id']})
    if count == 0: # one date
        one_day_option(result, True, *widgets)
    else:
        multiple_days_option(result, True, *widgets)



"""
MAIN
"""
def main():
    global_vars.initialize()

    # starts off by making the user select a collection to view
    view_which_log(None)
    global_vars.root.mainloop()

main()
       