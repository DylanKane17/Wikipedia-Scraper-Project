'''This module scrapes a wikipedia article and then its citations (in accordance with robots.txt)'''
from urllib.parse import urlsplit, urlunsplit, SplitResult
import urllib.robotparser
from bs4 import BeautifulSoup
import requests
import trafilatura

def scrape_wiki(url):
    '''Scrapes article HTML and obtains external source tags'''

    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.text, "html.parser")

    sources = soup.find_all("a", class_="external text")

    source_objects = []
    for source in sources:
        if not source.string:
            continue
        if source.string and (
            "https://www.google.com/search" in source.string or
            "https://www.jstor.org" in source.string or
            "https://en.wikipedia.org" in source.string
        ):
            continue

        if source.string and (
            source.string != 'Archived' and 
            source.string != 'the original' and
             not source.string.isdigit()
        ):
            source_objects.append({
                'name': source.string,
                'href': source['href']
            })

    print(source_objects)
    return source_objects


def check_robots(url) -> bool:
    '''Checks robot.txt of site. If permitted to scrape, returns true'''
    
    split_url = urlsplit(url)
    split_base_url = SplitResult(scheme=split_url.scheme, netloc=split_url.netloc, path='', query='', fragment='')
    base_url = urlunsplit(split_base_url)

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url + "/robots.txt")
    try:
        rp.read()
        return rp.can_fetch("*", base_url)
    except Exception:
        return False


def scrape_source(url) -> str:
    '''If allowed to scrape, obtains site's text body'''

    if check_robots(url):
        article_fetch = trafilatura.fetch_url(url)
        article_content = trafilatura.extract(article_fetch, include_comments=False, include_tables=False)
        print(article_content)
        return article_content
        
    return "Disallowed"
