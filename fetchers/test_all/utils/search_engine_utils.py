def browser_phone_translater(phone_number):
    if isinstance(phone_number, bytes):
        phone_number = phone_number.decode("utf-8")

    translated_phone = phone_number.replace("(", "%28")
    translated_phone = translated_phone.replace(")", "%29")
    translated_phone = translated_phone.replace(" ", "+")
    return translated_phone


def valid_domain_check(url):
    valid_domain = False
    valid_domains = ['yelp.com', 'bbb.org', 'yellowpages.com',
                     'manta.com', 'mapquest.com', 'chamberofcommerce.com']
    for domain in valid_domains:
        if domain in url:
            valid_domain = True
            break
    return valid_domain


def source_url_filter(url):
    valid_url = False
    if 'yelp.com' in url:
        if '/biz/' in url:
            valid_url = True
    elif 'bbb.org' in url:
        if '/profile/' in url:
            valid_url = True
    elif 'yellowpages.com' in url:
        if '/mip/' in url:
            valid_url = True
    elif 'mapquest.com' in url:
        if '/us/' in url:
            valid_url = True
        if '/ca/' in url:
            valid_url = True
        if '/canada/' in url:
            valid_url = True
    elif 'manta.com' in url:
        if '/c/' in url:
            valid_url = True
    elif 'chamberofcommerce.com' in url:
        if '/united-states/' in url:
            valid_url = True
        if '/canada/' in url:
            valid_url = True
    return valid_url
