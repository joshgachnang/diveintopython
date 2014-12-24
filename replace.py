#!/usr/bin/python
# vim:expandtab:ts=4
import os
import sys
import re
import argparse
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, Comment

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

# MAIN PROGRAM STARTS HERE
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--extension", action="append", default=['.html'],
                    help="limit processing only to specified extensions")
parser.add_argument("-d", "--directory", default=".",
                    help="target data directory")
parser.add_argument("-f", "--replacefixed", nargs=2, required=True,
					help="literal strings, first is replaced by second")

args = parser.parse_args()

reload(sys)
sys.setdefaultencoding("utf-8")

if args.replacefixed:
	literalreplace  = args.replacefixed[0]
	literalreplaceby = args.replacefixed[1]
	print "%s will be replaced by %s" % (literalreplace, literalreplaceby)

for fn in getFiles(args.directory, args.extension):
	found = 0
	try:
		fd = open(fn, 'r')
		soup = BeautifulSoup(fd.read())
		fd.close()
	except IOError, e:
        print "io error code: %d msg: %s" % (e.returncode, e.message)

	for i in soup.findAll('a'):
		if i.has_key('href'):
			#p = re.compile('http://www\.diveintopython\.net', re.IGNORECASE)
			#m = p.match(i['href'])
			if i['href']==literalreplace:
				print "was: %s" % i['href']
				i['href']=literalreplaceby
				print "is: %s" % i['href']
			#if m:
				#print "was: %s" % i['href']
				#i['href']= (i['href'])[m.end():]
				#print "is: %s" % i['href']
				found += 1	
	if found : dumpSoup(fn, soup)
