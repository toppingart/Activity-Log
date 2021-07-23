from imports import *
import global_vars
from view import view_which_log

#import collections_relateds


"""
MAIN
"""
def main():
    global_vars.initialize()

    # starts off by making the user select a collection to view
    view_which_log(None)
    global_vars.root.mainloop()

main()
       