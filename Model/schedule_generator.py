import sys, os
import data_parser
import numpy as np
# Test, Fixed, Progressing, 
class Schedule:

    def __init__(self, scheduleType="Fixed", wake_up=7.0, sleep=11.0, typical=1, num_outings=4, variation_weekday=1, variation_weekend=1, abrupt_change_per_year=2, test_id=0, progression_rate = 0):
        self.scheduleType = scheduleType
        self.wake_up = wake_up
        self.sleep = sleep
        self.typical = typical
        self.variation_weekday = variation_weekday
        self.variation_weekend = variation_weekend
        self.abrupt_change_per_year = abrupt_change_per_year
        self.progression_rate = progression_rate
        self.functions = {}
        self.functions = {
            'Test': self.getTimesTest,
            'Fixed': self.getTimesFixed,
            'Progressing': self.getTimesProgressing,
        }
        
        self.activities_data = np.array(data_parser.load_data(os.path.abspath(os.path.dirname(sys.argv[0])) + "/Data/not_at_home_activities.csv"))
        idx = np.r_[0:1, 50001:75002]
        self.activities_data = self.activities_data[idx]

        self.activities_data = np.append(self.activities_data, np.array(data_parser.load_data(os.path.abspath(os.path.dirname(sys.argv[0])) + "/Data/clusters.csv")), axis=1)
        #print(self.activities_data[0])

        self.clustered_data = []
        for row in self.activities_data:
            #print row
            if row[7] != '0':
                self.clustered_data.append(row)
        #print self.clustered_data.shape

            
        #print(self.activities_data[self.test_id][0])

        self.test_id = test_id
        self.rand_id = np.random.randint(1, max(self.activities_data.shape))
        self.num_outings = num_outings

        self.base_start_times = []
        self.base_durations = []

        self.clust_id = np.random.randint(1, len(self.clustered_data))
        self.past_clust_id = [0]
        for i in range(num_outings):
            #print self.clustered_data[self.clust_id][7]
            #print self.past_clust_id
            while self.clustered_data[self.clust_id][7] in self.past_clust_id:
                self.clust_id = np.random.randint(1, len(self.clustered_data))
            self.past_clust_id.append(self.clustered_data[self.clust_id][7])

            self.base_start_times.append(float(self.clustered_data[self.clust_id][4]))
            self.base_durations.append(float(self.clustered_data[self.clust_id][3]))
        #print self.base_start_times
        #print self.base_durations
            
        self.base_weekend_start_times = []
        self.base_weekend_durations = []

        self.clust_id = np.random.randint(1, len(self.clustered_data))
        self.past_clust_id = [0]
        for i in range(num_outings):
            #print self.clustered_data[self.clust_id][7]
            #print self.past_clust_id
            while self.clustered_data[self.clust_id][7] in self.past_clust_id:
                self.clust_id = np.random.randint(1, len(self.clustered_data))
            self.past_clust_id.append(self.clustered_data[self.clust_id][7])

            self.base_weekend_start_times.append(float(self.clustered_data[self.clust_id][4]))
            self.base_weekend_durations.append(float(self.clustered_data[self.clust_id][3]))

        #print self.base_weekend_start_times
        #print self.base_weekend_durations
        
    #1440x7
    def getTimesTest(self, day_start, day_end):
        start_times_mins = float(self.activities_data[self.test_id][4]) * 60.0
        end_times_mins = float(self.activities_data[self.test_id][5]) * 60.0

        start_times_mins_2 = float(self.activities_data[self.test_id+100][4]) * 60.0
        end_times_mins_2 = float(self.activities_data[self.test_id+100][5]) * 60.0
        #print self.activities_data[self.test_id][4]
        #print self.activities_data[self.test_id][5]

        #print self.activities_data[self.test_id+100][4]
        #print self.activities_data[self.test_id+100][5]

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
        num_days = day_end - day_start + 1
        times = []
        
            

        for i in range(1440):
            times.append([])
            for j in range(num_days):
                times[i].append(1)
        for j in range(num_days):
            start_times = []
            durations = []
            start_times_weekend = []
            durations_weekend = []
            #Modulate start and duration for the day
            for idx in range(len(self.base_start_times)):
                start_times.append(self.base_start_times[idx] + np.random.ranf() * self.variation_weekday - self.variation_weekday/2.0)
                durations.append(self.base_durations[idx] + np.random.ranf() * self.variation_weekday * 60.0 - self.variation_weekday/2.0 * 60.0)
            for idx in range(len(self.base_weekend_start_times)):
                start_times_weekend.append(self.base_weekend_start_times[idx] + np.random.ranf() * self.variation_weekend - self.variation_weekend/2.0)
                durations_weekend.append(self.base_weekend_durations[idx] + np.random.ranf() * self.variation_weekend * 60.0 - self.variation_weekend/2.0 * 60.0)
            for i in range(1440):
                if j < 5:
                    for k in range(len(start_times)):
                        #print k
                        if i >= start_times[k] * 60.0  and i < start_times[k] * 60.0 + durations[k]:
                            #print k
                            times[i][j] = 0
                else:
                    for k in range(len(start_times_weekend)):
                        if i >= start_times_weekend[k] * 60.0 and i < start_times_weekend[k] * 60.0 + durations_weekend[k]:
                            times[i][j] = 0
        return np.array(times)
    def getTimesProgressing(self, day_start, day_end):
        num_days = day_end - day_start + 1
        times = []
        
            

        for i in range(1440):
            times.append([])
            for j in range(num_days):
                times[i].append(1)
        for j in range(num_days):
            start_times = []
            durations = []
            start_times_weekend = []
            durations_weekend = []
            #Modulate start and duration for the day
            for idx in range(len(self.base_start_times)):
                start_times.append(self.base_start_times[idx] + np.random.ranf() * self.variation_weekday - self.variation_weekday/2.0)
                durations.append(self.base_durations[idx] + np.random.ranf() * self.variation_weekday * 60.0 - self.variation_weekday/2.0 * 60.0)
            for idx in range(len(self.base_weekend_start_times)):
                start_times_weekend.append(self.base_weekend_start_times[idx] + np.random.ranf() * self.variation_weekend - self.variation_weekend/2.0)
                durations_weekend.append(self.base_weekend_durations[idx] + np.random.ranf() * self.variation_weekend * 60.0 - self.variation_weekend/2.0 * 60.0)

            for idx in range(len(self.base_start_times)):
                self.base_start_times[idx] += self.progression_rate * num_days/7.0
            for idx in range(len(self.base_weekend_start_times)):
                self.base_weekend_start_times[idx] += self.progression_rate * num_days/7.0
            for i in range(1440):
                if j < 5:
                    for k in range(len(start_times)):
                        #print k
                        if i >= start_times[k] * 60.0  and i < start_times[k] * 60.0 + durations[k]:
                            #print k
                            times[i][j] = 0
                else:
                    for k in range(len(start_times_weekend)):
                        if i >= start_times_weekend[k] * 60.0 and i < start_times_weekend[k] * 60.0 + durations_weekend[k]:
                            times[i][j] = 0

        return np.array(times)

    def getTimes(self, day_start, day_end):
        return self.functions[self.scheduleType](day_start, day_end)

if __name__=="__main__":
    sched = Schedule(scheduleType = "Progressing", num_outings = 4, test_id=10024, variation_weekday = .6, variation_weekend = .7, progression_rate=2)
    times = sched.getTimes(7, 9)
    np.set_printoptions(threshold=np.inf)
#    print times
#    print times.shape
