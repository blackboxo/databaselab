# coding=utf-8
## 这个文件负责创建测试数据
from engine_factory import EngineFactory

from model import PostsRecord, UsersRecord


def create_post_test_data_in_test_db(num):
    """
    利用全表服务器在测试服务器上创建新的数据,这个创建得是用户表得测试数据
    :param num: 要取得测试数据得数目
    :return:
    """
    ## 接下来的三行代码从旧的总表中获取想要的数目的数据，作为之后插入的数据源，其实也可以读文件得到，但是那就太麻烦了
    old_session = EngineFactory.create_session_to_databackup_so(echo=False)
    new_session = EngineFactory.create_session_to_test_so(echo=False)
    old_post_list = old_session.query(PostsRecord).limit(num)

    for post in old_post_list:
        new_session.add(post.make_copy())

    new_session.commit()


def create_user_test_data_in_test_db(num):
    """
    利用全表服务器在测试服务器上创建新的数据，为测试做准备
    :param num: 要取得测试数据得数目
    :return:
    """
    ## 接下来的三行代码从旧的总表中获取想要的数目的数据，作为之后插入的数据源，其实也可以读文件得到，但是那就太麻烦了
    old_session = EngineFactory.create_session_to_databackup_so(echo=False)
    new_session = EngineFactory.create_session_to_test_so(echo=False)
    old_user_list = old_session.query(UsersRecord).limit(num)

    for user in old_user_list:
        new_session.add(user.make_copy())

    new_session.commit()


def delete_user_test_data_in_test_db():
    """
    删除测试服务器得用户表数据
    :param num: 要取得测试数据得数目
    :return:
    """
    test_session = EngineFactory.create_session_to_test_so(echo=False)
    UsersRecord.delete_all(test_session)


def delete_post_test_data_in_test_db():
    """
    删除测试服务器得帖子表数据
    :param num: 要取得测试数据得数目
    :return:
    """
    test_session = EngineFactory.create_session_to_test_so(echo=False)
    PostsRecord.delete_all(test_session)


if __name__=="__main__":
    create_user_test_data_in_test_db(100000)
