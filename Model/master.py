import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import building_model as bld
import heating_zone as hz
import schedule_generator as sg
import classify as cl
import regression as rg
import outside_temp_generator as ot
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
        self.time_step = 5 #min 
        self.accuracy = [1]
    
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

    def updateAccuracy(self,results,today):
        today = today.flatten()
        correct = 0.0
        total = 0.0
        for i in range(0,len(results),self.time_step):
            if today[i] == round(results[i]):
                correct = correct + 1
            total = total + 1
            self.accuracy.append(correct/total)

    def plotAccuracy(self):
        plt.subplot(211)
        plt.plot(self.time, self.accuracy)
        plt.xlabel('time')
        plt.ylabel('accuracy')
        plt.subplot(212)
        plt.plot(self.time, thermostat.zone.temp)
        plt.xlabel('time')
        plt.ylabel('temperature')
        plt.show()

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
        future = round(results[index])

        if(zone.time[-1]%(24.0) + time_need/24 >= bld.morning and zone.time[-1]%(24.0*60) + time_need/24 < bld.day):
            target_temp = zone.morning_temp
        elif(zone.time[-1]%(24.0) + time_need/24 >= bld.day and zone.time[-1]%(24.0) + time_need/24 < bld.night):
            target_temp = zone.day_temp
        else:
            target_temp = zone.night_temp

        if round(results[last_time]) == 1 or future == 1 or person == 1:
            zone.update_temp(target_temp,outside_temp=outside_temp,timestep_min=self.time_step,status=1) 
        elif round(results[last_time]) == 0 and future == 0 and person == 0:
            zone.update_temp(target_temp,outside_temp=outside_temp,timestep_min=self.time_step,status=0)
        self.time.append(self.time[-1] + self.time_step / 60)

    def checkPerson(self,today):
        person = today[int(self.zone.time[-1]*60)]
        return person
        

if __name__=="__main__":
    event = np.random.randint(400,24637)
    days = 2
    current_day = 0
    out = ot.outside_temp()
    outs = out.get_temp(1, 365)
    thermostat = Thermo([25, 20, 18], 100, 1.8,0.033/60,100)

    while current_day < days:
        event = event+1 
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
        thermostat.zone.time = [0]
        while thermostat.zone.time[-1] < 23.999:
            thermostat.updateTemp(results,outs[int(np.floor(thermostat.zone.time[-1])),current_day],thermostat.checkPerson(today))
        thermostat.updateAccuracy(results,today)
        current_day = current_day + 1

    print("DONE")
    thermostat.plotAccuracy()
 
