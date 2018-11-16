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

def read_csv2mongodb_forposts(filename,collectionName):
    mydb = CollectionFactory.create_client_and_db()
    mydb[collectionName].delete_many({})
    count = 0
    with open(filename, encoding='utf-8',errors="ignore") as fr:
        rows = csv.DictReader(fr)
        post_list = []
        # print(type(rows))
        for row in rows:
            # if len(row["OwnerUserId"]) > 10 or len(row["Views"]) > 7:
            #     continue
            row['Id'] = int(row['Id']) if row["Id"] != ''else 0
            row["PostTypeId"] = int(row["PostTypeId"]) if row["PostTypeId"] != ''else 0
            row["AcceptedAnswerId"] = int(row["AcceptedAnswerId"]) if row["AcceptedAnswerId"] != ''else 0
            row["ParentId"] = int(row["ParentId"]) if row["ParentId"] != ''else 0
            row["Score"] = int(row["Score"]) if row["Score"] != ''else 0
            row["ViewCount"] = int(row["ViewCount"]) if row["ViewCount"] != ''else 0
            row["OwnerUserId"] = int(row["OwnerUserId"]) if row["OwnerUserId"] != ''else 0
            row["LastEditorUserId"] = int(row["LastEditorUserId"]) if row["LastEditorUserId"] != ''else 0
            row["AnswerCount"] = int(row["AnswerCount"]) if row["AnswerCount"] != ''else 0
            row["CommentCount"] = int(row["CommentCount"]) if row["CommentCount"] != ''else 0
            row["FavoriteCount"] = int(row["FavoriteCount"]) if row["FavoriteCount"] != ''else 0
            post_list.append(row)
            count += 1
        mydb[collectionName].bulk_write(list(map(InsertOne, post_list)))
    return count

def read_csv2mongodb_forusers(filename,collectionName):
    mydb = CollectionFactory.create_client_and_db()
    mydb[collectionName].delete_many({})
    count = 0
    with open(filename, encoding='utf-8',errors="ignore") as fr:
        rows = csv.DictReader(fr)
        post_list = []
        for row in rows:
            if len(row["Age"])>3 or len(row["Views"])>7:
                continue
            # print(row['Id'])
            row['Id'] = int(row['Id']) if row["Id"] != ''else 0
            row["Reputation"] = int(row["Reputation"]) if row["Reputation"] != ''else 0
            row["Views"] = int(row["Views"]) if row["Views"] != ''else 0
            row["Age"] = int(row["Age"]) if row["Age"] != ''else 0
            row["UpVotes"] = int(row["UpVotes"]) if row["UpVotes"] != ''else 0
            row["DownVotes"] = int(row["DownVotes"]) if row["DownVotes"] != ''else 0
            post_list.append(row)
            count += 1
        mydb[collectionName].bulk_write(list(map(InsertOne, post_list)))
    return count

if __name__ == '__main__':
    start = datetime.datetime.now()
    fileName = "posts.csv"
    collectionName = "posts100"
    count = read_csv2mongodb_forposts(fileName,collectionName)
    print(count)



