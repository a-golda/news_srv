from request_parser import ParseUpdateNewsRequest, ParseUpdateUsersHistRequest, ParseUpdateUsersRequest
from request_parser import SelectNews, DeleteNews, SelectUser, DeleteUser
from db_utils import NewsPostgreUtils, UsersPostgreUtils, UsersHistPostgreUtils


def update_news_table(reqdict):
    req = ParseUpdateNewsRequest(reqdict)
    table = NewsPostgreUtils()
    table.update_news_table(req.news_id,
                            req.tag_id,
                            req.source,
                            req.role,
                            req.url,
                            req.keywords,
                            req.key_point,
                            req.parsed_news,
                            req.score,
                            req.news_date)

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


def update_users_table(reqdict):
    req = ParseUpdateUsersRequest(reqdict)
    table = UsersPostgreUtils()
    table.update_u_table(req.user_id,
                         req.is_bot,
                         req.first_name,
                         req.last_name,
                         req.username,
                         req.role,
                         req.language_code)


def select_user_by_id(reqdict):
    req = SelectUser(reqdict)
    table = UsersPostgreUtils()
    result = table.select_by_user_id(req.user_id)
    return result


def delete_user_by_id(reqdict):
    req = DeleteUser(reqdict)
    table = UsersPostgreUtils()
    result = table.delete_by_user_id(req.user_id)
    return result


def update_users_hist_table(reqdict):
    req = ParseUpdateUsersHistRequest(reqdict)
    table = UsersHistPostgreUtils()
    table.update_uh_table(req.user_id,
                          req.news_id)


def select_user_hist_by_id(reqdict):
    req = SelectUser(reqdict)
    table = UsersHistPostgreUtils()
    result = table.select_by_user_id(req.user_id)
    return result


def delete_user_hist_by_id(reqdict):
    req = DeleteUser(reqdict)
    table = UsersHistPostgreUtils()
    result = table.delete_by_user_id(req.user_id)
    return result
