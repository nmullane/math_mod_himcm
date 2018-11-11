import matplotlib.pyplot as plt
import building_model as bld

#This file creates and tracks rooms and determines temperature within a room based on surrounding rooms and oustide temperature

class heating_zone:
    def __init__(self, morning_temp, day_temp, night_temp, wattage, size=1):
        self.energy_usage = []
        self.time = []
        self.temp = []
        #Morning: 7:00  Day: 12:00  Night 20:00
        self.morning_temp = morning_temp #Celcius
        self.day_temp = day_temp
        self.night_temp = night_temp
        self.temp.append(self.morning_temp)
        self.wattage = wattage
        self.energy_usage.append(0)   #KwH
        self.time.append(0)
        
    def update_temp(self, target_temp, outside_temp=-1, timestep_min=5.0, heating_constant = .020):
        self.temp.append( self.temp[-1] + timestep_min * heating_constant * (target_temp - self.temp[-1]))
        self.energy_usage.append(self.energy_usage[-1] + self.wattage  * timestep_min / 60)
        self.time.append(self.time[-1] + timestep_min / 60)
        #print self.temp[-1]
    def graph_over_time(self, var):
        plt.plot(self.time, var)
        plt.show()


if( __name__ == "__main__"):
    zone = heating_zone(25, 20, 18, 1.5)
    while zone.time[-1] < 48:
        if(zone.time[-1]%24.0 >= bld.morning and zone.time[-1]%24.0 < bld.day):
            zone.update_temp(zone.morning_temp)
        elif(zone.time[-1]%24.0 >= bld.day and zone.time[-1]%24.0 < bld.night):
            zone.update_temp(zone.day_temp)
        else:
            zone.update_temp(zone.night_temp)
    zone.graph_over_time(zone.temp)
    #zone.graph_over_time(zone.energy_usage)
