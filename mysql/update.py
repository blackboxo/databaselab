# coding=utf-8
# 整个脚本用来测试在一张新的表中更新数据的需要花的时间
# 目前两个实现了四个不同的测试用例，单表单条件更新，单表多条件多值更新，多表联查单表更新，多表联查多表更新

import datetime
import json
from util.index_util import add_score_view_count_index, delete_score_view_count_index

from util.engine_factory import EngineFactory
from util.model import PostsRecord, UsersRecord
from sqlalchemy.sql import func
from sqlalchemy import text


def update_one_table_one_filter(num, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_session_to_test_so(echo=False)
        res = session.query(PostsRecord).filter(PostsRecord.id < num).update({
            'view_count':
            PostsRecord.view_count + 1
        })
        session.commit()
        print("update_one_table_one_filter_result:", res)

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_update_one_table_one_filter num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time

    for i in range(0, average_iteration_num):
        session = EngineFactory.create_session_to_test_so(echo=False)
        res = session.query(PostsRecord).filter(PostsRecord.id < num).update({
            'view_count':
            PostsRecord.view_count - 1
        })
        session.commit()
        print("update_one_table_one_filter_back_result:", res)
    return {
        "type": "update_one_table_one_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def update_one_table_mul_filter(num, average_iteration_num=1):
    add_score_view_count_index()
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_session_to_test_so(echo=False)

        res = session.query(PostsRecord).filter(
            PostsRecord.score > 20, PostsRecord.view_count > num).update({
                'view_count':
                PostsRecord.view_count + 1,
                'favorite_count':
                PostsRecord.favorite_count + 1
            })
        session.commit()
        print("update_one_table_mul_filter_result:", res)

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_update_one_table_mul_filter num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time

    for i in range(0, average_iteration_num):
        session = EngineFactory.create_session_to_test_so(echo=False)

        res = session.query(PostsRecord).filter(
            PostsRecord.score > 20, PostsRecord.view_count > num).update({
                'view_count':
                PostsRecord.view_count - 1,
                'favorite_count':
                PostsRecord.favorite_count - 1
            })
        session.commit()
        print("update_one_table_mul_filter_back_result:", res)
    return {
        "type": "update_one_table_mul_filter",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def update_multi_table(num, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_engine_to_test_so()

        # query = UsersRecord.update().values({
        #     'reputation':
        #     UsersRecord.reputation + 1
        # })
        # query = query.where(PostsRecord.owner_user_id == UsersRecord.id,
        #                     PostsRecord.view_count > num)
        # res = session.query(PostsRecord, UsersRecord).filter(
        #     PostsRecord.owner_user_id == UsersRecord.id,
        #     PostsRecord.view_count > num).update({
        #         'reputation':
        #         UsersRecord.reputation + 1
        #     })
        conn = session.connect()
        sql = 'UPDATE users INNER JOIN posts ON users.id = posts.OwnerUserId SET users.reputation = users.Reputation + 1 WHERE posts.ViewCount  > {num}'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("update_multi_table_result:", res.rowcount)
        conn.close()
        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_update_multi_table num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time

    for i in range(0, average_iteration_num):
        session = EngineFactory.create_engine_to_test_so()

        # res = session.query(PostsRecord, UsersRecord).filter(
        #     PostsRecord.owner_user_id == UsersRecord.id,
        #     PostsRecord.view_count > num).update({
        #         'reputation':
        #         UsersRecord.reputation - 1
        #     })
        # session.commit()
        conn = session.connect()
        sql = 'UPDATE users INNER JOIN posts ON users.Id = posts.OwnerUserId SET users.Reputation = users.Reputation - 1 WHERE posts.ViewCount  > {num}'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("update_multi_table_back_result:", res.rowcount)
        conn.close()
        
    return {
        "type": "update_multi_table",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def update_aggregate(num, average_iteration_num=1):
    sum_time = 0.0
    for i in range(0, average_iteration_num):
        starttime = datetime.datetime.now()

        session = EngineFactory.create_engine_to_test_so()

        # res = session.query(PostsRecord, UsersRecord).filter(
        #     PostsRecord.owner_user_id == UsersRecord.id,
        #     PostsRecord.view_count > num).update({
        #         'view_count':
        #         PostsRecord.view_count + 1,
        #         'reputation':
        #         UsersRecord.reputation + 1
        #     })
        # session.commit()
        conn = session.connect()
        sql = 'UPDATE users INNER JOIN posts ON users.Id = posts.OwnerUserId SET users.Reputation = users.Reputation + 1,posts.ViewCount = posts.ViewCount+1 WHERE posts.ViewCount > {num}'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("update_aggregate_result:",  res.rowcount)
        conn.close()
        

        endtime = datetime.datetime.now()
        time = (endtime - starttime).total_seconds()
        print("test_update_aggregate num={num} time={time}".format(
            num=num, time=time))
        sum_time = sum_time + time

    for i in range(0, average_iteration_num):
        session = EngineFactory.create_engine_to_test_so()

        # res = session.query(PostsRecord, UsersRecord).filter(
        #     PostsRecord.owner_user_id == UsersRecord.id,
        #     PostsRecord.view_count > num).update({
        #         'view_count':
        #         PostsRecord.view_count - 1,
        #         'reputation':
        #         UsersRecord.reputation - 1
        #     })
        # session.commit()
        conn = session.connect()
        sql = 'UPDATE users INNER JOIN posts ON users.Id = posts.OwnerUserId SET users.Reputations = users.Reputation - 1,posts.ViewCount = posts.ViewCount-1 WHERE posts.ViewCount > {num}'.format(
            num=num)
        s = text(sql)
        res = conn.execute(s)
        print("update_aggregate_back_result:", res.rowcount)
        conn.close()
        
    return {
        "type": "update_aggregate",
        "num": num,
        "time": sum_time / average_iteration_num
    }


def start_test_update_and_record_result((start_test_num=10000,
                                        max_test_num=100000,
                                        iteration_num=3,
                                        step=10000):
    result_list = []
    for num in range(start_test_num, max_test_num, step):
        ## 测试单表单条件更新平均运行时间值
        result = update_one_table_one_filter(
            num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试单表多条件多值更新平均运行时间值
        result = update_one_table_mul_filter(
            num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试多表联查单表更新平均运行时间值
        result = update_multi_table(
            num=num, average_iteration_num=iteration_num)
        result_list.append(result)

        ## 测试多表联查多表更新平均运行时间值
        result = update_aggregate(num=num, average_iteration_num=iteration_num)
        result_list.append(result)

    delete_score_view_count_index()
    output_file_name = "experiment_update.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    start_test_update_and_record_result()
