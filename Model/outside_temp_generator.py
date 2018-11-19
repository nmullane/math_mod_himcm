import numpy as np
import sys, os
import data_parser

#3pm hottest part of the dAY
class outside_temp:
    def __init__(self):
        self.weather_data = np.array(data_parser.load_data(os.path.abspath(os.path.dirname(sys.argv[0])) + "/Data/MonthlyDurham.csv"))
    def get_temp(self, day_start, day_end):
        temps = np.empty((24, 365))
#        print(self.weather_data[1])
        for i in range(day_start, day_end + 1):
            for j in range(24):
                day_max = float(self.weather_data[i+1][2])
                day_min = float(self.weather_data[i+1][4])
                temp_step = (day_max - day_min)/24.0
                temps[j][i-1] = day_max + -1 * temp_step * abs(15.0 - j)
        return temps

if __name__ == "__main__":
    out = outside_temp()
    np.set_printoptions(threshold=np.inf)
    outs = out.get_temp(1, 365)

    print(outs[:,1])
    print(outs.shape)

