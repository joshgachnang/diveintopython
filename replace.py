#!/usr/bin/python
# vim:expandtab:ts=4
import os
import sys
import re
#from bs4 import BeautifulStoneSoup, BeautifulSoup, Comment
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, Comment


reload(sys)
sys.setdefaultencoding("utf-8")

rootdir = '.'

def getFiles(directory, fileExtList):                                        
	fileList = []
	for subdir, dirs, files in os.walk(directory):
		fileList += [os.path.join(subdir, f) for f in files
			if os.path.splitext(f)[1] in fileExtList ]
	return fileList

def dumpSoup(file, soup):
	print "writing file %s" % file
	fd = open(file, 'w')
    fd.write(soup.renderContents())
	fd.close()	

for fn in getFiles(rootdir, '.html'):
	found = 0
	try:
		fd = open(fn, 'r')
		soup = BeautifulSoup(fd.read())
		fd.close()
	except IOError, e:
        print "io error code: %d msg: %s" % (e.returncode, e.message)

	for i in soup.findAll('a'):
		if i.has_key('href'):
			p = re.compile('http://www\.diveintopython\.net', re.IGNORECASE)
			#if i['href']=='http://www.diveintopython.net':
			m = p.match(i['href'])
			if m:
				#print "was: %s" % i['href']
				i['href']= (i['href'])[m.end():]
				#print "is: %s" % i['href']
				found += 1	
	if found : dumpSoup(fn, soup)
