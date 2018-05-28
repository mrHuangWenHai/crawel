# -*- coding: utf-8 -*-
import multiprocessing
import config.baseConfig
import dataprocess
import mysqlhandler
import time

def run(type, queue):
    print "aaaaaaaaaaaa"
    data = dataprocess.DataProcess(type, queue)
    data.run();

def start():

    manager = multiprocessing.Manager()
    queue = manager.Queue(config.baseConfig.QUEUE_SIZE)

    process_num = len(config.baseConfig.send_url)
    pool = multiprocessing.Pool(process_num+1)

    # pool.apply_async(run, args=(1, queue))

    for i in range(process_num):
       pool.apply_async(run, args=(i, queue))
    pool.close()

    with mysqlhandler.mysql() as cursor:
        while True:
            product = queue.get(timeout=180)
            cursor.execute("insert into product (image,price,title,deal,shop,location, platform,url) "
                           "values (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (product["image"],product["price"],product["title"],product["deal"],
                            product["shop"],product["location"],
                            product["platform"],product["url"]))

    print 'manger shutdown'

    manager.shutdown()
    pool.terminate()

if __name__ == '__main__':
    start()
    # with mysqlhandler.mysql() as cursor:
    #     cursor.execute("select * from product")
    #     row = cursor.fetchone()
    #     row1 = cursor.fetchone()
    #     print row
    #     print row1













