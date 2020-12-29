from pymongo import MongoClient
from tkinter import * # will be used to create graphical user interface later
from datetime import datetime



print("=======================================================================")
print("ACTIVITY LOG")
print("=======================================================================")

print("MENU:")
def display_results(results):
    for index, result in enumerate(results, start = 1):
        print('Result', index)
        print('DATE: ', result['date'])
        print('DETAILS: ', result['details'])
        print('NUMBER OF HOURS: ', result['hours'], '\n')

def sort_by_factor():
    pass

def search_keywords():
    keyword = '.*stu.*' # wildcard characters in between
    #user_keyword = input('What keyword would you like to search? ')
    results = vol.find({'details': {'$regex': keyword, '$options': 'i'}})

    display_results(results)

def alter_date_format():
    pass
    # https://www.programiz.com/python-programming/datetime/strptime


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

def destroy(*widgets):
    for item in widgets:
        item.destroy()

def add_hours(details, *widgets):

    user_input_list = [details] # obtained from add_details()
    destroy(*widgets)

    hours_text = Label(root, text = "How many hours did this take?")
    hours_text.grid(row=0,column=1,padx=50,pady=10)

    hours_entry = Entry(root)
    hours_entry.grid(row=1, column=1,ipadx=10, ipady = 10,padx=50,pady=50)

    submit_button = Button(root, text = "Submit", 
        command = lambda: add_dates(user_input_list, hours_entry.get(), hours_text, hours_entry, submit_button))
    submit_button.grid(row=2, column=1, padx=50,pady=50)

def add_dates(user_list, hours,*widgets):

    destroy(*widgets)

    user_list.append(hours)
  

    dates_text = Label(root, text = "Did this take place over the span of one day or multiple days?")
    dates_text.grid(row=0,column=1,padx=50,pady=10)

    one_day_button = Button(root, text = "One day", 
        command = lambda: one_day_option(user_list, dates_text, one_day_button, m_days_button))
    one_day_button.grid(row=2, column=1, padx=50,pady=50)

    m_days_button = Button(root, text = "Multiple days", 
        command = lambda: multiple_days_option(user_list, dates_text, one_day_button, m_days_button))

    m_days_button.grid(row=3, column=1, padx=50, pady=50)

def one_day_option(user_list, *widgets):

    destroy(*widgets)

    day_text = Label(root, text = "What day did this take place (eg. 25/12/2020) ")
    day_text.grid(row=0,column=1,padx=50,pady=10)

    day_entry = Entry(root)
    day_entry.grid(row=1,column=1,padx=50,pady=10)

    submit_button = Button(root, text = "Submit", 
        command = lambda: all_user_inputs(user_list, day_text, day_entry, submit_button, date = day_entry.get()))
    submit_button.grid(row=2, column=1, padx=50,pady=50)



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
            startdate = start_day_entry.get(), enddate = end_day_entry.get() ))


    submit_button.grid(row=5, column=1, padx=50,pady=50)

def all_user_inputs(user_list, *widgets, **days):

    destroy(*widgets)

    # add date(s)
    for key, value in days.items():
        if key == "date":
            user_list.append(value)
        else:
            user_list.append(days["startdate"])
            user_list.append(days["enddate"])
            break

    print(user_list)
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

def view_log():
    # tdl (to do later): add previous and next buttons
    # fix - one date also shows 00:00:00
    results = vol.find().limit(5)
    for result in results:
       # date = Label(root, text = result['date'].strftime("%m/%d/%Y"))
        print(result['date'])

    # {'_id': ObjectId('5fe2adc955957e2ab04be27c'), 'date': datetime.datetime(2017, 8, 24, 0, 0), 'details': 'Principal Breakfast Volunteer', 'hours': 3}

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

    global menu_label, add_record_1, view_2
    menu_label = Label(root, text="MENU")
    menu_label.grid(row=0,column=1,padx=50,pady=10)    

    add_record_1 = Button(root, text = "Add a new log record", padx = 50, pady=10, command=lambda: add_details())
    add_record_1.grid(row=2, column=1)

    print(add_record_1)

    view_2 = Button(root, text = "View activity log", padx = 50, pady=10, command = lambda: view_log())
    view_2.grid(row=3, column=1)

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

