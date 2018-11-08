# -*- coding: UTF-8 -*-
'''
@project:mongodb
@author:wangfy
@time:2018/11/8 11:01
'''
import json
import datetime
from collection_factory import CollectionFactory
from pymongo import InsertOne
from pymongo import *
from data_factory import  Datafactory
from pymongo.errors import BulkWriteError
def query_batch(num, average_iteration_num=3):
    pass
    # return {
    #     "type": "insert batch",
    #     "num": num,
    #     "time": sum_time
    # }

def insert_separate(num,average_iteration_num=3):
    pass
    # mydb = CollectionFactory.create_client_and_db()
    # starttime = datetime.datetime.now()
    # # 逐条写
    # for i in range(0,num):
    #     # 不存在会新建一个数据库表
    #     # 插入测试的时候目前没有用post或者tags，之后自己修改
    #     mydb['test_1'].insert_one({'_id':i,'x':1})
    # endtime = datetime.datetime.now()
    # sum_time = (endtime - starttime).total_seconds()
    #
    # return {
    #     "type": "insert separate",
    #     "num": num,
    #     "time": sum_time
    # }

def start_test_insert_exp(num,iteration_num=3):
    pass
    # result_list = []
    # ## 测试批量的插入操作时间
    #
    # ## 计算平均运行时间值
    # result = insert_batch(num=num)
    # result_list.append(result)
    #
    # ## 测试非批量的插入操作时间
    # result = insert_separate(num=num)
    # result_list.append(result)
    #
    # filename = "experiment_mongodb_result.json"
    # save(filename,result_list)

def save(filename, result_list):
    with open(filename, "w") as f:
        json.dump(result_list, f)

if __name__ == '__main__':
    # list_tags = Datafactory.create_tags(100)
    # mydb = CollectionFactory.create_client_and_db()
    # try:
    #     mydb['delete_tags'].bulk_write(list(map(InsertOne,list_tags)))
    # except BulkWriteError as bwe:
    #     print(bwe.details)
    # mydb = CollectionFactory.create_client_and_db()
    # list_tags = Datafactory.create_tags(10000)
    # # res = []
    # # for tags in tags:
    # #     res.append()
    # mydb['delete_tags'].bulk_write(list(map(InsertOne,list_tags)))
    mydb = CollectionFactory.create_client_and_db()
    test = mydb['delete_tags'].aggregate([{'$limit': 6 }])
    # test = mydb['delete_tags'].aggregate([{'$sample': { 'size' : 5 }}])
    for item in test:
        print(item)


