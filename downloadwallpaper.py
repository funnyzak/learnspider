#-*-coding: utf-8 -*-

import urllib2
import re
import urllib
import os
import logging
import time
import sys

___author___ = "fangwei"

class downBing(object):
	"""
	download 'cn.bing.com' wallpaper
	"""
	def __init__(self,urlpath,filepath):
		self.urlpath = urlpath
		self.filepath = filepath
		self.rulepng = re.compile("(http://[^\{\;\,\<]*\.png)\w*?")
		self.rulejpg = re.compile("(http://[^\{\;\,\<]*\.jpg)\w*?")
		self.rulegif = re.compile("(http://[^\{\;\,\<]*\.gif)\w*?")
		self.count = 1
	def start(self)	:
		urlhandler = urllib2.urlopen(self.urlpath)
		pageContent = urlhandler.read()
		pageContent = pageContent.replace(r"\/","/")
		pattern= self.rulepng.findall(pageContent)
		print pattern.__len__()
		length = pattern.__len__()
		if length > 1:
			for imageurl in pattern:
				print imageurl
				self.count = self.count+1
				urllib.urlretrieve(imageurl,str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(self.count)+".png"))
		
		pattern = self.rulejpg.findall(pageContent)
		length = pattern.__len__()
		if length > 1:
			for imageurl in pattern:
				print imageurl
				self.count = self.count+1
				urllib.urlretrieve(imageurl,str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(self.count)+".jpg"))
		pattern = self.rulegif.findall(pageContent)
		length = pattern.__len__()
		if length > 1:
			for imageurl in pattern:
				print imageurl
				self.count = self.count+1
				urllib.urlretrieve(imageurl,str(time.strftime("%Y-%b-%d-%a-%H-%M-%S",time.localtime())+"-"+str(self.count)+".gif"))

if __name__ == '__main__':
	len = len(sys.argv)
	if len == 2:
		downbing = downBing(sys.argv[1],"os.getcwd()")
		logging.warning("DownLoading......starting......")
		downbing.start()
		print "we have download the image"
		exit()
#urlpage = "http://cn.bing.com"
#indexpage = urllib2.urlopen(urlpage)
#pagecontent =  indexpage.read()
#rule = "http\S*\.jpg"
#pattern = re.compile(rule)
#matchimg = pattern.search(pagecontent)
#imageurl = matchimg.group()
#urllib.urlretrieve(imageurl,'biing.jpg')
