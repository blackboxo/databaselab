# -*- coding: UTF-8 -*-
'''
@project:mysqllab-master
@author:wangfy
@time:2018/11/6 16:28
'''
import pymongo

class CollectionFactory:
    """
    这个类负责创建mongodb数据库的连接，session
    """

    @staticmethod
    def create_client_and_db(db_name="mongotest", client_name="mongodb://localhost:27017/"):
        # 连接数据库
        myclient = pymongo.MongoClient(client_name)
        mydb = myclient[db_name]
        return mydb

    @staticmethod
    def create_collection(coll_name="tags"):
        mydb = CollectionFactory.create_client_and_db()
        mycol =mydb[coll_name]
        return mycol

if __name__ == '__main__':
    mycoll = CollectionFactory.create_client_and_db()
    colllist = mycoll.list_collection_names()
    for sites in colllist:
        print(sites)


