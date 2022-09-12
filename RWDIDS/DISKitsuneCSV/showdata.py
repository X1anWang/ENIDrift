import psutil
import os
import time

def showinfo():
    
    info = psutil.virtual_memory()
    print(u'当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )
    print(u'电脑总内存：%.4f GB' % (info.total / 1024 / 1024 / 1024) )
    print(u'当前使用的总内存占比：',info.percent)
    print(u'cpu个数：',psutil.cpu_count())
    
    t = time.time()
    
    print('the time now:'+str(t))