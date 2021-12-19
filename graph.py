import tkinter
from tkinter import messagebox
from tkinter import filedialog

import open_file
import matplotlib


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
    

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        self.configure(background='grey')
        self.set_main_menu()
        self.set_matplotlib()

        self.title("Show graph")
        self.geometry("700x500")

        self.data_list=list()
        self.view_line=0

    def set_matplotlib(self):
        # create a figure
        
        self.figure = matplotlib.figure.Figure(figsize=(6, 4), dpi=100)
        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        # create the toolbar
        self.toolbar=NavigationToolbar2Tk(self.figure_canvas, self)
        self.figure.set_facecolor("grey") 
        
        self.figure_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    
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
 
         
        menubar.add_cascade(label="Edit", menu=edit)          
    
        help = tkinter.Menu(menubar, tearoff=0) 
        help.add_command(label="About", command=self.about)  
        menubar.add_cascade(label="Help", menu=help)  
    
        self.config(menu=menubar)

    def set_osc(self,osc_list : list):
        self.data_list=osc_list
        # create axes
        self.view_line=-1
        self.next_osc()

    def prev_osc(self):
        self.view_line=self.view_line-2
        self.next_osc()

    def next_osc(self):
        self.view_line +=1
        if self.view_line>len(self.data_list)-1: self.view_line=0
        if self.view_line<0: self.view_line=len(self.data_list)-1
         

        
        axs = self.figure.axes
        for ax in axs[:]:
            ax.remove()       
        

        self.figure.legends.clear()
        legend = list()
        self.axes = self.figure.add_subplot()
        # create the barchart
        for lines_in_osc in self.data_list[self.view_line].lines:
            x,y = zip(*lines_in_osc.get_list_of_points())
            self.axes.plot(x,y,color=lines_in_osc.get_color())
            legend.append(lines_in_osc.get_line_name())

        self.figure.legend(legend, loc='upper left')

        
        self.axes.set_facecolor("black")
        self.axes.set_title(self.data_list[self.view_line].get_name())

      
        self.axes.plot()

        self.figure.canvas.draw_idle()
        

    


    def about(self):
        messagebox.showinfo('Аналізатор', 'Перегляд графіків під Linux')

    def menu_open_file(self): 
        filename=filedialog.askopenfilename(filetypes=[("REC files", ".fg")])
        osc_list=open_file.open_file_REC_configuration(filename)
        filename=filename[:-2:]+'rec'
        open_file.open_file_REC(filename,osc_list)
        self.set_osc(osc_list)



if __name__ == '__main__':
    main_app = App()
    main_app.mainloop()
