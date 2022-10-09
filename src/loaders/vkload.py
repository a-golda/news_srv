import vk_api
import json
import getpass
import datetime
import os
import click

from typing import Any

def safe_mkdir(dirname : str) -> None:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def get_date(unixtime):
    return str(datetime.datetime.utcfromtimestamp(unixtime).date())

def dump_json(obj, fname):
    with open(fname, mode="w", encoding="utf-8") as file:
        json.dump(obj, file)

def get_posts(group: str, vk: Any, dirname: str, min_date: str) -> None:
    offset = 0

    while True:
        new_posts = vk.wall.get(domain=group, offset=offset,
							    count=100)['items']

        fname = f"posts_{group}_{offset}.json"
        full_name = os.path.join(dirname, fname)
        dump_json(new_posts, full_name)

        current_date = get_date(new_posts[0]["date"])
        if len(new_posts) == 0 or current_date < min_date:
            return
        offset += 100

@click.command()
@click.option("--output", help="Path to store data", type=click.STRING, required=True)
@click.option("--min_date", help="Min date to collect data", type=click.STRING, required=True)
@click.option("--groups", help="; separated groups", type=click.STRING, required=True)
def download_groups(output: str, groups: str, min_date: str) -> None:

    groups_list = groups.split(";")
    print('login:', end=' ')
    login = str(input())
    password = str(getpass.getpass())
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    vk = vk_session.get_api()

    safe_mkdir(output)

    for group in groups_list:
        try:
            print('Getting posts from', group)
            get_posts(group, vk, output, min_date)
        except Exception as e:
            print(e)
            print('Rate limit reached, last group is', group)
            break

if __name__ == "__main__":
    download_groups()
