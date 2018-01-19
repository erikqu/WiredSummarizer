# -*- coding: utf-8 -*-
import urllib 
import bs4 
import requests
import textrank 

setpage = "https://www.wired.com/"
link_list=[]
def remove_related(soup):
	links = (soup.find_all("li",{"class": "article-list-item-embed-component__post"}))

def remove_refs(input_string):
		tmp=""
		flag = False
		stringbuilder= ""
		stringbuilder = input_string
		for x in input_string:
			if x == "[":
				flag=True
				tmp = tmp+x
			elif flag == True and x == "]":
				tmp=tmp+x
				flag = False
				stringbuilder = stringbuilder.replace(tmp,"")
				tmp=""
				stringbuilder = " ".join(stringbuilder.split())
			elif flag == True:
				tmp=tmp +x
		return stringbuilder

def remove_trail(txt,delim):
	txt = txt.rsplit(delim, 1)[0]
	return txt 

def create_summary(page):
	resp = urllib.request.urlopen(page)
	soup = bs4.BeautifulSoup(resp,'html.parser')

	title = (soup.find('h1')).text
	pgraph= soup.find_all('p')
	text=""
	for x in range((len(pgraph))):
		if "Use of this site constitutes" not in pgraph[x].text:
			text = text + pgraph[x].text

	text = remove_refs(text)

	summary = textrank.extract_sentences(text)
	summary = remove_trail(summary,".")
	summary = summary + "."
	print('\n', title, '\n')
	print(summary)

def getsoup():
	page = setpage
	resp = urllib.request.urlopen(page)
	soup = bs4.BeautifulSoup(resp,'html.parser')
	return soup
def remove_section(tag):
	buildup=""
	for x in tag:
		if x.islower():
			buildup = buildup+x
		else:
			break
	if len(buildup) > 0:
		buildup = tag.replace(buildup,"")
	return buildup

def remove_trail(txt,delim):
	txt = txt.rsplit(delim, 1)[0]
	return txt 

def create_link(website,url):
		website = website + url
		return website 

def get_most_popular():
	soup = getsoup()
	mostpopular = (soup.find_all("li", {"class": "post-listing-list-item__post"}))
	links = (soup.find_all("a",{"class": "post-listing-list-item__link"}))
	link_number=5
	link_names =[]
	for x in range(link_number):
		link_list.append(links[x].get('href'))
		text = remove_section(mostpopular[x].text)
		text = remove_trail(text,'Author')
		link_names.append(text)
		print('[',(x+1),']', text)
	selection = input("\nSelect article by # >")
	return selection,link_names

def main():
	print("\nWelcome to the WIRED summarizer!\nChoose an article to be summarized (or enter h for help):")
	choice,names = get_most_popular()
	while(True):
		if choice =='h':
			print("1-5 to summarize an article\no to open the article\nq to quit")
			choice = input("Select article by # >")
			continue
		elif choice == 'q':
			print("Quitting..")
			exit()
		elif choice == 'o':
			special = input("Enter the article #>")
			#finish me
		elif len(choice) >1:
			print("Not a valid command! Enter q to quit!")
			continue
		choice = int(choice)
		choice -=1
		urlname = setpage + link_list[choice]
		create_summary(urlname)
		print("\n")
		for x in range(len(names)):
			print('[',(x+1),']',names[x])
		choice = input("Select article by # >")
		
main()

