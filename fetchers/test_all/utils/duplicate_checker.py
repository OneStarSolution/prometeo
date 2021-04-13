import requests


def clean_phone(raw_phone):
    return ''.join([char for char in raw_phone if char.isdigit()])


def _load_historical_data():
    return set(), set()
    historical_phones = set()
    for i in range(2, 10):
        with open(f'{i}_historical_phones.txt', "r+") as file:
            phones = set([phone.strip() for phone in file.readlines()])
            historical_phones |= phones

    sources = ["yelp", "bbb", "yp"]
    historical_urls = set()
    for source in sources:
        with open(f'historical_{source}_urls.txt', "r+") as file:
            urls = set([url.strip() for url in file.readlines()])
            historical_urls |= urls

    return historical_phones, historical_urls


print("Loading hitorical data....")
historical_phones, historical_urls = _load_historical_data()


def duplicate_checker(source, data_point):
    print(
        f"data point and source {source} {data_point} type of the data point {type(data_point)}")
    if isinstance(data_point, bytes):
        data_point = data_point.decode("utf-8")
        print(f"new data point {data_point} type: {type(data_point)}")

    data_point = str(data_point)
    unique_status = False

    if "url" in source.lower():
        data_point = data_point[:-1] if data_point[-1] == "'" else data_point
        print(f"url now is: {data_point}")
        unique_status = False if data_point in historical_urls else True

    if source == "phone":
        data_point = clean_phone(data_point)
        try:
            if data_point in historical_phones:
                unique_status = False
            else:
                # query th HC API
                # api_endpoinT = f"https://mfe7wxd6q0.execute-api.us-west-2.amazonaws.com/dev?phone_number={data_point}"
                # api_key = "wDFncJwyDX4HXHD7w0vBQ7cRADAD24jz4KiUCvhS"
                # headers = {'x-api-key': api_key}
                # response = requests.get(url=api_endpoinT, headers=headers).text
                # unique_status = False if "salesforce_lead_id" in response else True
                unique_status = True
        except Exception as e:
            print(e)
            unique_status = False

    return unique_status
