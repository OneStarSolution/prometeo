import os


# MongoDB env vars
NOSQL_USER = os.environ.get('NOSQL_USER', '')
NOSQL_PASS = os.environ.get('NOSQL_PASS', '')
NOSQL_PORT = os.environ.get('NOSQL_PORT', '27017')
NOSQL_HOST = os.environ.get('NOSQL_HOST', 'mongo_db')

# YELP API tokens
YELP_TOKEN_1 = os.environ.get('YELP_TOKEN_1', '')
YELP_TOKEN_2 = os.environ.get('YELP_TOKEN_2', '')
YELP_TOKEN_3 = os.environ.get('YELP_TOKEN_3', '')
YELP_API_TOKENS = [YELP_TOKEN_1, YELP_TOKEN_2, YELP_TOKEN_3]
NUMBER_YELP_API_TOKENS = len(YELP_API_TOKENS)


def get_mongo_url():
    ''' Returns proper mongo connection URL from env file. '''
    # return f'mongodb+srv://{NOSQL_HOST}/'
    return f'mongodb://{NOSQL_HOST}:{NOSQL_PORT}/'


def get_yelp_token():
    for token in YELP_API_TOKENS:
        yield token
