#Trademe negative feedback viewer by Hayden Harrison
# To use run application and enter the url of the members feedback page i.e
# http://www.trademe.co.nz/Members/Feedback.aspx?member=1234567

import os
import shutil
import sys
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

def generateListOfPages(url):
	soup = BeautifulSoup(urlopen(url))
	links = soup.findAll(href=re.compile("^Feedback")) #grab all the links beginning with Feedback
	linkList.append(url) #include the entered URL in our list

	#Creates a list of all the unique URLs representing each page of feedback
	for i in links:
		linkToAdd = BASE_URL + i.get("href")
		if linkToAdd not in linkList:
			linkList.append(linkToAdd)


  	 
def getNegativeFeedback(links):
	feedbackCount = 0
	sellerResponse = "No response."

	for feedbackPage in links:
		soup = BeautifulSoup(urlopen(feedbackPage))
		negative = soup.findAll("div", { "class" : "feedback-item wordwrap" }) #this is the class associated with feedback directed towards user
 		
 		for i in negative:
 			if(i.parent.parent.findPreviousSibling("tr") != None):
 				f = i.parent.parent.findPreviousSibling("tr")
 				if(SAD_FACE in f.prettify()):
 					feedbackCount += 1

 					criticName = "Name of user complaining: " + f.b.string
 					userWasBuyerOrSeller = f.div.string
 					negativeFeedback = f.findNextSibling("tr").div.string.replace("&nbsp;","")
 				
 					if(f.nextSibling.nextSibling.nextSibling.div != None and f.nextSibling.nextSibling.nextSibling.div.string != userWasBuyerOrSeller):
 						sellerResponse = f.nextSibling.nextSibling.nextSibling.div.string

 					print(criticName + "\n\n" + userWasBuyerOrSeller + "\n\n" + "Feedback: \n" + negativeFeedback + "\n\n" + "Response: \n" 
 						+ sellerResponse + "\n\n" + "Feedback page for more info: \n" + str(feedbackPage))
 					print("\n\n\n\n")

 					sellerResponse = "No response."
 	print(str(feedbackCount) + " negative feedbacks found.")
 	



#Constants for locating data in the webpage sourcecode
HAPPY_FACE = "/images/happy_face1.gif"
SAD_FACE = "/images/sad_face1.gif"
NEUTRAL_FACE = "/images/neutral_face1.gif"
BASE_URL = "http://www.trademe.co.nz/Members/"
linkList = []

trademeURL = raw_input("Enter the address of the target feedback page: ")
generateListOfPages(trademeURL)
getNegativeFeedback(linkList)


