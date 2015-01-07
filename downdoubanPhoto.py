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



class urlopener: 
	def __init__(self,path):
        	self.path = path
 		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0'}
	        cookie = cookielib.CookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) 
 	
	def __enter__(self):
	    try: 
		request = urllib2.Request(self.path)
		request.add_header('User-Agent',self.headers['User-Agent'])
		request.add_header('Connection','keep-alive')
		response = self.opener.open(request)
		return response	
	    except urllib2.HTTPError:
		print "please try download again"
		sys.exit()
	
	def __exit__(self, exc_type, exc_value, exc_tb):
		self.opener.close()
		if exc_tb is None:
                	print '[Exit %s]: Exited without exception.' % self.path
            	else:
                	print '[Exit %s]: Exited with exception raised.' % self.path

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
		self.photorule = re.compile('''<h1>(.*)</h1>''')
		self.movierule = re.compile('''>(.*)<''')

	def multiThreadDown(self,url,count,allcount,path):
		time.sleep(random.uniform(1,1.7)+ random.uniform(0.5,1.2))
		if url.__len__()> 2 :
			urllib.urlretrieve(url,path+'/'+str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(count)+".jpg"))
			print '%s/%s'%(count+1,allcount)
			print url

	def getnextandimgurl(self,path):
		with urlopener(path) as response:	
			pageContent = response.read()
			soup = BeautifulSoup(pageContent)
			searchnextref = soup.select("#next_photo")
			nexturltmp = self.nextrule.search(str(searchnextref))
			
			self.nexturl = nexturltmp.group(1)
			searchdownurl = soup.find_all(class_='mainphoto')
			downurltmp = self.imgrule.search(str(searchdownurl))
			self.downurl = downurltmp.group(1)
	
	def getphotoinfo(self,path):
		with urlopener(path) as response:	   		
			pageContent = response.read()
			countresult = self.countrule.search(pageContent)
			self.count = int(countresult.group(1))
			self.allcount =int(countresult.group(2))
			soup = BeautifulSoup(pageContent)	
			photonamelement = soup.select(".info")
			photonametmp = self.photorule.search(str(photonamelement))
			
			if photonametmp is  None:
				photonamelement = soup.select("#content")
				photonametmp = self.photorule.search(str(photonamelement))
			if photonametmp is None:
				photonamelement = soup.select("#title-anchor")
				photonametmp = self.movierule.search(str(photonamelement))
			
			self.photoname = photonametmp.group(1)	
	
	def multiThreadstart(self):
		self.getphotoinfo(self.url)
		isexist = os.path.exists(self.photoname)
		
		if isexist:
			self.photoname = self.photoname + '1'
		os.mkdir(self.photoname)
		self.photoname = os.path.abspath('.')+'/'+ self.photoname 		
		self.getnextandimgurl(self.url)
		for i in  range(self.allcount):
			t1 = threading.Thread(target=self.multiThreadDown,args=(self.downurl,i,self.allcount,self.photoname))
			t1.start()
			time.sleep(random.uniform(0.5,1.2))
			self.getnextandimgurl(self.nexturl)
	
	def genThread(self):
		t=threading.Thread(target=multiThreadDown)
		t.start()	
	
	def start(self):
		self.getphotoinfo(self.url)
		isexist = os.path.exists(self.photoname)
		
		if isexist:
			self.photoname = self.photoname + '1'
		os.mkdir(self.photoname)
		self.photoname = os.path.abspath('.')+'/'+ self.photoname 	
		self.getnextandimgurl(self.url)
		while self.count<=self.allcount:
			 print self.downurl
			 urllib.urlretrieve(self.downurl,self.photoname+'/'+str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(self.count)+".jpg"))
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
		exit()


