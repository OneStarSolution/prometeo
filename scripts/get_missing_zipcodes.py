import os

import argparse
import requests
import subprocess


instance_names = ("instance-team-1-2j48", "instance-team-1-3ph2", "instance-team-1-95x5", "instance-team-1-ch6w",
                  "instance-team-1-fxfl", "instance-team-1-g03g", "instance-team-1-hb8h", "instance-team-1-j0k2",
                  "instance-team-1-jkm2", "instance-team-1-kzq9", "instance-team-1-m42s", "instance-team-1-m9mp",
                  "instance-team-1-mk32", "instance-team-1-mwlp", "instance-team-1-n9g8", "instance-team-1-nvxl",
                  "instance-team-1-q2xl", "instance-team-1-s131", "instance-team-1-v94h", "instance-team-1-zhp8")

instance_names_2 = ("replaceof1", "replaceof2")


if __name__ == "__main__":
    # Parse commands
    parser = argparse.ArgumentParser(description='Process crawl params.')
    parser.add_argument('--pattern', '-p', metavar='pattern', type=str, dest="pattern",
                        default=1, help='regex', required=True)
    args = parser.parse_args()
    results = []

    for i in range(1, 21):
        try:
            instance_name = f'CE_INSTANCE_{i}'
            host = os.getenv(instance_name)
            url = f"http://{host}:8000/enhanced"
            print(f"Querying: {instance_name} - {url}")
            params = {"pattern": args.pattern}
            res = requests.get(url, params=params, timeout=5)
            results.extend(res.json())
        except Exception as e:
            print(e)

    # read all the zipcodes
    with open('valid_zipcodes.csv', 'r') as f:
        zipcodes = set([line.replace('\n', '').zfill(5)
                        for line in f.readlines()])

    zipcodes_crawled = set([zipcode.split('-')[1].strip().zfill(5)
                            for zipcode in results])

    not_crawled_yet = zipcodes.difference(zipcodes_crawled)

    print(len(not_crawled_yet))
