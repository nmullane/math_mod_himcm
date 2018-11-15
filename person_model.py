#This file creates and tracks individual peoples schedules and can adjust their schedule over time or abruptly to test our model
import building_model as bd


class Person
    def __init__(self, scheduleType="Fixed", wake_up=7.0, sleep=11.0, typical=1, num_outings=1, variation=0, abrupt_change_per_year=0)
        self.scheduleType = scheduleType
        self.times = []     #Format [leave_time, return_time, leave_time, return_time, ..., return_time] 
    def get_times(self)
        

