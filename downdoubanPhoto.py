#-*-coding:utf-8 -*-

___author___ = "fangwei"
import threading
import time
import random
import urllib2
import re
import urllib
import os
import time
import sys
import cookielib
from bs4 import BeautifulSoup

def multiThreadDown(url,count):
	if url.__len__()> 2 :
		urllib.urlretrieve(url,str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(count)+".jpg"))
		print url

class DownloadDouBan(object):
	"""
	download the photo from the douban.com photo
	"""
	def __init__(self,starturl,filepath,data):
		self.url = starturl
		self.filepath = filepath
		self.nextrule = re.compile('''href=\"(\S*)\"''')
		self.imgrule = re.compile('''(http://[^\{\;\,\<\"]*\.jpg)\w*?''')
		self.countrule = re.compile('''第(\d*)张.*共(\d*)张''')
		self.allcount = 0
		self.count = 0
		self.downurl = ''
		self.nexturl = ''
		self.multiThreadurl = ''
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0'}
	        cookie = cookielib.CookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) 
		self.downcount = 0
	def getnextandimgurl(self,path):	
		request = urllib2.Request(path)
		request.add_header('User-Agent',self.headers['User-Agent'])
		request.add_header('Connection','keep-alive')
		response = self.opener.open(request)
		pageContent = response.read()
		countresult = self.countrule.search(pageContent)
		self.count = int(countresult.group(1))
		self.allcount =int(countresult.group(2))
		soup = BeautifulSoup(pageContent)
		searchnextref = soup.select("#next_photo")
		nexturltmp = self.nextrule.search(str(searchnextref))
		self.nexturl = nexturltmp.group(1)
		searchdownurl = soup.find_all(class_='mainphoto')
		downurltmp = self.imgrule.search(str(searchdownurl))
		self.downurl = downurltmp.group(1)
		self.opener.close()
	def multiThreadstart(self):
		self.getnextandimgurl(self.url)
		for i in  range(self.allcount):
			t1 = threading.Thread(target=multiThreadDown,args=(self.downurl,i))
			t1.start()
			self.getnextandimgurl(self.nexturl)
	def genThread(self):
		t=threading.Thread(target=multiThreadDown)
		t.start()	
	def start(self):
		self.getnextandimgurl(self.url)
		while self.count<=self.allcount:
			 print self.downurl
			 urllib.urlretrieve(self.downurl,str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(self.count)+".jpg"))
			 self.getnextandimgurl(self.nexturl)
			 print "%s/%s" %(self.count,self.allcount)
			 self.downcount = self.downcount+1
			 if self.downcount == int(self.allcount):
				break
			 time.sleep(random.uniform(1,2.7))

if __name__ == '__main__':
	len = len(sys.argv)
	if len >= 2:
		downdouban = DownloadDouBan(sys.argv[1],"os.getcwd()",{'URL':'URL'})
		if len==3 and sys.argv[2]=='m':
				downdouban.multiThreadstart()
		else:
			downdouban.start()
				
		print "we have download the image"
		exit()


