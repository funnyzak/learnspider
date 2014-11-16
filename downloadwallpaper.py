#-*-coding: utf-8 -*-
import urllib2
import re
import urllib

urlpage = "http://cn.bing.com"
indexpage = urllib2.urlopen(urlpage)
pagecontent =  indexpage.read()
rule = "http\S*\.jpg"
pattern = re.compile(rule)
matchimg = pattern.search(pagecontent)
imageurl = matchimg.group()
urllib.urlretrieve(imageurl,'bing.jpg')
