from imports import *
def main():

    global root, client, db, vol, my_canvas

    root = Tk()
    root.title("Activity Log")
    root.geometry("720x400")
    root.resizable(False, False)

    bg=ImageTk.PhotoImage(file="394901.png") # pink and light blue background

    my_canvas = Canvas(root, width=800, height=500)
    my_canvas.grid(row=0, column=1)

    # setting image in canvas
    my_canvas.create_image(0,0, image=bg, tag='img', anchor='nw')

    client = MongoClient('mongodb://localhost:27017') # connects to a specific port

    # open the database
    db = client["activities"]
    
    # starts off by making the user select a collection to view
    view_which_log(None)
    root.mainloop()

main()
       