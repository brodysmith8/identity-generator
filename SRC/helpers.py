from io import TextIOWrapper
from csv import writer
import time
import helper_types as ht

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
        max = self.max_entry
        for stage in self.stages:
            ret.append(f'{stage[0]:{max}} : {float(stage[1])/1e9:6.5f} s')
        return ret