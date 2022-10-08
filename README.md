# news_srv
Alias of news

Build

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Deployment

```shell
mkdir -p data
python src/loaders/vkload.py --output ./data/posts --min_date "2022-10-01" --groups "rbc;ria"
python src/tranform/create_base_dataset.py --input ./data/posts/prof_media --output ./data/base_dataset.csv --stopwords_path ./stopwords.json
python src/tranform/create_scoring.py --input ./data/base_dataset.csv --output ./data/scored_dataset.csv --output_trends ./data/trends.json
python src/tranform/create_tag_model.py --input ./data/base_dataset.csv --output ./data/tagged_dataset.csv --model_output ./models
python src/tranform/create_tags.py --input ./data/scored_dataset.csv --model_input ./models/tag_model.sav --output ./data/final.csv
```
