"""
Crawling script
"""

import re
import requests
from bs4 import BeautifulSoup


class VocabularCollector():
    """Receives an article link and returns a dict of words and other parameters

    Args:
        journal_name (str): The journal name.
        journal_link (str): the link of the article to be scraped.

    Returns:
        A list of dictionaries e.g. {"word":"", "sentence:""}
    """
    newVoc = []

    def __init__(self, data):
        self.name = data['journal_name']
        self.link = data['journal_link']

    @property
    def crawl(self):
        """Checks which journal the links belongs."""
        page = VocabularCollector.requests_object(self.link)
        if isinstance(page, dict):  # if req failed, returns a dict of error
            return page
        soup = BeautifulSoup(page.content, 'html.parser')
        return self.build_dictionary(soup)

    def build_dictionary(self, soup):
        """To scrape articles from Spiegel journal

        Args:
            soup (obj): A beautifulsoup object.
        """
        _p_texts = []
        _words_list = []
        _refined = []

        if self.name == "Spiegel":
            regex = re.compile('RichText RichText--iconLinks')
            for div in soup.find_all("div", {"class": regex}):
                _p_texts.append(div.p.text.replace('\n', '').strip())
        elif self.name == "Tagesschau":
            for div in soup.find_all("div", class_="mod modA modParagraph"):
                for p in div.find_all("p", class_="text small"):
                    _p_texts.append(p.text.replace('\n', '').strip())
        else:
            return {"error": "provided journal is not known"}

        for p_text in _p_texts:
            p_text_list = p_text.split(" ")
            for index, each_word in enumerate(p_text_list):
                for char in '".,()-„':
                    each_word = each_word.replace(char, '')
                each_word = each_word.strip()
                if each_word and len(each_word) > 1 and each_word not in _words_list and not each_word.isnumeric() and not any(x in "_@#$%&*?/" for x in each_word):
                    _refined.append({"word": each_word, "sentence": VocabularCollector.extract_sentence(index, p_text_list)})

        return _refined

    @staticmethod
    def extract_sentence(index, p_tags):
        """To re-construct the sentence that a word belongs."""
        p_length = len(p_tags)
        start = index-3
        end = index+4
        if start < 0:
            start = 0
        if end > p_length:
            end = p_length
        return ' '.join(p_tags[start:end])

    @staticmethod
    def requests_object(link):
        """Gets the link content through bs4 and returns an object"""
        try:
            page = requests.get(f"{link}")
        except requests.exceptions.HTTPError as err:
            return {"error": "Http"}
        except requests.exceptions.ConnectionError as err:
            return {"error": "Connection"}
        except requests.exceptions.Timeout as err:
            return {"error": "Timeout"}
        except requests.exceptions.RequestException as err:
            return {"error": "RequestException"}
        return page
