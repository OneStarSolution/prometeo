import os

import requests


def get_tokens():
    i = 0
    tokens = []

    while True:
        i += 1
        token = os.environ.get(f'YELP_TOKEN_{i}', '')

        if not token:
            break

        tokens.append(token)

    return tokens


def get_yelp_token():
    yelp_api_tokens = get_tokens()
    for token in yelp_api_tokens:
        print(token)
        yield token


def get_request_available():
    yelp_api_tokens = get_tokens()
    request_available = 0

    for token in yelp_api_tokens:
        # get request with the aim of get the headers only
        bearer_token = {"Authorization": f"Bearer {token}"}
        result = requests.get(
            f'https://api.yelp.com/v3/businesses/jVUBlA1DxC_q3qzBtAyYmA', headers=bearer_token)
        request_available += int(result.headers.get('ratelimit-remaining', 1)) - 1

    return request_available
