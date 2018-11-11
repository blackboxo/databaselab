# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:yetianqi
@time:2018/11/6 18:16
'''

import datetime
from collection_factory import CollectionFactory


def update_batch(num):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['test_tags']
    sum_time = 0.0
    starttime = datetime.datetime.now()
    tag.update_many({}, {'$set': {'Count': 10001}})
    endtime = datetime.datetime.now()
    sum_time += (endtime - starttime).total_seconds()

    return {
        "type": "update batch",
        "num": num,
        "time": sum_time
    }

def update_separate(num):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['test_tags']
    sum_time = 0.0

    for iter in range(num):
        starttime = datetime.datetime.now()
        tag.update_one({'Id':iter},{'$set': {'Count': 10002}})
        endtime = datetime.datetime.now()
        sum_time = (endtime - starttime).total_seconds()

    return {
        "type": "update separate",
        "num": num,
        "time": sum_time
    }

def start_test_update_exp(num):

    ## 计算平均运行时间值
    result = update_batch(num)
    print(result)

    ## 测试非批量的更新操作时间
    result = update_separate(num)
    print(result)

if __name__ == '__main__':
    start_test_update_exp(50000)


