import imports
import global_vars
from view import view_which_log

def main():
    global_vars.initialize()

    view_which_log(None)
    global_vars.root.mainloop()

main()
       