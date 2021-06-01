from tkinter import *


def configure(row, column):

    if row != None:
        for row_num in range(0, row+1):
            Grid.rowconfigure(root, index=row_num, weight=1)

    if column != None:
        for col_num in range(0,column+1):
            Grid.columnconfigure(root, index=col_num, weight=1)


root = Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.geometry("700x400")


frame_main = Frame(root, bg="gray")
frame_main.grid(sticky='news')


# Create a frame for the canvas with non-zero row&column weights
frame_canvas = Frame(frame_main)
frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)


# Create a frame to contain the buttons
frame_buttons = Frame(canvas, bg="white")
canvas.create_window((0,0), window=frame_buttons, anchor='nw')

# Add 9-by-5 buttons to the frame
rows = 9
columns = 5
buttons = [[Label() for j in range(columns)] for i in range(rows)]
for i in range(0, 5):
    for j in range(0, 1):
        buttons[i][j] = Button(frame_buttons, text= "a \n b \n c")
        buttons[i][j].grid(row=i, column=j, ipadx=330, ipady=100, pady=50)

# Update buttonsframes idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 1)])
first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
frame_canvas.config(width=buttons[0][j].winfo_width() + vsb.winfo_width(),
                    height=buttons[0][j].winfo_height())

#configure(10,10)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

# Launch the GUI
root.mainloop()


# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grids