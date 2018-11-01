# coding=utf-8
# 整个脚本用来测试在一张新的表中插入数据的需要花的时间，需要有一张表，里面已经存有完整的数据
# 目前两个实现了两者不同的测试用例，一个逐条插入，一个是批量插入。

import datetime
import json

from engine_factory import EngineFactory
from model import PostsRecord


def insert_batch(num, clean=True):
    starttime = datetime.datetime.now()

    old_session = EngineFactory.create_session_to_so_old(echo=False)
    new_session = EngineFactory.create_session_to_new_so(echo=False)

    old_post_list = old_session.query(PostsRecord).limit(num)
    for post in old_post_list:
        new_session.add(post.make_copy())

    ## 全部写入缓存再一次性commit写入数据库

    new_session.commit()

    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("test_insert_batch num={num} time={time}".format(num=num, time=time))
    if clean:
        PostsRecord.delete_all(new_session)

    return {
        "type": "insert batch",
        "num": num,
        "time": time
    }


def insert_seperate(num, clean=True):
    starttime = datetime.datetime.now()

    old_session = EngineFactory.create_session_to_so_old(echo=False)
    new_session = EngineFactory.create_session_to_new_so(echo=False)

    old_post_list = old_session.query(PostsRecord).limit(num)
    for post in old_post_list:
        new_session.add(post.make_copy())
        ## 每插入一条就commit写入数据库
        new_session.commit()

    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("test_insert_seperate num={num} time={time}".format(num=num, time=time))
    if clean:
        PostsRecord.delete_all(new_session)

    return {
        "type": "insert seperate",
        "num": num,
        "time": time
    }


def start_test_insert_and_record_result():
    max_test_num = 300
    result_list = []
    for num in range(10, max_test_num, 100):
        result = insert_batch(num=num)
        result_list.append(result)
        result = insert_seperate(num=num)
        result_list.append(result)

    output_file_name = "experiment_insert.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    start_test_insert_and_record_result()
