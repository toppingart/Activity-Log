from imports import *
from others import *

"""
Takes the user to the appropiate method depending on if they want to edit one date or two dates (start and end date)

Input:
- result 
(eg. {'_id': ObjectId('60ceae4fb431e4027d400b1d'), 'date': datetime.datetime(2018, 1, 12, 0, 0), 'details': 'Green Team (Collected bottles in the social department))', 'hours': 0.5, 'others': ''}
- *widgets

Calls: one_day_option() or multiple_days_option()
"""
def make_date_changes(result, *widgets):
    from add import one_day_option, multiple_days_option
    count = global_vars.vol.count_documents({"startdate": {"$exists": True}, '_id': result['_id']})
    if count == 0: # one date
        one_day_option(result, True, *widgets)
    else:
        multiple_days_option(result, True, *widgets)

"""
Asks the user what part of their entry they would like to change.

Input:
- result: 
(eg. {'_id': ObjectId('60b4418688db9bce7b378c09'), 'date': datetime.datetime(2020, 12, 27, 0, 0), 'details': 'aa\n', 'hours': '1'})
- *widgets

Calls: add_details() or add_hours() or make_date_changes() or view_log()
"""
def ask_entry_changes(result, keyword, *widgets):
    from add import add_details, add_hours
    from view import view_log, view_additional_notes
    from changes import make_date_changes

    destroy(*widgets)

    frame = create_frame(0,1)

    where_to_edit = Label(frame, text="What part would you like to change?")
    where_to_edit.grid(row=1, column=1, padx=10, pady=10)

    details_button = Button(frame, text = "Details", 
        command = lambda: add_details(True, result, keyword,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, 
        frame, additional, delete_entry_button))
    details_button.grid(row=2, column=0, padx=10, pady=10)

    hours_button = Button(frame, text = "Hours", command = lambda: add_hours(result, None, None,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, 
        frame, additional, delete_entry_button))
    hours_button.grid(row=2, column=1, padx=10, pady=10)

    dates_button = Button(frame, text = "Date(s)", command = lambda: make_date_changes(result,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, 
        frame, additional, delete_entry_button))
    dates_button.grid(row=2, column=2, padx=10, pady=10)

   
    go_back_button = Button(frame, text = "Go back", 
        command = lambda: view_log(False, keyword, where_to_edit, details_button, hours_button, dates_button, 
            go_back_button, frame, additional, delete_entry_button))
    go_back_button.grid(row=3, column=1, padx=10, pady=10)

    additional = Button(global_vars.root, text = "View Additional Notes", 
        command = lambda: view_additional_notes(result, keyword, where_to_edit, details_button, hours_button, 
            dates_button, go_back_button, frame, additional, delete_entry_button))
    additional.place(x=300, y=300)

    delete_entry_button = Button(global_vars.root, text = "Delete this entry", command = lambda: delete_entry(result, keyword,
        where_to_edit, details_button, hours_button, dates_button, go_back_button, frame, additional, delete_entry_button))
    delete_entry_button.place(x=300, y=350)



def delete_entry(result,keyword, *widgets):
    from view import view_log
    
    answer = messagebox.askyesno("Delete Entry", "Are you sure you want to delete this entry?")
    if answer == True:
        global_vars.vol.delete_one({'_id': result['_id']})
        view_log(False, keyword, *widgets) # user is prompted to select another collection



"""
Will take the appropiate action depending on what part ot the entry the user wants to make edits to

input:
- type_of_change:  details - 1, hours- 2, date - 3, dates (start and end date) - 4 (int)
- edited_entry: edits made by the user (str)
- edited_entry_2: another edited entry (used for the additional notes). If there's no additional notes, then it will be None.
- result: (eg. {'_id': ObjectId('60b4418688db9bce7b378c09'), 'date': datetime.datetime(2020, 12, 27, 0, 0), 'details': 'aa\n', 'hours': '1'})
- *widgets

Calls: successful_message(), check_date(), to_datetime()
"""
def types_of_changes(type_of_change, edited_entry, edited_entry_2, result, *widgets):
    from dates import check_date, to_datetime

    destroy(*widgets)
    
    if type_of_change == 1: # edit details
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'details': edited_entry}})
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'others': edited_entry_2}})
        successful_message(None, 2)

    elif type_of_change == 2: # edit hours
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'hours': edited_entry}})
        successful_message(None, 2)

    elif type_of_change == 3: # edit single date
        check_date(edited_entry)
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'date': edited_entry}})
        to_datetime([result])
        successful_message(None, 2)

    else: # edit two dates
        check_date(edited_entry[0])
        check_date(edited_entry[1])
        datetime_start = datetime.strptime(edited_entry[0], "%m/%d/%y")
        datetime_end = datetime.strptime(edited_entry[1], "%m/%d/%y")
        global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'startdate': datetime_start, 'enddate': datetime_end}})



