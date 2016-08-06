__author__ = 'zhangxa'

import sys
sys.path.append('.')

from show_in_matplot import zp_show_oneZw_gzddCounts_Pie,zp_show_oneZw_gzjyCounts_Pie,zp_show_oneZw_xlCounts_Pie
from show_in_matplot import zp_show_oneZw_gzddCounts_Bar,zp_show_oneZw_gzjyCounts_Bar,zp_show_oneZw_xlCounts_Bar
from show_in_matplot import zp_show_YyYxInBar,zp_show_YyCountsInBar
from show_in_matplot import zp_show_YyCountsInPie

if __name__ == "__main__":
    #zp_show_YyCountsInPie('./1.jpg')
    #zp_show_YyCountsInBar('./1.jpg')
    #zp_show_YyYxInBar('./1.jpg')
    zp_show_oneZw_gzddCounts_Bar('Java','./4.jpg')
    zp_show_oneZw_gzjyCounts_Bar('Java','./5.jpg')
    zp_show_oneZw_xlCounts_Bar('Java','./6.jpg')
    zp_show_oneZw_gzddCounts_Pie('C++','./1.jpg')
    zp_show_oneZw_gzjyCounts_Pie('C++','./2.jpg')
    zp_show_oneZw_xlCounts_Bar('C++','./3.jpg')