config_cfpb = {
    'urls_config': {
        'base_url': 'https://www.consumerfinance.gov',
        'seed_url': 'https://www.consumerfinance.gov/about-us/newsroom/'
    },
    'pagination_config': {
        'type': 1,
        'scrape_url': 'https://www.consumerfinance.gov/about-us/newsroom/?page={}',
        'pagination': {
            'start_page': 1,
            'end_page': 4,
        },

    },
    'parser_schema': {
        'main_div': './/section[contains(@class,"filterable")]',
        'rows': './/article[@class="o-post-preview"]',
        'attributes': {
            'link': {
                'xpath': './/h3//@href',
            },
            'title': {
                'xpath': './/h3//a'
            },
            'date': {
                'xpath': './/time[@class="datetime_date"]',
            },
        }
    }
}

config_hpra = {
    'urls_config': {
        'base_url': 'https://www.hpra.ie/homepage/medicines',
        'seed_url': 'https://www.hpra.ie/homepage/medicines/news-events'
    },
    'pagination_config': {
        'type': 1,
        'scrape_url': 'https://www.hpra.ie/homepage/medicines/news-events?page={}&type=ALL&orderby=PUBLICATIONDATE_NEWEST',
        'pagination': {
            'start_page': 1,
            'end_page': 4,
        },

    },
    'parser_schema': {
        'main_div': './/table',
        'rows': './/tbody//tr',
        'attributes': {
            'link': {
                'xpath': './/td[2]//@href',
            },
            'title': {
                'xpath': './/td[2]//a'
            },
            'date': {
                'xpath': './/td[1]//span',
                'date_format': '%d/%m/%Y',
            },
            'extras': {
                'attribute_1': {
                    'key': ''
                }
            }

        }

    }}
