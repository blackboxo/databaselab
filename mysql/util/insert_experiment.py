# coding=utf-8
# 整个脚本用来测试在一张新的表中插入数据的需要花的时间，需要有一张表，里面已经存有完整的数据
# 目前两个实现了两者不同的测试用例，一个逐条插入，一个是批量插入。

import datetime
import json

from engine_factory import EngineFactory
from model import PostsRecord


def insert_batch(num, clean=True, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):

        ## 接下来的三行代码从旧的总表中获取想要的数目的数据，作为之后插入的数据源，其实也可以读文件得到，但是那就太麻烦了
        old_session = EngineFactory.create_session_to_databackup_so(echo=False)
        test_session = EngineFactory.create_session_to_test_so(echo=False)
        old_post_list = old_session.query(PostsRecord).limit(num)

        starttime = datetime.datetime.now()

        for post in old_post_list:
            test_session.add(post.make_copy())

        ## 全部写入缓存再一次性commit写入数据库

        test_session.commit()
        endtime = datetime.datetime.now()

        time = (endtime - starttime).total_seconds()
        print("test_insert_batch num={num} time={time}".format(num=num, time=time))
        if clean:
            PostsRecord.delete_all(test_session)
        sum_time = sum_time + time

    return {
        "type": "insert batch",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def insert_separate(num, clean=True, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):

        old_session = EngineFactory.create_session_to_databackup_so(echo=False)
        test_session = EngineFactory.create_session_to_test_so(echo=False)

        old_post_list = old_session.query(PostsRecord).limit(num)

        starttime = datetime.datetime.now()

        for post in old_post_list:
            test_session.add(post.make_copy())
            ## 每插入一条就commit写入数据库
            test_session.commit()

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_insert_separate num={num} time={time}".format(num=num, time=time))
        if clean:
            PostsRecord.delete_all(test_session)
        sum_time = sum_time + time
    return {
        "type": "insert separate",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def start_test_insert_and_record_result(start_test_num=100, max_test_num=2000, iteration_num=3, step=100):
    result_list = []
    for num in range(start_test_num, max_test_num, step):
        ## 测试批量的插入操作时间

        ## 计算平均运行时间值
        result = insert_batch(num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试非批量的插入操作时间
        result = insert_separate(num=num, average_iteration_num=iteration_num)
        result_list.append(result)

    output_file_name = "experiment_insert.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    start_test_insert_and_record_result(max_test_num=300, iteration_num=3)
