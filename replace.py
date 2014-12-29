#!/usr/bin/python
# vim:expandtab:ts=4
import os
import sys
import re
import argparse
from BeautifulSoup import BeautifulSoup

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

def initParser():
	p = argparse.ArgumentParser()
	p.add_argument("-e", "--extension", action="append", default=['.html'],
                    help="limit processing only to specified extensions")
	p.add_argument("-d", "--directory", default=".",
                    help="target data directory")
	p.add_argument("--dry", action="store_true", help="dry run")

	grpexcl = p.add_mutually_exclusive_group(required=True)
	grpexcl.add_argument("-f", "--replacefixed", nargs=2, required=False,
					metavar="pattern",
					help="literal strings, first is replaced by second")
	grpexcl.add_argument("-r", "--replaceregexp", nargs=2, required=False,
					metavar="pattern",
					help="regexp strings, first replaced by second")

	return(p.parse_args())


# MAIN PROGRAM STARTS HERE
args = initParser()

reload(sys)
sys.setdefaultencoding("utf-8")

if args.replaceregexp:
	regptrn = args.replaceregexp[0]
	reginto = args.replaceregexp[1]
	p = re.compile(regptrn, re.IGNORECASE)

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
			if args.replacefixed:
				literalreplace  = args.replacefixed[0]
				literalreplaceby = args.replacefixed[1]

				if i['href']==literalreplace:
					print "@ %s" % fn
					print "was: %s" % i['href']
					i['href']=literalreplaceby
					print "is: %s" % i['href']
					found +=1

			if args.replaceregexp:
                m = p.match(i['href'])
				if m: 
					print "@ %s" % fn
					print "was: %s" % i['href']
					i['href']= reginto + (i['href'])[m.end():]
					print "is: %s" % i['href']
					found += 1	

	if found and not args.dry: dumpSoup(fn, soup)
