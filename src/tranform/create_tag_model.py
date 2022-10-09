import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline, Pipeline

from numpy import ndarray
from pandas import read_csv

from typing import Tuple

from joblib import dump

import click

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

logger = logging.getLogger()

def create_model(n_clusters: int) -> Pipeline:

    return make_pipeline(
        TfidfVectorizer(
            min_df=4,
        ),
        TruncatedSVD(n_components=200),
        KMeans(n_clusters=n_clusters),
    )


def fit_model(model: Pipeline, df: ndarray) -> Tuple[Pipeline, ndarray]:
    model.fit(df)
    preds = model.predict(df)
    return model, preds


@click.command()
@click.option("--input", help="Input data folder", required=True, type=click.STRING)
@click.option("--output", help="Output data folder", required=True, type=click.STRING)
@click.option("--model_output", help="Output data folder", required=True, type=click.STRING)
@click.option("--n_tags", help="Number of tags", default=25, type=click.INT)
def fit(input, output, model_output, n_tags) -> None:
    logger.info("Creating model")
    model = create_model(n_tags)
    logger.info("Reading data")
    data = read_csv(input)
    logger.info("Fitting model")
    model, tags = fit_model(model, data.texts_norm.values)
    data["tag"] = tags
    logger.info("Saving data")
    data.to_csv(output, index=None)

    if not os.path.exists(model_output):
        os.mkdir(model_output)

    model_name = "tag_model.sav"
    full_path = os.path.join(model_output, model_name)
    logger.info("Saving model")
    dump(model, full_path)

if __name__ == "__main__":
    fit()
