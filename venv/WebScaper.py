#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re

from bs4 import BeautifulSoup
import requests
import csv
import time
from selenium import webdriver
from googletrans import Translator


URL = "https://www.amazon.com"
HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
out_file = "amazom.txt"

# list with links for all categories
links_categories = list()
links_products = list()
set_all_products = set()


def translateSequence(input):
    translator = Translator()
    result = translator.translate(input, dest='ro')
    return result.text

# returneaza codul HTML al unei pagini web
def getHTML(my_url):
    browser = webdriver.Firefox()
    #webpage =
    browser.get(my_url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    browser.quit()
    return soup


# # returneaza o lista cu LINK-urile pentru fiecare categorie de pe pagina amazon.com
def getCategoriesLink(soup):
    links = list()
    regex = re.compile('.*a-link-normal see-more.*')
    for a in soup.find_all('a', {"class": regex}):
        links.append("https://www.amazon.com" + a['href'])
    return links


# returneaza o lista cu LINK-urile PRODUSELOR
def getProductsLink(link):
    soup = getHTML(link)
    links = list()
    regex = re.compile('a-link-normal a-text-normal')

    for a in soup.find_all('a', {"class": regex}):
        href = a['href']
        if not href.startswith("https://www.amazon.com"):
            href = "https://www.amazon.com" + href
        links.append(href)

    print(link, "- page 1 - parsed")
    page = 1
    # daca butonul de Next e vizibil, mergem pe link&page=...
    while soup.find('li', {"class": "a-last"}) or soup.find('a', {"id": "pagnNextLink"}):
        page = page + 1
        new_link = link + "&page=" + str(page)
        soup = getHTML(new_link)
        for a in soup.find_all("a", {"class": regex}):
            href = a['href']
            if not href.startswith("https://www.amazon.com"):
                href = "https://www.amazon.com" + href
            links.append(href)
        print(link, "page ", str(page), "- parsed")

    return links


# salveaza toate review-urile dintr-un produs (doar prima pagina)
def getReviewsFromURL(link):
    soup = getHTML(link)
    review_list = list()
    regex = re.compile('.*reviewText review-text-content.*')

    for div in soup.find_all('div', {"class": regex}):
        print(div.text)
        try:
            x = translateSequence(div.text)
            review_list.append(x)
        except:
            pass



    return review_list


# daca functia de mai sus nu a dat rezultate, incercam cu functia urmatoare
def getReviewsFromURL2(link):
    soup = getHTML(link)
    review_list = list()
    regex = re.compile('.*review-text review-text-content.*')
    for div in soup.find_all('div', {"class": regex}):
        review_list.append(div.text)

    return review_list


# salveaza continutul unui dictionar intr-un fisier
def save_dict_to_file(my_file, my_dict):
    print(my_dict)
    with open(my_file, "w+") as file:
        for key, value in my_dict.items():
            x = f'{str(key)} : {str(value)}'
            file.write(x)
    #    # for item in my_dict:
    #     print(str(item))
    #     print(str(my_dict[item]))
    #

# salveaza continutul unei liste, intr-un fisier
def save_list_to_file(my_file, my_list):
    file = open(my_file, "w+")
    for item in my_list:
        line_to_write = item + '\n'
        file.write(line_to_write)

    file.close()


# 1. citim continutul paginii https://www.amazon.com
#amazon_html = getHTML(URL)

# 2. parsam link-urile pentru fiecare categorie, de pe pagina principala
#links_categories = getCategoriesLink(amazon_html)


# 3. mergem pe fiecare categorie, extragem link-urile cu produsele, si salvam in fisiere.
def extractAllProducts():
    for link_cat in links_categories:
        links_products = getProductsLink(link_cat)

        filename = link_cat.replace("https://www.amazon.com/", "")
        # sterge caracterele dubioase din numele fisierelor.
        filename = filename.replace("?", "")
        filename = filename.replace("/", "")
        filename = filename.replace("\\", "")
        filename = filename.replace("*", "")
        filename = filename.replace("\"", "")

        save_list_to_file(str(filename) + ".txt", links_products)


## decomenteaza, daca vrei sa rulezi parserul:
# extractAllProducts()


# 4. eliminare duplicate
def readAllLinks_removeDuplicates():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(file, 'r') as content:
                for line in content.readlines():
                    set_all_products.add(line)


print('\n\n...\n* Citim toate linkurile si eliminam duplicatele')
readAllLinks_removeDuplicates()
print('DONE - 100%\n* Total produse extrase de pe https://www.amazon.com:', len(set_all_products))


# 4.5 Salvam toate linkurile cu produsele intr-un singur fisier: all_products_txt
def save_all_productsLink():
    file = open('Output/all_products.txt', "w+")
    for item in set_all_products:
        file.write(item)

    file.close()


print('\n\n...\n* Salvam TOATE linkurile produselor in fisierul Output/all_products.txt')
save_all_productsLink()
print('DONE - 100%')


# 5. accesam link-urile produselor, citim comentariile, si le punem intr-un fisier all_comments
def setCommentsToDataFrame(file_path):
    link_review = dict()
    with open(file_path) as links:
        for link in links.readlines():
            reviews = getReviewsFromURL(link)
            if len(reviews) == 0:
                new_link = getCustomerRatingsLink(link)
                reviews = getReviewsFromURL2(new_link)
            link_review[link] = reviews

    save_dict_to_file("Output/all_comments.txt", link_review)
    #data_frame = pd.Series(link_review)
    #data_frame.to_csv("Output/output.csv")


# returneaza link-ul pentru 000 customer ratings
def getCustomerRatingsLink(link):
    soup = getHTML(link)
    try:
        link_to_return = soup.find('a', {"innerText": ".*ratings.*"})
        return link_to_return
    except:
        print(link)
    finally:
        return link


print('\n\n...\n* Salvam comentariile produselor intr-un dataframe')
setCommentsToDataFrame('Output/all_products_short.txt')
print('DONE - 100%')


# 6. Curatam data-frameul de NA
def cleanDataFrameComments():
    print("to do")





