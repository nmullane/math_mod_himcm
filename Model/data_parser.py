import csv


def load_data(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lines = 0
        data = []
        for row in csv_reader:
            if lines == 0:
                print('Column names are ' + ", ".join(row))
                lines += 1
            else:
                data.append(row)
                lines += 1
    return data
    #print data 
if __name__=="__main__":
    load_data("Data/not_at_home_activities.csv")
