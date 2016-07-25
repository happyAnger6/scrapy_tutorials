__author__ = 'zhangxa'

import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt

from show_in_matplot import get_data_from_mongo,set_ch

avg,num = get_data_from_mongo()

set_ch()
sizes = list(num.values())
labels = tuple(num.keys())
colors = ['yellowgreen','gold','lightskyblue','lightcoral','red','white']
colors_use = []
for i in range(len(sizes)):
    colors_use.append(colors[i%len(colors)])

print(num)
plt.pie(sizes,labels=labels,colors=colors_use,autopct='%1.1f%%',shadow=True)
plt.show()
