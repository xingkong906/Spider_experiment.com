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
