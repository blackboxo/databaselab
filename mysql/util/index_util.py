from sqlalchemy import text

from mysql.util.engine_factory import EngineFactory
from mysql.util.model import PostsRecord


def add_score_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    index_name = "score_index"
    text_sql = 'alter table {table_name} add index {index_name}(score)'.format(table_name=PostsRecord.__tablename__,
                                                                               index_name=index_name)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


def add_view_count_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    index_name = "view_count_index"
    text_sql = 'alter table {table_name} add index {index_name}(ViewCount)'.format(
        table_name=PostsRecord.__tablename__,
        index_name=index_name)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


def delete_score_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    index_name = "score_index"
    text_sql = 'alter table `{table_name}` drop index `{index_name}`'.format(table_name=PostsRecord.__tablename__,
                                                                             index_name=index_name)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


def delete_view_count_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    index_name = "view_count_index"
    text_sql = 'alter table `{table_name}` drop index `{index_name}`'.format(table_name=PostsRecord.__tablename__,
                                                                             index_name=index_name)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


def add_score_view_count_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    index_name = "score_view_count_index"
    text_sql = 'alter table {table_name} add index {index_name}(score,ViewCount)'.format(
        table_name=PostsRecord.__tablename__,
        index_name=index_name)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


def delete_score_view_count_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    index_name = "score_view_count_index"
    text_sql = 'alter table `{table_name}` drop index `{index_name}`'.format(table_name=PostsRecord.__tablename__,
                                                                             index_name=index_name)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


def show_index():
    engine = EngineFactory.create_engine_to_test_so()
    conn = engine.connect()
    text_sql = 'show index from {table_name}'.format(table_name=PostsRecord.__tablename__)
    s = text(text_sql)
    conn.execute(s)
    conn.close()


if __name__ == "__main__":
    add_score_view_count_index()
    show_index()
    # delete_view_count_index()
