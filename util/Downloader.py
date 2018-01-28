from requests import exceptions as reqException
import requests
from util.Throttle import Throttle
from util.Log import Log


class Downloader:
    logger = Log("downloader")

    def __init__(self, delay=5, user_agent=r"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
                 num_retries=1):
        """

        :param delay:
        :param user_agent:
        :param prxies:
        :param num_retries:
        :param cache:
        """
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.num_retries = num_retries

    def __call__(self, url):
        result = self.download(url=url, headers={"User-Agent": self.user_agent}, num_retries=self.num_retries)
        return result

    def download(self, url, headers, num_retries):
        self.logger.i("Downloading: " + url)
        try:
            req = requests.get(url, headers=headers)
            html = req.text
            if self.num_retries > 0 and 500 <= req.status_code < 600:
                # 服务器错误则忽略缓存并重新下载
                html = None
        except reqException as e:
            self.logger.e(e)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code <= 600:
                    html = self.download(url=url, headers=headers, num_retries=num_retries - 1)
        if html is None:
            self.throttle.wait(url)
            html = self.download(url=url, headers=headers, num_retries=num_retries)
        return html


if __name__ == '__main__':
    dow = Downloader()
    print(dow(r'http://www.baidu.com/'))
