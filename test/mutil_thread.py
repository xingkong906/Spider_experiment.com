import threading
from time import ctime, sleep
from util.Downloader import Downloader


def timer(func):
    def wrapper():
        print("开始时间" + ctime())
        func()
        sleep(3)
        print("完成")
        print("结束时间" + ctime())

    return wrapper


@timer
def func1():
    dow = Downloader()
    print(ctime())
    dow(r'http://www.baidu.com/')

    print("func1")


@timer
def func2():
    dow = Downloader()
    dow(r'http://www.swu.edu.cn.com/')
    print("func2")


threads = []
t1 = threading.Thread(target=func1, )
threads.append(t1)
t2 = threading.Thread(target=func2, )
threads.append(t2)
if __name__ == '__main__':
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    #
    # print("all over %s" % ctime())
    t1.start()
    t2.start()
