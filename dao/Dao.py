# -*- coding:utf8 -*-
import sqlite3
from util.log2 import logger
from util.stringUtil import *

logger = logger(__name__)


class Dao(object):
    item = dict()
    con = None
    cursor = None

    def __init__(self, **args):
        """
        对数据库的操作
        :param table_name: 表名
        :param args: 数据字典
        """
        for key in args.keys():
            self.__setitem__(key=key, value=args[key])
        # self.item['table'] = args['table']
        # if 'data' in args.keys():
        #     self.item['data'] = args['data']
        self.con = self.get_con()
        self.cursor = self.con.cursor()

    # def __init__(self, table, data):
    #     self.item['table'] = table
    #     self.item['data'] = data

    def __setitem__(self, key, value):
        if key == "con":
            self.con = value
            self.cursor = self.con.cursor()
        else:
            self.item[key] = value

    def __getitem__(self, item):
        return self.item.get(item)

    @staticmethod
    def get_con():
        return sqlite3.connect("../data/experiment.db")

    def open_data_base(self):
        try:
            self.con
        except Exception as e:
            logger.error("There is a error in connecting database,we are fixing!")
            self.con = self.get_con()
            self.cursor = self.con.cursor()

    def insert(self, **kwargs):
        for key in kwargs.keys():
            self.__setitem__(key=key, value=kwargs[key])
        if self.con is None:
            self.con = Dao.get_con()
            self.cursor = self.con.cursor()
        if 'id' in self.item.keys() and self.item['table'] != 'project' and 'project_id' not in kwargs.keys():
            self.item['data']['project_id'] = self.item['id']
        col = " ,".join(self.item['data'].keys())
        row = ",".join(len(self.item['data']) * "?")
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.item['table'], col, row)
        try:
            print(type(self.item['data'].values()))
            self.cursor.execute(sql, tuple(self.item['data'].values()))
            self.con.commit()
        except sqlite3.Error as e:
            if 'UNIQUE constraint' in e:
                print("existed,can't insert " + self.item['table'])
            logger.error(self.item['data'])
            logger.error(e)
        logger.info("Inserting success")

    def insert_dict_list(self, **kwargs):
        # 遍历列表中的元素进行插入，每一个元素为一个字典json字符串
        if kwargs['data'] is None:
            return
        if "table" in kwargs.keys():
            self.item['table'] = kwargs['table']
        for cell in kwargs['data']:
            self.item['data'] = cell
            self.insert()

    def insert_update(self, select, key="", value="", **kwargs):
        if self.con is None:
            self.con = Dao.get_con()
            self.cursor = self.con.cursor()
        sql = "SELECT %s FROM %s WHERE %s='%s'" % (select, kwargs['table'], key, value)
        try:
            rs = self.cursor.execute(sql).fetchall()
            if rs:
                data = str(rs[0][0]).split('\t')
                if str(kwargs['data'][select]) not in str(rs[0][0]):
                    data.append(sql_str(kwargs['data'][select]))
                s = kwargs.copy()
                s['data'][select] = '\t'.join(data)
                self.update(key=key, value=value, table=s['table'], data=s['data'])
            else:
                self.insert(table=kwargs['table'], data=kwargs['data'])
        except sqlite3.Error as e:
            logger.error("insert_update EROOR " + kwargs)
            logger.error(e)

    def select(self, key, data):
        if self.con is None:
            self.con = Dao.get_con()
            self.cursor = self.con.cursor()
        data = str(data)
        sql = "SELECT * FROM %s WHERE %s = ?" % (self.item['table'], key)
        try:
            rs = self.cursor.execute(sql, data)
            self.con.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(e)
        logger.info("select success")

    def exist(self, key, data):
        if self.con is None:
            self.con = Dao.get_con()
            self.cursor = self.con.cursor()
        data = str(data)
        sql = "SELECT * FROM %s WHERE %s = '%s'" % (self.item['table'], key, data)
        try:
            rs = self.cursor.execute(sql)
            print(self.cursor.rowcount)
            if rs.rowcount > 1:
                return True
        except sqlite3.Error as e:
            logger.error(e)
        return False

    def update(self, key="", value="", **kwargs):
        for cell in kwargs.keys():
            self.__setitem__(key=cell, value=kwargs[cell])
        if self.con is None:
            self.con = Dao.get_con()
            self.cursor = self.con.cursor()
        temp = []
        for cell in self.item['data'].keys():
            temp.append('"%s" = "%s"' % (cell, sql_str(self.item['data'][cell])))
        s = ' ,'.join(temp)
        sql = 'UPDATE %s SET %s WHERE "%s" = "%s"' % (self.item['table'], s, str(key), str(value))
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except sqlite3.Error as e:
            logger.error("Update ERROR:" + e)
            logger.error(self.item['data'])
        logger.info('Update sucessed')

    def to_string(self):
        # 将所有的数据转换为字符串类型
        for x in self.item['data']:
            self.item['data'][x] = str(self.item['data'][x])

    def close(self):
        # 先提交事务后关闭
        try:
            self.con.commit()
            self.cursor.close()
            self.con.close()
            logger.info("database was closed")
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    a = {"a": 320, "b": 2}
    dao = Dao(data=a, table="data")
    # dao.insert()
    # print(dao.cursor.execute(r"SELECT * FROM data WHERE a = 3").rowcount)
    # print(dao.exist('a', 3))
    # print(dao.select('a', 2))
    a = {'project_id': 11}
    dao.insert_update(select="project_id", key='id', value=1, table='backers', data=a)
