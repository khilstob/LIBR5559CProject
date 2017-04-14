from htmllaundry import strip_markup
from goodreads import client
import xml
import requests
import random
import time
import os
import sys
import calendar
import datetime
from bs4 import BeautifulSoup
from pprint import pprint
import json

gc = client.GoodreadsClient('sySok63UyYyWi2Wof1HocA', 'CyuRTp1MAMtnmF839U6653Uv8yn1Y0SWh0EF5d8ACNQ')

unixTimeCode = calendar.timegm(datetime.datetime.now().timetuple())

def getAuthors ():
  filesSaved = 0
  while filesSaved < 221:
    randomAuthorId = str(random.randrange(1000, 7253283))
    result = requests.get('https://www.goodreads.com/author/show/' + randomAuthorId + '?format=xml&key=sySok63UyYyWi2Wof1HocA')
    if len(result.text) > 33:
      soup = BeautifulSoup(result.text, 'xml')
      gender = soup.findAll('gender')[0].contents
      if len(gender) == 1:
        authorFileName = './authors/' + randomAuthorId + '.xml'
        try:
          authorFile = open(authorFileName, 'w')
          authorFile.write(result.text)
          authorFile.close()
          filesSaved = filesSaved + 1
          print "\nFiles saved: " + str(filesSaved) + ", latest author: " + randomAuthorId
        except UnicodeEncodeError:
          print '\nOne item skipped: UnicodeDecodeError'
          os.remove(authorFileName)
      time.sleep(0.25)
      print('.')

def getBooks():
  authors = []
  authorFiles = os.listdir('./authors/')
  for index, file in enumerate(authorFiles):
    authorFile = open('./authors/' + file, 'r')
    soup = BeautifulSoup(authorFile.read(), 'xml')
    try:
      author = {
        'name': soup.findAll('name')[0].string,
        'gender': soup.GoodreadsResponse.author.gender.contents[0],
        'firstBookId': soup.GoodreadsResponse.author.id.contents[0],
        'authorId': soup.GoodreadsResponse.author.id.contents[0],
        'authorAverageRating': soup.GoodreadsResponse.author.average_rating.contents[0]
      }
      authors.append(author)
    except AttributeError:
      print 'attribute aerroror'
    except IndexError:
      print 'no name'
  jsonOutput = open('Authors_' + str(unixTimeCode) + '.json', 'w')
  print jsonOutput.write(json.dumps(authors, indent=2))

def getAverageRatings(fileName):
  jsonFile = open('./' + fileName)
  girls = 0
  boys = 0
  girlPower = 0
  boyPower = 0
  authors = json.loads(jsonFile.read())
  for author in list(authors):
    if author['gender'] == 'female':
      girlPower = girlPower + float(author['authorAverageRating'])
      girls = girls + 1
    if author['gender'] == 'male':
      boyPower = boyPower + float(author['authorAverageRating'])
      boys = boys + 1
  print "Average female author rating: " + str(girlPower / girls)
  print "Average male author rating: " + str(boyPower / boys)

def getComments(fileName):
  jsonFile = open('./' + fileName)
  authors = json.loads(jsonFile.read())
  authorSentimentsFile = open('./Analysis' + str(unixTimeCode) + '.json', 'w')
  authorSentiments = []
  for index, author in enumerate(list(authors)):
    goodreadsPage = requests.get('https://www.goodreads.com/book/show/' + author['firstBookId'])
    print author['firstBookId']
    print goodreadsPage.text
    soup = BeautifulSoup(goodreadsPage.text)
    comments = soup.findAll(attrs={'class': 'reviewText'})
    for comment in comments:
      try:
        comment = strip_markup(str(comment))
        analysis = requests.post('http://text-processing.com/api/sentiment/', data={"text": comment}, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
        analysisJson = json.loads(analysis.text)
        sentiment = {
          'gender': author['gender'],
          'overallSentiment': analysisJson['label']
        }
        authorSentiments.append(sentiment)
        print "At author " + str(index)
      except UnicodeDecodeError:
        print "i got a stupid error"
      except ValueError:
        print "ValueError"
  authorSentimentsFile.write(json.dumps(authorSentiments, indent=2))

def getAverageCommentRatings(fileName):
  jsonFile = open('./' + fileName)
  girls = 0
  boys = 0
  girlPower = 0
  boyPower = 0
  authors = json.loads(jsonFile.read())
  for author in list(authors):
    if author['gender'] == 'female':
      girls = girls + 1
      if author['overallSentiment'] == 'pos':
        girlPower = girlPower + 1
      if author['overallSentiment'] == 'neg':
        girlPower = girlPower - 1
    if author['gender'] == 'male':
      boys = boys + 1
      if author['overallSentiment'] == 'pos':
        boyPower = boyPower + 1
      if author['overallSentiment'] == 'neg':
        boyPower = boyPower - 1
  print "Average female author rating: " + str(girlPower)
  print "Average male author rating: " + str(boyPower)

if sys.argv[1] == "getAuthors":
  getAuthors()

if sys.argv[1] == "getAverageRatings":
  try:
    getAverageRatings(sys.argv[2])
  except IndexError:
    print "Please supply JSON array of authors."

if sys.argv[1] == "getComments":
  try:
    getComments(sys.argv[2])
  except IndexError:
    print "Please supply JSON array of authors."

if sys.argv[1] == "getAverageCommentRatings":
  try:
    getAverageCommentRatings(sys.argv[2])
  except IndexError:
    print "Please supply JSON array of analysis."

if sys.argv[1] == "getBooks":
  getBooks()
