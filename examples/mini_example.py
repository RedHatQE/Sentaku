#!env python
"""
  Sentaku pypi search exampple
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  before running::

    $ pip install selenium  requests sentaku
"""
import argparse
import contextlib
import sentaku
import requests
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--fast', action='store_true')


FastSearch = sentaku.ImplementationName(
    'FastSearch',
    """Used to implement fast search""")

Browser = sentaku.ImplementationName(
    'FastSearch',
    """used to implement all browser actions and browser based slow search""")


class Search(sentaku.Element):
    """sentaku element for really simple pypi searching"""
    search = sentaku.ContextualMethod()

    @search.implemented_for(Browser)
    def search(self, text):
        """do a slow search via the website and return the first match"""
        self.impl.get('https://pypi.python.org/pypi')

        search_div = self.impl.find_element_by_id('search')
        search_term = search_div.find_element_by_id('term')
        search_term.send_keys(text)
        search_div.find_element_by_id('submit').click()
        e = self.impl.find_element_by_css_selector('table.list tr td a')
        return e.get_attribute('href')

    @search.implemented_for(FastSearch)
    def search(self, text):
        """do a sloppy quick "search" via the json index"""

        resp = self.impl.get(
            'https://pypi.python.org/pypi/{text}/json'.format(text=text))
        return resp.json()['info']['package_url']

    open_page = sentaku.ContextualMethod()

    @open_page.implemented_for(Browser)
    def open_page(self, url):
        self.impl.get(url)


def main(search, query):
    """main function that does the search"""
    url = search.search(query)
    print(url)
    search.open_page(url)


def cli_main():
    """cli entrypoitns, sets up everything needed"""
    args = parser.parse_args()
    # open up a browser
    firefox_remote = Remote(
        'http://127.0.0.1:4444/wd/hub',
        DesiredCapabilities.FIREFOX)
    with contextlib.closing(firefox_remote):

        search = Search({
            FastSearch: requests,
            Browser: firefox_remote,
        })

        if args.fast:
            with search.use(FastSearch, Browser):
                main(search, args.query)
        else:
            with search.use(Browser):
                main(search, args.query)


if __name__ == '__main__':
    cli_main()
