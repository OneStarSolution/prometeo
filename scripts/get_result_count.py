import os

import argparse
import requests


if __name__ == "__main__":
    # Parse commands
    parser = argparse.ArgumentParser(description='Process crawl params.')
    parser.add_argument('--pattern', '-p', metavar='pattern', type=str, dest="pattern",
                        default=1, help='regex', required=True)
    args = parser.parse_args()
    results = {}

    for i in range(1, 21):
        try:
            instance_name = f'CE_INSTANCE_{i}'
            host = os.getenv(instance_name)
            url = f"http://{host}:8000/enhanced"
            print(f"Querying: {instance_name} - {url}")
            params = {"pattern": args.pattern}
            res = requests.get(url, params=params, timeout=5)
            results[instance_name] = len(res.json()) if res else 0
        except Exception as e:
            print(e)

    # Print results
    for gcp_machine, files_found in results.items():
        print(f"{gcp_machine} -> {files_found} ({(files_found/2050*100):.2f})%")
