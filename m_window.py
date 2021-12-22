import tkinter
from tkinter import messagebox
from tkinter import filedialog
from types import NoneType

import open_file_REC
import matplotlib





from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

import ch_window
    

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        self.configure(background='grey')
        self.set_main_menu()
        self.set_matplotlib()

        self.title("Show graph")
        self.geometry("700x500")

        self.data_list=list()
        self.view_osc_number=0
        self.valuewindow=None
        self.view_osc=None

    def set_matplotlib(self):
        # create a figure
        
        self.figure = matplotlib.figure.Figure(figsize=(6, 4), dpi=100)
        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        # create the toolbar
        self.toolbar=NavigationToolbar2Tk(self.figure_canvas, self)
        self.figure.set_facecolor("grey") 
        
        self.figure_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_move)

    
    def set_main_menu(self):
        menubar = tkinter.Menu(self) 
        self.config (menu=menubar)
        file = tkinter.Menu(menubar, tearoff=0)  
        file.add_command(label="Open", command=self.menu_open_file) 
        file.add_separator() 
        file.add_command(label="Exit", command=self.quit) 
        menubar.add_cascade(label="File", menu=file)

        edit = tkinter.Menu(menubar, tearoff=0) 
        edit.add_command(label="Next", command=self.next_osc) 
        edit.add_command(label="Previos", command=self.prev_osc)
        edit.add_separator() 
        edit.add_command(label="Values", command=self.create_window)
        menubar.add_cascade(label="Edit", menu=edit)          
    
        help = tkinter.Menu(menubar, tearoff=0) 
        help.add_command(label="About", command=self.about)  
        menubar.add_cascade(label="Help", menu=help)  
    
        self.config(menu=menubar)

    def prev_osc(self):
        self.view_osc_number-=1
        self.set_osc()

    def next_osc(self):
        self.view_osc_number +=1
        self.set_osc()

    def set_osc(self):
        # if len(self.data_list)==0 : return None
        if self.view_osc_number>len(self.data_list)-1: self.view_osc_number=0
        if self.view_osc_number<0: self.view_osc_number=len(self.data_list)-1
         
        axs = self.figure.axes
        for ax in axs[:]:
            ax.remove()       

        self.figure.legends.clear()
        legend = list()
        self.axes = self.figure.add_subplot()
        # create the barchart
        for lines_in_osc in self.data_list[self.view_osc_number].lines:
            x,y = zip(*lines_in_osc.get_list_of_points())
            self.axes.plot(x,y,color=lines_in_osc.get_color())
            legend.append(lines_in_osc.get_line_name())
        
        
        if self.valuewindow != None:
            try:
                self.valuewindow.table_del() #deltable
                self.valuewindow.new_table_create(len(self.data_list[self.view_osc_number].lines)+1)
                self.set_lines_name_in_table()
            except:
                pass

        self.view_osc=self.data_list[self.view_osc_number]

        self.figure.legend(legend, loc='upper left')

        self.axes.set_facecolor("black")

        self.axes.set_title(self.data_list[self.view_osc_number].get_name())
        self.axes.plot()
        self.figure.canvas.draw_idle()

    def on_move(self, event):
        # get the x and y pixel coords
        x, y = event.x, event.y
        if event.inaxes and self.valuewindow != None:
            legend_y=self.view_osc.get_values(event.xdata)
            for n in range(len(legend_y)):
                try:
                    self.valuewindow.table.set(n+1,1,format(legend_y[n],'.3f'))
                except:
                    pass
                    # self.valuewindow.table.set(n+1,1,'0')

                


    def about(self):
        messagebox.showinfo('Аналізатор', 'Перегляд графіків під Linux, Windows')

    def create_window(self):
        if self.valuewindow != None: self.valuewindow.confirm_delete()
        self.create_table_window()

    def create_table_window(self):
        if self.data_list :
            self.valuewindow = ch_window.ValuesWindow(len(self.data_list[self.view_osc_number].lines)+1)
            self.set_lines_name_in_table()

    def set_lines_name_in_table(self):
        i=0
        for lines_in_osc in self.data_list[self.view_osc_number].lines:
            i+=1
            self.valuewindow.table.set(i,0,lines_in_osc.get_line_name())

        

    def menu_open_file(self): 
        filename=filedialog.askopenfilename(filetypes=[("REC files", ".fg")])
        if filename:
            osc_list=list()
            if open_file_REC.open_file_REC_configuration(filename, osc_list) ==None : return None
            filename=filename[:-2:]+'rec'
            if open_file_REC.open_file_REC(filename,osc_list)==None: return None 
            self.data_list=osc_list
            self.view_osc_number=0
            self.set_osc()
