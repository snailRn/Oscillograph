from types import NoneType
import osc
import struct

rec_names = ('I, A','U, B','','','',('CM','Uf','If','ID','IQ'),('CM','D'),('CM','S','Me','Mt'),
                ('AM','ID','ID'),('AM','S','Me','Mt'),('AM','n','Md'),'*U, B','F')

def REC_name_from_int(type: int, number: int =0)-> str:
    if type in range(5,11): return rec_names[type][number]
    return rec_names[type]

def open_file_REC(filename :str,osc_list:list) -> list:
    try:
        f = open(filename, "rb")
        
        max_point=0
        n_lines = 0
        list_of_points=list()
        
        for n_osc in osc_list:
            n_lines +=1
            for n_of_line in n_osc.lines:
                n_lines +=1
                if n_of_line.get_number_of_points()>max_point: max_point=n_of_line.get_number_of_points()
        
        for line in range(n_lines):
            list_of_points.append(list())
        for point in range(max_point):
            for line in range(n_lines):
                list_of_points[line].append(struct.unpack('f',f.read(4))[0])

        n_line = 0
        for n_osc in osc_list:
            time_line=list_of_points[n_line]
            n_line +=1
            for n_of_line in n_osc.lines:
                n_of_line.set_list_of_points(list(zip(time_line,list_of_points[n_line])))
                n_line +=1
        return osc_list
    except:
        return NoneType
    finally:
        f.close()






def open_file_REC_configuration(filename :str, osc_list: list) -> list:
    try:
        f = open(filename, "r")
        coord = f.readline()
        coord = f.readline()
        # if coord[0]=='N':
            # print('N')
        while True:
            coord = f.readline()
            if coord[0]=='E':
                break
            if coord[0]=='W':
                param_of_osc=f.readline().split()

                oscillograph=osc.Oscillograph(coord[1:])
                
                osc_list.append(oscillograph)
                
                for n in range(int(param_of_osc[2])):
                    param_of_osc_line=f.readline().split()
                    osc_line=osc.OscillographLine('№'+param_of_osc_line[2]+' '+REC_name_from_int(int(param_of_osc[0]),n),
                                                    int(param_of_osc[4]),
                                                    n+1)
                    oscillograph.add_line(osc_line)

        return osc_list
    except:
        return NoneType
    finally:
        f.close() 
