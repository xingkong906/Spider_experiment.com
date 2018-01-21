import requests
from util.Downloader import Downloader
from util.Log import Log
from dao import Dao
from lxml import html
from dao.Dao import Dao
import json
import re

logger = Log(__name__)


class ProjectPage(object):
    project = dict()

    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.dow = Downloader()
        self.html = self.dow(url)
        self.etree = html.etree
        self.selector = None
        self.dao = Dao()
        self.dao.item['id'] = id

    def over_view(self):
        selector = self.selector
        if self.html != "":
            selector = self.etree.HTML(self.html)

        self.project['content'] = selector.xpath(r'//*[@id="about"]/div/div/p')[0].text
        data = selector.xpath(r'//div[@class="react-component"]/@data-react-props')
        budget = json.loads(data[2])['items']
        self.dao.insert_dict_list(table="budget", data=budget)
        backers = json.loads(data[3])['backers']
        self.dao.insert_dict_list(table="backers", data=backers)
        endorsed = selector.xpath('//*[@id="endorsements"]//div[@class="endorsement"]')
        print(endorsed)

    def lab_notes(self):
        pass

    def discussion(self):
        pass


if __name__ == '__main__':
    url = 'https://experiment.com/projects/sequencing-the-fungi-of-the-ecuadorian-andes'
    item = ProjectPage(1, url)
    item.over_view()
