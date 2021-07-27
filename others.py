from imports import *
import global_vars

def create_frame(row_num, col_num):
    frame = LabelFrame(global_vars.root, padx=10, pady=10)
    frame.grid(row=row_num, column=col_num)
    return frame

def configure(row, column):
    if row != None:
        for row_num in range(0, row+1):
            Grid.rowconfigure(global_vars.root, index=row_num, weight=1)

    if column != None:
        for col_num in range(0,column+1):
            Grid.columnconfigure(global_vars.root, index=col_num, weight=1)


"""
Used to help with the "scrolling feature" when viewing the activity log
"""
def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

"""
There are two purposes.
1. Informs the user that the experience/activity record has been successfully added to the database. 
2. The user is then presented with two buttons: one that exits the program and the other takes them back to the menu screen.

Input: 
- The user list that contains the details, additional notes, hour(s), and date(s) 
(note that all have been checked to be valid already). Can also be None if not needed.
- type_of_success: 1 if it's a new entry being added successful, 2 if it's an entry being successfully edited
- Any number of widgets to be destroyed (these widgets are either from one_day_option() or multiple_days_option())

Calls: to_datetime() and menu()
"""
def successful_message(user_list, type_of_success, *widgets):
    from menu_screen import menu
    from dates import to_datetime

    try:
        destroy(*widgets)
        frame1 = create_frame(0,1)
        frame2 = create_frame(1,1)

        if type_of_success == 1: # new entry
            if len(user_list) == 4: # one date ([details, additional notes (others), hours, date(s)])
                vol_record = {"date": user_list[3], "details": user_list[0], "hours": user_list[2], "others": user_list[1] }
            
            else: # ([details, additional notes (others), hours, start date, end date])
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
        back_to_menu_button.place(x=300, y=250)

        # exit option
        exit_button= Button(global_vars.root, text = "Exit", command = lambda: sys.exit()) 
        exit_button.place(x=400, y=250)

        configure(2,1)

    except Exception as e:
        pass

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
Calls: menu()
"""
def no_entries(search, *widgets):
    from menu_screen import menu
    destroy(*widgets)
    frame = create_frame(0,1)

    if search == False: # if no search was done (the collection was empty to begin with)
        no_logs = Label(frame, text = "There are currently no entries in this collection.")
        no_logs.grid(row=1, column=1)
    else: # if the user searched for something, but no results have been returned
        no_logs = Label(frame, text = "No results have been returned based on your search.")
        no_logs.grid(row=1, column=1)

    # allows the user to go back to the menu
    menu_button = Button(global_vars.root, text = "Back to Menu", 
    command = lambda: menu(no_logs, menu_button, frame))
    menu_button.place(x=310, y=250)

    configure(2,1)









# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grids