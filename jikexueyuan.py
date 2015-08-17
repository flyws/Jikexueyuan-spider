#coding=utf-8

from bs4 import BeautifulSoup
import re
import urllib2
import time
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class See_Course_History(object):
	"""docstring for See_Course_History
       this application is designed to see all of the course
       names and dates added to the "www.jikexueyuan.com"
	"""
	def __init__(self, website='http://www.jikexueyuan.com/course/web/', pageNum=11):
		super(See_Course_History, self).__init__()
		self.website = website
		self.pageNum = pageNum

	def Htmlparser(self):
		print 'I am retrieving the .html files of all pages under this category'
		global emptybox
		emptybox = []
		for i in xrange(1, self.pageNum+1):
			url = urllib2.urlopen(self.website+'?pageNum=' + str(i))
			soup = BeautifulSoup(url)
			lesson_list = soup.find_all(class_ = 'lesson-info-h2')
			emptybox += lesson_list

	def get_page_urls(self):
		global urlbox
		self.Htmlparser()
		print 'I am working hard to get the urls on the .html files'
		urlbox_string = []
		for i in emptybox:
			i = str(i)
			urlbox_string.append(i)
		urlbox_string = ','.join(urlbox_string)
		# print urlbox_string
		urlbox = re.findall(r'href=\"(.*?)\"', urlbox_string)
		
	def write_urls(self):
		"""
			write urls to a txt file. This is for saving the time
			when we use get_course_info method later, without having
			to connect to websites to get urls again.
		"""
		self.get_page_urls()
		file = open('../desktop/page_urls.txt','w')
		for i in urlbox:
			file.write(i+'\n')
		file.close()
		print 'I have successfully finished writing the document. Now you can check it.'
	
	def get_course_info(self):
		print 'I am scanning and connecting all the urls in the document...It might take some time.'
		file = open('../desktop/page_urls.txt','r')
		b = file.read()
		b = b.rstrip()
		urlbox2 = str(b).split('\n')
		d = {}
		for i in urlbox2:
			url = urllib2.urlopen(i)
			soup = BeautifulSoup(url)
			info = soup.find_all(class_='bc-box')
			for a in info:
				d[a.h2.string] = a.div.span.next.next.string
		# print json.dumps(d,ensure_ascii=False,encoding='UTF-8')
		d = sorted(d.iteritems(), key=lambda d:d[1], reverse = False )
		# output = json.dumps(d,ensure_ascii=False,encoding='UTF-8')

		file = open('../desktop/courses_info.txt','w')
		for i in d:
			file.write(i[0] + '  ' + i[1] + '\n')
		file.close()
		print 'All work is done. You can see the courses_info.txt right now'

if __name__ == '__main__':
	a1 = See_Course_History()
	filename = r'../desktop/page_urls.txt'
	if os.path.exists(filename):
		pass
	else:
		a1.write_urls()
	time.sleep(3)
	a1.get_course_info()
