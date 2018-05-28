import pymysql
import contextlib


def test():
    pass

@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='', db='commodity',charset='utf8'):
  conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
  cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
  try:
    yield cursor
  finally:
    conn.commit()
    cursor.close()
    conn.close()
