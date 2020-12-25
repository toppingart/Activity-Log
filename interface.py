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
    print("Is there one date or does it span over more than one day?")
    print("Give some details about the experience.")
    print("How many hours did this take?")

    menu_label.destroy()
    add_record_1.destroy()
    view_2.destroy()


    details_text = Label(root, text="Give some details about the experience.")
    details_text.grid(row=0,column=1,padx=50,pady=10)   
    details_entry = Entry(root)
    details_entry.grid(row=1, column=1,ipadx=70, ipady = 70,padx=50,pady=50)

    submit_button = Button(root, text = "Submit")
    submit_button.grid(row=2, column=1, padx=50,pady=50)

def modify_log():
    pass

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

    view_2 = Button(root, text = "View activity log", padx = 50, pady=10)
    view_2.grid(row=3, column=1)

    print(add_record_1)
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
