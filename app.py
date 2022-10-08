import logging
from src.conf import Conf
from src.db_processiong import update_news_table, select_by_id, delete_by_id
from flask import Flask, jsonify, request


app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as _:
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_SELECT_NEWS_BY_ID, methods=['POST'])
def select_news():
    """
        Select news by news_id
    """
    try:
        req = request.get_json()
        return jsonify(select_by_id(req))
    except Exception as _:
        return jsonify(Conf.FAILED_STATUS_CODE)


@app.route(Conf.URL_DELETE_NEWS_BY_ID, methods=['POST'])
def delete_news():
    """
        Del news by news_id
    """
    try:
        req = request.get_json()
        delete_by_id(req)
        return jsonify(Conf.SUCCESS_STATUS_CODE)
    except Exception as _:
        return jsonify(Conf.FAILED_STATUS_CODE)


# run standalone
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
