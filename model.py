"""
Script to analyse 'Project Sleep' data.
Gianluca Truda
November 2016
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import os

class Night:
    """
    Represents an individual night of sleep, holding all data points for it.
    """
    def __init__(self, datetime, labels):
        self.date_time = datetime
        self.duration_mins = 0.0
        self.quality = 0.0
        self.data = {"1 tsp. Peanut butter": 0, "45 mins of no screens": 0, "Ate healthily today": 0,
                     "Avoided blue-light": 0, "Brushed teeth":0, "Chamomile tea": 0, "Exercised": 0,
                     "Eye mask": 0, "Fap": 0, "Had alcohol in past 3 hours": 0,
                     "Had caffeine after 2pm": 0, "Kept bed sacred today": 0, "Krill oil": 0,
                     "Listened to relaxing music": 0, "Meditated since 12pm": 0, "Napped today": 0,
                     "Podcast / audiobook": 0, "Read a paper book": 0, "Sex": 0,
                     "Small snack": 0, "Stretched before bed": 0, "Took 1 Somnil tablet": 0,
                     "Took 2+ Somnil tablets": 0,"Walked > 5000 steps": 0, "Warm shower in past hour": 0,
                     "Wearing socks": 0}
        for e in labels:
            self.data[e] = 1

        self.data_list = [self.data["1 tsp. Peanut butter"], self.data["45 mins of no screens"],
                          self.data["Ate healthily today"], self.data["Avoided blue-light"],
                          self.data["Brushed teeth"], self.data["Chamomile tea"], self.data["Exercised"],
                          self.data["Eye mask"], self.data["Fap"], self.data["Had alcohol in past 3 hours"],
                          self.data["Had caffeine after 2pm"], self.data["Kept bed sacred today"],
                          self.data["Krill oil"], self.data["Listened to relaxing music"],
                          self.data["Meditated since 12pm"], self.data["Napped today"],
                          self.data["Podcast / audiobook"], self.data["Read a paper book"], self.data["Sex"],
                          self.data["Small snack"], self.data["Stretched before bed"],
                          self.data["Took 1 Somnil tablet"], self.data["Took 2+ Somnil tablets"],
                          self.data["Walked > 5000 steps"], self.data["Warm shower in past hour"],
                          self.data["Wearing socks"]]


    def get_vector(self):
        return self.data_list

    def set_sleep_details(self, duration_mins, quality):
        self.duration_mins = duration_mins
        self.quality = quality


# The parameter records are loaded into an array of Night objects.
data_file = open('nights_data.txt')
data = data_file.readlines()
data_file.close()
nights = []
for l in data:
    time_data = time.strptime(l[0:l.find('\t')], '%B %d, %Y %I:%M:%S%p')
    info_string = l[l.find('\t')+1:].replace("\n", "").replace("\t", "").replace(" , ", ", ")
    labels = info_string.split(",")
    labels.sort()
    nights.append(Night(time_data, labels))

# The sleep records are loaded into the environment.
data_file = open('sleep_data.txt')
data = data_file.readlines()
data_file.close()
# All sleep records which have corresponding parameter records are found and the Night objects are updated.
for l in data:
    start_time = time.strptime(l[0:l.find('\t')], '%Y/%m/%d %H:%M')
    parts = l.split("\t")
    quality = float(parts[2])
    duration = time.strptime(parts[3], '%H:%M').tm_hour*60 + time.strptime(parts[3], '%H:%M').tm_min
    for n in nights:
        if start_time.tm_yday == n.date_time.tm_yday:
            n.set_sleep_details(duration, quality)

# Remove Night objects which do not possess sleep quality data.
for n in nights:
    if n.quality <= 0.0 or n.duration_mins <= 0.0:
        nights.remove(n)


# Create a single matrix from the parameters of all nights.
a = np.ndarray(shape=(len(nights), 26), dtype=float)
for i in range(len(nights)):
    a[i] = nights[i].get_vector()
# Create a vector matrix from the sleep quality.
b = np.ndarray(shape=(len(nights), 1),  dtype=float)
for i in range(len(nights)):
    b[i] = nights[i].quality

# Matrix solving performed using Numpy
x = np.linalg.lstsq(a, b, rcond=-1)
result = x[0]
for j in range(len(nights)):
    total = 0
    for i in range(26):
        total += nights[j].data_list[i]*result[i]
    print(total, nights[j].quality)


#Plotting the data
names = ["1 tsp. Peanut butter", "45 mins of no screens", "Ate healthily today", "Avoided blue-light", "Brushed teeth",
         "Chamomile tea", "Exercised", "Eye mask", "Fap", "Had alcohol in past 3 hours", "Had caffeine after 2pm",
         "Kept bed sacred today", "Krill oil", "Listened to relaxing music", "Meditated since 12pm", "Napped today",
         "Podcast / audiobook", "Read a paper book", "Tender Time", "Small snack", "Stretched before bed",
         "Took 1 Somnil tablet", "Took 2+ Somnil tablets", "Walked > 5000 steps", "Warm shower in past hour",
         "Wearing socks"]
plt.clf()
fig, ax = plt.subplots()
plt.style.use('ggplot')
x = names
y = result
fig, ax = plt.subplots()
width = 0.90
ind = np.arange(len(y))
ax.barh(ind, y, width, color="blue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(x, minor=False)
plt.title('PROJECT SLEEP : Sleep Quality Model', y=1.05)
plt.text(-0.65, 29, str(len(nights))+" data points")
plt.text(-0.65, 30, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#plt.tight_layout()
#plt.show()
plt.savefig(os.path.join('ProjectSleep.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures