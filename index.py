from goodreads import client
import requests

gc = client.GoodreadsClient("sySok63UyYyWi2Wof1HocA", "CyuRTp1MAMtnmF839U6653Uv8yn1Y0SWh0EF5d8ACNQ")

print gc.book(1)
print gc.book(1).authors[0]




# import random
# print (random.randrange(1, 1000))

# import xml.etree.ElementTree as ET
# tree = ET.parse('country_data.xml')
# root = tree.getroot()
# for i<1000:
r = requests.get('https://www.goodreads.com/author/show/1234?format=xml&key=sySok63UyYyWi2Wof1HocA')
print r.text


