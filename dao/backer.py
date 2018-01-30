# -*- coding:utf8 -*-
from util.log2 import logger
from util.Downloader import Downloader
from util.stringUtil import *
from dao.Dao import Dao
from lxml import html

logger = logger(__name__)


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

    @staticmethod
    def func(selector, xpath, order=-1):
        rs = None
        try:
            rs = selector.xpath(xpath)
        except IndexError as e:
            logger.error("可能不存在，请检查\t" + e)
            rs = ""
        except Exception as e:
            logger.error(e)
            rs = ""
        finally:
            if rs and order >= 0:
                return rs[order]
            else:
                if not rs:
                    return ''
                return rs

    def run(self):
        self.backer['lab_notes_count'] = self.func(self.selector, xpath='//*[@id="updates-nav"]/a/h3/span/text()',
                                                   order=0)
        self.backer['comment_count'] = self.func(self.selector, xpath='//*[@id="comments-nav"]/a/h3/span/text()',
                                                 order=0)
        self.backer['started_count'] = self.func(self.selector,
                                                 xpath='//*[@id="created_projects-nav"]/a/h3/span/text()',
                                                 order=0)
        self.backer['backed_count'] = self.func(self.selector, xpath='//*[@id="backed_projects-nav"]/a/h3/span/text()',
                                                order=0)
        self.get_projects_backed()
        self.get_projects_started()
        self.dao.update(key='id', value=self.id, table='backers', data=self.backer)
        self.dao.update(key="id", value=self.id, table='backers', data={'process_status': "true"})

    def get_projects_started(self):
        selector = self.func(self.selector, xpath='.//*[@id="created_projects"]', order=0)
        self.backer['started'] = self.get_projects_card(selector)

    def get_projects_backed(self):
        selector = self.func(self.selector, xpath='.//*[@id="backed_projects"]', order=0)
        self.backer['backed'] = self.get_projects_card(selector)

    def get_projects_card(self, node):
        # 解析card
        rs = {}
        temp = []
        try:
            for cell in node.xpath('.//*[@class="project-card"]'):
                rs.clear()
                rs['id'] = to_int(self.func(cell, xpath='./@id', order=0))
                rs['url'] = self.func(cell, xpath='./div[2]/h3/a/@href', order=0)
                rs['title'] = self.func(cell, xpath='./div[2]/h3/a/text()', order=0)
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
