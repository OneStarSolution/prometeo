import pytest

from yelp.yelp_data_scraper_sc import scrape_item_yelp


@pytest.mark.parametrize("url,expected_output", [('www.yelp.com/biz/alkaline-me-plano',
                                                  ['Alkaline Me', '(469) 914-5794', 'www.yelp.com/biz/alkaline-me-plano', '3131 Custer Rd',
                                                   'Plano', '75075', '75075', '', '', '', 'Claimed', '', '', 'Me', '', '', 'No', '', '']),
                                                 ('www.yelp.com/biz/classica-gregory-water-treatment-system-carrollton',
                                                  ['Classica Gregory Water Treatment System', '(972) 245-6937', 'www.yelp.com/biz/classica-gregory-water-treatment-system-carrollton', '1614 S Broadway St', 'Carrollton', '75006', '75006', '', '', '', 'Unclaimed', '', '', 'System', '', '', 'No', '', ''])])
def test_crawler_yelp(url, expected_output):
    result = scrape_item_yelp(url)
    assert expected_output == result
