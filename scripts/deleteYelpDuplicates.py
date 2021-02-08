import pandas as pd


def deleteYELPduplicates():
    df = pd.read_csv('YELP_CANADA.csv')
    df.drop_duplicates(subset="id", keep="last", inplace=True)
    df.to_csv('YELP_CANADA_clean.csv')


deleteYELPduplicates()
