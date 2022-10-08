class ParseUpdateNewsRequest():
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        self.news_id = reqdict['news_id']
        self.tags = reqdict['tags']
        self.segment = reqdict['segment']
        self.key_point = reqdict['key_point']
        self.title = reqdict['title']
        self.parsed_news = reqdict['parsed_news']
        self.raw_news = reqdict['raw_news']


class ParseUpdateUsersHistRequest:
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        self.user_id = reqdict['user_id']
        self.news_id = reqdict['news_id']
        self.date_updated = reqdict['date_updated']


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
        self.date_updated = reqdict['date_updated']


class SelectNews():
    """
    Parse json given to 'api/update_news'.
    """
    def __init__(self, reqdict):
        self.news_id = reqdict['news_id']


class DeleteNews():
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


class DeleteUser():
    """
    Parse json given to 'api/delete...'.
    """
    def __init__(self, reqdict):
        self.user_id = reqdict['news_id']