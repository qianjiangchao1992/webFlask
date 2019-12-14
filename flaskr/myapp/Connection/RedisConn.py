import redis
from configparser import ConfigParser


class RedisConn:
    __v = None

    def __init__(self, name='REDIS'):
        self.cf = ConfigParser()
        self.cf.read(r"C:\Users\Administrator\PycharmProjects\webFlask\flaskr\myapp\Connection\MYSQL.ini")
        self.host = self.cf.get(name, 'HOST')
        self.port = self.cf.getint(name, 'PORT')
        self.password = self.cf.get(name, 'PASSWORD')
        self.db = self.cf.getint(name, 'DB')
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.__v:
            return cls.__v
        else:
            cls.__v = cls(*args, **kwargs)
            return cls.__v

    def get_conn(self):
        r = redis.Redis(connection_pool=self.pool)
        return r
