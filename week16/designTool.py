import tkinter as tk
import re

class app(tk.Tk):

    inputs = ["Torque T", 
              "Magnetic Loading B",
              "Electrical Loading Q",
              "Current Density J",
              "Design flux Density Bmax",
              "Number of pole pairs p"
              "Number of slots q",
              "Outer diameter Do"]

    def __init__(self):
        super().__init__()

        #add title
        label = tk.Label(text="3 Phase motor design utility")
        label.pack()

        #setup input boxes
        vcmd = (self.register(self.inputValidation), '%P') #used to update the validation before it's entered into box
        self.entries = []
        for i in self.inputs:
            label = tk.Label(text=i)
            label.pack()
            entry = tk.Entry(self,width=50,validate="key",validatecommand=vcmd)
            entry.pack()            
            self.entries.append(entry)

        button = tk.Button(text="Compute solution",command=self.enterValues)
        button.pack()

    def enterValues(self):
        for i in self.entries:
            print(i.get())

    def inputValidation(window,newStr):
        return re.search(r"^$|^\d+[.]?\d*$",newStr) != None
        

window = app()  

window.mainloop()