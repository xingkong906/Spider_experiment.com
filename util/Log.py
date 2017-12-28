import logging


class Log:

    def __init__(self, pid, *tag):
        self.PID = pid
        self.TAG = tag[0]
        self
        self.logger = self.get_logger()

    def set_tag(self, tag):
        self.TAG = tag

    def i(self, message):
        self.logger.info(message);

    def d(self, message):
        self.logger.debug(message)

    def e(self, message):
        self.logger.debug(message)

    def set_level(self, level):
        self.logger.setLevel(level)

    def get_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename="../log/" + str(self.PID) + '.log',
                            filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        log = logging.getLogger(self.TAG)
        log.addHandler(console)
        return log


if __name__ == '__main__':
    logger = Log(1, __name__)
    logger.i("start")
