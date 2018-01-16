import threading
from time import ctime, sleep
from util.Downloader import Downloader


class MyThread(object):
    def __init__(self, length, thread_num=6):
        self.thread_num = thread_num
        self.length = length

    def get_range(self):
        ranges = []
        length = self.getLength()
        offset = int(int(length) / self.threadNum)
        for i in range(self.threadNum):
            if i == (self.threadNum - 1):
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        return ranges

    def run(self):
        # do someThing
        pass

    def start(self):
        thread_list = []
        n = 1
        for ran in self.get_range():
            start, end = ran
            print('starting:%d thread ' % n)
            n += 1
            thread = threading.Thread(target=self.run, args=(start, end))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            i.join()
        print("进程执行完成")

    @staticmethod
    def timer(func):
        def wrapper():
            print("开始时间" + ctime())
            func()
            sleep(3)
            print("完成")
            print("结束时间" + ctime())

        return wrapper


if __name__ == '__main__':
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    #
    # print("all over %s" % ctime())
    pass
