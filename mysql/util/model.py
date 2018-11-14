# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime, SmallInteger, MetaData
from sqlalchemy.ext.declarative import declarative_base

from mysql.util.engine_factory import EngineFactory

Base = declarative_base()


class PostsRecord(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True, name="Id")
    post_type_id = Column(SmallInteger, name="PostTypeId")
    accepted_answer_id = Column(Integer, name="AcceptedAnswerId")
    parent_id = Column(Integer, name="ParentId")
    score = Column(Integer, name="Score")
    view_count = Column(Integer, name="ViewCount")
    body = Column(Text(), name="Body")
    owner_user_id = Column(Integer, name="OwnerUserId")
    owner_display_name = Column(String(256), name="OwnerDisplayName")
    last_editor_user_id = Column(Integer, name="LastEditorUserId")
    last_edit_date = Column(DateTime(), name="LastEditDate")
    last_activity_date = Column(DateTime(), name="LastActivityDate")
    title = Column(String(256), name="Title")
    tags = Column(String(256), name="Tags")
    answer_count = Column(Integer, name="AnswerCount")
    comment_count = Column(Integer, name="CommentCount")
    favorite_count = Column(Integer, name="FavoriteCount")
    creation_date = Column(DateTime(), name="CreationDate")

    __table_args__ = (
        {
            "mysql_charset": "utf8"
        },
        # Index('update_index', 'view_count', 'score')  #给view_count和score创建索引，索引名为update_index
    )

    def __init__(self):
        pass

    def make_copy(self):
        post = PostsRecord()

        post.id = self.id

        post.post_type_id = self.post_type_id

        post.accepted_answer_id = self.accepted_answer_id

        post.parent_id = self.parent_id

        post.score = self.score

        post.view_count = self.view_count

        post.body = self.body

        post.owner_user_id = self.owner_user_id

        post.owner_display_name = self.owner_display_name

        post.last_editor_user_id = self.last_editor_user_id

        post.last_edit_date = self.last_edit_date

        post.last_activity_date = self.last_activity_date

        post.title = self.title

        post.tags = self.tags

        post.answer_count = self.answer_count

        post.comment_count = self.comment_count

        post.favorite_count = self.favorite_count

        post.creation_date = self.creation_date

        return post

    def make_copy_without_primary_key(self):
        post = PostsRecord()

        post.post_type_id = self.post_type_id

        post.accepted_answer_id = self.accepted_answer_id

        post.parent_id = self.parent_id

        post.score = self.score

        post.view_count = self.view_count

        post.body = self.body

        post.owner_user_id = self.owner_user_id

        post.owner_display_name = self.owner_display_name

        post.last_editor_user_id = self.last_editor_user_id

        post.last_edit_date = self.last_edit_date

        post.last_activity_date = self.last_activity_date

        post.title = self.title

        post.tags = self.tags

        post.answer_count = self.answer_count

        post.comment_count = self.comment_count

        post.favorite_count = self.favorite_count

        post.creation_date = self.creation_date

        return post

    def __repr__(self):
        return '<POSTS: id=%r score=%r title=%r tags=%r>' % (
            self.id, self.score, self.title, self.tags)

    @staticmethod
    def delete_all(session):
        session.query(PostsRecord).delete()
        session.commit()

    @staticmethod
    def delete_by_id(session, id):
        session.query(PostsRecord).filter(PostsRecord.id == id).delete()


class UsersRecord(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, name="Id")
    reputation = Column(Integer, name="Reputation")
    creation_date = Column(DateTime(), name="CreationDate")
    display_name = Column(String(256), name="DisplayName")
    last_access_date = Column(DateTime(), name="LastAccessDate")
    views = Column(Integer, name="Views")
    web_site_url = Column(String(256), name="WebsiteUrl")
    location = Column(String(256), name="Location")
    about_me = Column(Text(), name="AboutMe")
    age = Column(Integer, name="Age")
    up_votes = Column(Integer, name="UpVotes")
    down_votes = Column(Integer, name="DownVotes")
    email_hash = Column(String(256), name="EmailHash")

    __table_args__ = ({
        "mysql_charset": "utf8",
    })

    def __init__(self):
        pass

    @staticmethod
    def delete_all(session):
        session.query(UsersRecord).delete()
        session.commit()

    def make_copy(self):
        user = UsersRecord()

        user.id = self.id

        user.reputation = self.reputation

        user.creation_date = self.creation_date

        user.display_name = self.display_name

        user.last_access_date = self.last_access_date

        user.views = self.views

        user.web_site_url = self.web_site_url

        user.location = self.location

        user.about_me = self.about_me

        user.age = self.age

        user.up_votes = self.up_votes

        user.down_votes = self.down_votes

        user.email_hash = self.email_hash

        return user

    def make_copy_without_primary_key(self):
        user = UsersRecord()

        user.reputation = self.reputation

        user.creation_date = self.creation_date

        user.display_name = self.display_name

        user.last_access_date = self.last_access_date

        user.views = self.views

        user.web_site_url = self.web_site_url

        user.location = self.location

        user.about_me = self.about_me

        user.age = self.age

        user.up_votes = self.up_votes

        user.down_votes = self.down_votes

        user.email_hash = self.email_hash

        return user


if __name__ == "__main__":
    engine = EngineFactory.create_engine_to_test_so()
    metadata = MetaData(bind=engine)
    # create all the table by model
    Base.metadata.create_all(bind=engine)
