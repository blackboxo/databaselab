# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:yetianqi
@time:2018/11/6 18:16
'''

import datetime
from collection_factory import CollectionFactory
from pymongo import InsertOne, DeleteOne


def delete_batch(num, average_iteration_num=1):
    mydb = CollectionFactory.create_client_and_db()

    starttime = datetime.datetime.now()
    res = []
    for i in range(0, num):
        res.append(DeleteOne({'_id': i, 'x': 1}))
    mydb['test_2'].bulk_write(res)

    endtime = datetime.datetime.now()
    sum_time = (endtime - starttime).total_seconds()

    return {
        "type": "delete batch",
        "num": num,
        "time": sum_time
    }

def delete_separate(num,average_iteration_num=1):

    mydb = CollectionFactory.create_client_and_db()
    starttime = datetime.datetime.now()
    # 逐条写
    for i in range(0,num):
        # 不存在会新建一个数据库表
        # 插入测试的时候目前没有用post或者tags，之后自己修改
        mydb['test_1'].delete_one({'_id':i,'x':1})
    endtime = datetime.datetime.now()
    sum_time = (endtime - starttime).total_seconds()

    return {
        "type": "delete separate",
        "num": num,
        "time": sum_time
    }

def start_test_delete_exp(num,iteration_num=1):
    result_list = []
    ## 测试批量的删除操作时间

    ## 计算平均运行时间值
    result = delete_batch(num=num)
    print(result)
    result_list.append(result)

    ## 测试非批量的删除操作时间
    result = delete_separate(num=num)
    print(result)
    result_list.append(result)

if __name__ == '__main__':

    start_test_delete_exp(10000)

    # # result_list = None
    # filename = "experiment_mongodb_insert.json"
    # # time = insert_seperate(100)
    # # result_list.append(time)
    # # save(filename,result_list)
    # with open(filename) as f:
    #     result_list = json.load(f)
    # result_list.append(result_list[0])
    # with open(filename, 'w') as f:
    #     json.dump(result_list, f)


