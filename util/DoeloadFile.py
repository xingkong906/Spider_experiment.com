import requests

file_name = "../data/data.html"
url = 'https://experiment.com/projects/nyu-research-labs-need-your-help'
with open(file_name, 'w') as file:
    file.write(requests.get(url).text)
print("写入完成")
