import interface

def create_frame():
    frame1 = LabelFrame(root, padx=10, pady=10)
    frame1.grid(row=0, column=1)
    return frame1