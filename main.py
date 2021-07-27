import imports
import global_vars
from view import view_which_log

def main():
    global_vars.initialize()

    view_which_log(None) # prompts user to select a collection
    global_vars.root.mainloop()

main()
       
