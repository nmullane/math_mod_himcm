import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import building_model as bld
import heating_zone as hz
import schedule_generator as sg
import classify as cl
import regression as rg
from cycler import cycler
import time

class Thermo:
    def __init__(self, temp, area, wattage,insulation,epochs):
        self.temp = temp
        self.area = area
        self.wattage = wattage
        self.insulation = insulation
        self.zone = hz.heating_zone(self.temp[0],self.temp[1],self.temp[2],self.area,self.wattage)
        self.time = []
        self.time.append(0)
        self.epochs = epochs
        

    def newDay(self,weekly,monthly,yearly):
        results = [0,0,0]
        
        week = cl.Classify() 
        history = week.trainNetwork(self.epochs,weekly[:,:7:],weekly[:,7:8:])
        results[0] = week.testNetwork(weekly[:,1:8:]) 
        
        month = rg.Regression()
        history = month.trainNetwork(self.epochs,monthly[:,:30:],monthly[:,30:31:])
        results[1] = month.testNetwork(monthly[:,1:31:]) 
        results[1] = results[1].flatten()
 
        year = rg.Regression()
        history = year.trainNetwork(self.epochs,yearly[:,:365:],yearly[:,365:366:])
        results[2] = year.testNetwork(yearly[:,1:366:])
        results[2] = results[2].flatten()
        
        self.results = np.average(results, axis=0)
        return self.results

    def updateTemp(self,results,outside_temp,person):
        zone = self.zone
        last_time = round(zone.time[-1]*60)

        if(zone.time[-1]%(24.0) >= bld.morning and zone.time[-1]%(24.0*60) < bld.day):
            temp = zone.morning_temp
        elif(zone.time[-1]%(24.0) >= bld.day and zone.time[-1]%(24.0) < bld.night):
            temp = zone.day_temp
        else:
            temp = zone.night_temp

        time_need = (self.wattage/(zone.airmass*abs(temp - zone.temp[-1]+1)))/60
        index = int(last_time + round(time_need))
        future = results[index]

        if(zone.time[-1]%(24.0) + time_need/24 >= bld.morning and zone.time[-1]%(24.0*60) + time_need/24 < bld.day):
            target_temp = zone.morning_temp
        elif(zone.time[-1]%(24.0) + time_need/24 >= bld.day and zone.time[-1]%(24.0) + time_need/24 < bld.night):
            target_temp = zone.day_temp
        else:
            target_temp = zone.night_temp

        if round(results[last_time]) == 1 or future == 1 or person == 1:
            zone.update_temp(target_temp,outside_temp=outside_temp,status=1) 
        else:# round(results[last_time]) == 0 and future == 0 and person == 0:
            zone.update_temp(target_temp,outside_temp=outside_temp,status=0)

    def checkPerson(self,today):
        person = today[round(self.zone.time[-1]*60)]
        return person
        

if __name__=="__main__":
    event = np.random.randint(367,233100)

    thermostat = Thermo([25, 20, 18], 100, 1.8,0.033/60,100)

    sched = sg.Schedule(test_id=event-8)
    weekly = sched.getTimesTest(1,8) 
    sched = sg.Schedule(test_id=event-31)
    monthly = sched.getTimesTest(1,31)
    sched = sg.Schedule(test_id=event-366)
    yearly = sched.getTimesTest(1,366)
    sched = sg.Schedule(test_id=event)
    today = sched.getTimesTest(1,1) 
    
    before = time.time()
    results = thermostat.newDay(weekly,monthly,yearly)
    print(time.time()-before)

while thermostat.zone.time[-1] < 23.99:
    thermostat.updateTemp(results,10,thermostat.checkPerson(today))
print("DONE")
thermostat.zone.graph_over_time(thermostat.zone.temp)

 
