from joblib import load
from pandas import read_csv

import click

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger()


@click.command()
@click.option("--input", help="Input data folder", required=True, type=click.STRING)
@click.option(
    "--model_input", help="Output data folder", required=True, type=click.STRING
)
@click.option("--output", help="Output data folder", required=True, type=click.STRING)
def create_tags(input: str, model_input: str, output: str) -> None:
    logger.info("Loading model")
    model = load(model_input)
    logger.info("Loading data")
    data = read_csv(input)
    logger.info("Inference")
    data["tag"] = model.predict(data.texts_norm)
    logger.info("Saving data")
    data.to_csv(output)


if __name__ == "__main__":
    create_tags()
