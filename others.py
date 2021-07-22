from tkinter import *
import global_vars

def create_frame(row_num, col_num):
    frame1 = LabelFrame(global_vars.root, padx=10, pady=10)
    frame1.grid(row=row_num, column=col_num)
    return frame1


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
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))



# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grids