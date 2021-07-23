from imports import *
from others import *
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
