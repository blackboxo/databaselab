# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:yetianqi
@time:2018/11/6 18:16
'''

import datetime
import json
from collection_factory import CollectionFactory
from pymongo import InsertOne
from pymongo import DeleteOne
from data_factory import Datafactory
from pymongo.errors import BulkWriteError


def delete_batch(num,mydb,average_iteration_num=1,tags_id=False):
    sum_time = 0.0
    # 获取数据，可以修改mydb.find().limit(num)
    if tags_id == True:
        tags_list = Datafactory.create_tags_id(num)
    else:
        tags_list = Datafactory.create_tags(num)

    for i in range(average_iteration_num):
        mydb["testDleteTags"].delete_many({})  # 清空数据库
        # 向测试的collection插入数据
        try:
            mydb["testDleteTags"].bulk_write(list(map(InsertOne, tags_list)))
        except BulkWriteError as bwe:
            print(bwe.details)

        # 主要删除操作
        starttime = datetime.datetime.now()
        # 批量删除  delete_many({})
        mydb["testDleteTags"].bulk_write(list(map(DeleteOne, tags_list)))
        endtime = datetime.datetime.now()
        sum_time = (endtime - starttime).total_seconds()

    type = "delete batch _id" if tags_id else "delete batch id"
    return {
        "type": type,
        "num": num,
        "time": sum_time
    }

    # res = []
    # for i in range(0, num):
    #     res.append(DeleteOne({'_id': i, 'x': 1}))
    # mydb['test_2'].bulk_write(res)

def delete_separate(num,mydb,average_iteration_num=1,tags_id=False):
    sum_time = 0.0
    if tags_id==True:
        tags_list = Datafactory.create_tags_id(num)
    else:
        tags_list = Datafactory.create_tags(num)
    for i in range(average_iteration_num):
        # 向测试的collection插入数据
        mydb["testDleteTags"].delete_many({})  # 清空数据库
        try:
            mydb["testDleteTags"].bulk_write(list(map(InsertOne,tags_list)))
        except BulkWriteError as bwe:
            print(bwe.details)

        starttime = datetime.datetime.now()
        # 逐条删除
        for tags in tags_list:
            mydb['testDleteTags'].delete_one(tags)

        endtime = datetime.datetime.now()
        sum_time = (endtime - starttime).total_seconds()

    type = "delete separate _id" if tags_id else "delete separate id"
    return {
        "type": type,
        "num": num,
        "time": sum_time/average_iteration_num
    }



def start_test_delete_exp(num_list,mydb,iteration_num=3):
    result_list = []

    for num in num_list:
        ## 计算批量删除（id）时间值
        result = delete_batch(num,mydb,iteration_num)
        result_list.append(result)

    for num in num_list:
        ## 计算批量删除（_id)时间值
        result = delete_batch(num,mydb,iteration_num,tags_id=True)
        result_list.append(result)

    for num in num_list:
        ## 测试非批量的删除(id)操作时间
        result = delete_separate(num,mydb,iteration_num)
        result_list.append(result)

    for num in num_list:
        ## 测试非批量的删除(_id)操作时间
        result = delete_separate(num,mydb,iteration_num,tags_id=True)
        result_list.append(result)

    filename = "experiment_mongodb_delete_result.json"
    save(filename,result_list)


def save(filename, result_list):
    with open(filename, "w") as f:
        json.dump(result_list, f)

def demo():
    mydb = CollectionFactory.create_client_and_db()
    num_list = [5000, 10000]
    # 传入数据量，数据库，测试次数
    start_test_delete_exp(num_list, mydb, 3)

if __name__ == '__main__':
    mydb = CollectionFactory.create_client_and_db()
    num_list = [5000]
    # 传入数据量，数据库，测试次数
    start_test_delete_exp(num_list,mydb,3)


