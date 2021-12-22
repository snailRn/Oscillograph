import tkinter
from types import NoneType
#import Tkinter as tk  # for python 2

class SimpleTable(tkinter.Frame):
    def __init__(self, parent, rows=1, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        self.count_columns=columns
        self.count_rows=rows
        
        tkinter.Frame.__init__(self, parent, background="gray")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tkinter.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    
    def delete_widgets(self):
        for row in range(self.count_rows):
            for column in range(self.count_columns):        
                self._widgets[row][column].destroy()
        


class ValuesWindow(tkinter.Toplevel):
    def __init__(self, row_counts :int = 2):
        super().__init__()
        self.title("Values")
        self.geometry("300x100")
        self.attributes('-topmost', True)
        self.table=NoneType

        self.new_table_create(row_counts)

    def confirm_delete(self):
        self.destroy()
    
    def table_set(self, row, column, value):
        self.table.set(row, column, value)
    
    def table_del(self):
        self.table.delete_widgets()
        self.table.destroy()
        self.table = NoneType
    
    def new_table_create(self, rows_count: int):
        if self.table != NoneType: self.table_del()
        self.table = SimpleTable(self, rows_count,2)
        self.table.pack(side="top", fill="x")
        self.table.set(0,0,"Item")
        self.table.set(0,1,"Value")



