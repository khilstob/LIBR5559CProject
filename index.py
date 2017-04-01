from goodreads import client
import xml
import requests
import random
import time
from os import listdir
import sys
from bs4 import BeautifulSoup

def getAuthors ():
  for i in range(0, 225):
    randomAuthorId = str(random.randrange(1000, 7253283))
    authorFile = open('./authors/' + randomAuthorId + '.xml', 'w')
    result = requests.get('https://www.goodreads.com/author/show/' + randomAuthorId + '?format=xml&key=sySok63UyYyWi2Wof1HocA')
    try:
      authorFile.write(result.text)
    except UnicodeEncodeError:
      print 'One item skipped: UnicodeDecodeError'
    print "Going to sleeep for 2 seconds."
    time.sleep(2)
    print "Awake!"
    print randomAuthorId + " saved"
    authorFile.close()

def getBooks():
  authorFiles = listdir('./authors/')
  for file in authorFiles:
    soup = BeautifulSoup(open('./authors/' + file), 'xml')
    genders = soup.findAll('gender')
    if genders:
      print genders[0]

if sys.argv[1] == "getAuthors":
  getAuthors()

if sys.argv[1] == "getBooks":
  getBooks()
