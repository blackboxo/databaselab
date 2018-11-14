from mysql.util.insert_delete_experiment import start_test_insert_and_delete_and_record_result

if __name__ == "__main__":
    start_test_insert_and_delete_and_record_result(start_test_num=10000,
                                                   max_test_num=100000,
                                                   step=10000,
                                                   iteration_num=3)
