class Conf:
    URL_ALIVE = '/alive'

    URL_UPDATE_NEWS = '/api/update_news'
    URL_SELECT_NEWS_BY_ID = '/api/select_news_by_id'
    URL_DELETE_NEWS_BY_ID = '/api/delete_news_by_id'

    URL_UPDATE_USERS = '/api/update_users'
    URL_SELECT_USERS_BY_ID = '/api/select_users_by_id'
    URL_DELETE_USERS_BY_ID = '/api/delete_users_by_id'

    URL_UPDATE_USERS_HIST = '/api/update_users_history'
    URL_SELECT_USERS_HIST_BY_ID = '/api/select_users_history_by_id'
    URL_DELETE_USERS_HIST_BY_ID = '/api/delete_users_history_by_id'

    URL_GET_RELEVANT_NEWS = '/api/get_relevant_news'

    URL_DB = 'postgresql://localhost/andrey.golda'
    mama = 'papa-penis'

    NEWS_AMOUNT = 5

    SUCCESS_STATUS_CODE: int = 200
    FAILED_STATUS_CODE: int = 400
