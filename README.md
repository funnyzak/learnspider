learnspider
===========
+  下载豆瓣相册的小爬虫，用到了beautifulsoup ，使用的时候需要安装python版本的beautiful,使用方法是“python downdoubanPhoto.py 相册首页地址” 例如 “python  downdoubanPhoto.py  http://www.douban.com/online/11989552/photo/2212821906/?sortby=time”

+  后来又加入了爬取果壳网的小爬虫，使用python自带的库，主要是用到了正则表达式代替了beautifulsoup,里边用到了多线程的同步下载，首选是一个线程解析地址，解析完一页的地址后，通知另一个线程工作，然后再继续解析，类似于生产者和消费者，使用的主要方法是，打开guoke.py，然后修改 if __name__ == '__main__':
	gk_down = guokefetch("http://www.guokr.com/group/48/","")
	gk_down.start()
	上面的url是果壳小组的一个地址，可以随便更改，它会下载回帖中的比较大的图片
