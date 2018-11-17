# coding=utf-8
# 整个脚本用来测试在一张新的表中查询数据的需要花的时间
# 目前两个实现了四个不同的测试用例，单表单条件查询，单表多条件查询，多表联合查询，聚合查询。

import datetime
import json

from util.engine_factory import EngineFactory
from util.model import PostsRecord, UsersRecord
from sqlalchemy.sql import func
from sqlalchemy import text


def search_one_table_one_filter(num, average_iteration_num, session):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        res = session.query(PostsRecord).limit(num).count()
        # if len(res) > 0:
        #     print("search_one_table_one_filter_result:", len(res), ":", res[0])
        # else:
        #     print("search_one_table_one_filter_result: null")

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_one_table_one_filter num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time

    return {
        "type": "search_one_table_one_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def search_one_table_mul_filter(num, average_iteration_num, session):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()
        session = EngineFactory.create_engine_to_test_so()
        # res = session.query(PostsRecord).filter(
        #     PostsRecord.view_count > 1000,
        #     PostsRecord.owner_user_id < num)
        # if len(res) > 0:
        #     print("search_one_table_mul_filter_result:", len(res), ":", res[0])
        # else:
        #     print("search_one_table_mul_filter_result: null")
        conn = session.connect()
        sql = 'SELECT * FROM posts WHERE posts.ViewCount > 1000 and posts.OwnerUserId < {num}'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("search_one_table_mul_filter_result:", res.rowcount)
        conn.close()
        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_one_table_mul_filter num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time
    return {
        "type": "search_one_table_mul_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def search_multi_table(num, average_iteration_num, session):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()
        session = EngineFactory.create_engine_to_test_so()
        # res = session.query(
        #     PostsRecord.title, PostsRecord.tags, PostsRecord.favorite_count,
        #     UsersRecord.display_name, UsersRecord.reputation).filter(
        #         PostsRecord.owner_user_id == UsersRecord.id,
        #         UsersRecord.reputation > num)
        # if len(res) > 0:
        #     print("search_multi_table_result:", len(res), ":", res[0])
        # else:
        #     print("search_multi_table_result: null")
        conn = session.connect()
        sql = 'SELECT posts.Title,posts.Tags,posts.FavoriteCount,users.DisplayName,users.Reputation FROM posts INNER JOIN users ON users.Id = posts.OwnerUserId WHERE users.Reputation > {num}'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("search_multi_table_result:", res.rowcount)
        conn.close()
        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_multi_table num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time
    return {
        "type": "search_multi_table",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def search_aggregate(num, average_iteration_num, session):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        # res = session.query(
        #     func.sum(PostsRecord.favorite_count), UsersRecord.display_name,
        #     UsersRecord.reputation).filter(
        #         PostsRecord.owner_user_id == UsersRecord.id,
        #         UsersRecord.id < num).group_by(UsersRecord.id)
        # if len(res) > 0:
        #     print("search_aggregate_result:", len(res), ":", res[0], res[1])
        # else:
        #     print("search_aggregate_result: null")
        conn = session.connect()
        sql = 'SELECT SUM(posts.FavoriteCount),users.DisplayName,users.Reputation FROM posts INNER JOIN users ON users.Id = posts.OwnerUserId WHERE users.Id < {num} GROUP BY users.Id'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("search_aggregate_result:", res.rowcount)
        conn.close()
        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_search_aggregate num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time
    return {
        "type": "search_aggregate",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def start_test_search_and_record_result(start_test_num=20000,
                                        max_test_num=100000,
                                        iteration_num=3,
                                        step=10000):
    result_list = []
    session = EngineFactory.create_session_to_test_so(echo=False)
    for num in range(start_test_num, max_test_num, step):

        ## 测试单表单条件查询平均运行时间值
        result = search_one_table_one_filter(
            num=num, average_iteration_num=iteration_num, session=session)
        result_list.append(result)

        ## 测试单表多条件查询平均运行时间值
        result = search_one_table_mul_filter(
            num=num, average_iteration_num=iteration_num, session=session)
        result_list.append(result)

        ## 测试多表联合查询平均运行时间值
        result = search_multi_table(
            num=num, average_iteration_num=iteration_num, session=session)
        result_list.append(result)

        ## 测试聚合查询平均运行时间值
        result = search_aggregate(
            num=num, average_iteration_num=iteration_num, session=session)
        result_list.append(result)

    output_file_name = "experiment_search.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    start_test_search_and_record_result()
