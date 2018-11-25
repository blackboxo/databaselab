# coding=utf-8
# 整个脚本用来测试在一张新的表中插入数据的需要花的时间，需要有一张表，里面已经存有完整的数据
# 目前两个实现了两者不同的测试用例，一个逐条插入，一个是批量插入。

import datetime
import json

from util.engine_factory import EngineFactory
from util.model import PostsRecord


def insert_batch_with_primary_key(num, clean=True):
    """
    批量地往数据库插入数据,指定主键的值
    :param num: 插入的数据数目
    :param clean:是否清空表
    :return:花费的时间
    """
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
    print("insert_batch_with_primary_key num={num} time={time}".format(num=num, time=time))

    # 清空所有插入的数据
    if clean:
        PostsRecord.delete_all(test_session)
    return time


def delete_batch_with_primary_key(num):
    """
    批量地往数据库插入数据,指定主键的值
    :param num: 插入的数据数目
    :param clean:是否清空表
    :return:花费的时间
    """
    old_session = EngineFactory.create_session_to_databackup_so(echo=False)
    test_session = EngineFactory.create_session_to_test_so(echo=False)
    old_post_list = old_session.query(PostsRecord).limit(num)
    starttime = datetime.datetime.now()
    for post in old_post_list:
        PostsRecord.delete_by_id(session=test_session, id=post.id)
    ## 全部删除操作提交再一次性commit修改数据库
    test_session.commit()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("delete_batch_with_primary_key num={num} time={time}".format(num=num, time=time))
    return time


def delete_separate_with_primary_key(num):
    """
    批量地往数据库插入数据,指定主键的值
    :param num: 插入的数据数目
    :param clean:是否清空表
    :return:花费的时间
    """
    old_session = EngineFactory.create_session_to_databackup_so(echo=False)
    test_session = EngineFactory.create_session_to_test_so(echo=False)
    old_post_list = old_session.query(PostsRecord).limit(num)
    starttime = datetime.datetime.now()
    for post in old_post_list:
        PostsRecord.delete_by_id(session=test_session, id=post.id)
        ## 每次删除操作提交再一次性commit修改数据库
        test_session.commit()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("delete_separate_with_primary_key num={num} time={time}".format(num=num, time=time))
    return time


def insert_batch_without_primary_key(num, clean=True):
    """
    批量地往数据库插入数据，不指定主键的值
    :param num: 插入的数据数目
    :param clean:是否清空表
    :return:花费的时间
    """
    ## 接下来的三行代码从旧的总表中获取想要的数目的数据，作为之后插入的数据源，其实也可以读文件得到，但是那就太麻烦了
    old_session = EngineFactory.create_session_to_databackup_so(echo=False)
    test_session = EngineFactory.create_session_to_test_so(echo=False)
    old_post_list = old_session.query(PostsRecord).limit(num)
    starttime = datetime.datetime.now()
    for post in old_post_list:
        test_session.add(post.make_copy_without_primary_key())
    ## 全部写入缓存再一次性commit写入数据库
    test_session.commit()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("insert_batch_without_primary_key num={num} time={time}".format(num=num, time=time))

    # 清空所有插入的数据
    if clean:
        PostsRecord.delete_all(test_session)
    return time


def insert_separate_with_primary_key(num, clean=True):
    """
       逐条地往数据库插入数据，指定主键的值
       :param num: 插入的数据数目
       :param clean:是否清空表
       :return:花费的时间
       """
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
    print("insert_separate_with_primary_key num={num} time={time}".format(num=num, time=time))
    if clean:
        PostsRecord.delete_all(test_session)
    return time


def insert_separate_without_primary_key(num, clean=True):
    """
           逐条地往数据库插入数据，不指定主键的值
           :param num: 插入的数据数目
           :param clean:是否清空表
           :return:花费的时间
           """
    old_session = EngineFactory.create_session_to_databackup_so(echo=False)
    test_session = EngineFactory.create_session_to_test_so(echo=False)
    old_post_list = old_session.query(PostsRecord).limit(num)
    starttime = datetime.datetime.now()
    for post in old_post_list:
        test_session.add(post.make_copy_without_primary_key())
        ## 每插入一条就commit写入数据库
        test_session.commit()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("insert_separate_without_primary_key num={num} time={time}".format(num=num, time=time))
    if clean:
        PostsRecord.delete_all(test_session)
    return time


def insert_delete_separate_repeatedly(num, repeat_time=1):
    """
        测试插入和删除的实验，采用逐条的方式
        :param num:
        :param repeat_time:
        :return:
        """

    insert_id_sum_time = 0.0
    delete_sum_time = 0.0
    insert_sum_time = 0.0

    for i in range(0, repeat_time):
        time = insert_separate_with_primary_key(num, clean=False)
        insert_id_sum_time = insert_id_sum_time + time

        time = delete_separate_with_primary_key(num)
        delete_sum_time = delete_sum_time + time

        time = insert_separate_without_primary_key(num=num, clean=True)
        insert_sum_time = insert_sum_time + time

    return [
        {
            "type": "insert id separate",
            "num": num,
            "time": insert_id_sum_time / repeat_time
        }, {
            "type": "delete id separate",
            "num": num,
            "time": delete_sum_time / repeat_time
        },
        {
            "type": "insert separate",
            "num": num,
            "time": insert_sum_time / repeat_time
        }

    ]


def insert_delete_batch_repeatedly(num, repeat_time=1):
    """
    测试插入和删除的实验，采用批量的方式
    :param num:
    :param clean:
    :param repeat_time:
    :return:
    """

    insert_id_sum_time = 0.0
    delete_sum_time = 0.0
    insert_sum_time = 0.0

    for i in range(0, repeat_time):
        time = insert_batch_with_primary_key(num, clean=False)
        insert_id_sum_time = insert_id_sum_time + time

        time = delete_batch_with_primary_key(num)
        delete_sum_time = delete_sum_time + time

        time = insert_batch_without_primary_key(num=num, clean=True)
        insert_sum_time = insert_sum_time + time

    return [
        {
            "type": "insert id batch",
            "num": num,
            "time": insert_id_sum_time / repeat_time
        }, {
            "type": "delete id batch",
            "num": num,
            "time": delete_sum_time / repeat_time
        },
        {
            "type": "insert batch",
            "num": num,
            "time": insert_sum_time / repeat_time
        }

    ]


def start_test_insert_and_delete_and_record_result(start_test_num=100, max_test_num=2000, iteration_num=3, step=100):
    result_list = []
    #test_data_point = range(start_test_num, max_test_num + 1, step)
    for num in range(start_test_num, max_test_num, step):
        ## 测试批量的插入操作时间

        ## 计算平均运行时间值
        result = insert_delete_batch_repeatedly(num=num, repeat_time=iteration_num)
        result_list.extend(result)

        ## 测试非批量的插入操作时间
        result = insert_delete_separate_repeatedly(num=num, repeat_time=iteration_num)
        result_list.extend(result)

        # output_file_name = "experiment_insert_delete_mysql.json"
        # with open(output_file_name, "w") as f:
        #     json.dump(result_list, f)
    output_file_name = "experiment_insert_delete_mysql.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    start_test_insert_and_delete_and_record_result(start_test_num=10000,
                                                   max_test_num=110000,
                                                   step=10000,
                                                   iteration_num=3)

    # start_test_insert_and_delete_and_record_result(start_test_num=100,
    #                                                max_test_num=200,
    #                                                step=100,
    #                                                iteration_num=3)