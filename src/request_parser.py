import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ParseUpdateNewsRequest:
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        try:
            self.news_id = reqdict['news_id']
            self.tag_id = reqdict['tag_id']
            self.source = reqdict['source']
            self.role = reqdict['role']
            self.url = reqdict['url']
            self.keywords = reqdict['keywords']
            self.key_point = reqdict['key_point']
            self.parsed_news = reqdict['parsed_news']
            self.score = reqdict['score']
            self.news_date = reqdict['news_date']
        except KeyError as e:
            logger.error(f"Parsing error: {e}")


class ParseUpdateUsersHistRequest:
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        self.user_id = reqdict['user_id']
        self.news_id = reqdict['news_id']


class ParseUpdateUsersRequest:
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        self.user_id = reqdict['user_id']
        self.is_bot = reqdict['is_bot']
        self.first_name = reqdict['first_name']
        self.last_name = reqdict['last_name']
        self.username = reqdict['username']
        self.role = reqdict['role']
        self.language_code = reqdict['language_code']


class SelectNews:
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        self.news_id = reqdict['news_id']


class DeleteNews:
    """
    Parse json given to 'api/delete_news'.
    """
    def __init__(self, reqdict):
        self.news_id = reqdict['news_id']


class SelectUser:
    """
    Parse json given to 'api/update...'.
    """
    def __init__(self, reqdict):
        self.user_id = reqdict['user_id']


class DeleteUser:
    """
    Parse json given to 'api/delete...'.
    """
    def __init__(self, reqdict):
        self.user_id = reqdict['user_id']
