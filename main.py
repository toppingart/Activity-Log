import imports
import global_vars
from view import view_which_log
from backups import dump, restore

def main():
    global_vars.initialize()
    view_which_log(None) # prompts user to select a collection
    global_vars.root.mainloop()

    path = r'C:\Users\USER\Documents\volunteer'
    #dump(path)
    #restore(path)

main()
       
