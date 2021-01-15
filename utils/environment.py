import os


# MongoDB env vars
NOSQL_USER = os.environ.get('NOSQL_USER', '')
NOSQL_PASS = os.environ.get('NOSQL_PASS', '')
NOSQL_PORT = os.environ.get('NOSQL_PORT', '27017')
NOSQL_HOST = os.environ.get('NOSQL_HOST', 'mongo_db')


def get_mongo_url():
    ''' Returns proper mongo connection URL from env file. '''
    return f'mongodb+srv://{NOSQL_HOST}/'
    # return f'mongodb://{NOSQL_HOST}:{NOSQL_PORT}/'
