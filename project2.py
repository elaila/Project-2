## SI 206 F18 - Project 2

## COMMENT HERE WITH:
## Your name: Laila Elnaggar
## Anyone you worked with on this project and how you worked together
## You can not share code, but can share ideas
###########

## Import statements
import unittest
import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

## PART 1  - Complete grab_headlines
## INPUT: soup - the soup object to process
## Grab the headlines from the "Most Read" section
## and return them in a list
def grab_headlines(soup):

    # get the most read div
    # get the ordered list from that div
    # get the links from the ordered list div
    # return the headlines

    div = soup.find(class_ ="view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266")
    list = []
    headline = div.find_all('a')
    for title in headline:
        list.append(title.text)
    return list

## PART 2 Complete a function called get_headline_dict. It will take a soup object and return a dictionary
## with each story headline as a key and each story url as the value
## INPUT: soup - the soup object
## OUTPUT: Return - a dictionary with each story headline as the key and the story url as the value
def get_headline_dict(soup):

    # create the empty dictionary

    # get the story wrap divs

    # get the short headline

    # find the link in headline div

    # set the dictionary key to the headline and the url as the value

    headline_dict = {}
    x = soup.find_all(class_ = "views-field views-field-field-short-headline")
    for y in x:
        z = y.find('a')
        headline_dict[y.text.strip()] = z.get('href')
    return headline_dict


## PART 3 Define a function called get_page_info. It will take a soup object for a story
## and return a tuple with the title, author, date, and the number of paragraphs
## in the body of the story
## INPUT: soup - the soup object
## OUTPUT: Return - a tuple with the title, author, date, and number of paragraphs
def get_page_info(soup):

    # get the title

    # get the date

    # get the author

    # get the number of paragraphs

    # return the tuple

    title = soup.find(class_ = "pane-content")
    title2 = title.find('h2')
    title3 = title2.text.strip()

    date = soup.find_all(class_ = "pane-content")
    date2 = date[1]
    date3 = date2.get_text().strip()

    author = soup.find(class_ = "link")
    author2 = author.get_text().strip()

    paragraph_class = soup.find_all(class_ = "field-item even")
    paragraphs = paragraph_class[3].find_all('p')
    numParagraphs = len(paragraphs)
    return (title3, date3, author2, numParagraphs)

## Extra Credit
## INPUT: the dictionary that was returned from part 2
## OUTPUT: a new dictionary with just items that contain the word U-M or Ann Arbor
def find_mich_stuff(dict):
    mich_dict = {}
    for x in dict.items():
        text = x[0]
        if (re.findall(r'\b(U-M|Ann Arbor)\b', text)):
            mich_dict[text] = x[1]
    return mich_dict


########### TESTS; DO NOT CHANGE ANY CODE BELOW THIS LINE! ###########

def getSoupObjFromURL(url):
    """ return a soup object from the url """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getSoupObjFromFile(fileName):
    """ return a soup object from the file with the passed fileName"""
    file = open(fileName, 'r')
    text = file.read().strip()
    file.close()
    soup = BeautifulSoup(text, "html.parser")
    return soup

# testing on live urls - remove the string comments to run this
"""
soup = getSoupObjFromURL("https://www.michigandaily.com/section/news")
print(grab_headlines(soup))
hDict = get_headline_dict(soup)
print(hDict)
# get page info for each story in hDict
for key, value in hDict.items():
    tuple = getPageInfo(hDict, "http://www.michigandaily.com/")
    print(tuple)
#nDict = find_mich_stuff(hDict) # for extra credit
#print(nDict)
"""

# Test using unittests and saved pages
class TestP2(unittest.TestCase):

    def setUp(self):
        self.soup = getSoupObjFromFile("news1.html")
        self.soup2 = getSoupObjFromFile("newsStory1.html")
        self.dict = get_headline_dict(self.soup)

    def test_grab_headlines(self):
        self.assertEqual(grab_headlines(self.soup),['Broken Record: Student survivor navigates painful reporting process', 'Assistant women’s gymnastics coach resigns after charge of obscene conduct with gymnast', 'Ann Arbor Pieology shuts down because of “unfortunate circumstances”', 'To the white men who told me that they “prefer” white women', 'Op-Ed: Why I declined to write a letter of recommendation  '])

    def test_get_headline_dict(self):
        dict = get_headline_dict(self.soup)
        url = dict['Dialogues on Diversity holds discussion on microaggressions, accountability']
        self.assertEqual(len(dict.items()), 19)
        self.assertEqual(url,'https://www.michigandaily.com/section/campus-life/diversity-sciences')

    def test_get_page_info(self):
        self.assertEqual(get_page_info(self.soup2), ('Panel discusses pros, cons of Library Lot ballot proposal', 'Thursday, October 25, 2018 - 9:28pm', 'Leah Graham', 17))

    def test_find_mich_stuff(self):
        dict = find_mich_stuff(self.dict)
        url1 = dict['Ann Arbor state Rep. proposes bill to vastly increase renewable energy']
        url2 = dict['U-M freshman runs for Ann Arbor School Board position']
        self.assertEqual(len(dict), 4)
        self.assertEqual(url1,'https://www.michigandaily.com/section/government/state-rep-proposes-bill-100-percent-renewable-energy-michigan-2050')
        self.assertEqual(url2,'https://www.michigandaily.com/section/ann-arbor/school-board-candidates-fight-name-recognition-race')

unittest.main(verbosity=2)
