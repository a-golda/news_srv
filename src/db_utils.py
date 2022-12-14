import logging
import pandas as pd
from src.conf import Conf
from datetime import datetime
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, String, Integer, ARRAY, Float, DateTime, BOOLEAN

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NewsPostgreUtils:
    def __init__(self):
        self.db = create_engine(Conf.URL_DB)
        self.meta = MetaData(self.db)
        self.news_table = Table('news', self.meta,
                                Column('news_id', Integer),
                                Column('tag_id', Integer),
                                Column('source', String),
                                Column('role', String),
                                Column('url', String),
                                Column("text_formated", String),
                                Column('parsed_news', String),
                                Column('score', Float),
                                Column('date_updated', DateTime),
                                Column("news_date", DateTime))

        if not inspect(self.db).has_table('news'):
            with self.db.connect() as _:
                self.news_table.create()
        logger.info(f"News table has been created successfully!")

    def update_news_table(self, news_id, tag_id, source,
                          role, url, text_formated,
                          parsed_news, score, news_date,
                          date_updated=datetime.now()):

        with self.db.connect() as conn:
            statement = self.news_table.insert().values(news_id=news_id,
                                                        tag_id=tag_id,
                                                        source=source,
                                                        role=role,
                                                        url=url,
                                                        text_formated=text_formated,
                                                        parsed_news=parsed_news,
                                                        score=score,
                                                        news_date=news_date,
                                                        date_updated=date_updated)
            conn.execute(statement)

    def select_by_news_id(self, news_id):

        result = []
        select_statement = self.news_table.select().where(self.news_table.c.news_id == news_id)
        with self.db.connect() as conn:
            result_set = conn.execute(select_statement)
            for row in result_set:
                result.append(row)
        result = result[0]
        response = {
            "news_id": result[0],
            "tag_id": result[1],
            "source": result[2],
            "role": result[3],
            "url": result[4],
            "text_formated":[5],
            "parsed_news": result[6],
            "score": result[7],
            "news_date": result[8],
            "date_updated": result[9]
        }
        return response

    def delete_by_news_id(self, news_id):
        delete_statement = self.news_table.delete().where(self.news_table.c.news_id == news_id)
        with self.db.connect() as conn:
            conn.execute(delete_statement)


class UsersHistPostgreUtils:
    def __init__(self):
        self.db = create_engine(Conf.URL_DB)
        self.meta = MetaData(self.db)
        self.uh_table = Table('users_history', self.meta,
                              Column('user_id', Integer),
                              Column('news_id', Integer),
                              Column('date_updated', DateTime))

        if not inspect(self.db).has_table('users_history'):
            with self.db.connect() as _:
                self.uh_table.create()
        logger.info(f"Users history table has been created successfully!")

    def update_uh_table(self, user_id, news_id, date_updated=datetime.now()):
        with self.db.connect() as conn:
            statement = self.uh_table.insert().values(user_id=user_id,
                                                      news_id=news_id,
                                                      date_updated=date_updated)
            conn.execute(statement)

    def select_by_user_id(self, user_id):
        result = []
        select_statement = self.uh_table.select().where(self.uh_table.c.user_id == user_id)
        with self.db.connect() as conn:
            result_set = conn.execute(select_statement)
            for row in result_set:
                result.append(row)
        result = result[0]
        response = {
            "user_id": result[0],
            "news_id": result[1],
            "date_updated": result[2],
        }
        return response

    def delete_by_user_id(self, user_id):
        delete_statement = self.uh_table.delete().where(self.uh_table.c.user_id == user_id)
        with self.db.connect() as conn:
            conn.execute(delete_statement)


class UsersPostgreUtils:
    def __init__(self):
        self.db = create_engine(Conf.URL_DB)
        self.meta = MetaData(self.db)
        self.u_table = Table('users', self.meta,
                             Column('user_id', Integer),
                             Column('is_bot', BOOLEAN),
                             Column('first_name', String),
                             Column('last_name', String),
                             Column('username', String),
                             Column('role', String),
                             Column('language_code', String),
                             Column('date_updated', DateTime))

        if not inspect(self.db).has_table('users'):
            with self.db.connect() as _:
                self.u_table.create()
        logger.info(f"Users table has been created successfully!")

    def update_u_table(self, user_id, is_bot, first_name,
                       last_name, username, role, language_code,
                       date_updated=datetime.now()):
        with self.db.connect() as conn:
            statement = self.u_table.insert().values(user_id=user_id,
                                                     is_bot=is_bot,
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     username=username,
                                                     role=role,
                                                     language_code=language_code,
                                                     date_updated=date_updated)
            conn.execute(statement)
        logger.info(f"Users data added successfully!")

    def select_by_user_id(self, user_id):
        result = []
        select_statement = self.u_table.select().where(self.u_table.c.user_id == user_id)
        with self.db.connect() as conn:
            result_set = conn.execute(select_statement)
            for row in result_set:
                result.append(row)
        result = result[0]
        response = {
            "user_id": result[0],
            "is_bot": result[1],
            "first_name": result[2],
            "last_name": result[3],
            "username": result[4],
            "role": result[5],
            "language_code": result[6],
            "date_updated": result[7]
        }
        return response

    def delete_by_user_id(self, user_id):
        delete_statement = self.u_table.delete().where(self.u_table.c.user_id == user_id)
        with self.db.connect() as conn:
            conn.execute(delete_statement)


class GetRelevant:
    def __init__(self):
        self.db = create_engine(Conf.URL_DB)
        self.meta = MetaData(self.db)
        self.df = pd.DataFrame()

    def get_relevant(self, user_id):
        select_statement = f'select * from news where news_id not in (select news_id from users_history where user_id={user_id}) and role in (select role from users where user_id={user_id})'
        with self.db.connect() as conn:
            result_set = conn.execute(select_statement)
        self.df = pd.DataFrame(result_set)
        self.df.columns = ['news_id', 'tag_id', 'source', 'role', 'url',
                           'text_formated', 'parsed_news', 'score',
                           'news_date', 'date_updated']
        self.df.score = self.df.score.sub(self.df.score.min())
        self.df.score = self.df.score.divide(self.df.score.sum())
        self.df = self.df.sample(n=Conf.NEWS_AMOUNT, weights="score")
        relevant_news = self.df.to_dict('records')

        return relevant_news