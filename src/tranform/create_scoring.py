import datetime
import json
import re

from pandas import read_csv, to_datetime, DataFrame

from nltk import ngrams
from joblib import Parallel, delayed

from sklearn.preprocessing import scale
from pymorphy2 import MorphAnalyzer
import click

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

logger = logging.getLogger()

def score(df: DataFrame) -> None:

    X = scale(df)

    return .7 * X[:, 0] + .15 * X[:, 1] + .15 * X[:, 2]


def get_ngrams(x, n=2):
    all_words = []
    for i in range(1, n + 1):
        all_words.extend(map(" ".join, ngrams(x, i)))
    return all_words


def find_trends(words, trends):
    positions = []
    for i, word in enumerate(words):
        for trend in trends:
            if trend == word:
                positions.append(i)
                break
    return positions


def extract_indices(words, indices):
    return [words[i] for i in indices]


def hightlight_keywords(text, words):
    for word in words:
        pattern = re.compile("(" + re.escape(word) + ')', flags=re.IGNORECASE)
        text = pattern.sub('*\g<1>*', text)
    return text


class ScoredDataset:
    def __init__(self, path: str, top_trends: int) -> None:
        self.path = path
        self.top_trends = top_trends

    def load_data(self) -> None:
        self.data = read_csv(self.path)
        self.df = self.data.copy()
        self.df["date_iso"] = to_datetime(self.df.date, unit="s").dt.date.astype("str")
        self.max_date = self.df.date_iso.max()

    def find_trends(self) -> None:
        texts_norm = self.df.texts_norm.str.split().tolist()
        texts = self.df.texts_standard.str.split().tolist()
        self.df["n_grams"] = Parallel(n_jobs=-1)(map(delayed(get_ngrams), texts_norm))
        self.df["n_grams_raw"] = Parallel(n_jobs=-1)(map(delayed(get_ngrams), texts))
        df_ngrams = self.df.explode("n_grams", ignore_index=True)

        ngrams_dyn = (
            df_ngrams.groupby(["date_iso", "n_grams"])
            .size()
            .sort_index(level=[0, 1], ascending=False)
        )

        last_date = (
            datetime.date.fromisoformat(self.max_date) - datetime.timedelta(7)
        ).strftime("%Y-%m-%d")

        s1 = ngrams_dyn[self.max_date].rename("cnt").reset_index()
        s2 = ngrams_dyn[last_date].rename("cnt").reset_index()

        diff = s1.merge(s2, how="left", on="n_grams").fillna({"cnt_y": 0})

        diff["score"] = diff["cnt_x"] - diff["cnt_y"]
        self.trends = diff.sort_values(by="score", ascending=False).n_grams.tolist()

        score = diff.drop(["cnt_x", "cnt_y"], axis=1)

        df_ngrams = df_ngrams.merge(score, how="left", on="n_grams")
        mean_score = (
            df_ngrams.groupby("id")["score"].mean().rename("score_trend").reset_index()
        )

        self.df = self.df.loc[self.df.date_iso == self.max_date]
        self.df = self.df.merge(mean_score, how="left", on="id")

        self.df_trends = df_ngrams.loc[
            (df_ngrams.date_iso == self.max_date),
            ["id", "n_grams"]
        ]

    def classify_trends(self) -> None:

        morph = MorphAnalyzer()

        cleared_trends = []
        for trend in self.trends[: 2000]:
            flag = False
            for word in trend.split():
                tag = morph.tag(word)[0]
                if "NOUN" in tag or "VERB" in tag:
                    flag = True
            if flag:
                cleared_trends.append(trend)

        self.trends_main = cleared_trends[: self.top_trends]
        logger.info(f"Top 10 trends {self.trends_main[: 10]}")
        self.df_trends = self.df_trends.loc[self.df_trends.n_grams.isin(self.trends_main)]
        

    def find_keywords_in_text(self) -> None:
        
        positions = list(
            map(lambda x: find_trends(x, self.trends_main), self.df["n_grams"].tolist())
        )

        self.df["positions"] = positions

        keywords = list(
            map(
                lambda x: extract_indices(x[0], x[1]),
                zip(self.df["n_grams_raw"].tolist(), positions),
            )
        )

        self.df["keywords"] = keywords

        texts_highlighted = list(map(
            lambda x: hightlight_keywords(x[0], x[1]),
            zip(self.df.text, keywords)
        ))

        self.df["texts_format"] = texts_highlighted

    def postprocess(self) -> None:
        X = self.df[["score_trend", "reposts_count", "views_count"]]
        self.df["score"] = score(X)

    def save(self, fname: str, fname_trends: str, trends_path: str) -> None:
        self.df.to_csv(fname, index=None)
        self.df_trends.to_csv(fname_trends, index=None)

        with open(trends_path, "w", encoding="utf-8") as file:
            json.dump(self.trends_main, file)

    def main_etl(self) -> None:
        logger.info("Loading data")
        self.load_data()
        logger.info("Finding trends")
        self.find_trends()
        logger.info("classifying trends")
        self.classify_trends()
        logger.info("Finding key words")
        self.find_keywords_in_text()
        logger.info("Postprocessing")
        self.postprocess()

@click.command()
@click.option("--input", help="Input data folder", required=True, type=click.STRING)
@click.option("--output", help="Output data folder", required=True, type=click.STRING)
@click.option("--output_trends", help="Output trends file", required=True, type=click.STRING)
@click.option("--output_json", help="Output trends json file", required=True, type=click.STRING)
@click.option("--top_trends", help="Top trends to find", default=30, type=click.INT)
def create_scoring_dataset(
    input: str,
    output: str,
    output_trends: str,
    output_json: str,
    top_trends: int
) -> None:
    dataset = ScoredDataset(input, top_trends)
    dataset.main_etl()
    dataset.save(output, output_trends, output_json)

if __name__ == "__main__":
    create_scoring_dataset()