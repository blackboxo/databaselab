# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:yetianqi
@time:2018/11/6 18:16
'''

import datetime
import json
from collection_factory import CollectionFactory


def init_env(num):
   mydb = CollectionFactory.create_client_and_db()
   users = mydb['users']
   posts = mydb['posts']
   for iter in range(num):
       user = {};
       user['id'] = iter;
       user['reputation'] = 'reputation'+ str(iter)
       user['display_name'] = 'display_name'+ str(iter)
       user['age']= 28;
       post = {}
       post['id'] = iter;
       post['body'] = 'body'+ str(iter)
       post['owner_user_id'] = user['id'];
       post['title'] = 'title'+ str(iter)
       users.insert_one(user)
       posts.insert_one(post)

## 单表单条件更新
def update_batch(num, average_iteration_num=1):
    sum_time = 0.0
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['posts']
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()
        tag.update_many({'Id':{'$lt': num}}, {'$inc': {'ViewCount': 1}})
        endtime = datetime.datetime.now()
        sum_time += (endtime - starttime).total_seconds()
    return {
        "type": "update_one_table_one_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


## 单表多条件更新
def update_batch_mutiple(num, average_iteration_num=1):
    sum_time = 0.0
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['posts']
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()
        tag.update_many({'Id':{'$lt': num},'Score':{'$gt': 20}}, {'$inc': {'ViewCount': 1}})
        endtime = datetime.datetime.now()
        sum_time += (endtime - starttime).total_seconds()
    return {
        "type": "update_one_table_mul_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }

## 多表联查单表更新
def update_batch_mutiple_query_one_update(num, average_iteration_num=1):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['users']
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()
        cursor = mydb["users"].aggregate([
            {
                "$lookup":
                    {
                        "from":"posts",
                        "localField": "Id",
                        "foreignField": "OwnerUserId",
                        "as":"inventory_docs"
                    }

            },
            {
                "$match":
                    {
                        "ViewCount":{"$gt":num}
                    }
            }
        ])
        quarymap = {'Id':-1000}
        if(cursor.alive):
            quarymap =cursor.next()
        queryid = quarymap['Id']
        tag.update_many({'Id':queryid}, {'$inc': {'Reputation': 1}})
        endtime = datetime.datetime.now()
        sum_time += (endtime - starttime).total_seconds()
    return {
        "type": "update_aggregate",
        "num": num,
        "time": sum_time / average_iteration_num
    }


## 多表联查多表更新
def update_batch_mutiple_query_mutiple_update(num, average_iteration_num=1):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['users']
    tag_posts = mydb['posts']
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()
        cursor = mydb["users"].aggregate([
            {
                "$lookup":
                    {
                        "from":"posts",
                        "localField": "Id",
                        "foreignField": "OwnerUserId",
                        "as":"inventory_docs"
                    }

            },
            {
                "$match":
                    {
                        "ViewCount":{"$gt":num}
                    }
            }
        ])
        quarymap = {'Id':-1000}
        if(cursor.alive):
            quarymap =cursor.next()
        queryid = quarymap['Id']
        tag.update_many({'Id':queryid}, {'$inc': {'Reputation': 1}})
        tag_posts.update_many({'OwnerUserId':queryid}, {'$inc': {'ViewCount':1}})
        endtime = datetime.datetime.now()
        sum_time += (endtime - starttime).total_seconds()
    return {
        "type": "update_aggregate",
        "num": num,
        "time": sum_time / average_iteration_num
    }

def start_test_update_exp(start_test_num=10000,
                          max_test_num=100000,
                          iteration_num=3,
                          step=10000):
    ## init_env(5000)
    result_list = []
    for num in range(start_test_num, max_test_num, step):
        result = update_batch(num=num, average_iteration_num=iteration_num)
        print(result)
        result_list.append(result)

        result = update_batch_mutiple(num=num, average_iteration_num=iteration_num)
        print(result)
        result_list.append(result)

        result = update_batch_mutiple_query_one_update(num=num, average_iteration_num=iteration_num)
        print(result)
        result_list.append(result)

        result = update_batch_mutiple_query_mutiple_update(num=num, average_iteration_num=iteration_num)
        print(result)
        result_list.append(result)
    output_file_name = "experiment_update.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)

if __name__ == '__main__':
    start_test_update_exp()


