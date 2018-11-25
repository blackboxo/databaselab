# coding=utf-8
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

metadata = MetaData()


class EngineFactory:
    """
    这个类负责创建数据库的连接，stackoverflow的数据是作为数据备份的SO，testso是所有测试进行的SO
    """
    @staticmethod
    def create_engine_to_databackup_so(echo=True):
        #engine = create_engine("mysql+pymysql://root:Root2018!@39.108.182.236/stackoverflow?charset=utf8", encoding='utf-8',echo=echo)

        # engine = create_engine("mysql+pymysql://root:root@10.131.252.160/stackoverflow?charset=utf8", encoding='utf-8',
        #                        echo=echo)
        engine = create_engine("mysql+pymysql://root:root@localhost/stackoverflow?charset=utf8", encoding='utf-8',echo=echo)
        return engine

    @staticmethod
    def create_engine_to_test_so(echo=True):
        engine = create_engine("mysql+pymysql://root:root@localhost/testso?charset=utf8", encoding='utf-8',echo=echo)
        #engine = create_engine("mysql+pymysql://root:Root2018!@39.108.182.236/testso?charset=utf8", encoding='utf-8',echo=echo)
        #engine = create_engine("mysql+pymysql://root:root@10.141.221.87/test?charset=utf8", encoding='utf-8',echo=echo)
        return engine

    @staticmethod
    def create_session_to_test_so(autocommit=False, echo=True):
        engine = EngineFactory.create_engine_to_test_so(echo=echo)
        Session = sessionmaker(bind=engine, autocommit=autocommit)
        session = Session()
        return session

    @staticmethod
    def create_session_to_databackup_so(autocommit=False, echo=True):
        engine = EngineFactory.create_engine_to_databackup_so(echo=echo)
        Session = sessionmaker(bind=engine, autocommit=autocommit)
        session = Session()
        return session