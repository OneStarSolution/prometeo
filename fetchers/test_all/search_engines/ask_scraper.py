def ask_scraper(phone_number, pages_per_search_engine):
    # print(space)
    ask_results = []
    pages_per_search_engine = pages_per_search_engine + 1
    for i in range(1, pages_per_search_engine):
        translated_phone = browser_phone_translater(phone_number)
        search_url = 'https://www.ask.com/web?o=0&l=dir&qo=homepageSearchBox&q=' + \
            translated_phone + '&page=' + str(i)
        driver.get(search_url)
        html_page = driver.page_source
        page_soup = soup(html_page, 'html.parser')
        try:
            no_result_container = page_soup.find(
                "div", {"class": "PartialSearchResults-noresults-body"})
            no_result_container = no_result_container.text.strip()
            if 'we did not find any results' in no_result_container:
                break
        except:
            pass
        result_containers = page_soup.findAll(
            "div", {"class": "PartialSearchResults-item"})
        for container in result_containers:
            for link in container.find_all('a'):
                link = link.get('href')
                link = str(link)
                valid_domain = valid_domain_check(link)
                if valid_domain:
                    valid_url = source_url_filter(link)
                    if valid_url:
                        if 'https' in link:
                            link = link.split('https://')[-1]
                        if '?' in link:
                            link = link.split('?')[0]
                        if '%' in link:
                            pass
                        else:
                            if link in ask_results:
                                pass
                            else:
                                ask_results.append(link)
                                # print("ask ---> " + link)
    return ask_results