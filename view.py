from interface2 import *
from imports import *
import global_vars
import searching


"""
The date(s), details of the experience/activity, and the hour(s) are displayed on the screen.

Input: 
- Any number of widgets to be destroyed (from menu())

Output: None
Calls: access_collection(), create_new_collection() or search_keywords()
"""

def view_which_log(filter_col, *widgets):
    import collections_related

    destroy(*widgets)

    choose_col = Label(global_vars.root, text = "Which collection would you like to look at?", font="Helvetica 18 bold")
    choose_col.place(relx=0.5, rely=0, anchor="n")

    if filter_col == None:
        collection_list = list(global_vars.db.list_collection_names())
        collection_list.sort()
    else:
        collection_list = filter_col

    selected_option = StringVar()

    combo_box = ttk.Combobox(global_vars.root, values=collection_list, state="readonly")
    combo_box.config(height=5)
    combo_box.place(x=250, y=100)
    combo_box.current(0)

  
    new_col = Button(global_vars.root, text = "Add new collection instead", command = lambda: collections_related.create_new_collection(choose_col, combo_box, new_col, search_col, access_button))
    new_col.place(x=150, y=330)


    search_col = Button(global_vars.root, text = "Search for collections by keyword", 
        command = lambda: searching.search_keywords(True,choose_col, combo_box, new_col, search_col, access_button))
    search_col.place(x=380, y=330)


    access_button = Button(global_vars.root, text = "Access this collection", command = lambda: collections_related.access_collection(combo_box.get(), choose_col, combo_box, new_col,
        search_col, access_button))
    access_button.place(x=250, y=150)


    #configure(5,5)


    """
Allows the user to see the entries displayed, and they are able to scroll through them and make edits, if necessary.

Input:
- vol
- search: True if we want to allow the user to search using keywords (display the search entrybox, etc), False otherwise.
- keyword: keyword used to search, otherwise None
- *widgets

Output: None
Calls: search_keywords(), ask_entry_changes() or menu()
"""

def view_log(search, keyword=None, *widgets):

    destroy(*widgets)

    # if keyword is None and we want to allow the user to search
    if not isinstance(keyword,str) and search == True:
        search_keywords(False, *widgets)

    # user has searched but no search results popped up
    elif search == True and vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}}) == 0:
        no_entries(True)

    try:
        # if we don't want searching (or if the user has already searched before), then go ahead and display the results
        if not search:
            if isinstance(keyword, str): # if a keyword has been given by the user
                results = global_vars.vol.find({'details': {'$regex': keyword, '$options': 'i'}}) # has all the results
                count = global_vars.vol.count_documents({'details': {'$regex': keyword, '$options': 'i'}}) # number of entries (documents)

                if count == 0: # no entries
                    no_entries(True)

            elif keyword == None: # viewing all
                results = global_vars.vol.find()
                count = global_vars.vol.estimated_document_count()

                if count == 0: # no entries
                    no_entries(False)

            if (count >= 1): # 1 or more entries

                results = results.sort([("date", 1), ("startdate", 1)])

                row_num = 0
                frame_main = Frame(global_vars.my_canvas, width=800, height=400, bg='light pink')
                frame_main.grid(row=0, column=1, sticky='news')

                global_vars.my_canvas.create_window((0,0), window=frame_main, anchor='nw')#, width=750)
        
                frame_main.grid_rowconfigure(0, weight=1)
                frame_main.grid_columnconfigure(0, weight=1)
                
                # Create a frame for the canvas with non-zero row&column weights
                frame_canvas = Frame(frame_main)
                frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
                frame_canvas.grid_rowconfigure(0, weight=1)
                frame_canvas.grid_columnconfigure(0, weight=1)
                # Set grid_propagate to False to allow 5-by-5 buttons resizing later
                frame_canvas.grid_propagate(False)

                # Add a canvas in that frame
                canvas = Canvas(frame_canvas, bg="lavender blush")
                canvas.grid(row=0, column=0, sticky="news")


                # Link a scrollbar to the canvas
                vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
                vsb.grid(row=0, column=1, sticky='ns')
                canvas.configure(yscrollcommand=vsb.set)
                bg=ImageTk.PhotoImage(file="394901.png")
                canvas.create_image(0,0, image=bg, tag='img', anchor='nw')

                # Create a frame to contain the buttons
                frame_buttons = Frame(canvas, bg='lavender blush')


                # Set image in canvas
                canvas.create_window((0,0), window=frame_buttons, anchor='nw')

                # allows you to use arrow keys
                canvas.bind("<Up>",    lambda event: canvas.yview_scroll(-1, "units"))
                canvas.bind("<Down>",  lambda event: canvas.yview_scroll( 1, "units"))
           
                canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int((event.delta / 120)), "units"))
                canvas.focus_set()
                canvas.bind("<1>", lambda event: self.canvas.focus_set())
                
                # Add 9-by-5 buttons to the frame
                rows = count 
                columns = 1
                buttons = [[Button() for j in range(columns)] for i in range(rows)]
                
                for i in range(0, rows):
                    if global_vars.vol.count_documents({"startdate": {"$exists": True}, '_id': results[i]['_id']}) == 1 :
                        date_display = results[i]['startdate'].strftime('%m/%d/%y') + ' - ' + results[i]['enddate'].strftime('%m/%d/%y')
                    elif isinstance(results[i]['date'], str):
                        date_display = results[i]['date']
                    else:
                        date_display = results[i]['date'].strftime('%m/%d/%y')

                    for j in range(0, columns):
                        buttons[i][j] = Button(frame_buttons, bg = 'white', fg='black', font="Helvetica 9", height = 10, width=10, 
                            text= 'date: ' + date_display + '\n' + 
                            'details: ' + results[i]['details'].strip('\n') + '\n' + 'hours: ' + str(results[i]['hours']),
                            command = lambda i=i: ask_entry_changes(results[i], keyword, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))
                        buttons[i][j].grid(row=i, column=j, ipadx=310, ipady=50,pady=50)

                # Update buttonsframes idle tasks to let tkinter calculate buttons sizes
                frame_buttons.update_idletasks()

                # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
                first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, columns)])
                first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, rows)])
                frame_canvas.config(width=buttons[0][j].winfo_width() + vsb.winfo_width(),
                                        height=buttons[0][j].winfo_height())

                # Set the canvas scrolling region
                canvas.config(scrollregion=canvas.bbox("all"))

                
                search_keywords_button = Button(global_vars.root, text = "Search using keywords instead", 
                    command = lambda: search_keywords(False, buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, 
                        menu_button, search_keywords_button))

                search_keywords_button.place(x=280, y=350)

                menu_button = Button(global_vars.root, text = "Menu", 
                    command = lambda: menu(buttons, frame_main, frame_canvas, canvas, vsb, frame_buttons, menu_button, search_keywords_button))
                menu_button.place(x=350, y=300)
                
    except Exception as e:
        print(e)


#global_vars.initialize()