# python多线程与多进程

- 什么是进程？

计算机程序只不过是磁盘中可执行的二进制（或其他类型）数据。它们只有在被读取
到内存中、被操作系统调用的时候才开始它们的生命周期。进程是程序的一次执行，每个
进程都有自己的地址空间、内存、数据栈，以及其他记录其运行轨迹的辅助数据。操作系
统管理在其上面运行的所有进程，并为这些进程公平地分配时间。

- 什么是线程？

线程（有时被称为轻量级进程）与进程有些相似，不同的是，所有的线程都运行在同
一个进程中，共享相同的运行环境。我们可以想象成是在主进程或“主线程”中并行运行
的“迷你进程”。

## 单线程的时代

在单线程的时代，当处理器需要处理多个任务时，必须对这些任务安排执行顺序，并按照
这个顺序来执行任务。假如我们创建了两个任务；听音乐（music）和看电影（movie），
在单线程中，我们只能按先后顺序来执行这两个任务。


```python
from time import sleep, ctime

def music():
    print("%s" %ctime())
    sleep(2)

def movie():
    print("%s" % ctime())
    sleep(5)

if __name__ == "__main__":
    music()
    movie()
    print("all end;", ctime())
```


这里我们修改一下，music和movie作为播放器，在用户使用时，可以根据用户的需求来播放任意的歌曲
和影片


    from time import sleep, ctime

    def music(func, loop):
        for i in range(loop):
            print("listen %s %s" % (func, ctime()))
            sleep(2)

    def movie(func, loop):
        for i in range(loop):
            print("look %s %s" % (func, ctime()))
            sleep(5)

    if __name__ == "__main__":
        music('122', 2)
        movie('movie', 2)
        print('all end:', ctime())



## 多线程技术

python通过两个标志库thread和threading提供对线程的支持。thread提供了低级别的、
原始的线程以及一个简单的锁。threading基于Java的线程模型设计。锁（Lock）和条件变量
（Condition）在Java中是对象的基本行为（每个对象都自带了锁和条件变量），而在Python
中则是独立的对象。

### 10.2.1 threading 模块

我们应该避免使用thread模块，原因是它不支持守护线程。当主线程退出时，所有的子线程不管
它们是否还在工作，都会被强行退出。有时我们不希望发生这种行为，这时就引入了守护线程的概念。
threading模块支持守护线程，所以，我们直接使用threading来改进。


    from time import sleep, ctime
    import threading
    
    def music(func, loop):
        for i in range(loop):
            print("listen %s %s" % (func, ctime()))
            sleep(2)
    
    def movie(func, loop):
        for i in range(loop):
            print("look %s %s" % (func, ctime()))
            sleep(5)
            
    # 创建线程数组
    threads = []
    
    # 创建线程t1，并添加到线程数组
    t1 = threading.Thread(target=music, args=('爱情买卖', 2))
    threads.append(t1)
    
    # 创建线程t2，并添加到线程数组
    t2 = threading.Thread(target=movie, args=('阿凡达', 2))
    threads.append(t2)
    
    if __name__ == '__main__':
        # 启动线程
        for t in threads:
            t.start()
        # 守护线程
        for t in threads:
            t.join()
        print('all end: %s' % ctime())
        
        
通过for循环遍历threads数组中所装载的线程；start()开始线程活动，join()等待线程
终止。如果不使用join()方法对每个线程做等待终止，那么在线程运行的过程中可能会去执行
最后的打印"all end:...".


### 优化线程的创建

从上面例子中发现线程的创建是颇为麻烦的，每创建一个线程都需要创建一个t(t1、t2、...),
当创建的线程较多时这样极其不方便。下面对例子进行更改。

    from time import sleep, ctime
    import threading
    
    def super_player(file_, time):
        for i in range(2)
        # 这里的for循环用于两次播放，来线程并行运行的时间差别
            print('Start playing: %s %s' %(file_, ctime()))
            sleep(time)
    
    lists={'歌曲1':3,'视频2':3,'歌曲3':4'}   
    threads = []
    files = range(len(lists))
    
    # 创建线程
    for file_, time in lists.items():
        t = threading.Thread(target=super_player, args=(file_, time))
        threads.append(t)
        
    if __name__ == '__main__':
        # 启动线程
        for t in files:
            threads[t].start()
        for t in files:
            threads[t].join()
        print('end: %s' % ctime())                    


我们对播放器进行增强。首先，创建一个super_player()函数，这个函数可以接收播放文件和播放时长，
可以播放任何文件。

然后，我们创建了一个lists字典用于存放播放文件名和时长，通过for循环读取字段，
并调用super_player()函数创建字典，接着将创建的字典都追加到threads数组中。

最后，通过循环启动线程组threads中的线程，运行结果如下。 


### 10.2.3 创建线程类

除直接使用Python所提供的线程类外，我们还可以根据需求自定义自己的线程类

    import threading
    from time import sleep, ctime
    
    # 创建线程类
    class MyThread(threading.Thread):
        
        def __init__(self, func, args, name=''):
            threading.Thread.__init__(self)
            self.func = func
            self.args = args
            self.name = name
        
        def run(self):
            self.func(*self.args)
            
    def super_play(file_, time):
        for i in range(2):
            print('Start playing: %s %s' % (file_, ctime()))
            sleep(time)
    
    lists = {'歌曲':3, '视频':4}
    
    threads = []
    files = range(len(lists))
    
    for file_, time in lists.items():
        t = MyThread(super_play, (file_, time), super_play.__name__)
        threads.append(t)
        
        
    if __name__ == '__main__':
        for i in files:
            threads[i].start()
        for i in files:
            threads[i].join()
        print('end:%s' % ctime())
        
> MyThread(threading.Thread)

创建MyThread类，用于继承threading.Thread类。

__init__()类的初始化方法对func、args、name等参数进行初始化。

在python2中，apply(func[,args[,kwargs]])函数的作用是当函数参数已经存在于一个元组或
字典中时，apply()间接地调用函数。args是一个包含将要提供给函数的按位置传递的参数的元组。
如果省略了args，则任何参数都不会被传递，kwargs是一个包含关键字参数的字典。

python3中已经不再支持apply()函数，所以将
    
    apply(self.func, self.args)
    
修改为

    self.func(*self.args)
    
## 10.3 多进程技术

### 10.3.1 multiprocessing模块

多进程multiprocessing模块的使用与多线程threading模块的用法类似。multiprocessing
提供了本地和远程的并发性，有效地通过全局解释锁(Global Interceptor Lock, GIL)来使
用进程（而不是线程）。由于GIL的存在，在CPU密集型的程序当中，使用多线程并不能有效地利用
多核CPU的优势，因为一个解释器在同一时刻只会有一个线程在执行。所以，multiprocessing模块
可以充分利用硬件的多处理器来进行工作。它支持UNIX和Windows系统上的运行。

修改多线程的例子，将threading模块中的Thread方法替代为multiprocessing模块的Process就
实现了多进程。

    from time import sleep, ctime
    import multiprocessing
    
    def super_player(file_, time):
        for i in range(2):
            print("start playing: %s %s" %(file_, ctime())
            sleep(time)
            
    lists = {...}
    
    processes = []
    files = range(len(lists))            
                                            
    for file_, time in lists.items():
        t = multiprocessing.Process(target=super_player, args=(file_, time))
        threads.append(t)
        
    if __name__ == '__main__':
        # 启动进程
        for t in files:
            processes[t].start()
        for t in files:                       
            processes[t].join()
            
        print("end:%s" % ctime())
        
从上面的实例可以看到，多进程的用法几乎与多线程一样。

我们利用Process对象来创建一个进程。Process对象和Thread对象的用法相同，也有
start()、run()、join()等方法。
                                                                                                        
    multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})

target表示调用对象，args表示调用对象的位置参数元组，kwargs表示调用对象的字典，
name为别名，Group实际上不使用。

### 10.3.2 Pipe和Queue
multiprocessing提供了threading包中没有的IPC（进程间通信），效率上更高。应优先
考虑Pipe和Queue，避免使用Lock/Event/Semaphore/Condition等同步方式（因为它们占
据的不是用户进程的资源）。

multiprocessing包中有Pipe类和Queue类来分别支持这两种IPC机制。Pipe和Queue
可以用来传送常见的对象。

（一）Pip可以是单向（half-duplex），也可以是双向（duplex）。我们通过mutiprocessing.Pipe
(duplex=False)创建单向管道(默认为双向)。一个进程从pipe一端输入对象，然后被pipe
另一端的进程接收。单向管道只允许管道一端的进程输入，而双向管理则允许从两端输入。

pipe.py

    import multiprocessing
    
    def proc1(pipe):
        pipe.send('hello')
        print('proc1 rec:', pipe.recv())
        
    def proc2(pipe):
        print('proc2 rec:', pipe.recv())
        pipe.send('hello, too')

    if __name__ == '__main__':
        multiprocessing.freeze_support()
        pipe = multiprocessing.Pipe()
        
        p1 = multiprocessing.Process(target=proc1, args=(pipe[0],))
        p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
        
        p1.start()
        p2.start()
        p1.join()
        p2.join()


这里的pipe是双向的。pipe对象建立的时候，返回一个含有两个元素的表，每个元素
代表pipe的一端（Connection对象）。我们对pipe的某一端调用send()方法来传送对象，
在另一端使用recv()来接收。

（二）Queue类与Pipe相类似，都是先进先出结构。但Queue类允许多个进程放入，多个
进程从队列取出对象。Queue类使用Queue(maxsize)创建，maxsize表示队列中可以存放
对象的最大数量。

queue.py

    import multiprocessing
    import os, time
    
    def inputQ(queue):
        info = str(os.getpid()) + '(put):' + str(time.time())
        queue.put(info)
    
    def outputQ(queue, lock):
        info = queue.get()
        lock.acquire()
        print((str(os.getpid()) + '(get):' + info))
        lock.release()
        
    if __name__ == '__main__':
        record1 = []
        record2 = []
        lock = multiprocessing.Lock() # 加锁，为防止散乱的打印
        queue = multiprocessing.Queue(3)
        
        for i in range(10):
            process = multiprocessing.Process(target=inputQ, args=(queue,))
            process.start()
            record1.append(process)
            
        for i in range(10):
            process = multiprocessing.Process(target=outputQ, args=(queue,lock))
            process.start()
            record2.append(process)
    
        for p in record1:
            p.join()
            
        queue.close()
        
        for p in record2:
            p.join()                                    
                        

        
        
                                                                                                                           