#!/usr/bin/env python
#-*-coding:utf-8 -*-
import socket
import threading
import os
import sys
import re
import urllib
import urllib2
import cookielib
import time
import random
import logging
import logging.handlers

LOG_FILE = 'tst.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) 
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   
handler.setFormatter(formatter)      

logger = logging.getLogger('tst')    
logger.addHandler(handler)          
logger.setLevel(logging.DEBUG)

path = []
gk_mutex = threading.Condition()
gk_mutex_img = threading.Condition()

gk_content_url = []
gk_img_url = []
bfinish = 0

fetchImgUrl_re = re.compile('''<img src="([\w\/\.\?\-\:]*)" alt''')
contentUrl_re = re.compile('''<a href="([\w\/\.\:]*)" title\=''')
nextIndex_re = re.compile('''<a href="([\/\w\?\=_\.:]*)" >后页''')

startpage = ""
class fetchImgUrlThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def multiThreadDown(self,url,path):
		time.sleep(random.uniform(1,1.7)+ random.uniform(0.5,1.2))
		strfile=path+'/'+time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(random.uniform(1,100))+".jpg"
		try:
			urllib.urlretrieve(url,strfile)
			print url
			if os.path.exists(strfile) and os.path.getsize(strfile) < 1024*25:
				os.remove(strfile) 
		except Exception, e:
			print "---------error-----------"
	def run(self):
		global gk_mutex
		global gk_content_url
		global gk_img_url
		global fetchImgUrl_re
		print "--------fetch aquire gk_mutex------"
		while True:
			gk_mutex.acquire()
			res = []
			global bfinish
			if bfinish:
				gk_mutex.release()
				break
			print "-------len:%d------"%len(gk_content_url)
			if len(gk_content_url) == 0:
				print "---------------%d----------------------"%bfinish
				print "--------I'm waiting-----------"
				gk_mutex.wait()
				if bfinish:
					gk_mutex.release()
					break
			else:
				self.url = gk_content_url.pop()
				with urlopener(self.url) as response:
					if response is not None:
						page = response.read()
						res = fetchImgUrl_re.findall(page)
				gk_mutex.release()
				for img in res:
					downThread = threading.Thread(target=self.multiThreadDown,args=(img,os.getcwd()))
					downThread.start()
				if bfinish:
					break

class ImgDownThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def shedule(self,a,b,c):
		per = 100.0*a*b/c
		if per >100:
			per=100
		print "-----%.2f%%"%per
	def run(self):
		global gk_img_url
		global gk_mutex_img
		global path
		print "------downImg gk_mutex_img  acquire------"
		while True:
			gk_mutex_img.acquire()
			if len(gk_img_url) == 0:
				print "------downImg gk_mutex_img wait------"
				gk_mutex_img.wait()
			else:
				for url in gk_img_url:
					url = gk_img_url.pop()
					print url
					strfile = path+'/'+str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+str(random.uniform(1,2.7))+".jpg")
					try:
						socket.setdefaulttimeout(30)
						urllib.urlretrieve(url,strfile,self.shedule)
					
					except UnicodeDecodeError as e:  
    						print('-----UnicodeDecodeErrorurl:',url)  
					except Exception, e:  
    						print("-----socket timout:",url) 
					time.sleep(random.uniform(1,3.2))
					if os.path.exists(strfile) and os.path.getsize(strfile) < 1024*25:
						os.remove(strfile)
					print "-----------------list:%d------------"%len(gk_img_url)
				gk_mutex_img.notifyAll()
				print "----notifyall------"
			gk_mutex_img.release()

class urlopener:
	"""
	when open the url use like this with urlopener(path) as response
	"""
	def __init__(self,path):
		self.path = path
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0'}
	def __enter__(self):
		cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		request = urllib2.Request(self.path)
		request.add_header('User-Agent',self.headers['User-Agent'])
		request.add_header('Connection','keep-alive')
		response = None
		try:
			response = self.opener.open(request)
		except Exception,e:
			print "-----openerror-----"
			response = None
		finally:
			return response
	def __exit__(self,exc_type, exc_value, exc_tb):
		self.opener.close()
		if exc_tb is None:
			print "------success------"
		else:
			print "------error------"

class guokefetch:
	def __init__(self,url,pathdown):
		self.url = url
		global path
		if len(path) > 0:
			path = pathdown
		else:
			path = os.getcwd()
	def start(self):
		global gk_mutex
		global gk_content_url
		global bfinish
		fetchThread = fetchImgUrlThread()
		self.preurl = ""
		trycount=0
		fetchThread.start()
		while True:
			print self.url
			time.sleep(random.uniform(1,1.7)+ random.uniform(0.5,1.2))
			with urlopener(self.url) as response:
				if response is not None:
					page = response.read()
					res = contentUrl_re.findall(page)
					gk_mutex.acquire()
					for content in res:
						gk_content_url.append(content)
					global logger
					logger.info(self.url)
					nextImg = nextIndex_re.findall(page)
					if len(nextImg)==0:
						bfinish=1
						gk_mutex.notifyAll()
						gk_mutex.release()
						break
					else:
						print self.url
						self.url = nextImg[0]
					gk_mutex.notifyAll()
					gk_mutex.release()
		fetchThread.join()

if __name__ == '__main__':
	len = len(sys.argv)
	if len >= 2:
		gk_down = guokefetch(sys.argv[1],"")
		gk_down.start()
