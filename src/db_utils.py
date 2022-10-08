import logging
from src.conf import Conf
from datetime import datetime
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, String, Integer, DateTime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NewsPostgreUtils:
    def __init__(self):
        self.db = create_engine(Conf.URL_DB)
        self.meta = MetaData(self.db)
        self.news_table = Table('news', self.meta,
                                Column('news_id', Integer),
                                Column('tags', String),
                                Column('segment', String),
                                Column('key_point', String),
                                Column('title', String),
                                Column('parsed_news', String),
                                Column('raw_news', String),
                                Column('date_updated', DateTime))
        try:
            if not inspect(self.db).has_table('news'):
                with self.db.connect() as _:
                    self.news_table.create()
            logger.info(f"News table has been created successfully!")
        except Exception as e:
            pass
            logger.error(f"News table creation failed with exception: {e}")

    def update_news_table(self, news_id, tags, segment, key_point, title, parsed_news, raw_news, date_updated=str(datetime.now())):
        try:
            with self.db.connect() as conn:
                statement = self.news_table.insert().values(news_id=news_id,
                                                            tags=tags,
                                                            segment=segment,
                                                            key_point=key_point,
                                                            title=title,
                                                            parsed_news=parsed_news,
                                                            raw_news=raw_news,
                                                            date_updated=date_updated)
                conn.execute(statement)
            logger.info(f"News data added successfully!")
        except Exception as e:
            logger.error(f"News table update failed with exception: {e}")

    def select_by_news_id(self, news_id):
        try:
            result = []
            select_statement = self.news_table.select().where(self.news_table.c.news_id == news_id)
            with self.db.connect() as conn:
                result_set = conn.execute(select_statement)
                for row in result_set:
                    result.append(row)
            logger.info(f"News selected successfully!")
            return str(result)
        except Exception as e:
            logger.error(f"News selection failed!")
            return f';('


    def delete_by_news_id(self, news_id):
        try:
            delete_statement = self.news_table.delete().where(self.news_table.c.news_id == news_id)
            with self.db.connect() as conn:
                conn.execute(delete_statement)
        except Exception as e:
            logger.error(f"News table del failed with exception: {e}")