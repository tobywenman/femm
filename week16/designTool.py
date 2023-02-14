import tkinter as tk
import re

class app(tk.Tk):

    def __init__(self):
        super().__init__()
        label = tk.Label(text="3 Phase motor design utility")
        label.pack()
        vcmd = (self.register(self.inputValidation), '%P') #used to update the validation before it's entered into box
        entry = tk.Entry(self,width=50,validate="key",validatecommand=vcmd)
        entry.pack()

    def inputValidation(window,newStr):
        return re.search(r"^$|^\d+[.]?\d*$",newStr) != None
        

window = app()  

window.mainloop()