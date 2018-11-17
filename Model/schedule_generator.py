import sys, os
import data_parser
import numpy as np
# Test, Fixed, Progressing, 
class Schedule:

    def __init__(self, scheduleType="Fixed", wake_up=7.0, sleep=11.0, typical=1, num_outings=1, variation=0, abrupt_change_per_year=0, test_id=0):
        self.scheduleType = scheduleType
        self.wake_up = wake_up
        self.sleep = sleep
        self.typical = typical
        self.variation = variation
        self.abrupt_change_per_year = abrupt_change_per_year
        self.functions = {}
        self.functions = {
            'Test': self.getTimesTest,
            'Fixed': self.getTimesFixed,
            'Progressing': self.getTimesProgressing,
        }
        
        self.activities_data = data_parser.load_data(os.path.abspath(os.path.dirname(sys.argv[0])) + "/Data/not_at_home_activities.csv")
        self.id = test_id
        #print(self.activities_data[self.id][0])

        self.typical_outings = []  #form  [leave_time, return_time, ... ,retiurn_time]
         
        
    #1440x7
    def getTimesTest(self, day_start, day_end):
        start_times_mins = float(self.activities_data[self.id][4]) * 60.0
        end_times_mins = float(self.activities_data[self.id][5]) * 60.0

        start_times_mins_2 = float(self.activities_data[self.id+100][4]) * 60.0
        end_times_mins_2 = float(self.activities_data[self.id+100][5]) * 60.0
        #print self.activities_data[self.id][4]
        #print self.activities_data[self.id][5]

        #print self.activities_data[self.id+100][4]
        #print self.activities_data[self.id+100][5]

        #print start_times_mins
        #print end_times_mins
        times = []
        num_days = day_end - day_start + 1
        for i in range(1440):
            times.append([])
            for j in range(num_days):
                times[i].append(0)
        for j in range(num_days):
            for i in range(1440):
                if j < 5:
                    if i >= start_times_mins and i < end_times_mins:
                        times[i][j] = 0
                    else:
                        times[i][j] = 1
                else:
                    if i >= start_times_mins_2 and i < end_times_mins_2:
                        times[i][j] = 0
                    else:
                        times[i][j] = 1
        times = np.array(times)
        return times
            

    def getTimesFixed(self, day_start, day_end):
        times = []
        num_days = day_end - day_start
    def getTimesProgressing(self, day_start, day_end):
        times = []
        num_days = day_end - day_start
    def getTimes(self, day_start, day_end):
        return functions[scheduleType](day_start, day_end)

if __name__=="__main__":
    sched = Schedule(test_id=10024)
    times = sched.getTimesTest(7, 7)
    #print times.shape
