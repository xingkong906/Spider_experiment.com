from lxml import html
import requests

url = 'https://experiment.com/projects/sequencing-the-fungi-of-the-ecuadorian-andes'
text = requests.get(url).text
etree = html.etree
ht = etree.HTML(text)
endorsed = ht.xpath('//*[@id="endorsements"]//div[@class="endorsement"]')
data = ht.xpath('//*[@id="endorsements"]/div/div[1]/div[1]/div/div[1]')

data = endorsed[0].xpath('/text')
print(ht.xpath('//*[@id="endorsements"]/div/div/div/div/text()'))
