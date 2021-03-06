# -*- coding:utf8 -*-
import re


def sql_str(sql):
    return str(sql).replace('"', '""').replace("'", "''")


def is_num(text):
    for x in text:
        if x in range(0, 10):
            return True
    return False


def to_int(text):
    # 提取字符串中的数字
    text = clean(text)
    rs = re.sub('[\D\s]', "", text)
    try:
        rs = int(rs)
    except ValueError:
        rs = 0
    finally:
        return rs


def to_money(text):
    text = clean(text)
    rs = re.sub('[\$,]', "", text)
    try:
        rs = float(rs)
    except ValueError:
        rs = 0
    finally:
        return rs


def list_to_string(list=[]):
    return '\t'.join(list)


def dict_to_string(tag, dict={}):
    return dict[tag]


def list_dict_to_string(tag, list=[]):
    rs = []
    for cell in list:
        if type(cell) == type({}):
            rs.append(str(cell[tag]).strip())
    return '\t'.join(rs)


def clean(text):
    # 清除字符串中的空白字符,包括换页（‘\f’）、换行（‘\n’）、回车（‘\r’）、水平制表符（‘\t’）、垂直制表符（‘\v’），以及多个连续的空格
    rs = re.sub("[\n\t\v\f]", '', text)
    rs = re.sub(' {1,}', ' ', rs)
    return rs


if __name__ == '__main__':
    clean("Exploring water data\n                with high school students in Flint, MI")
    print(to_money('$4,865'))
    print(to_int(""))
