import re


def to_int(text):
    # 提取字符串中的数字
    text = clean(text)
    rs = re.sub('[\D\s]', "", text)
    return int(rs)


def to_money(text):
    pass


def clean(text):
    # 清除字符串中的空白字符,包括换页（‘\f’）、换行（‘\n’）、回车（‘\r’）、水平制表符（‘\t’）、垂直制表符（‘\v’），以及多个连续的空格
    rs = re.sub("[\n\t\v\f]", '', text)
    rs = re.sub(' {1,}', ' ', rs)
    return rs


if __name__ == '__main__':
    clean("Exploring water data\n                with high school students in Flint, MI")