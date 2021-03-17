# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: threading_demo.py
Author: gaoyw
Create Date: 2021/3/12
-------------------------------------------------
"""
import threading
from time import ctime, sleep


def music(func, results):
    for i in range(2):
        print("I was listening to %s. %s" % (func, ctime()))
        sleep(1)
        results.append("music" + str(i))


def move(func, results):
    for i in range(2):
        print("I was at the %s! %s" % (func, ctime()))
        sleep(5)
        results.append("move" + str(i))


threads = []
results = []
t1 = threading.Thread(target=music, args=(u'爱情买卖', results))
threads.append(t1)
t2 = threading.Thread(target=move, args=(u'阿凡达', results))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
    print(results)
    print("all over %s" % ctime())
