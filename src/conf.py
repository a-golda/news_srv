class Conf:
    URL_ALIVE = '/alive'
    URL_UPDATE_NEWS = '/api/update_news'
    URL_SELECT_NEWS_BY_ID = '/api/select_news_by_id'
    URL_DELETE_NEWS_BY_ID = '/api/delete_news_by_id'
    URL_DB = 'postgresql://localhost/andrey.golda'
    mama = 'papa'
    SUCCESS_STATUS_CODE: int = 200
    FAILED_STATUS_CODE: int = 400