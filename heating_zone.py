import matplotlib
#This file creates and tracks rooms and determines temperature within a room based on surrounding rooms and oustide temperature
morning = 7
day = 12
night = 20

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
        self.time.append(morning)
        
    def update_temp(self, target_temp, outside_temp=-1, timestep_min=5, heating_constant = .01):
        self.temp.append(timestep_min * heating_constant * (target_temp - self.temp[-1]))
        self.energy_usage.append(self.energy_usage[-1] + self.wattage  * timestep_min / 60)
        self.time.append(self.time[-1] + timestep_min / 60)
    def graph_temp(self):
        plot(self.temp, self.time)


if( __name__ == "__main__"):
    zone = heating_zone(25, 20, 18, 1500)
    while zone.time[-1] < 24:
        zone.update_temp(30)
    zone.graph_temp()
