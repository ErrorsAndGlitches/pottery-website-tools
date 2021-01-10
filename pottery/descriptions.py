import csv

import requests
from bs4 import BeautifulSoup
from termcolor import colored

_WEBSITE_HOST = 'https://seattlepotterysupply.com/'


class Descriptions(object):
    def __init__(self, output_filename):
        self._output_filename = output_filename

    def run(self):
        all_product_paths = []
        for type_path in _SearchByTypePage(HtmlRequest(_SearchByTypePage.PATH).soup()).type_paths():
            all_product_paths.extend(_TypePage(type_path).product_paths())

        unique_product_paths = set(all_product_paths)

        with open(self._output_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for product_path in unique_product_paths:
                info = _ProductPage(product_path).product_info()
                writer.writerow([info.title, info.description])


class HtmlRequest(object):
    def __init__(self, path):
        self._path = path

    def soup(self):
        print(colored('querying for: {}'.format(self._path), 'green'))
        return BeautifulSoup(requests.get(_WEBSITE_HOST + self._path).text, 'html.parser')


class _SearchByTypePage(object):
    PATH = 'pages/search-by-type'

    def __init__(self, soup):
        self._soup = soup

    def type_paths(self):
        return [
            anchor['href']
            for anchor in self._soup.find(id='content').find_all('a')
        ]


class _TypePage(object):
    def __init__(self, path):
        self._path = path

    def product_paths(self):
        all_anchors = []

        page_num = 1
        anchors = self._page_anchors(page_num)
        while len(anchors) > 0:
            all_anchors.extend([anchor['href'] for anchor in anchors])
            page_num += 1
            anchors = self._page_anchors(page_num)

        return all_anchors

    def _page_anchors(self, page_num):
        collection = HtmlRequest(self._path + '?page={}'.format(page_num)) \
            .soup() \
            .find(id='collection')

        if collection is None:
            return []
        else:
            return [
                anchor
                for header in collection.find_all('h5')
                for anchor in header.find_all('a') if '?page=' not in anchor['href']
            ]


class _ProductPage(object):
    def __init__(self, path):
        self._path = path

    def product_info(self):
        soup = HtmlRequest(self._path).soup()
        product_header = soup.find('h1', {'class': 'product-header'}).get_text().strip()
        description_ele = soup.find(id='description')
        description = description_ele.get_text().strip() if description_ele is not None else ''
        return _ProductInfo(
            product_header,
            description
        )


class _ProductInfo(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return 'title={}, description={}'.format(self.title, self.description[:100])
