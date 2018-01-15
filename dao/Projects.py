import json
import requests
from bs4 import BeautifulSoup
from util.stringUtil import *
from dao.Dao import Dao

home_page = r"https://experiment.com"
url = r'https://experiment.com/discover/more'
req = requests.get(url, params={'offset': '12', 'order': 'founded'})
html = json.loads(req.text)


# con = sqlite3.connect("../data/experiment.db")
# cursor = con.cursor()
# cursor.execute("created")
def get(text):
    rs = {}
    researcher = {}
    soup = BeautifulSoup(text, 'lxml')
    projects = soup.find_all('div', attrs={'class': 'project-card'})
    for project in projects:
        rs['id'] = to_int(project['id'])
        rs['href'] = project.a['href']
        rs['title'] = clean(str(project.find('h3', attrs={'class': 'project-title'}).a.string))
        footer = project.find('div', attrs={'class': 'project-card-footer'})
        rs['researcher'] = footer.div.a.string
        rs['institution'] = footer.find('div', attrs={'class', 'institution'}).a.string
        rs['url_researcher'] = footer.div.a['href']
        researcher['name'] = rs['researcher']
        researcher['url'] = rs['url_researcher']
        status = footer.find('div', attrs={'class', 'row stats-row'})
        rs['funding_percent'] = to_int(h4_founding(status.select("#funding-percent")[0].h4)) / 100
        rs['funding_goal'] = to_int(h4_goal(status.select("#funding-goal")[0].h4))
        rs['count_lab_notes'] = to_int(h41(status.find('div', attrs={'id': 'time-remaining'})))
    print(rs)


def h4_founding(text):
    text = str(text)
    match = re.match(r'<h4>(.*)?%<b', text)
    return str(match.group(1))


def h4_goal(text):
    text = str(text)
    pattern = re.compile(u'>\$(.*)?<')
    match = re.match('>\$(.*)?<', text)
    return str(match.group(1))


if __name__ == '__main__':
    html = open('../data/project.html', 'r').read()
    get(html)
