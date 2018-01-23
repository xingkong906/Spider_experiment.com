# -*- coding:utf8 -*-
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

    def run(self):
        self.backer['lab_notes_count'] = self.selector.xpath('//*[@id="updates-nav"]/a/h3/span/text()')[0]
        self.backer['comment_count'] = self.selector.xpath('//*[@id="comments-nav"]/a/h3/span/text()')[0]
        self.backer['started_count'] = self.selector.xpath('//*[@id="created_projects-nav"]/a/h3/span/text()')[0]
        self.backer['backed_count'] = self.selector.xpath('//*[@id="backed_projects-nav"]/a/h3/span/text()')[0]
        self.get_projects_backed()
        self.get_projects_started()
        self.dao.uodate(table='backers', data=self.backer)
        self.dao.close()

    def get_projects_started(self):
        selector = self.selector.xpath('.//*[@id="created_projects"]')[0]
        self.backer['started'] = Backer.get_projects_card(selector)

    def get_projects_backed(self):
        selector = self.selector.xpath('.//*[@id="backed_projects"]')[0]
        self.backer['backed'] = Backer.get_projects_card(selector)

    @staticmethod
    def get_projects_card(node):
        # 解析card
        rs = {}
        temp = []
        try:
            for cell in node.xpath('.//*[@class="project-card"]'):
                rs.clear()
                rs['id'] = to_int(cell.xpath('./@id')[0])
                rs['url'] = cell.xpath('./div[2]/h3/a/@href')[0]
                rs['title'] = cell.xpath('./div[2]/h3/a/text()')[0]
                temp.append(str(rs['id']) + '\t' + rs['title'] + '\t' + rs['url'])
            return '\n'.join(temp)
        except Exception:
            return ""

    def update_status(self):
        # 更新处理状态为完成
        self.dao.update(table='backers', data={'process_status': "true"})


if __name__ == '__main__':
    b = Backer(id=23, url='https://experiment.com/users/hsauro')
    b.run()
