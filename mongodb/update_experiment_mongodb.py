# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:yetianqi
@time:2018/11/6 18:16
'''

import datetime
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
def update_batch(num):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['users']
    sum_time = 0.0
    starttime = datetime.datetime.now()
    tag.update_many({'id':1}, {'$set': {'display_name': 'update_name'}})
    endtime = datetime.datetime.now()
    sum_time += (endtime - starttime).total_seconds()

    return {
        "type": "update batch",
        "num": num,
        "time": sum_time
    }

## 单表多条件更新
def update_batch_mutiple(num):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['users']
    sum_time = 0.0
    starttime = datetime.datetime.now()
    tag.update_many({'id':1,'display_name':'update_name2'}, {'$set': {'display_name': 'update_name'}})
    endtime = datetime.datetime.now()
    sum_time += (endtime - starttime).total_seconds()

    return {
        "type": "update_batch_mutiple",
        "num": num,
        "time": sum_time
    }

## 多表联查单表更新
def update_batch_mutiple_query_one_update(num):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['users']
    sum_time = 0.0
    starttime = datetime.datetime.now()
    quarymap = mydb["users"].aggregate([
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
                    "id":1
                }
        },
        {
            "$project":
                {
                    "id": 1
                }
        }
    ]).next()
    queryid = quarymap['id']
    tag.update_many({'id':queryid}, {'$set': {'display_name': 'update_name3'}})
    endtime = datetime.datetime.now()
    sum_time += (endtime - starttime).total_seconds()

    return {
        "type": "update_batch_mutiple_query_one_update",
        "num": num,
        "time": sum_time
    }

## 多表联查多表更新
def update_batch_mutiple_query_mutiple_update(num):
    mydb = CollectionFactory.create_client_and_db()
    tag = mydb['users']
    sum_time = 0.0
    starttime = datetime.datetime.now()
    quarymap = mydb["users"].aggregate([
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
                    "id":1
                }
        },
        {
            "$project":
                {
                    "id": 1
                }
        }
    ]).next()
    queryid = quarymap['id']
    tag.update_many({'id':queryid}, {'$set': {'display_name': 'update_name4'}})
    mydb['posts'].update_many({'id':queryid}, {'$set': {'score': '1000'}})
    endtime = datetime.datetime.now()
    sum_time += (endtime - starttime).total_seconds()

    return {
        "type": "update_batch_mutiple_query_mutiple_update",
        "num": num,
        "time": sum_time
    }

def start_test_update_exp(num):

    init_env(5000)

    result = update_batch(num)
    print(result)

    result = update_batch_mutiple(num)
    print(result)

    result = update_batch_mutiple_query_one_update(num)
    print(result)

    result = update_batch_mutiple_query_mutiple_update(num)
    print(result)


if __name__ == '__main__':
    start_test_update_exp(5000)


