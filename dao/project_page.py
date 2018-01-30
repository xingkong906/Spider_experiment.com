from util.Downloader import Downloader
from util.log2 import logger
from util.stringUtil import *
from dao import Dao
from lxml import html
from dao.Dao import Dao
import json
import re

logger = logger(__name__)


class ProjectPage(object):
    project = dict()

    def __init__(self, id, url, **kwargs):
        self.id = id
        self.url = url
        self.dow = Downloader()
        if 'html' in kwargs.keys():
            self.html = kwargs['html']
        else:
            self.html = self.dow(url)
        self.etree = html.etree
        self.selector = None
        self.dao = Dao()
        self.dao.item['id'] = id

    def run(self):
        # try:
        logger.debug("id=%s\turl=%s" % (str(self.id), self.url))
        print(("id=%s\turl=%s" % (str(self.id), self.url)))
        self.over_view()
        self.discussion()
        self.lab_notes()
        print(self.project)
        self.update_status()
        # except Exception as e:

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

    def over_view(self):
        selector = self.selector
        if self.html != "":
            selector = self.etree.HTML(self.html)
        try:
            # 以p标记段落
            ps = selector.xpath('//*[@id="about"]/div/div/p')
            if ps:
                rs = ''
                for cell in ps:
                    rs += sql_str(cell.text)
                self.project['content'] = rs
            else:
                self.project['content'] = sql_str(selector.xpath('//*[@id="about"]/div/div/text()')[0])
        except Exception as e:
            print(e)
            self.project['content'] = ''
        data = self.func(selector, xpath=r'//div[@class="react-component"]/@data-react-props')
        budget = None
        backers = None
        for temp in data:
            if str(temp)[0:10].__contains__('items'):
                budget = json.loads(temp)['items']
            if str(temp)[0:10].__contains__('backers'):
                backers = json.loads(temp)['backers']
        self.dao.insert_dict_list(table="budget", data=budget)
        # self.dao.insert_dict_list(table="backers", data=backers)
        self.get_backers(data=backers)
        self.project['backers'] = list_dict_to_string('full_name', backers)
        researchers = self.func(selector, xpath='/html/body/div[2]/header/div[2]/div[1]/a')
        self.get_researchers(researchers)
        endorsed = self.func(selector, xpath='//*[@id="endorsements"]//div[@class="endorsement"]')
        self.get_endorsed(endorsed)
        time_line = self.func(selector, xpath='//*[@id="milestones"]/div/div/div[2]/div/div/div/div[2]')
        self.get_time_line(time_line)
        self.project['funding_raised'] = to_money(
            self.func(selector, xpath='//*[@id="prj-backers"]/ul/li[3]/span[1]/text()', order=0))
        self.project['average_donation'] = to_money(
            self.func(selector, xpath='//*[@id="prj-backers"]/ul/li[4]/span[1]/text()', order=0))
        self.project['count_backers'] = to_int(
            self.func(selector, xpath='//*[@id="prj-backers"]/ul/li[1]/span[1]/text()', order=0))
        self.project['location'] = sql_str(
            self.func(selector, xpath='.//div[@class="tags"]/div[1]/text()', order=0))
        self.project['DOI'] = re.sub('DOI: ', '',
                                     self.func(selector,
                                               xpath='.//div[@class="tags"]/div[@class="tag doi"]/text()', order=0))
        '/html/body/div[2]/header/div[2]/div[3]/div[2]/a[2]'
        self.project['categoryies'] = list_to_string(
            self.func(selector,
                      xpath='.//div[@class="tags"]/a[contains(@class,"tag category")]/text()'))
        self.project['count_labNotes'] = to_int(
            self.func(selector, xpath='/html/body/div[2]/nav/div/ul/li[6]/a/text()', order=0))
        self.project['count_disscussion'] = to_int(
            self.func(selector, xpath='/html/body/div[2]/nav/div/ul/li[7]/a/text()', order=0))
        self.dao.update(key='id', value=self.id, table="project", data=self.project)

    def get_endorsed(self, node_list):
        if not node_list:
            return
        self.dao.item["table"] = "endorsed"
        data = {}
        endorsed = []
        for node in node_list:
            data.clear()
            data['quote'] = sql_str(self.func(selector=node, xpath='.//div[@class="quote"]/text()', order=0))
            data['name'] = sql_str(self.func(selector=node, xpath='.//div[@class="name"]/text()', order=0))
            endorsed.append(data['name'])
            data['professional_title'] = sql_str(
                self.func(selector=node, xpath='.//div[@class="professional-title"]/text()',
                          order=0))
            data['affiliation'] = self.func(selector=node, xpath='.//div[@class="affiliation"]/text()', order=0)
            self.dao.insert(table='endorsed', data=data)
        # 将数据放入project表
        self.project['endorsed'] = list_to_string(endorsed)

    def get_time_line(self, node):
        if not node:
            return
        data = {}
        temp = []
        for cell in node:
            if not self.func(cell, xpath='./div'):
                data.clear()
                data['description'] = self.func(cell, xpath='./h2/text()', order=0)
                data['time'] = self.func(cell, xpath='./h4/text()', order=0)
                s = data['time'] + '\t' + data['description']
                temp.append(s)
                self.dao.insert(table='timeline', data=data)
        self.project['timeline'] = '\n'.join(temp)

    def get_researchers(self, node):
        if not node:
            return
        researchers = {}
        temp = []
        for cell in node:
            researchers.clear()
            researchers['name'] = sql_str(cell.text)
            temp.append(sql_str(cell.text))
            researchers['project_id'] = self.id
            researchers['url'] = 'https://experiment.com' + self.func(cell, xpath='.//@href', order=0)
            self.dao.insert_update(select="project_id", key='name', value=researchers['name'], table='researchers',
                                   data=researchers)
        self.project['researchers'] = '\t'.join(temp)

    def get_backers(self, **kwargs):
        # 遍历列表中的元素进行插入，每一个元素为一个字典json字符串
        if not kwargs['data']:
            return
        for cell in kwargs['data']:
            cell['project_id'] = self.id
            self.dao.insert_update(select="project_id", key='username', value=cell['username'], table='backers',
                                   data=cell)

    def lab_notes(self):
        selector = self.etree.HTML(self.dow(self.url + "/labnotes"))
        data = {}
        lab_note = self.func(selector, xpath='//*[@id="labnotes"]/div/div/div/div/div/a/div[2]')
        if lab_note == '':
            return
        for note in lab_note:
            data.clear()
            data['title'] = sql_str(self.func(note, xpath='.//div[1]/text()', order=0))
            data['url'] = r"https://experiment.com" + self.func(note, xpath='..//@href', order=0)
            data['date'] = sql_str(self.func(note, xpath='.//div[2]/text()', order=0))
            data['comment'] = sql_str(self.func(note, xpath='.//ul/li[1]/text()', order=0))
            data['heart'] = sql_str(self.func(note, xpath='.//ul/li[2]/text()', order=0))
            data['view'] = sql_str(self.func(note, xpath='.//ul/li[3]/text()', order=0))
            data['project_id'] = self.id
            self.dao.insert(table='lab_notes', data=data)

    def discussion(self):
        selector = self.etree.HTML(self.dow(self.url + "/discussion"))
        root = self.func(selector, xpath='//*[@id="discussion"]//div[@class="react-component"]/@data-react-props',
                         order=0)
        if not root:
            return
        comments = \
            json.loads(root)[
                'initialComments']
        for note in comments:
            if note['children']:
                self.get_children(note)
            else:
                note['children'] = ''
                note['project_id'] = self.id
                self.dao.insert(table='discussion', data=note)

    def get_children(self, node={}):
        # 使用迭代器遍历出所有的discussion
        for cell in node['children']:
            node['children'] = cell['id']
            node['project_id'] = self.id
            self.dao.insert(table='discussion', data=node)
            if cell['children']:
                self.get_children(cell)
            else:
                cell['children'] = ''
                cell['project_id'] = self.id
                self.dao.insert(table='discussion', data=cell)

    def update_status(self):
        # 更新处理状态为完成
        self.dao.update(key="id", value=self.id, table='project', data={'process_status': "true"})


if __name__ == '__main__':
    root = 'https://experiment.com'
    url = '/projects/cannibalism-in-giant-tyrannosaurs'
    item = ProjectPage(22, root + url)
    # item.lab_notes()
    item.run()
