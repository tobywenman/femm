import tkinter as tk
import re, math

class app(tk.Tk):

    inputs = ["Torque T", #0
              "Magnetic Loading B", #1
              "Electrical Loading Q", #2
              "Current Density J", #3
              "Design flux Density Bmax", #4
              "Number of pole pairs p", #5
              "Number of slots q", #6
              "Outer diameter Do"] #7

    defaults = [60,0.8,50000,3,1.4,2,24,0.2]

    outputs = ["Split ratio D/Do",
               "Active Diameter D",
               "Active Length L",
               "Tooth width WT",
               "Back iron depth dB",
               "Slot Area As",
               "Slot bottom dia. Ds"]

    specs = []

    def __init__(self):
        super().__init__()

        #add title
        label = tk.Label(text="3 Phase motor design utility")
        label.grid(column=0,columnspan=2)

        #setup input boxes
        vcmd = (self.register(self.inputValidation), '%P') #used to update the validation before it's entered into box
        self.entries = []
        default = 0
        for i in self.inputs:
            label = tk.Label(text=i)
            label.grid(column=0)
            entry = tk.Entry(self,validate="key",validatecommand=vcmd)
            entry.insert(0,str(self.defaults[default]))
            default += 1
            entry.grid(column=0)          
            self.entries.append(entry)

        self.results = []
        row = 1
        for i in self.outputs:
            label = tk.Label(text=i)
            label.grid(column=1,row=row)
            row += 1
            entry = tk.Entry(self,state="readonly")
            self.results.append(entry)
            entry.grid(column=1,row=row)
            row += 1          
            

        button = tk.Button(text="Compute solution",command=self.enterValues)
        button.grid(column=0)

        row = button.grid_info()["row"]

        button =  tk.Button(text="Clear output",command=self.clearOutput)
        button.grid(column=1,row=row)

    def enterValues(self):
        self.specs = []
        for i in self.entries:
            try:
                self.specs.append(float(i.get()))
            except:
                self.specs.append(i.get())
        self.calcDo()

    def inputValidation(window,newStr):
        return re.search(r"^$|^\d+[.]?\d*$",newStr) != None
    
    def setOutput(self,entry,output):
        entry.config(state="normal")
        entry.delete(0,tk.END)
        entry.insert(0,str(output))
        entry.config(state="readonly")

    def clearOutput(self):
        for i in self.results:
            i.config(state="normal")
            i.delete(0,tk.END)
            i.config(state="readonly")


    def calcDo(self):
        p = self.specs[5]
        B = self.specs[1]
        Bmax = self.specs[4]
        Q = self.specs[2]
        Do = self.specs[7]
        J = self.specs[3]

        J *= 1000*1000

        exp1 = ((1+p)/p)*(B/Bmax)+((2*Q)/(Do*J))
        exp2 = exp1**2
        exp3 = ((1+2*p)/p**2)*((B/Bmax)**2)+(2*B/Bmax)-1
        output = round((exp1 - math.sqrt(exp2-exp3))/exp3,3)

        self.setOutput(self.results[0],output)
        

window = app()  

window.mainloop()