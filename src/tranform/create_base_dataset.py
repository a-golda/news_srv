import json
import pandas as pd
import glob
import os
from itertools import chain
from typing import Optional, Union

import click

from nltk.corpus import stopwords
from nltk import word_tokenize

from pymorphy2 import MorphAnalyzer

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger()


def media_from_path(path):
    """get media from filename (standardized by vk_api)
    input: '../data/posts/general_media/posts_rt_russian_21800.json'
    output: 'rt'
    """
    return path.split("/")[-1].split("_")[1]


from typing import List


def get_words(x: str, sw: List[str]) -> List:

    all_words = []

    for word in word_tokenize(x):
        if word not in sw:
            all_words.append(word)

    return all_words


class WordNormalizer:
    def __init__(self):
        self.norm_dict = {}
        self.morph = MorphAnalyzer()

    def normalize(self, seq):

        data = []

        for item in seq:
            new_seq = []
            for word in item:
                if word in self.norm_dict:
                    new_seq.append(self.norm_dict[word])
                else:
                    norm_word = self.morph.normal_forms(word)[0]
                    self.norm_dict[word] = norm_word
                    new_seq.append(norm_word)

            data.append(new_seq)

        return data


class TransformedNews:
    """function receives folder with row data from VK as an input
    and get transformed dataset as output"""

    def __init__(self, path: str, stopwords_path: Optional[str]) -> None:
        self.path = path
        self.files = glob.glob(os.path.join(self.path, "*"))
        self.data = list(chain.from_iterable(map(self.load_json, self.files)))
        self.df = pd.DataFrame(self.data).reset_index(drop=True)
        if stopwords_path is not None:
            with open(stopwords_path, "r", encoding="utf-8") as file:
                self.sw = json.load(file)
        else:
            self.sw = stopwords.words("russian")

    @staticmethod
    def load_json(file_name: str) -> Union[list, str]:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            [news.update({"source": media_from_path(file_name)}) for news in data]
        return data

    def load_data(self) -> None:
        self.data = list(chain.from_iterable(map(self.load_json, self.files)))
        self.df = pd.DataFrame(self.data).reset_index(drop=True)

    def transform_df(self) -> None:
        df = self.df
        df = df[df["views"].notna()].copy()  # 0.1% data loss

        # feature engineering
        df["views_count"] = df.views.apply(lambda x: x["count"])
        df["reposts_count"] = df.reposts.apply(lambda x: x["count"])
        df["likes_count"] = df.likes.apply(lambda x: x["count"])
        df["comments_count"] = df.comments.apply(lambda x: x["count"])

        # drop extra
        df = df[df.marked_as_ads == 0].copy()  # drop ads
        df = df.drop(
            [
                "from_id",
                "owner_id",
                "marked_as_ads",
                "is_favorite",
                "post_type",
                "post_source",
                "zoom_text",
                "is_pinned",
            ],
            axis=1,
        )
        df = df.drop(
            ["attachments", "views", "reposts", "likes", "comments", "copy_history"],
            axis=1,
        )  # TODO: we are loosing info here!!!
        df = df[df.text != ""]  # TODO: we are loosing info here!!!
        if "copyright" in df.columns:
            df = df.drop("copyright", axis=1)
        self.df = df.reset_index(drop=True)

    def preprocess_text(self):
        punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~«»—1234567890"
        translate_table = dict((ord(char), None) for char in punctuation)
        logger.info("Texts to lowercase")
        texts = (
            self.df.text.str.lower()
            .str.translate(translate_table)
            .apply(get_words, sw=self.sw)
        )

        normalizer = WordNormalizer()
        logger.info("Texts normalization")
        texts_norm = normalizer.normalize(texts)
        self.df["texts_norm"] = list(map(" ".join, texts_norm))

    def main_etl(self) -> None:
        logger.info("Loading data")
        self.load_data()
        logger.info("Transforming data")
        self.transform_df()
        logger.info("Preprocessing texts")
        self.preprocess_text()

    def save(self, fpath: str) -> None:
        logger.info("Saving data")
        self.df.to_csv(fpath, index=None)


@click.command()
@click.option("--input", help="Input data folder", required=True, type=click.STRING)
@click.option("--output", help="Output data folder", required=True, type=click.STRING)
@click.option(
    "--stopwords_path", help="Stopwords data path", default=None, type=click.STRING
)
def create_dataset(
    input: str,
    output: str,
    stopwords_path: Optional[str],
) -> None:
    dataset = TransformedNews(input, stopwords_path)
    dataset.main_etl()
    dataset.save(output)


if __name__ == "__main__":
    create_dataset()
