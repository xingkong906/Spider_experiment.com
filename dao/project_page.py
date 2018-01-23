from util.Downloader import Downloader
from util.Log import Log
from util.stringUtil import *
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
        self.project['backers'] = list_dict_to_string('full_name', backers)
        researchers = selector.xpath('/html/body/div[2]/header/div[2]/div[1]/a')
        self.get_researchers(researchers)
        endorsed = selector.xpath('//*[@id="endorsements"]//div[@class="endorsement"]')
        self.get_endorsed(endorsed)
        time_line = selector.xpath('//*[@id="milestones"]/div/div/div[2]/div/div/div/div[2]')
        self.get_time_line(time_line)
        self.project['funding_raised'] = to_money(selector.xpath('//*[@id="prj-backers"]/ul/li[3]/span[1]/text()')[0])
        self.project['average_donation'] = to_money(selector.xpath('//*[@id="prj-backers"]/ul/li[4]/span[1]/text()')[0])
        self.project['count_backers'] = to_int(selector.xpath('//*[@id="prj-backers"]/ul/li[1]/span[1]/text()')[0])
        self.project['location'] = selector.xpath('/html/body/div[2]/header/div[2]/div[3]/div[2]/div[1]/text()')[0]
        self.project['DOI'] = re.sub('DOI: ', '',
                                     selector.xpath('/html/body/div[2]/header/div[2]/div[3]/div[2]/div[2]/text()')[0])
        self.project['categoryies'] = list_to_string(
            selector.xpath('/html/body/div[2]/header/div[2]/div[3]/div[2]/a[contains(@class,"tag category")]/text()'))
        self.project['count_labNotes'] = to_int(selector.xpath('/html/body/div[2]/nav/div/ul/li[6]/a/text()')[0])
        self.project['count_disscussion'] = to_int(selector.xpath('/html/body/div[2]/nav/div/ul/li[7]/a/text()')[0])
        print(self.project)
        self.dao.uodate(key='id', value=self.id, table="project", data=self.project)

    def get_endorsed(self, node_list):
        self.dao.item["table"] = "endorsed"
        data = {}
        endorsed = []
        for node in node_list:
            data.clear()
            data['quote'] = node.xpath('.//div[@class="quote"]/text()')[0]
            data['name'] = node.xpath('.//div[@class="name"]/text()')[0]
            endorsed.append(data['name'])
            data['professional_title'] = node.xpath('.//div[@class="professional-title"]/text()')[0]
            try:
                data['affiliation'] = node.xpath('.//div[@class="affiliation"]/text()')[0]
            except Exception:
                data['affiliation'] = ''
            self.dao.insert(table='endorsed', data=data)
        # 将数据放入project表
        self.project['endorsed'] = list_to_string(endorsed)

    def get_time_line(self, node):
        data = {}
        temp = []
        for cell in node:
            if not cell.xpath('./div'):
                data.clear()
                data['description'] = cell.xpath('./h2/text()')[0]
                data['time'] = cell.xpath('./h4/text()')[0]
                s = data['time'] + '\t' + data['description']
                temp.append(s)
                self.dao.insert(table='timeline', data=data)
        self.project['timeline'] = '\n'.join(temp)

    def get_researchers(self, node):
        researchers = {}
        temp = []
        for cell in node:
            researchers.clear()
            researchers['name'] = cell.text
            temp.append(cell.text)
            researchers['url'] = 'https://experiment.com' + cell.xpath('.//@href')[0]
            self.dao.insert(table='researchers', data=researchers)
        self.project['researchers'] = '\t'.join(temp)

    def lab_notes(self):
        selector = self.etree.HTML(self.dow(self.url + "/labnotes"))
        data = {}
        for note in selector.xpath('//*[@id="labnotes"]/div/div/div/div/div/a/div[2]'):
            data.clear()
            data['title'] = note.xpath('.//div[1]/text()')[0]
            data['url'] = r"https://experiment.com" + note.xpath('..//@href')[0]
            data['date'] = note.xpath('.//div[2]/text()')[0]
            data['comment'] = note.xpath('.//ul/li[1]/text()')[0]
            data['heart'] = note.xpath('.//ul/li[2]/text()')[0]
            data['view'] = note.xpath('.//ul/li[3]/text()')[0]
            self.dao.insert(table='lab_notes', data=data)

    def discussion(self):
        selector = self.etree.HTML(self.dow(self.url + "/discussion"))
        comments = \
            json.loads(selector.xpath('//*[@id="discussion"]//div[@class="react-component"]/@data-react-props')[0])[
                'initialComments']
        for note in comments:
            if note['children']:
                self.get_children(note)
            else:
                note['children'] = ''
                self.dao.insert(table='discussion', data=note)

    def get_children(self, node={}):
        # 使用迭代器遍历出所有的discussion
        for cell in node['children']:
            node['children'] = cell['id']
            self.dao.insert(table='discussion', data=node)
            if cell['children']:
                self.get_children(cell)
            else:
                cell['children'] = ''
                self.dao.insert(table='discussion', data=cell)


if __name__ == '__main__':
    url = 'https://experiment.com/projects/sequencing-the-fungi-of-the-ecuadorian-andes'
    item = ProjectPage(4103, url)
    # item.lab_notes()
    item.discussion()
