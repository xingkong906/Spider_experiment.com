import json
import requests
from util.stringUtil import *
from dao.Dao import Dao
from lxml import html
import time

home_page = r"https://experiment.com"
url = r'https://experiment.com/discover/more'
etree = html.etree
dao = Dao(table='project')


# con = sqlite3.connect("../data/experiment.db")
# cursor = con.cursor()
# cursor.execute("created")
# def get(text):
#     dao_project = Dao(table='project')
#     dao_researchers = Dao(table='researchers')
#     rs = {}
#     researcher = {}
#     soup = BeautifulSoup(text, 'lxml')
#     projects = soup.find_all('div', attrs={'class': 'project-card'})
#     for project in projects:
#         try:
#             rs['id'] = to_int(project['id'])
#             rs['href'] = project.a['href']
#             rs['title'] = clean(str(project.find('h3', attrs={'class': 'project-title'}).a.string))
#             footer = project.find('div', attrs={'class': 'project-card-footer'})
#             rs['researcher'] = footer.div.a.string
#             rs['institution'] = footer.find('div', attrs={'class', 'institution'}).a.string
#             rs['url_researcher'] = footer.div.a['href']
#             researcher['name'] = rs['researcher']
#             researcher['url'] = rs['url_researcher']
#             status = footer.find('div', attrs={'class', 'row stats-row'})
#             rs['funding_percent'] = to_int(h4_founding(status.select("#funding-percent")[0].h4)) / 100
#             rs['funding_goal'] = to_int(h4_goal(status.select("#funding-goal")[0].h4))
#             rs['count_lab_notes'] = to_int(h4_founding(status.select(".time-remaining")[0].h4))
#             # 写入数据库
#             dao_project.item['data'] = rs
#             dao_researchers.item['data'] = researcher
#             dao_project.insert()
#             dao_researchers.insert()
#         except Exception as e:
#             print(e)
#         # 清空
#         rs.clear()
#         researcher.clear()

def get(text):
    selector = etree.HTML(text)
    rs = {}
    researcher = {}
    for cell in selector.xpath('//*[@class="project-card"]'):
        rs.clear()
        researcher.clear()
        rs['id'] = to_int(cell.xpath('.//@id')[0])
        rs['url'] = cell.xpath('.//div[2]/h3/a/@href')[0]
        rs['title'] = cell.xpath('.//div[2]/h3/a/text()')[0]
        rs['researcher'] = cell.xpath('.//div[3]/div[1]/div/span[1]/a/text()')[0]
        try:
            rs['institution'] = cell.xpath('.//div[@class="institution"]/a/text()')[0]
            rs['url_institution'] = cell.xpath('.//div[3]/div[1]/div/span[1]/a/@href')[0]
        except Exception:
            try:
                rs['institution'] = cell.xpath('.//div[@class="institution"]/text()')[0]
                rs['url_institution'] = ""
            except Exception:
                rs['institution'] = ""
                rs['url_institution'] = ""
        rs['url_researcher'] = cell.xpath('.//div[3]/div[1]/div/span[1]/a/@href')[0]
        researcher['name'] = rs['researcher']
        researcher['url'] = rs['url_researcher']
        rs['funding_percent'] = to_int(cell.xpath('.//*[@id="funding-percent"]/h4/text()')[0]) / 100
        rs['funding_goal'] = to_int(cell.xpath('//*[@id="funding-goal"]/h4/text()')[0])
        rs['count_lab_notes'] = to_int(cell.xpath('.//div[3]/div[3]/div[3]/h4/text()')[0])
        dao.insert(table='project', data=rs)
        dao.item['id'] = rs['id']
        dao.insert(table="researchers", data=researcher)


def do(start, end):
    times = time.time()
    for i in range(start, end + 1):
        print(i)
        req = requests.get(url, params={'offset': i * 6, 'order': 'founded'})
        html = json.loads(req.text)['cards']
        get(html)
    print("完成%d" % time.time() - times)


if __name__ == '__main__':
    # html = open('../data/project.html', 'r').read()
    url = r'https://experiment.com/discover/more'
    req = requests.get(url, params={'offset': 13 * 6, 'order': 'founded'})
    html = json.loads(req.text)['cards']
    print(html)
    # get(html)
    do(1, 128)
