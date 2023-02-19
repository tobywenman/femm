import tkinter as tk
import re

class app(tk.Tk):

    inputs = ["Torque T", 
              "Magnetic Loading B",
              "Electrical Loading Q",
              "Current Density J",
              "Design flux Density Bmax",
              "Number of pole pairs p",
              "Number of slots q",
              "Outer diameter Do"]

    outputs = ["Split ratio D/Do",
               "Active Diameter D",
               "Active Length L",
               "Tooth width WT",
               "Back iron depth dB",
               "Slot Area As",
               "Slot bottom dia. Ds",
               "Outer diameter Do"]

    def __init__(self):
        super().__init__()

        #add title
        label = tk.Label(text="3 Phase motor design utility")
        label.grid(column=0,columnspan=2)

        #setup input boxes
        vcmd = (self.register(self.inputValidation), '%P') #used to update the validation before it's entered into box
        self.entries = []
        for i in self.inputs:
            label = tk.Label(text=i)
            label.grid(column=0)
            entry = tk.Entry(self,validate="key",validatecommand=vcmd)
            entry.grid(column=0)          
            self.entries.append(entry)

        self.results = []
        row = 1
        for i in self.outputs:
            label = tk.Label(text=i)
            label.grid(column=1,row=row)
            row += 1
            entry = tk.Entry(self,state="disabled")
            entry.grid(column=1,row=row)
            row += 1          
            self.results.append(entry)

        button = tk.Button(text="Compute solution",command=self.enterValues)
        button.grid(column=0,columnspan=2) 

    def enterValues(self):
        for i in self.entries:
            print(i.get())

    def inputValidation(window,newStr):
        return re.search(r"^$|^\d+[.]?\d*$",newStr) != None
        

window = app()  

window.mainloop()