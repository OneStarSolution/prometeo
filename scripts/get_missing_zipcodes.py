import os

import argparse
import requests
import random

from math import ceil


def split_list(zipcodes: list, chunks: int):

    chunk_size = ceil(len(zipcodes) / chunks)
    end = len(zipcodes)

    for start in range(0, end, chunk_size):
        zipcodes_target = list(map(
            lambda x: x+'\n', zipcodes[start: start + chunk_size]))
        yield zipcodes_target


if __name__ == "__main__":
    # Parse commands
    parser = argparse.ArgumentParser(description='Process crawl params.')
    parser.add_argument('--pattern', '-p', metavar='pattern', type=str, dest="pattern",
                        default=1, help='regex', required=True)
    parser.add_argument('-r', '--redistribute',
                        dest="redistribute", action='store_true')
    parser.add_argument('--save', '-s', metavar='save', type=bool, dest="save",
                        default=True, help='save the missing zipcodes in a file')
    # parser.add_argument('--files', '-f', metavar='paths',
    #                     dest="paths", required=True,  nargs='*', default=[])
    parser.add_argument('-i', '--instances', metavar='instances',
                        dest="instances", required=True,  type=int)
    args = parser.parse_args()

    # for i in range(1, 21):
    #     try:
    #         instance_name = f'CE_INSTANCE_{i}'
    #         host = os.getenv(instance_name)
    #         url = f"http://{host}:8000/enhanced"
    #         print(f"Querying: {instance_name} - {url}")
    #         params = {"pattern": args.pattern}
    #         res = requests.get(url, params=params, timeout=2)
    #         if res.json():
    #             results.extend(res.json())
    #     except Exception as e:
    #         print(e)

    # read all the zipcodes
    with open('valid_zipcodes.csv', 'r') as f:
        zipcodes = set([line.replace('\n', '').zfill(5)
                        for line in f.readlines()])

    # with open('CAN_city.csv', 'r') as f:
    #     zipcodes = set([line.replace('\n', '').zfill(5)
    #                     for line in f.readlines()])

    with open('paths_crawled.txt', 'r') as f:
        paths = set([line.replace('\n', '').zfill(5)
                     for line in f.readlines()])

    zipcodes_crawled = set([zipcode.split('-')[1].strip().zfill(5)
                            for zipcode in paths])

    not_crawled_yet = zipcodes.difference(zipcodes_crawled)

    not_crawled_yet = list(not_crawled_yet)

    print(args.redistribute)
    if args.redistribute:
        print("entre")
        random.shuffle(not_crawled_yet)

        for i, data in enumerate(split_list(not_crawled_yet, args.instances)):
            # instance_name = f'CE_INSTANCE_{i + 1}'
            # host = os.getenv(instance_name)
            # url = f"http://{host}:8000/redistribution"
            # requests.post(url, json=data)
            with open(f"data/redistribution/instance_{i+1}.txt", "w") as f:
                f.writelines(data)

    if args.save:
        with open(f"missing_zipcodes_of_{args.pattern}.csv", "w") as f:
            f.writelines(list(map(lambda x: f"{x}\n", not_crawled_yet)))

    print(len(not_crawled_yet))
