#-*-coding: utf-8 -*-

import urllib2
import re
import urllib
import os
import logging

___author___ = "fangwei"

class downBing(object):
	"""
	download 'cn.bing.com' wallpaper
	"""
	def __init__(self,urlpath,filepath):
		self.urlpath = urlpath
		self.filepath = filepath
		self.rule  =re.compile("http\S*\.jpg")
	def start(self)	:
		urlhandler = urllib2.urlopen(self.urlpath)
		pageContent = urlhandler.read()
		pattern= self.rule.search(pageContent)
		imageurl = pattern.group()
		urllib.urlretrieve(imageurl,'bing.jpg')

if __name__ == '__main__':

	downbing = downBing("http://cn.bing.com","os.getcwd()")
	logging.warning("DownLoading......starting......")
	downbing.start()
	print "we have download the image"
		
#rlpage = "http://cn.bing.com"
#ndexpage = urllib2.urlopen(urlpage)
#pagecontent =  indexpage.read()
#rule = "http\S*\.jpg"
#pattern = re.compile(rule)
#matchimg = pattern.search(pagecontent)
#imageurl = matchimg.group()
#urllib.urlretrieve(imageurl,'bing.jpg')
