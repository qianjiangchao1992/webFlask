import time

import pymysql
from configparser import ConfigParser
from queue import Queue
import threading


# 装饰器来计算时间时间
def time_calculate(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        end_time = time.time()
        print("**********{}程序计算完成，所花时间为{}秒***********".format(f.__name__, round(end_time - start_time, 2)))
        return res

    return wrapper


class MysqlConn:
    __v = None
    _instance_lock = threading.Lock()

    def __init__(self, name='BDY', max_conn=10):
        self.cf = ConfigParser()
        self.cf.read(r"C:\Users\Administrator\PycharmProjects\webFlask\flaskr\myapp\Connection\MYSQL.ini")
        self.host = self.cf.get(name, 'HOST')
        self.port = self.cf.getint(name, 'PORT')
        self.user = self.cf.get(name, 'USERNAME')
        self.password = self.cf.get(name, 'PASSWORD')
        self.database = self.cf.get(name, 'DATABASE')
        self.charset = self.cf.get(name, 'CHARSET')
        self.max_conn = max_conn
        self.pool = Queue(max_conn)
        for i in range(self.max_conn):
            try:
                conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                       password=self.password, database=self.database, charset=self.charset)
                conn.autocommit(True)
                self.pool.put(conn)
            except Exception as e:
                raise IOError(e)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """
        获取实例
        type: object
        """
        if cls.__v:
            return cls.__v
        else:
            with cls._instance_lock:
                cls.__v = cls(*args, **kwargs)
                return cls.__v

    @time_calculate
    def exec_sql(self, sql, operation=None) -> None or int:
        """
        执行 Delete,Update,Insert
        type: object
        """

        response = None
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            response = cursor.execute(sql, operation) if operation else cursor.execute(sql)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.pool.put(conn)
            return response

    @time_calculate
    def exec_sql_fetch(self, sql: str, operation=None) -> None or list:
        """
        执行Select,返回结果集

        type: object
        """
        data = None
        response = None
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            response = cursor.execute(sql, operation) if operation else cursor.execute(sql)
            data = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.pool.put(conn)
            return response, data

    @time_calculate
    def exec_sql_many(self, sql: str, operation=None) -> None or list:
        """
        执行批量查询Select
        type: object
        """
        response = None
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            response = cursor.executemany(sql, operation) if operation else cursor.executemany(sql)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.pool.put(conn)
            return response
