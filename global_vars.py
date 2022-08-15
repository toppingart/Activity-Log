from imports import *
 
from os.path import join
import pymongo
from bson.json_util import dumps

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
    if "activities" not in collections_list:
        first_collection = db["first_collection"]
        first_entry = { 'date': datetime.now(), 'details': 'Insert details here', 'hours': 1, 'others': ''}
        first_collection.insert_one(first_entry)


# https://stackoverflow.com/questions/24610484/pymongo-mongoengine-equivalent-of-mongodump
def backup_db(backup_db_dir):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client["activities"]
    collections = db.list_collection_names()

    for i, collection_name in enumerate(collections):
        col = getattr(db,collections[i])
        collection = col.find()
        jsonpath = collection_name + ".json"
        jsonpath = join(backup_db_dir, jsonpath)
        with open(jsonpath, 'wb') as jsonfile:
            jsonfile.write(dumps(collection).encode())


#backup_db('C:\\Users\\USER\\Documents\\volunteer')