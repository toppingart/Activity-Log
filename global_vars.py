from imports import *
 
import pymongo


def initialize(): 
    global root, client, db, vol, my_canvas

    root = Tk()
    root.title("Activity Log")
    root.geometry("720x400")
    root.resizable(False, False) # does not allow resizing

    my_canvas = Canvas(root, width=800, height=500)
    my_canvas.grid(row=0, column=1)

    client = MongoClient('mongodb://localhost:27017') # connects to a specific port

    # open the database
    db = client["activities"]

    collections_list = db.list_collection_names()
    if len(collections_list) == 0:
        first_collection = db["first_collection"]
        first_entry = { 'date': datetime.now(), 'details': 'Insert details here', 'hours': 1, 'others': ''}
        first_collection.insert_one(first_entry)


# https://stackoverflow.com/questions/24610484/pymongo-mongoengine-equivalent-of-mongodump


#backup_db('C:\\Users\\USER\\Documents\\volunteer')