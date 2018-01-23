from util.Log import *
from util.Downloader import Downloader
from util.stringUtil import *
from dao.Dao import Dao
from lxml import html

logger = Log(__name__)


class Backer(object):
    backer = dict()

    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.dow = Downloader()
        self.html = self.dow(url)
        self.etree = html.etree
        self.selector = self.etree.HTML(self.html)
        self.dao = Dao()

    def get_projects_started(self):
        selector = self.selector.xpath('//*[@id="created_projects"]')
        self.backer['started'], self.backer['started_count'] = Backer.get_projects_card(selector)

    def get_projects_backed(self):
        selector = self.selector.xpath('//*[@id="backed_projects"]')
        self.backer['backed'], self.backer['backed_count'] = Backer.get_projects_card(selector)

    @staticmethod
    def get_projects_card(node):
        # 解析card
        rs = {}
        temp = []
        count = 0
        for cell in node.xpath('.//*[@class="project-card"]'):
            rs.clear()
            rs['id'] = to_int(cell.xpath('.//@id')[0])
            rs['url'] = cell.xpath('.//div[2]/h3/a/@href')[0]
            rs['title'] = cell.xpath('.//div[2]/h3/a/text()')[0]
            temp.append(str(rs['id'] + '\t' + rs['url'] + '\t' + rs['title']))
            count += 1
        return ['\n'.join(temp), count]
