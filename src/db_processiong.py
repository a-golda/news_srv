from request_parser import ParseUpdateRequest, SelectNews, DeleteNews
from postgres_utils import NewsPostgreUtils

def update_news_table(reqdict):
    """see flasksrv"""

    req = ParseUpdateRequest(reqdict)
    table = NewsPostgreUtils()
    table.update_news_table(req.news_id,
                            req.tags,
                            req.segment,
                            req.key_point,
                            req.title,
                            req.parsed_news,
                            req.raw_news)


def select_by_id(reqdict):
    req = SelectNews(reqdict)
    table = NewsPostgreUtils()
    result = table.select_by_news_id(req.news_id)
    return result


def delete_by_id(reqdict):
    req = SelectNews(reqdict)
    table = NewsPostgreUtils()
    result = table.delete_by_news_id(req.news_id)
    return result



