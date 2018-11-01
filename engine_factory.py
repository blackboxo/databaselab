from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

metadata = MetaData()


class EngineFactory:
    @staticmethod
    def create_engine_to_so_old(echo=True):
        engine = create_engine("mysql+pymysql://root:root@10.131.252.160/stackoverflow?charset=utf8", encoding='utf-8',
                               echo=echo)
        return engine

    @staticmethod
    def create_engine_to_so(echo=True):
        engine = create_engine("mysql+pymysql://root:root@10.131.252.160/testso?charset=utf8", encoding='utf-8',
                               echo=echo)
        return engine

    @staticmethod
    def create_session_to_new_so(autocommit=False, echo=True):
        engine = EngineFactory.create_engine_to_so(echo=echo)
        Session = sessionmaker(bind=engine, autocommit=autocommit)
        session = Session()
        return session

    @staticmethod
    def create_session_to_so_old(autocommit=False, echo=True):
        engine = EngineFactory.create_engine_to_so_old(echo=echo)
        Session = sessionmaker(bind=engine, autocommit=autocommit)
        session = Session()
        return session