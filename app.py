import logging
from src.conf import Conf
from src.db_processiong import update_news_table, select_user_hist_by_id, delete_by_id, update_users_table, select_by_id
from src.db_processiong import select_user_by_id, update_users_hist_table, delete_user_by_id, delete_user_hist_by_id
from flask import Flask, jsonify, request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route(Conf.URL_ALIVE, methods=['GET'])
def alive():
    """
    Is server up and running
    """
    return jsonify(Conf.SUCCESS_STATUS_CODE)


@app.route(Conf.URL_UPDATE_NEWS, methods=['POST'])
def update_news():
    """
        Add new row to news table
    """
    try:
        req = request.get_json()
        update_news_table(req)
        app.logger.info(f"News data added successfully!")
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as e:
        app.logger.error(f"News table update failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_SELECT_NEWS_BY_ID, methods=['POST'])
def select_news():
    """
        Select news by news_id
    """
    try:
        req = request.get_json()
        app.logger.info(f"News selected successfully!")
        return jsonify(select_by_id(req))
    except Exception as e:
        app.logger.error(f"News selection failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_DELETE_NEWS_BY_ID, methods=['POST'])
def delete_news():
    """
        Del news by news_id
    """
    try:
        req = request.get_json()
        delete_by_id(req)
        app.logger.info(f"News table del success!")
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as e:
        app.logger.error(f"News table del failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_UPDATE_USERS, methods=['POST'])
def update_user():
    """
        Add new row to users table
    """
    try:
        req = request.get_json()
        update_users_table(req)
        app.logger.info(f"Users history data added successfully!")
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as e:
        app.logger.error(f"Users history table update failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_SELECT_USERS_BY_ID, methods=['POST'])
def select_user():
    """
        Select user's info by user_id
    """
    try:
        req = request.get_json()
        app.logger.info(f"Users history selected successfully!")
        return jsonify(select_user_by_id(req))
    except Exception as e:
        app.logger.error(f"Users history selection failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_DELETE_USERS_BY_ID, methods=['POST'])
def delete_user():
    """
        Del user by user_id
    """
    try:
        req = request.get_json()
        delete_user_by_id(req)
        app.logger.info(f"Users history del successfully!")
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as e:
        app.logger.error(f"Users history table del failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_UPDATE_USERS_HIST, methods=['POST'])
def update_user_history():
    """
        Add new row to users_history table
    """
    try:
        req = request.get_json()
        update_users_hist_table(req)
        app.logger.info(f"Users data added successfully!")
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as e:
        app.logger.error(f"Users table update failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_SELECT_USERS_HIST_BY_ID, methods=['POST'])
def select_user_hist():
    """
        Select user's history by user_id
    """
    try:
        req = request.get_json()
        app.logger.info(f"Users selected successfully!")
        return jsonify(select_user_hist_by_id(req))
    except Exception as e:
        app.logger.error(f"Users selection failed with exception: {e}")
        return f';('


@app.route(Conf.URL_DELETE_USERS_HIST_BY_ID, methods=['POST'])
def delete_user_hist():
    """
        Del user by user_id
    """
    try:
        req = request.get_json()
        delete_user_hist_by_id(req)
        app.logger.info(f"Users del successfully!")
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as e:
        app.logger.error(f"Users table del failed with exception: {e}")
        return jsonify(Conf.FAILED_STATUS_CODE)


# run standalone
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
