# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:wangfy
@time:2018/11/6 18:16
'''

import json
import datetime
from collection_factory import CollectionFactory
from pymongo import InsertOne
from data_factory import Datafactory
from pymongo.errors import BulkWriteError

def insert_batch(num, average_iteration_num=1):
    mydb = CollectionFactory.create_client_and_db()
    tags_list = Datafactory.create_tags(num)
    sum_time = 0.0
    for iter in range(average_iteration_num):
        mydb["test_tags"].delete_many({})
        starttime = datetime.datetime.now()
        try:
            mydb["test_tags"].bulk_write(list(map(InsertOne,tags_list)))
        except BulkWriteError as bwe:
            print(bwe.details)

        endtime = datetime.datetime.now()
        sum_time += (endtime - starttime).total_seconds()

    return {
        "type": "insert batch",
        "num": num,
        "time": sum_time/average_iteration_num
    }

def insert_separate(num,average_iteration_num=1):

    mydb = CollectionFactory.create_client_and_db()
    sum_time = 0.0
    tags_list = Datafactory.create_tags(num)

    for i in range(average_iteration_num):
        mydb["test_tags"].delete_many({})
        starttime = datetime.datetime.now()
        # 逐条写
        for tags in tags_list:
            # 不存在会新建一个数据库表
            # 插入测试的时候目前没有用post或者tags，之后自己修改
            mydb['test_tags'].insert_one(tags)
        endtime = datetime.datetime.now()
        sum_time = (endtime - starttime).total_seconds()

    return {
        "type": "insert separate",
        "num": num,
        "time": sum_time/average_iteration_num
    }

def start_test_insert_exp(num_list,iteration_num=3):
    result_list = []

    for num in num_list:
        ## 计算平均运行时间值
        result = insert_batch(num,iteration_num)
        result_list.append(result)

    for num in num_list:
        ## 测试非批量的插入操作时间
        result = insert_separate(num,iteration_num)
        result_list.append(result)

    filename = "experiment_mongodb_result.json"
    save(filename,result_list)

def save(filename, result_list):
    with open(filename, "w") as f:
        json.dump(result_list, f)


if __name__ == '__main__':
    num_list = [5000,10000,25000,50000]
    start_test_insert_exp(num_list,3)


