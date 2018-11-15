
#Fixed, Progressing, 
class Schedule
    def __init__(self, scheduleType="Fixed", wake_up=7.0, sleep=11.0, typical=1, num_outings=1, variation=0, abrupt_change_per_year=0):
        self.scheduleType = sheduleType
        self.wake_up = wake_up
        self.sleep = sleep
        self.typical = typical
        self.variation = variation
        self.abrupt_change_per_year = abrupt_change_per_year
        self.functions = {}
        self.functions = {
            'Fixed': getTimesFixed,
            'Progressing': getTimesProgressing,
        }

        self.typical_outings = []  #form  [leave_time, return_time, ... ,retiurn_time]
        for i in range(num_outings):
           outings.append( 
         
    def getTimes(day_start, day_end):
        return functions[scheduleType](day_start, day_end)
        
    def getTimesFixed(day_start, day_end):
        times = []
        num_days = day_end - day_start
    def getTimesProgressing(day_start, day_end):
        times = []
        num_days = day_end - day_start
