__author__ = 'zhangxa'

import pymongo

class DbHandle:
    def __init__(self,hostname,db,collection,port=27017):
        self.conn = pymongo.Connection('192.168.17.128',port)
        self.db = self.conn[db]
        self.collection = collection

    def get_countByColValue(self,col,value):
        return self.db[self.collection].find({col:value}).count()

    def get_countByColReg(self,col,regx):
        return self.db[self.collection].find({col:{"$regex":regx,"$options":"$i"}}).count()

    def get_countByColMultiReg(self,col,lst_regx):
        ret = {}
        for regx in lst_regx:
            ret[regx] = self.db[self.collection].find({col:{"$regex":regx,"$options":"$i"}}).count()
        return ret

    def get_countByColValueRegAndMultiReg(self,col,value,lst_col,lst_regx):
        ret = {}
        for regx in lst_regx:
            ret[regx] = self.db[self.collection].find({col:{"$regex":value,"$options":"$i"},lst_col:{"$regex":regx,"$options":"$i"}}).count()
        return ret

    def get_avgByColMultiReg(self,col,avg_col,lst_regx):
        ret = {}
        for regx in lst_regx:
            sum,count = 0,0
            for item in self.db[self.collection].find({col:{"$regex":regx,"$options":"$i"}}):
                if not item.get(avg_col):
                    continue
                sum = sum + item[avg_col]
                count = count + 1
            avg = float(sum) / count
            ret[regx] = avg
        return ret

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    hDb = DbHandle('192.168.17.128','db_zp','zp_info_table')
    #print(hDb.get_countByColReg('zwmc','java'))
    #print(hDb.get_countByColMultiReg('zwmc',['c语言','c++','java','python','ruby','html','R','ios','android']))
    #print(hDb.get_avgByColMultiReg('zwmc','yx_avg',['c语言','c++','java','python','ios','android']))
    #print(hDb.get_avgByColMultiReg('zwmc','yx_avg',['c语言','c++','java','python','ios','android']))
    #print(hDb.get_countByColValueRegAndMultiReg('zwmc','ios','zwyx',['不限','1-3','3-5','5-10','10年以上']))
    print(hDb.get_countByColValueRegAndMultiReg('zwmc','java','gzdd',['北京','上海','广州','深圳','杭州']))
    hDb.close()



