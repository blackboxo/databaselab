# coding=utf-8
from mysql.delete_filter import start_test_delete_filter_and_record_result
from mysql.insert_delete import start_test_insert_and_delete_and_record_result
from mysql.match import start_test_search_and_record_result
from mysql.update import start_test_update_and_record_result

if __name__ == "__main__":
    ## 这个脚本负责批量进行所有测试
    start_test_insert_and_delete_and_record_result(
        start_test_num=10000, max_test_num=110000, step=10000, iteration_num=3)

    start_test_delete_filter_and_record_result(
        start_test_num=10000, max_test_num=110000, step=10000, iteration_num=3)

    #start_test_update_and_record_result(
    #    start_test_num=10000, max_test_num=100000, step=10000, iteration_num=3)

    #start_test_search_and_record_result(
    #    start_test_num=10000, max_test_num=100000, step=10000, iteration_num=3)
