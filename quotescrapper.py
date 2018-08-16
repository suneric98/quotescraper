import requests
from bs4 import BeautifulSoup
import time
from quote import Quote
from authorinfo import Authorinfo
import sys
from pathlib import Path

#TODO: add option to export to a text file, show data about quotes and predictions, choose options other than "tags" -> do like search by word or author

def author_info(authors):
    authorinfos = []
    url = "http://quotes.toscrape.com/"
    for author in authors:
        author = author.replace(".","-",author.count(".") - 1)
        author = author.replace(".","")
        author = author.replace(" ","-")
        r = requests.get(url + "/author/" + author)
        soup = BeautifulSoup(r.text, "html.parser")
        check_empty = soup.find("h3", attrs={"class":"author-details"})
        if check_empty == "":
            authorinfos.append(Authorinfo(author,"","",""))
        else:
            name = soup.find("h3", attrs={"class":"author-title"}).text
            if name == "":
                name = author
            birthday = soup.find("span", attrs={"class":"author-born-date"}).text
            location = soup.find("span", attrs={"class":"author-born-location"}).text.split("in ")[0]
            description = soup.find(attrs={"class":"author-description"}).text
            description = description.translate(str.maketrans("","","\t\n"))
            authorinfos.append(Authorinfo(name, birthday, location, description))
    return authorinfos

def print_author_info(authorinfos):
    for info in authorinfos:
        if info.get_birthday() == "":
            print("\nSorry, we couldn't find any information on " + info.get_name() + ". You might have typed their name wrong, or we might not have found anything about them.\n")
        else: 
            print(info.get_name() + " was born" + info.get_home() + " on " + info.get_birthday() + ". Here's a short description about them:\n\n" + info.get_description() +"\n")

def random_page(num_quotes, quotes):
    url = "http://quotes.toscrape.com/random"
    i = 0
    while i < num_quotes:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        page_quote = soup.find("span", attrs= {"class":"text"})
        page_author = soup.find("small", attrs={"class":"author"}) 
        quotes.append(Quote(page_author.text, page_quote.text))
        i += 1
    return quotes

def loop_pages(num_quotes, pages, url, quotes):
    i = 1
    while i <= pages:
        r = requests.get(url + "/page/" + str(i))
        soup = BeautifulSoup(r.text, "html.parser")
        check_empty = soup.find(attrs={"class":"col-md-8"})
        if check_empty.text.strip() == "No quotes found!":
            return []
        page_quotes = soup.findAll("span", attrs= {"class":"text"})
        page_authors = soup.findAll("small", attrs={"class":"author"}) 
        quotes_get = num_quotes
        if num_quotes // (i * 10) == 0:
            quotes_get = num_quotes % 10
        else: 
            quotes_get = 10
        j = 0
        while j < quotes_get:
            try:
                quotes.append(Quote(page_authors[j].text, page_quotes[j].text))
            except IndexError:
                return quotes
            j += 1
        i += 1
    return quotes

def print_pages(quotes, checktext):
    if checktext:
        path = Path('text_files/quotes.txt')
        with open(path, "w") as f:
            f.close()
    if not quotes:
        print("Sorry, it looks like we couldn't find any quotes matching your tag.")
        sys.exit()
    counter = 1
    for q in quotes:
        if checktext:
            f = open(path, "a+")
            with f:
                f.write("Quote #" + str(counter) + ": " + q.get_quote() + " - " + q.get_author() + "\n")
                f.close()
        print("Quote #" + str(counter) + ": " + q.get_quote() + " - " + q.get_author())
        counter += 1

def check_exit(x):
    if x.lower().strip() == "exit":
        input("\nThanks for using this program!\n")
        sys.exit()

def create_tag():
    tag = ""
    while True:
        print("What tag would you like to look for your quote?\nIf you want to view general quotes, type 'general'.\nIf you want a random quote, type 'random'.")
        tag = input("Some examples of tags are 'love', 'friendship', and 'humor' \n> ")
        check_exit(tag)
        try: 
            int(tag)
            print("Please input a string")
        except ValueError:
            if "" != tag.strip():
                return tag

def select_num_quotes():
    while True:
        try:
            num_quotes = input("How many quotes would you like?\n> ")
            check_exit(num_quotes)
            if "" != num_quotes.strip() and int(num_quotes) > 0:
                return num_quotes
        except ValueError:
            print("Please enter a number")

def select_authors():
    while True:
        author = input("\nWould you like to find out more about the authors? Type each author's name seperated by a comma and a space (please capitalize their first and last name) to find out more about them.\n"
        "If you don't want more information, please type 'exit'.\n"
        "Ex: 'Albert Einstein, George Eliot'\n> ")
        check_exit(author)
        if "" != author.strip():
            return author

def check_text():
    text = input("\nIf you'd like to save the quotes into a text file, please type \'text\'. Otherwise press enter and the quotes will simply be printed to the terminal.\n> ")
    check_exit(text)
    if text == "text":
        print("Okay! Your quotes will be saved in a file called quotes.txt\n")
        return True
    print("Okay, your quotes will be displayed on the terminal.\n")
    return False


def main():
    print("Hi! This program scrapes quotes from the website quotes.toscrape.com and displays them to you! You can either have the quotes displayed in the console or put into a text file "
    "that you can open later. If you ever want to close this program, please type \'exit\'.\n")

    checktext = check_text()

    tag = create_tag()
    num_quotes = select_num_quotes()
    tag = tag.lower()
    num_quotes = int(num_quotes)
    pages = num_quotes // 10 + 1

    url = "http://quotes.toscrape.com/"
    if "general" != tag:
        url = url + "tag/" + tag
    
    quotes = []
    if tag == "random":
        quotes= random_page(num_quotes, [])
    else:
        quotes = loop_pages(num_quotes, pages, url, [])
    print_pages(quotes, checktext)

    author = select_authors()

    authorinfos = author_info(author.split(", "))
    print_author_info(authorinfos)

    check_exit("exit")

if __name__== "__main__":
    main()
