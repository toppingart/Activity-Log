from imports import *

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
