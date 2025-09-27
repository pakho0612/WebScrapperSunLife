import tkinter as tk
import re
from readDeposit import readAllDeposits, readTable
from src.dataClass import Deposits


from readDeposit import readAllDeposits
class dateEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.dateText = "YYYY/MM/DD"

        self.dateVar = tk.StringVar()
        self.dateVar.set(self.dateText)
        self.dateVar.trace_add("write", self.onChange)
        self.config(validate="key", textvariable=self.dateVar)

        self.bind("<FocusIn>", self.onFocusIn)
        self.bind("<FocusOut>", self.onFocusOut)

    def onFocusIn(self, event):
        if not self.validateDate():
            self.delete(0, tk.END)

    def onFocusOut(self, event):
        if not self.validateDate():
            self.delete(0, tk.END)
            self.insert(0, self.dateText)

    def onChange(self, *args):
        if not self.dateVar.get().isdigit() and self.dateVar.get() != self.dateText:
            self.dateVar.set(self.dateVar.get()[:-1]) ## remove last inserted character

    def validateDate(self):
        ## date must be YYYYmmdd
        if len(self.dateVar.get()) == 8 and self.dateVar.get().isdigit():
            return True
        return False
    
    def getValue(self):
        return self.dateVar.get()

class numEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.numVar = tk.StringVar()
        self.numVar.trace_add("write", self.onChange)
        self.config(validate="key", textvariable=self.numVar)

    def onChange(self, *args):
        if not self.validateFloat():
            self.numVar.set(self.numVar.get()[:-1]) ## remove last inserted character

    def validateFloat(self):
        if re.match(r'^\d*\.?\d*$', self.numVar.get()) != None:
            return True
        return False
    
    def getValue(self):
        return float(self.numVar.get())
    
class resultBoxes():
    def __init__(self, tkFrame):
        self.boxes = []
        self.frame = tkFrame

    def setResult(self, results):
        if results is not None:
            for deposit in results:
                if isinstance(deposit, Deposits):
                    box = tk.Text(self.frame)
                    box.insert(tk.END, deposit.detailToString())
                    self.boxes.append((box, deposit))
                else:
                    return TypeError("Invalid deposit result to set")
        else:
            box = tk.Text(self.frame)
            box.insert(tk.END, "No results found")
            self.boxes.append((box, None))

    def clearResults(self):
        for box in self.boxes:
            box[0].destroy()
        self.boxes = []

    def renderBox(self):
        for box, deposit in self.boxes:
            box.grid(pady=5)

    def setBoxes(self, results):
        ## render search results to result box
        self.clearResults()
        self.setResult(results)
        self.renderBox()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SunLife Claim Search")

        self.urlLabel = tk.Label(self, text="SunLife URL:")
        self.urlLabel.grid(row=0, column=0, padx=2)
        self.urlVar = tk.StringVar()
        self.urlEntry = tk.Entry(self, textvariable=self.urlVar)
        self.urlEntry.grid(row=0, column=1, pady=5)

        self.startDateLabel = tk.Label(self, text="Start Date:")
        self.startDateLabel.grid(row=1, column=0, padx=2)
        self.startDateEntry = dateEntry(self)
        self.startDateEntry.grid(row=1, column=1, pady=5)

        self.endDateLabel = tk.Label(self, text="End Date:")
        self.endDateLabel.grid(row=2, column=0, padx=2)
        self.endDateEntry = dateEntry(self)
        self.endDateEntry.grid(row=2, column=1, pady=5)

        self.amountLabel = tk.Label(self, text="Amount:")
        self.amountLabel.grid(row=3, column=0, padx=2)
        self.amountEntry = numEntry(self)
        self.amountEntry.grid(row=3, column=1, pady=5)

        self.confirmButton = tk.Button(self, text="Confirm", command=self.handleConfirm)
        self.confirmButton.grid(row=4, columnspan=2, pady=5)

        self.resultBox = resultBoxes(self)

    def handleConfirm(self):
        # Handle the confirm button click
        if self.startDateEntry.validateDate() and self.endDateEntry.validateDate()and self.urlVar.get() != "" and self.amountEntry.validateFloat():
            print(self.startDateEntry.getValue(), self.endDateEntry.getValue())
            print(self.amountEntry.getValue())
            tables = readTable(self.urlVar.get())
            allDeposits = readAllDeposits(tables.values)
            results = allDeposits.searchTotal(int(self.startDateEntry.getValue()), int(self.endDateEntry.getValue()), float(self.amountEntry.getValue()))
            self.resultBox.setBoxes(results)
            
        else:
            print("Invalid date Input")
    

if __name__ == "__main__":
    app = App()
    app.mainloop()

