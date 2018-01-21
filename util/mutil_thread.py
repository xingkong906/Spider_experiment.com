import threading
from time import ctime, time
from dao.Projects import *


class MyThread(object):
    def __init__(self, length, thread_num=6):
        self.thread_num = thread_num
        self.length = length

    def get_range(self):
        ranges = []
        length = self.length
        offset = int(int(length) / self.thread_num)
        for i in range(self.thread_num):
            if i == (self.thread_num - 1):
                ranges.append((i * offset, length))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        print(range)
        return ranges

    def do_someting(start, end):
        dao_project = Dao(table='project')
        dao_researchers = Dao(table='researchers')
        for i in range(start, end + 1):
            req = requests.get(url, params={'offset': i, 'order': 'founded'})
            html = json.loads(req.text)['cards']
            project, researcher = get(html)
            dao_project.item['data'] = project
            dao_researchers.item['data'] = researcher
            dao_researchers.insert()
            dao_researchers.insert()
        print("完成")

    def start(self):
        thread_list = []
        n = 1
        for ran in self.get_range():
            s1, s2 = ran
            print('starting:%d thread ' % n)
            n += 1
            thread = threading.Thread(target=self.do_someting(), args=(s1, s2))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            i.join()
        print("进程执行完成")


if __name__ == '__main__':
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    #
    # print("all over %s" % ctime())
    s = time()
    down = MyThread(128, 6)
    down.start()
    e = time()
    print("The time spent on this program is %f s" % (e - s))
