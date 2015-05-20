learnspider
===========
1. 下载豆瓣相册的小爬虫，用到了beautifulsoup ，使用的时候需要安装python版本的beautiful,使用方法是“python downdoubanPhoto.py 相册首页地址” 例如 “python  downdoubanPhoto.py  http://www.douban.com/online/11989552/photo/2212821906/?sortby=time”

2. 后来又加入了爬取果壳网的小爬虫，使用python自带的库，主要是用到了正则表达式代替了beautifulsoup,里边用到了多线程的同步下载，首选是一个线程解析地址，解析完一页的地址后，通知另一个线程工作，然后再继续解析，类似于生产者和消费者，使用的主要方法是，打开guoke.py，然后修改 if __name__ == '__main__':
	gk_down = guokefetch("http://www.guokr.com/group/48/","")
	gk_down.start()
	上面的url是果壳小组的一个地址，可以随便更改，它会下载回帖中的比较大的图片
learn python spider

1,the downloadwallpaper.py can download three format picture（eg, .png,.jpg,.gif） which includeed in html page
you can start the program like "python downloadwallpaper.py http://www.baidu.com "

2,the downdoubanPhoto.py can download the douban.com site photo ,you must give the first picture index ,you can
start the program like "python  downdoubanPhoto.py  http://www.douban.com/online/11989552/photo/2212821906/?sortby=time "
3,if you want to download the image with multiprocess you can start the program like "python  downdoubanPhoto.py  http://www.douban.com/online/11989552/photo/2212821906/?sortby=time m "  add a "m" in the url
