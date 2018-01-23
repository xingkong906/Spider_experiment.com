from lxml import html
from util.stringUtil import *
import re
import requests

url = 'https://experiment.com/projects/sequencing-the-fungi-of-the-ecuadorian-andes'
text = requests.get(url).text
etree = html.etree
ht = etree.HTML(text)
data = ht.xpath('/html/body/div[2]/header/div[2]/div[1]/a')
print(data[1].text)
print(data[1].xpath('.//@href')[0])
data = {'comment': 'Keep it up, guys <3', 'id': 22703, 'user_id': 132021, 'shadowbanned': False, 'likes_count': 1,
        'type': None, 'data_key': None, 'highlighted_text': None, 'user_show_page': '/users/kktretiakova',
        'user_avatar': '//d3t9s8cdqyboc5.cloudfront.net/assets/face-4-medium-fdae90eecf5db5aac49cbaab3f554ae9759327daabe7039cefff5070ec70ffa3.png',
        'user_name': 'Ksenia K Tretiakova', 'time_stamp': '2018-01-10T06:47:57.339-08:00', 'time_in_words': '13 days',
        'published_at': 'Jan 10, 2018', 'active_depth': 0, 'depth_limited': False, 'children': [], 'user_tag': 'Backer',
        'likeable_type': 'Comment', 'likeable_id': 22703, 'project_id': 4103}
