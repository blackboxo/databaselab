# -*- coding: UTF-8 -*-
'''
@project:mongodb
@author:wangfy
@time:2018/11/8 11:01
'''
import json
import datetime
import time
from pymongo import *
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

def query_separate(num,average_iteration_num=3):
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

# 1.单表单条件查询 match_1-table_1-filter：
# 根据帖子的id查询某个帖子的信息
# SELECT * FROM Posts LIMIT num (测10组：num从1万起递增1万，最后一组为10万)
def query_limit_num(mydb,mycoll='posts',max_num = 100000):
    # 主要使用posts和users数据库
    result = []
    for num in range(10000,max_num+1,100000):
        start = datetime.datetime.now()
        mydb['posts'].find().limit(num)
        end = datetime.datetime.now()
        time = (end-start).total_seconds()
        record = {
            "type": "query limit num",
            "num": num,
            "time": time
        }
        result.append(record)
    return result

# 2.单表多条件查询 match_1-table_multi-filters：
# 查询某个用户点击量大于1000的所有帖子
def query_limit_click(mydb,mycoll='posts',max_num = 100000):
    # 主要使用posts和users数据库
    sum_time = 0.0
    result = []
    for num in range(10000, max_num+1, 100000):
        # 查询信息
        query = {
            'ViewCount': {'$gt': 1000}
        }
        start = datetime.datetime.now()
        mydb[mycoll].find(query).limit(num)
        end = datetime.datetime.now()
        time =(end-start).total_seconds()
        record = {
            "type": "query limit num",
            "num": num,
            "time": time
        }
        result.append(record)
    return result

# 3.多表联合查询 match_multi-tables:
#
# 查询用户声誉大于某个值的用户的信息以及其post的基本信息
# 和被喜欢数（探寻用户的声誉和其帖子受欢迎程度的关系）
#
# SELECT Posts. Title, Posts.Tags, Posts. FavoriteCount,
#  Users. DisplayName, Users. Reputation
# FROM Posts,Users
# WHERE Users.Id = Posts. OwnerUserId and Users. Reputation>num (测10组：num从1万起递增1万，最后一组为10万)
# https://blog.csdn.net/u011113654/article/details/80353013
# https://blog.csdn.net/harleylau/article/details/77899223 很好
def query_posts_sums(mydb,mycoll='posts',max_num = 100000):
    # 主要使用posts和users数据库
    sum_time = 0.0
    result = []
    start = datetime.datetime.now()
    mydb["100wusers"].aggregate([
        {
            "$lookup":
                {
                    "from":"100wposts",
                    "localField": "Id",
                    "foreignField": "OwnerUserId",
                    "as":"inventory_docs"
                }

        },
        {
            "$match":
                {
                    "Reputation":{"$gt":220000}
                }
        },
        {
            "$project":
            {
                "_id": 0,
                "Reputation": 1,
                "inventory_docs":
                    {
                        "Title": 1,
                        "Tags": 1,
                    }
            }
        }
    ])
    end = datetime.datetime.now()
    sum_time += (end - start).total_seconds()
    record = {
        "type": "query limit num",
        "num": num,
        "time": time
    }
    result.append(record)
    return result

# 4.聚合查询 match_aggregate：
# 查询某个用户所有帖子的总被喜欢数：
# SELECT SUM(Posts. FavoriteCount), Users. DisplayName, Users. Reputation
# FROM Posts,Users
# WHERE Users.Id = Posts. OwnerUserId and Users.Id<num (
# 测10组：num从1万起递增1万，最后一组为10万)
def query_posts_sums():

    pass

def save(filename, result_list):
    with open(filename, "w") as f:
        json.dump(result_list, f)

def demo():
    mydb = CollectionFactory.create_client_and_db()
    start = datetime.datetime.now()
    query = {"Id": {'$lt': 10}}
    list = mydb.users.find(query)
    count = 0
    print(type(list))
    for i in list:
        # count+=1
        print(i)
    end = datetime.datetime.now()
    print((end - start))
    # for i in range(10000,110000,10000):
    #     print(i)

if __name__ == '__main__':
    mydb = CollectionFactory.create_client_and_db()
    start = datetime.datetime.now()
    mydb["100wposts"].aggregate([
        {
            "$lookup":
                {
                    "from": "100wusers",
                    "localField": "OwnerUserId",
                    "foreignField": "Id",
                    "as": "inventory_docs"
                }

        },
        {
            "$match":
                {
                    "OwnerUserId": 170
                }
        }
    ])
    end = datetime.datetime.now()
    time = (end - start).total_seconds()
    print(time)










