import os


# MongoDB env vars
NOSQL_USER = os.environ.get('NOSQL_USER2', '')
NOSQL_PASS = os.environ.get('NOSQL_PASS2', '')
NOSQL_PORT = os.environ.get('NOSQL_PORT2', 27017)
NOSQL_HOST = os.environ.get('NOSQL_HOST2', 'mongo_db')


def get_mongo_url():
    ''' Returns proper mongo connection URL from env file. '''
    # return f'mongodb+srv://{NOSQL_HOST}/'
    return f'mongodb://{NOSQL_HOST}:{NOSQL_PORT}/'
