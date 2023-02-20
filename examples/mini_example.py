#!env python
"""
  Sentaku pypi search exampple
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  before running::

    $ pip install selenium  requests sentaku
"""
from __future__ import annotations

import argparse
import contextlib
from typing import cast

import attr
import requests
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sentaku

parser = argparse.ArgumentParser()
parser.add_argument("query")
parser.add_argument("--fast", action="store_true")


class NS(argparse.Namespace):
    query: str
    fast: bool


@attr.s
class FastSearch:
    get = staticmethod(requests.get)


@attr.s
class Browser:
    driver: Remote = attr.ib()

    def __getattr__(self, key: str) -> object:
        return getattr(self.driver, key)


class SearchContext(sentaku.ImplementationContext):
    pass


@attr.s
class Search(sentaku.Element):
    """sentaku element for really simple pypi searching"""

    base_url: str = attr.ib(default="https://pypi.python.org/pypi")

    search = sentaku.ContextualMethod()
    open_page = sentaku.ContextualMethod()


@SearchContext.external_for(Search.search, Browser)
def search_browser(self: Search, text: str) -> str:
    """do a slow search via the website and return the first match"""
    self.impl.get(self.base_url)
    # get the search box
    search_div = self.impl.find_element_by_id("search")
    # input the search term
    search_div.send_keys(text)
    # click the search button to initiate search
    search_div.find_element_by_xpath(
        '//*[@id="content"]//div//button[contains(@type, "submit")]'
    ).click()
    # get the first element from the list of found items
    e = self.impl.find_element_by_xpath('//*[@id="content"]//li[1]/a')
    return cast(str, e.get_attribute("href"))


@SearchContext.external_for(Search.search, FastSearch)
def search_fast(self: Search, text: str) -> str:
    """do a sloppy quick "search" via the json index"""

    resp = self.impl.get(f"{self.base_url}/{text}/json")
    return cast(str, resp.json()["info"]["package_url"])


@SearchContext.external_for(Search.open_page, Browser)
def open_page(self: Search, url: str) -> None:
    self.impl.get(url)


def main(search: Search, query: str) -> None:
    """main function that does the search"""
    url = search.search(query)
    print(url)
    search.open_page(url)


def cli_main(args: list[str] | None = None) -> None:
    """cli entrypoitns, sets up everything needed"""
    config = parser.parse_args(args, NS())
    # open up a browser
    firefox_remote = Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.FIREFOX)
    with contextlib.closing(firefox_remote):
        context = SearchContext.from_instances([FastSearch(), Browser(firefox_remote)])
        search = Search(parent=context)

        if config.fast:
            with context.use(FastSearch, Browser):
                main(search, config.query)
        else:
            with context.use(Browser):
                main(search, config.query)


if __name__ == "__main__":
    cli_main()
