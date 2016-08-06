__author__ = 'zhangxa'

import pymongo
import re

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.pyplot import savefig

import sys
sys.path.append('..')

DB_HOSTNAME="192.168.0.3"
DB_DATABASE="db_zp"
DB_TABLE_NAME="zp_info_table"

#print(fm.FontProperties('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc').get_family())

from dbase.db import DbHandle

def _set_ch():
	return
	from pylab import mpl
	mpl.rcParams['font.family'] = ['/usr/share/fonts/truetype/wqy/wqy-microhei.ttc']  #指定默认字体
	mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

def get_data_from_mongo():
	conn = pymongo.Connection('192.168.17.128',27017)
	db = conn.db_lianjia
	results = db.scrapy_zlzp_info.find({},{"zwlb":1,"zwyx":1,"gsdz":1,"gsxz":1,"_id":0})
	#results = db.scrapy_zlzp_info.find({})
	zwlb = ['C语言','C++','C#','PYTHON','RUBY','JAVA','IOS','ANDROID','HTML','PHP']
	#zwlb = ['SCALA']
	zwnum_set = {}
	zwyx_set = {}

	je_re = re.compile('([0-9 ]*)-([0-9 ]*)')

	def get_average_salary(slary):
		r_slary = slary.replace(',','')
		m = je_re.match(r_slary)
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
		if isinstance(yx,str) and isinstance(zw,str):
			uzw = zw.upper()
			for zwfl in zwlb:
				if uzw.rfind(zwfl) != -1:
					zwnum_set[zwfl] = zwnum_set.get(zwfl,0) + 1
					zwyx_set[zwfl] = zwyx_set.get(zwfl,0) + get_average_salary(yx)
					#print(zwfl,yx,get_average_salary(yx))

	for key in zwnum_set.keys():
		zwyx_set[key] = zwyx_set[key]/float(zwnum_set[key])


	return zwyx_set,zwnum_set

'''
col:指定要处理的列名 zwmc
lst:指定列中的值列表,['c','java','python']
'''
def zp_show_lst_cnt_bar(col,lst,title='',color='red',filename=''):
	if not lst:
		return
	dh = DbHandle(DB_HOSTNAME,DB_DATABASE,DB_TABLE_NAME)
	results = dh.get_countByColMultiReg(col,lst)
	#print(results)
	zp_show_bar(results,title,xlabel=title,color=color,filename=filename)

'''
avg_col:平均值所在列 yx_avg
col:指定要处理的列名 zwmc
lst:指定列中的值列表,['c','java','python']
'''
def zp_show_avg_lst_bar(avg_col,col,lst,title='',color='red',filename=''):
	dh = DbHandle(DB_HOSTNAME,DB_DATABASE,DB_TABLE_NAME)
	results = dh.get_avgByColMultiReg(col,avg_col,lst)
	#print(results)
	zp_show_bar(results,title=title,xlabel='编程语言',ylabel='平均月薪',color=color,filename=filename)

'''
柱状图显示函数
results:要显示的字典，key为横坐标，value为纵坐标
title:柱状图标题
xlabel:x轴显示
ylabel:y轴显示
'''
def zp_show_bar(results,title='',xlabel='',ylabel='数量',color='red',filename=''):
	bar_with = 0.4
	values = results.values()
	index = np.arange(len(results))
	fig = plt.figure(figsize=(8,8))
	rect = plt.bar(index,values,bar_with,color=color)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.xticks(index+bar_with,results.keys())
	_set_ch()
	if filename:
		fig.savefig(filename)
	else:
		fig.show()

'''
显示某种职位不同工作地点的数量柱状图
'''
def zp_show_oneZw_gzddCounts_Bar(yy,filename='',color='red',title=''):
	zp_show_oneCol_lstCntBar('zwmc',yy,'gzdd',['北京','上海','广州','深圳','杭州','天津'],color=color,title=title,filename=filename)

'''
显示某种职位不同工作经验的数量的柱状图
'''
def zp_show_oneZw_gzjyCounts_Bar(yy,filename='',color='red',title=''):
	zp_show_oneCol_lstCntBar('zwmc',yy,'gzjy',['不限','1-3','3-5','5-10','10年以上'],color=color,title=title,filename=filename)

def zp_show_oneZw_xlCounts_Bar(yy,filename='',color='red',title=''):
	zp_show_oneCol_lstCntBar('zwmc',yy,'xl',['不限','专','本','硕','博'],color=color,title=title,filename=filename)

def zp_show_oneCol_lstCntBar(col,value,lst_col,lst_regx,filename='',color='red',title=''):
	dh = DbHandle(DB_HOSTNAME,DB_DATABASE,DB_TABLE_NAME)
	results = dh.get_countByColValueRegAndMultiReg(col,value,lst_col,lst_regx)
	zp_show_bar(results,title=title,color=color,filename=filename)

'''
显示表中指定列col中的按列表lst指定的分类的数量饼状图
col:指定要处理的列名 zwmc
lst:指定列中的值列表,['c','java','python']
'''
def zp_show_lst_cnt_pie(col,lst,filename):
	if not lst:
		return
	dh = DbHandle(DB_HOSTNAME,DB_DATABASE,DB_TABLE_NAME)
	results = dh.get_countByColMultiReg(col,lst)
	#print(results)
	zp_show_pie(results,filename=filename)

def zp_show_pie(results,filename='./2.jpg'):
	labels = list(results.keys())
	values = list(results.values())
	colors = ['yellow','red','green','yellowgreen','blue']
	draw_colors = []
	for i in range(len(values)):
		draw_colors.append(colors[i%len(colors)])
	fig = plt.figure(figsize=(8,8))
	plt.pie(values,labels=labels,colors=draw_colors,autopct='%1.2f%%')
	_set_ch()
	if filename:
		fig.savefig(filename)
	else:
		fig.show()

#显示某种职位不同工作地点需求量的饼状图
def zp_show_oneZw_gzddCounts_Pie(yy,filename=''):
	zp_show_oneCol_lstCntPie('zwmc',yy,'gzdd',['北京','上海','广州','深圳','杭州','天津'],filename=filename)

def zp_show_oneZw_gzjyCounts_Pie(yy,filename=''):
	zp_show_oneCol_lstCntPie('zwmc',yy,'gzjy',['不限','1-3','3-5','5-10','10年以上'],filename=filename)

def zp_show_oneZw_xlCounts_Pie(yy,filename=''):
	zp_show_oneCol_lstCntPie('zwmc',yy,'xl',['不限','专','本','硕','博'],filename=filename)

def zp_show_oneCol_lstCntPie(col,value,lst_col,lst_regx,filename=''):
	dh = DbHandle(DB_HOSTNAME,DB_DATABASE,DB_TABLE_NAME)
	results = dh.get_countByColValueRegAndMultiReg(col,value,lst_col,lst_regx)
	zp_show_pie(results,filename=filename)

#显示语言的月薪柱状图
def zp_show_YyYxInBar(filename,title='编程语言平均月薪',color='blue'):
	zp_show_avg_lst_bar('yx_avg','zwmc',['C语言','C++','Java','Python','Php','ios','android'],title=title,color=color,filename=filename)

#显示语言数量的柱状图
def zp_show_YyCountsInBar(filename,title='编程语言职位数量',color='red'):
	zp_show_lst_cnt_bar('zwmc',['C语言','C++','Java','Python','Php','ios','android'],title=title,color=color,filename=filename)

#显示语言招聘数量的饼状图
def zp_show_YyCountsInPie(filename):
	zp_show_lst_cnt_pie('zwmc',['C语言','C++','Java','Python','Php','ios','android'],filename=filename)

#显示不同工作经验的职位数量的柱状图
def zp_show_GzjyCountsInBar(filename,title='不同工作经验需求量',color='red'):
	zp_show_lst_cnt_bar('gzjy',['不限','1-3','3-5','5-10','10年以上'],title=title,color=color,filename=filename)

if __name__ == "__main__":
	#zp_show_list_cnt_bar('gzjy',['不限','1-3','3-5','5-10','10年以上'],'工作经验')
	#zp_show_lst_cnt_bar('zwmc',['C语言','C++','Java','Python','Php','ios','android'],'编程语言')
	#zp_show_lst_cnt_pie('zwmc',['C语言','C++','Java','Python','Php','ios','android'])
	#zp_show_avg_lst_bar('yx_avg','zwmc',['C语言','C++','Java','Python','Php','ios','android'])
	#zp_show_YyYxInBar('./3.jpg',color='green')
	#zp_show_YyCountsInPie('./4.jpg')
	#zp_show_YyCountsInBar('./3.jpg',color='green')
	#zp_show_GzjyCountsInBar('./3.jpg')
	#zp_show_oneZw_gzddCounts_Bar('C++','./3.jpg')
	#zp_show_oneZw_gzddCounts_Pie('C++','./4.jpg')
	#zp_show_oneZw_gzjyCounts_Pie('C++','./3.jpg')
	#zp_show_oneZw_gzjyCounts_Bar('C++','./4.jpg')
	#zp_show_oneZw_xlCounts_Pie('C++','./4.jpg')
	zp_show_oneZw_xlCounts_Bar('C++','./4.jpg')

"""
bar_width = 0.35
n_groups = len(zwyx_set)
index = np.arange(n_groups)
labels = list(zwyx_set.keys())
left = [0,1,2,3,4,5,6,7,8,9,10]
right = list(zwyx_set.values())
right_1 = list(zwnum_set.values())


print(zwnum_set)
plt.bar(left,right_1,bar_width,facecolor = 'yellowgreen')
plt.xlabel('languages')
plt.ylabel('nums')
plt.title("programmer's nums")
plt.xticks(index+bar_width,zwyx_set.keys())
plt.show()



plt.bar(left,right,bar_width,facecolor = 'yellowgreen')
plt.xlabel('languages')
plt.ylabel('slary/month')
plt.title("programmer's salary")
plt.xticks(index+bar_width,zwyx_set.keys())
plt.show()
"""
