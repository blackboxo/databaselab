# coding=utf-8
# 整个脚本用来测试在一张新的表中查询数据的需要花的时间
# 目前两个实现了四个不同的测试用例，单表单条件查询，单表多条件查询，多表联合查询，聚合查询。

import datetime
import json

from engine_factory import EngineFactory
from model import PostsRecord, UsersRecord
from sqlalchemy.sql import func


def search_one_table_one_filter(num, clean=True, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_session_to_test_so(echo=False)
        res = session.query(PostsRecord).limit(num).all()
        print("search_one_table_one_filter_result:", res)

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_one_table_one_filter num={num} time={time}".format(
            num=num, time=time))
        if clean:
            PostsRecord.delete_all(session)
        sum_time = sum_time + time

    return {
        "type": "search_one_table_one_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def search_one_table_mul_filter(num, clean=True, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_session_to_test_so(echo=False)

        res = session.query(PostsRecord).filter(
            PostsRecord.owner_user_id < num & PostsRecord.view_count > 1000
        ).all()
        print("search_one_table_mul_filter_result:", res)

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_one_table_mul_filter num={num} time={time}".format(
            num=num, time=time))
        if clean:
            PostsRecord.delete_all(session)
        sum_time = sum_time + time
    return {
        "type": "search_one_table_mul_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def search_multi_table(num, clean=True, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_session_to_test_so(echo=False)

        res = session.query(
            PostsRecord.title, PostsRecord.tags, PostsRecord.favorite_count,
            UsersRecord.display_name, UsersRecord.reputation).filter(
                PostsRecord.owner_user_id ==
                UsersRecord.id & UsersRecord.reputation > num).all()
        print("search_multi_table_result:", res)

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_multi_table num={num} time={time}".format(
            num=num, time=time))
        if clean:
            PostsRecord.delete_all(session)
        sum_time = sum_time + time
    return {
        "type": "search_multi_table",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def search_aggregate(num, clean=True, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_session_to_test_so(echo=False)

        res = session.query(
            func.sum(PostsRecord.favorite_count), UsersRecord.display_name,
            UsersRecord.reputation).filter(
                UsersRecord.id < num & PostsRecord.owner_user_id ==
                UsersRecord.id).all()
        print("search_aggregate_result:", res)

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_aggregate num={num} time={time}".format(
            num=num, time=time))
        if clean:
            PostsRecord.delete_all(session)
        sum_time = sum_time + time
    return {
        "type": "search_aggregate",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def start_test_search_and_record_result(start_test_num=1,
                                        max_test_num=5,
                                        iteration_num=3,
                                        step=1):
    result_list = []
    for num in range(start_test_num, max_test_num, step):

        ## 测试单表单条件查询平均运行时间值
        result = search_one_table_one_filter(
            num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试单表多条件查询平均运行时间值
        result = search_one_table_mul_filter(
            num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试多表联合查询平均运行时间值
        result = search_multi_table(
            num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试聚合查询平均运行时间值
        result = search_aggregate(num=num, average_iteration_num=iteration_num)
        result_list.append(result)

    output_file_name = "experiment_search.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    start_test_search_and_record_result()
