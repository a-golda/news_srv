import requests
import pandas as pd
from conf import Conf

# TODO: сделай это говно
def form_one_req(one_news):
    if one_news.source in Conf.MAPPING['buh']:
        role = 'buh'
    else:
        role = 'business'
    dict_request = {
        "news_id": int(one_news.id),
        "tag_id": int(one_news.tag),
        "source": str(one_news.source),
        "role": role,
        "url": 'https://moretech.vtb.ru',
        "text_formated": str(one_news.texts_format),
        "parsed_news": one_news.text,
        "score": float(one_news.score),
        "news_date": one_news.date_iso,
    }
    return dict_request

if __name__ == '__main__':
    df = pd.read_csv('./data/final.csv')

    for i in range(len(df)):
        requests.post('http://192.168.31.217:5000/api/update_news', json=form_one_req(df.iloc[i]))
