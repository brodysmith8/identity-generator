from io import TextIOWrapper
import csv
import math
import time
import helper_types as ht

# FiWr = list[ TextIOWrapper, writer ]

# # example call: [ f, fw ] = swap_file_writer('other.csv', f, fw)
# def swap_file_writer(new_f_name : str, *args) -> FiWr:
#     for arg in args:
#         if type(arg) == TextIOWrapper:
#             arg.close() # close the old file
#         elif type(arg) == writer:
#             fw = arg 
#     f = open(new_f_name, 'w')
#     fw = writer(f, dialect="unix")
#     return [ f, fw ]

def get_gauss():
    f = open('data/in/gauss-lookup-table.csv')
    fr = csv.reader(f, dialect='unix')
    gauss_lookup_table = []
    for line in fr:
        gauss_lookup_table.append([int(line[0]), float(line[3])])
    f.close()
    return gauss_lookup_table

# plan to implement multiplicative inverse and unify the unique number generation somehow
class UniqueNum:
    def __init__(self) -> None:
        pass

    def generate_unique_number() -> int:
        pass

class TimeAnalysis:
    def __init__(self) -> None:
        self.stages = [] # [ [stage_name, stage_time] ] 
        self.stage_names = set()
        self.current_stage = 0
        self._parent = None
        self._child = None
        self.max_entry = 0

    def new_stage(self, stage_name: str) -> None:
        if stage_name not in self.stage_names:
            self.max_entry = len(stage_name) if len(stage_name) > self.max_entry else self.max_entry
            self.stages.append([stage_name, -1])
            self.stage_names.add(stage_name)
            self.current_stage_name = stage_name
            self.current_stage = time.time_ns()

    def end_stage(self) -> ht.Seconds:
        end = time.time_ns()
        ret = self.new_time(self.current_stage_name, end, self.current_stage) # checks for us
        self.current_stage = 0
        self.current_stage_name = ""
        return ret

    def new_time(self, stage_name: str, end: int, begin: int) -> ht.Seconds:
        if stage_name in self.stage_names:
            idx = self.stages.index([stage_name, -1])
            self.stages[idx][1] = end - begin 
            return float(end - begin) / 1e9
        else:
            return -1

    def get_time(self, stage_name: str) -> ht.Seconds: 
        return float(self.stages[stage_name][1]) / 1e9

    def get_stats(self) -> list[str]:
        ret = []
        sum = 0
        for stage in self.stages:
            sum += stage[1]

        for stage in self.stages:
            ret.append([stage[0], float(stage[1])/1e9, stage[1] / sum * 100.0])
        return ret
    
    def get_parent(self):
        return self._parent

    def add_child(self, child, parent_stage):
        self._child = child
        self._child._parent = parent_stage

    def print_stats(self) -> None:
        stats = self.get_stats()
        max_str = self.max_entry
        
        max_time = 0
        for stage in self.stages:
            div = float(stage[1] / 1e9)
            if div > max_time:
                max_time = div

        cp = int(max_time)
        digits = 0
        while cp > 0:
            cp = int(cp / 10)
            digits +=1 
            
        max = self.max_entry
        row_len = 43
        print(f"\nStage{(max_str-5)*' '}{(6-digits)*' '}Time{(row_len - 35)*' '}% of Total\n{row_len*'-'}")
        for stat in stats:
            if self._child != None:
                if stat[0] == self._child.get_parent():
                    print(f'{stat[0]:{max if max >= 5 else 5}}{stat[1]:13.5f} s{stat[2]:11.2f} %')
                    for s in self._child.get_stats():
                        print(f'> {s[0]:{max -1 if max -1 >= 4 else 4}}{s[1]:13.5f} s{s[2]:11.2f} %')
                else: 
                    print(f'{stat[0]:{max if max >= 5 else 5}}{stat[1]:13.5f} s{stat[2]:11.2f} %')
            else:
                print(f'{stat[0]:{max if max >= 5 else 5}}{stat[1]:13.5f} s{stat[2]:11.2f} %')
        print('\n')