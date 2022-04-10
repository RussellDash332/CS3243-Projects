import os

"""
|_ logs                 -> to store all the logs
|  |_ 001.txt
|  |_ 002.txt
|
|_ process_logs.py      -> to be run every new log insertion
|_ log.txt              -> to insert new log

"""

# TimeStamp class to store all the timestamps
class TimeStamp:
    def __init__(self):
        self.data = []
    
    def add(self, time):
        """
        Adds a timestamp.
        """
        self.data.append(time)

    def max_val(self):
        """
        Displays the maximum runtime, up to 4 dp.
        """
        return round(max(self.data), 4)

    def min_val(self):
        """
        Displays the minimum runtime, up to 4 dp.
        """
        return round(min(self.data), 4)

    def mean(self):
        """
        Displays the mean runtime, up to 4 dp.
        """
        return round(sum(self.data) / len(self.data), 4)

    def variance(self):
        """
        Displays the runtimes' variance, up to 4 dp.
        """
        mu = sum(self.data) / len(self.data)
        return round(sum(map(lambda x: (x - mu)**2, self.data)) / len(self.data), 4)

    def __repr__(self):
        return f'(avg = {self.mean()}, var = {self.variance()}, min = {self.min_val()}, max = {self.max_val()})'

# Contain statistics of each 5 agents
stats = []
for _ in range(5):
    stats.append({'Lose': 0, 'Draw': 0, 'Win': 0, 'Time': TimeStamp()})

subdir = os.listdir('logs')

# Have another file log.txt to insert the newest log, if there is
check = open('log.txt').readlines()
if check != open(f'logs/{subdir[-1]}').readlines() and len(check) == 5:
    with open(f'logs/{str(len(subdir) + 1).zfill(3)}.txt', 'a+') as f:
        for row in check:
            f.write(row)
    f.close()

# Refresh subdirectory
subdir = os.listdir('logs')

# Crunch all into a single dictionary and timestamp object
for txt in subdir:
    with open(f'logs/{txt}') as f:
        r = 0
        for line in f.readlines():
            line = line.strip()
            idx = line.find('Time')
            ldw = eval(line[:idx])
            time = float(line[idx:].split()[1])
            for k in ldw:
                stats[r][k] += ldw[k]
            stats[r]['Time'].add(time)
            r += 1

# Display for each agent
times = []
for stat in stats:
    t = stat['Time']
    del stat['Time']
    print(stat)
    print('\tTime:', t)
    times.append(t) # In case it's still needed