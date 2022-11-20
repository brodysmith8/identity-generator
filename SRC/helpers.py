from io import TextIOWrapper
from csv import writer

FiWr = list[ TextIOWrapper, writer ]

# example call: [ f, fw ] = swap_file_writer('other.csv', f, fw)
def swap_file_writer(new_f_name : str, *args) -> FiWr:
    for arg in args:
        if type(arg) == TextIOWrapper:
            arg.close() # close the old file
        elif type(arg) == writer:
            fw = arg 
    f = open(new_f_name, 'w')
    fw = writer(f, dialect="unix")
    return [ f, fw ]