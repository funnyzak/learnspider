#-*-coding:utf-8 -*-

___author___ = "fangwei"

import urllib2
import re
import urllib
import os
import time
import sys
import cookielib
from bs4 import BeautifulSoup

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
	        cookie = cookielib.CookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) 
	def getnextandimgurl(self,path):	
		response = self.opener.open(path)
		pageContent = response.read()
		countresult = self.countrule.search(pageContent)
		self.count = countresult.group(1)
		self.allcount = countresult.group(2)
		soup = BeautifulSoup(pageContent)
		searchnextref = soup.select("#next_photo")
		nexturltmp = self.nextrule.search(str(searchnextref))
		self.nexturl = nexturltmp.group(1)
		searchdownurl = soup.find_all(class_='mainphoto')
		downurltmp = self.imgrule.search(str(searchdownurl))
		self.downurl = downurltmp.group(1)
		self.opener.close()
	def start(self):
		self.getnextandimgurl(self.url)	
		while self.count != self.allcount:
			 print self.downurl
			 urllib.urlretrieve(self.downurl,str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(self.count)+".jpg"))
			 self.getnextandimgurl(self.nexturl) #self.count = self.count+1


if __name__ == '__main__':
	len = len(sys.argv)
	if len >= 2:
		downdouban = DownloadDouBan(sys.argv[1],"os.getcwd()",{'URL':'URL'})
		downdouban.start()
		print "we have download the image"
		exit()


