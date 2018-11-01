# coding=utf-8
# 整个脚本用来测试在一张新的表中插入数据的需要花的时间，需要有一张表，里面已经存有完整的数据


import datetime

from engine_factory import EngineFactory
from model import PostsRecord


def test_insert_batch(num, clean=True):
    starttime = datetime.datetime.now()

    old_session = EngineFactory.create_session_to_so_old()
    new_session = EngineFactory.create_session_to_new_so()

    old_post_list = old_session.query(PostsRecord).limit(num)
    for post in old_post_list:
        new_session.add(post.make_copy())
    new_session.commit()

    endtime = datetime.datetime.now()
    time = endtime - starttime
    print("test_insert_batch num={num} time={time}".format(num=num, time=time))
    if clean:
        PostsRecord.delete_all(new_session)

    return {
        "type": "insert batch",
        "num": num,
        "time": time
    }


if __name__ == "__main__":
    max_test_num = 2000
    result_list = []
    for num in range(10, max_test_num, step=100):
        result = test_insert_batch(num=100)
        result_list.append(result)
