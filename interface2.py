
import globals

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

def create_frame(row_num, col_num):
    frame1 = LabelFrame(globals.root, padx=10, pady=10)
    frame1.grid(row=row_num, column=col_num)
    return frame1

def destroy(*widgets):

    for item in widgets:

        if isinstance(item, list):
            for i in item[0]:
                i.destroy()
            continue

        item.destroy()

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
    





#https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
