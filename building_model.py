import matplotlib.pyplot as plt
import heating_zone as hz
from cycler import cycler
#This file instantiates all the rooms and updates their temperatures
morning = 7.0
day = 12.0
night = 20.0


class building:
    def __init__(self, num_zones, zones=[]):
        self.num_zones = num_zones
        self.zones = zones
        self.time = []
        self.time.append(0)
    def update_zones(self, target_temps, outside_temp=-1, timestep_min=5.0, heating_constants = [0.020]):
        for i in range(self.num_zones):
            if len(heating_constants) == 1:
                self.zones[i].update_temp(target_temps[i], outside_temp, timestep_min, heating_constants[0])
            else:
                self.zones[i].update_temp(target_temps[i], outside_temp, timestep_min, heating_constants[i])
        self.time.append(self.time[-1] + timestep_min / 60)
        #print self.time[-1]
    def plot_zone_data_over_time(self, zones, var):
        plt.figure(1)
        plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y'])))
        for i in range(len(zones)):
            plt.plot(zones[i].time, getattr(zones[i], var))
        plt.show()


if __name__=="__main__":
    zone1 = hz.heating_zone(25, 20, 18, 1.5)
    zone2 = hz.heating_zone(28, 17, 20, 1.5)
    zone3 = hz.heating_zone(31, 23, 25, 1.5)

    house = building(3, [zone1, zone2, zone3])

    while house.time[-1] < 48:
        if(house.time[-1]%24.0 >= morning and house.time[-1]%24.0 < day):
            house.update_zones([zone1.morning_temp, zone2.morning_temp, zone3.morning_temp])
        elif(house.time[-1]%24.0 >= day and house.time[-1]%24.0 < night):
            house.update_zones([zone1.day_temp, zone2.day_temp, zone3.day_temp])
        else:   
            house.update_zones([zone1.night_temp, zone2.night_temp, zone3.night_temp])

    house.plot_zone_data_over_time([zone1, zone2, zone3],"temp")
