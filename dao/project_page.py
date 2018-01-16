import requests
from util.Downloader import Downloader
from bs4 import BeautifulSoup
import lxml
import re


class ProjectPage(object):
    project = dict()

    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.dow = Downloader()
        self.soup = BeautifulSoup(self.dow(url), 'lxml')

    def content(self):
        self.project['cntent'] = ""


if __name__ == '__main__':
    url = 'https://experiment.com/projects/sequencing-the-fungi-of-the-ecuadorian-andes'
    dow = Downloader()
    html = dow(url)
