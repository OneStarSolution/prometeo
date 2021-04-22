import argparse

from math import ceil


def split_file(path: str, chunks: int, chunk_to_keep: int):
    if chunk_to_keep > chunks:
        raise Exception(
            "The index of the chunk to keep should be smaller than the number of chunks")

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    chunk_size = ceil(len(lines) / chunks)
    end = chunk_to_keep * chunk_size
    start = end - chunk_size

    lines = map(lambda x: x+'\n', lines[start: end])
    with open('uscities_tocrawl.csv', 'w+') as f:
        f.writelines(lines)

# NOTE: Example: python scripts/split_file.py --path valid_zipcodes.csv --chunks 2 --keep 2


if __name__ == "__main__":
    # Parse commands (1 index base for keep)
    parser = argparse.ArgumentParser(description='Process crawl params.')
    parser.add_argument('--chunks', metavar='chunks', type=int,
                        dest="chunks", help='number of chunks', required=True)
    parser.add_argument('--path', metavar='path', type=str,
                        dest="path", help='path to file to split', required=True)
    parser.add_argument('--keep', metavar='keep', type=int,
                        dest="keep", help='chunk to keep', required=True)
    args = parser.parse_args()

    split_file(args.path, args.chunks, args.keep)
