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

def insert_batch(num,mydb,average_iteration_num=1,tags_id=False):
    # mydb = CollectionFactory.create_client_and_db()
    if tags_id==True:
        tags_list = Datafactory.create_tags_id(num)
    else:
        tags_list = Datafactory.create_tags(num)

    sum_time = 0.0
    for iter in range(average_iteration_num):
        mydb["testInsretTags"].delete_many({})
        starttime = datetime.datetime.now()
        try:
            mydb["testInsretTags"].bulk_write(list(map(InsertOne,tags_list)))
        except BulkWriteError as bwe:
            print(bwe.details)

        endtime = datetime.datetime.now()
        sum_time += (endtime - starttime).total_seconds()
    type = "insert batch _id" if tags_id else "insert batch id"
    return {
        "type": type,
        "num": num,
        "time": sum_time/average_iteration_num
    }

def insert_separate(num,mydb,average_iteration_num=1,tags_id=False):

    # mydb = CollectionFactory.create_client_and_db(db_name,client_name)
    sum_time = 0.0
    if tags_id==True:
        tags_list = Datafactory.create_tags_id(num)
    else:
        tags_list = Datafactory.create_tags(num)

    for i in range(average_iteration_num):
        # 先删除所有的数据
        mydb["testInsretTags"].delete_many({})
        starttime = datetime.datetime.now()
        # 逐条写
        for tags in tags_list:
            # 不存在会新建一个数据库表
            # 插入测试的时候目前没有用post或者tags，之后自己修改
            mydb['testInsretTags'].insert_one(tags)
        endtime = datetime.datetime.now()
        sum_time = (endtime - starttime).total_seconds()
    type = "insert separate _id" if tags_id else "insert separate id"
    return {
        "type": type,
        "num": num,
        "time": sum_time/average_iteration_num
    }


def start_test_insert_exp(num_list,mydb,iteration_num=3):
    result_list = []

    for num in num_list:
        ## 计算平均运行时间值，无索引
        result = insert_batch(num,mydb,iteration_num)
        result_list.append(result)

    for num in num_list:
        ## 计算平均运行时间值
        result = insert_batch(num,mydb,iteration_num,True)
        result_list.append(result)

    for num in num_list:
        ## 测试非批量的插入操作时间,无索引
        result = insert_separate(num,mydb,iteration_num)
        result_list.append(result)

    for num in num_list:
        ## 测试非批量的插入操作时间,_id
        result = insert_separate(num,mydb,iteration_num,True)
        result_list.append(result)


    filename = "experiment_mongodb_result_insert.json"
    save(filename,result_list)

def save(filename, result_list):
    with open(filename, "w") as f:
        json.dump(result_list, f)

def demo():
    mydb = CollectionFactory.create_client_and_db()
    num_list = [100000]
    # 传入数据量，数据库，测试次数
    start_test_insert_exp(num_list, mydb, 3)

if __name__ == '__main__':
    demo()


