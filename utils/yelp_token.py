import os
import random

import requests


def get_tokens():
    i = 0
    tokens = []

    while True:
        token = os.environ.get(f'YELP_TOKEN_{i}', '')

        if not token:
            break

        tokens.append(token)
        i += 1

    return tokens


def get_yelp_token():
    """Creates a random token generator"""
    yelp_api_tokens = get_tokens()
    random.shuffle(yelp_api_tokens)

    for token in yelp_api_tokens:
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


def get_token(process_number):
    tokens = get_tokens()
    total_tokens = len(tokens)
    return os.environ.get(f'YELP_TOKEN_{process_number % total_tokens}')
