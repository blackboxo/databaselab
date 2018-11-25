# coding=utf-8
import datetime
import json

from util.data_for_test_creator import create_post_test_data_in_test_db, delete_post_test_data_in_test_db
from util.engine_factory import EngineFactory
from util.index_util import add_score_view_count_index, delete_score_view_count_index
from util.model import PostsRecord


def delete_multi_filter(num, index=True):
    """
    根据复合条件从数据库Post删除数据
    :param num: 插入的数据数目
    :param clean:是否清空表
    :return:花费的时间
    """
    if index:
        add_score_view_count_index()
    create_post_test_data_in_test_db(num=num)

    test_session = EngineFactory.create_session_to_test_so(echo=False)
    starttime = datetime.datetime.now()
    test_session.query(PostsRecord).filter(
        PostsRecord.score < 20, PostsRecord.view_count < 100).delete()
    test_session.commit()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).total_seconds()
    print("delete_multi_filter num={num} time={time}".format(
        num=num, time=time))
    if index:
        delete_score_view_count_index()

    delete_post_test_data_in_test_db()
    return time


def delete_multi_filter_repeately(num, repeat_time=1):
    """
    测试插入和删除的实验，采用批量的方式
    :param num:
    :param clean:
    :param repeat_time:
    :return:
    """

    delete_sum_time_without_index = 0.0
    delete_sum_time_with_index = 0.0
    for i in range(0, repeat_time):
        time = delete_multi_filter(num, index=False)
        delete_sum_time_without_index = delete_sum_time_without_index + time
        time = delete_multi_filter(num, index=True)
        delete_sum_time_with_index = delete_sum_time_with_index + time
    return [{
        "type": "delete_multi-filters",
        "num": num,
        "time": delete_sum_time_without_index / repeat_time
    },
            {
                "type": "delete_multi-filters_index",
                "num": num,
                "time": delete_sum_time_with_index / repeat_time
            }]


def start_test_delete_filter_and_record_result(start_test_num=100,
                                               max_test_num=2000,
                                               iteration_num=3,
                                               step=100):
    result_list = []
    # test_data_point = range(start_test_num, max_test_num + 1, step)
    for num in range(start_test_num, max_test_num, step):
        ## 计算平均运行时间值
        result = delete_multi_filter_repeately(
            num=num, repeat_time=iteration_num)
        result_list.extend(result)
        # output_file_name = "experiment_delete_filter_mysql.json"
        # with open(output_file_name, "w") as f:
        #     json.dump(result_list, f)
    output_file_name = "experiment_delete_filter_mysql.json"
    with open(output_file_name, "w") as f:
        json.dump(result_list, f)


if __name__ == "__main__":
    # start_test_delete_filter_and_record_result(start_test_num=10000,
    #                                                max_test_num=100000,
    #                                                step=10000,
    #                                                iteration_num=3)

    start_test_delete_filter_and_record_result(
        start_test_num=100, max_test_num=200, step=100, iteration_num=3)
