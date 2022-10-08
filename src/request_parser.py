class ParseUpdateRequest():
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