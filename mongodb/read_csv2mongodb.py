# -*- coding: UTF-8 -*-
'''
@project:databaselab2
@author:wangfy
@time:2018/11/12 18:02
'''

import pymongo
import csv
import os
import datetime
from collection_factory import CollectionFactory
from pymongo import InsertOne

def read_csv2mongodb(filename,collectionName):
    mydb = CollectionFactory.create_client_and_db()
    # filename = "test2.csv"
    mydb[collectionName].delete_many({})
    count = 0
    with open(filename, encoding='utf-8',errors="ignore") as fr:
        rows = csv.DictReader(fr)
        post_list = []
        # print(type(rows))
        for row in rows:
            post_list.append(row)
            count += 1
        mydb[collectionName].bulk_write(list(map(InsertOne, post_list)))
    return count

if __name__ == '__main__':
    fileName = "posts.csv"
    collectionName = "posts"
    count = read_csv2mongodb(fileName,collectionName)
    print(count)


