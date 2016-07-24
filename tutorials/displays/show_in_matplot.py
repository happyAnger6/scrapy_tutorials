__author__ = 'zhangxa'

import pymongo
import re

import numpy as np
import matplotlib.pyplot as plt

conn = pymongo.Connection('192.168.17.128',27017)
db = conn.db_lianjia
results = db.scrapy_zlzp_info.find({},{"zwlb":1,"zwyx":1,"gsdz":1,"gsxz":1,"_id":0})
#results = db.scrapy_zlzp_info.find({})
zwlb = ['C','C++','C#','PYTHON','RUBY','SCALA','JAVA','IOS','ANDROID','HTML']
#zwlb = ['SCALA']
zwnum_set = {}
zwyx_set = {}

je_re = re.compile('([0-9]*)-([0-9]*)')

def get_average_salary(slary):
	m = je_re.match(slary)
	try:
		if m:
			low = m.group(1)
			high = m.group(2)
			return (float(low) + float(high)) / 2
	except:
		return 0
	return 0
	
#print(get_average_salary('面议'))	

for result in results:
	zw = result.get('zwlb')
	yx = result.get('zwyx')
	if isinstance(yx,str) and isinstance(zw,str) and yx.rfind('月') != -1:
		uzw = zw.upper()
		for zwfl in zwlb:
			if uzw.rfind(zwfl) != -1:
				zwnum_set[zwfl] = zwnum_set.get(zwfl,0) + 1
				zwyx_set[zwfl] = zwyx_set.get(zwfl,0) + get_average_salary(yx)
			
for key in zwnum_set.keys():
	zwyx_set[key] = zwyx_set[key]/float(zwnum_set[key])

bar_width = 0.50
n_groups = len(zwyx_set)
index = np.arange(n_groups)
labels = list(zwyx_set.keys())
left = [0,1,2,3,4,5,6,7,8,9]
right = list(zwyx_set.values())
print(left,zwyx_set,right)
plt.bar(left,right,bar_width)
plt.xlabel('languages')
plt.ylabel('slary/month')
plt.title("programmer's salary")
plt.xticks(index+bar_width,zwyx_set.keys())

plt.show()