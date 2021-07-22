"""
The widgets are destroyed so that the other widgets can be placed on the screen.

Input: Any number of widgets (*args) which will be in a list (input can be a single widget or a list of widgets)
Output: None
"""
def destroy(*widgets):
    for item in widgets:

        if isinstance(item, list):

            for i in item[0]:
                i.destroy()
            continue
        item.destroy()

#https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
