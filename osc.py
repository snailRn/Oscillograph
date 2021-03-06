import random

REC_COLORS = {1:'yellow',2:'green',3:'red',4:'purple',5:'blue', 6:'lime',7:'olive'}


def convert_num_color(number:int)->str:
    if number>7:
        return REC_COLORS[number - 7 * int(number//7)]
    else: return REC_COLORS[number]


class Oscillograph():
    """parameters of Oscilloscope graphic's line"""
    def __init__(self,name : str = ''):
        self.name=name
        self.number_of_lines=0
        self.lines=list()

    def add_line(self, osc_line):
        self.lines.append(osc_line)
        self.number_of_lines=len(self.lines)

    def get_line(self, number: int):
        return self.lines[number]
        
    def get_name(self):
        return self.name
    
    def get_values(self, x: float)->list:
        list_of_values= list()
        for line in self.lines:
            list_of_values.append(line.get_value(x))
        return list_of_values
        




class OscillographLine ():
    """parameters of Oscilloscope graphic's line"""
    def __init__(self,name : str = '', number_of_points : int=0, color:int =random.randint(1,7), list_of_points=list()):
        self.line_name=name
        self.number_of_points=number_of_points
        self.color=color
        self.list_of_points=list_of_points

    def set_list_of_points(self, list_of_points: list):
        self.list_of_points=list_of_points

    def get_number_of_points(self)-> int:
        return self.number_of_points
    
    def get_list_of_points(self) -> list:
        return self.list_of_points[:self.number_of_points]
    
    def get_color(self) -> str:
        return convert_num_color(self.color)

    def get_line_name(self) ->str:
        return self.line_name
    
    def get_value(self, x: float)->float:
        for x_point in range(1,len(self.list_of_points)):
            if self.list_of_points[x_point-1][0]<x<self.list_of_points[x_point][0]:
                a=1
                try:
                    a=(self.list_of_points[x_point][1]-self.list_of_points[x_point-1][1])/(self.list_of_points[x_point][0]-self.list_of_points[x_point-1][0])
                except:
                    a=1
                return self.list_of_points[x_point-1][1]+a*(x-self.list_of_points[x_point-1][0])

