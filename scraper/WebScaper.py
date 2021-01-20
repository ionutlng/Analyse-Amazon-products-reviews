#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import multiprocessing
import os
import re
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from googletrans import Translator
from joblib import Parallel, delayed
from selenium import webdriver

from scraper.textProcessing import AnalizaText

os.environ['MOZ_HEADLESS'] = '1'

URL = "https://www.amazon.com"
HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
out_file = "amazom.txt"

# fisiere
FILE_PATH = "output"
FILE_ALL_PRODUCTS = "all_products.txt"
FILE_ALL_COMMENTS = "\\Output\\all\\all_comments.txt"
FILE_ALL_COMMENTS_XML = 'Output\\all\\all_comments.xml'
FILE_ALL_REVIEWS_XML = 'Output\\all\\final_reviews.xml'

# list with links for all categories
links_categories = list()
links_products = list()
set_all_products = set()
all_comments = dict()

# traduce un text, in limba romana
def translateSequence(input):
    translator = Translator()
    result = translator.translate(input, dest='ro')
    return result.text


# returneaza codul HTML al unei pagini web
def getHTML(my_url):
    browser = webdriver.Chrome()
    browser.implicitly_wait(1)
    browser.get(my_url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    browser.quit()
    return soup

def getDriver(link):
    driver = webdriver.Chrome()
    driver.get(link)
    driver.implicitly_wait(10)
    return driver

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

    return links


# salveaza toate review-urile dintr-un produs (doar prima pagina)
def getReviewsFromURL(link):
    if not link.endswith('#customerReviews'):
        link = link + '#customerReviews'

    review_list = list()
    newDriver = getDriver(link)

    productName = newDriver.find_element_by_id('productTitle').text
    productName = productName.strip()
    productName = productName.replace("\n", '')
    review_list.append(productName)
    print(productName)

    try_step = 0
    max_try = 10

    sleep(10)
    element = newDriver.find_element_by_class_name('a-size-base review-text')
    print(element.text)
    while try_step < max_try:
        print(try_step)
        element = newDriver.find_element_by_class_name('a-size-base review-text')
        if element.text != "":
            try_step = 10
            print('founded')
        try_step = try_step + 1
        print(try_step)

    elements = newDriver.find_elements_by_class_name('a-size-base review-text')
    for i in elements:
        print(i.text)



    '''for div in soup.find_all('div', {"class": regex}):
        try:
            comment = div.text.strip()
            comment = comment.replace("\n", "")
            comment = translateSequence(comment)
            review_list.append(comment)
        except:
            pass

    print(review_list)
    if len(review_list) == 1:
        review_list = getReviewsFromURL2(getCustomerRatingsLink)

    try:
        save_dict_to_file(FILE_ALL_COMMENTS, link, review_list)

    except:
        pass'''
    return True





# daca functia de mai sus nu a dat rezultate, incercam cu functia urmatoare
def getReviewsFromURL2(link):
    soup = getHTML(link)
    review_list = list()
    regex = re.compile('.*review-text review-text-content.*')

    productName = soup.find('span', {'id': 'productTitle'}).text
    productName = productName.strip()
    productName = productName.replace("\n", '')
    review_list.append(productName)

    for div in soup.find_all('div', {"class": regex}):
        try:
            comment = div.text.strip()
            comment = comment.replace("\n", "")
            comment = translateSequence(comment)
            review_list.append(comment)
        except:
            pass
    # all_comments[link] = review_list
    # print('done link no.', len(all_comments), ":", all_comments)
    # return review_list
    return link, review_list



# salveaza continutul unui dictionar intr-un fisier
def save_dict_to_file(my_file, link, comments):
    path = os.getcwd() + my_file
    with codecs.open(path, "a+", "utf-8") as file:
        x = f'{str(link)} \\ {str(comments)}\n'
        file.write(x)
    print('Done!', len(comments), 'comentarii pentru link', link)


# salveaza continutul unei liste, intr-un fisier
def save_list_to_file(my_file, my_list):
    file = open(my_file, "w+")
    for item in my_list:
        line_to_write = item + '\n'
        file.write(line_to_write)

    file.close()




# 3. mergem pe fiecare categorie, extragem link-urile cu produsele, si salvam in fisiere.
def extractAllProducts():
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(extractProducts)(i) for i in links_categories)
    #for i in links_categories:
    #    extractProducts(i)

def extractProducts(link):
    links_products = getProductsLink(link)

    filename = link.replace("https://www.amazon.com/", "")
    # sterge caracterele dubioase din numele fisierelor.
    filename = filename.replace("?", "")
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    filename = filename.replace("*", "")
    filename = filename.replace("\"", "")

    save_list_to_file(str(filename) + ".txt", links_products)


# 4. eliminare duplicate
def readAllLinks_removeDuplicates():
    path = os.getcwd() + "\\Output\\all\\"
    print(path)
    for file in os.listdir(path):
        if file.endswith("cts.txt"):
            with open(path + file, 'r') as content:
                for line in content.readlines():
                    set_all_products.add(line)





# 4.5 Salvam toate linkurile cu produsele intr-un singur fisier: all_products_txt
def save_all_productsLink(filename):
    path = os.getcwd() + "\\Output\\all\\" + filename
    file = open(path, "w+")
    for item in set_all_products:
        file.write(item)

    file.close()



# 5. accesam link-urile produselor, citim comentariile, si le punem intr-un fisier all_comments
def getProductsComments(file_products, file_comments):
    list_of_products = list()
    path = os.getcwd() + "\\Output\\all\\" + file_products
    with open(path, "r") as links:
        for link in links.readlines():
            fixed_link = link.replace("\n", "")
            list_of_products.append(fixed_link)


    # for link in list_of_products:
    #     getReviewsFromURL(link)

    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores-1, maxtasksperchild=2)
    try:
        result_map = pool.map(getReviewsFromURL, [link for link in list_of_products], chunksize=1)
        '''for link, comments in (r for r in result_map):
            my_dict = dict()
            my_dict[link] = comments
            save_dict_to_file(file_comments, my_dict)'''

    except:
        pass
    finally:
        pool.close()
        pool.join()

    #save_dict_to_file(file_comments, all_comments)
    #data_frame = pd.Series(link_review)
    #data_frame.to_csv("Output/output.csv")


# returneaza link-ul pentru 000 customer ratings
def getCustomerRatingsLink(link):
    soup = getHTML(link)
    try:
        link_to_return = soup.find('a', {"innerText": ".*ratings.*"})
        return link_to_return
    except:
        pass
    finally:
        return link



# 6. Curatam data-frameul de NA
def cleanDataFrameComments():
    print("to do")




if __name__ == "__main__" :
    print("START:", datetime.now())
    # 1. citim HTML-ul amazon.com
    #amazon_html = getHTML(URL)

    # 2. citim link-urile pentru categorii

    print('\n\n...\n* Citim link-urile categoriilor')
    #links_categories = getCategoriesLink(amazon_html)
    print('DONE - 100% #\t', datetime.now(), '\n* Total categorii extrase:', len(links_categories))


    # 3. din fiecare categorie, citim toate link-urile produselor
    print('\n\n...\n* Citim link-urile produselor pentru fiecare categorie')
    #extractAllProducts()
    print('DONE - 100% #\t', datetime.now(), '\n* Total produse extrase:', len(links_products))


    # 4. Citim toate linkurile produselor si eliminam duplicatele
    print('\n\n...\n* Citim toate linkurile si eliminam duplicatele')
    #readAllLinks_removeDuplicates()
    print('DONE - 100% #\t', datetime.now(), '\n* Total produse unice ramase:', len(set_all_products))


    # 5. Salvam linkurile produselor in fisierul Output/all/all_products.txt
    print('\n\n...\n* Salvam TOATE linkurile produselor in fisierul Output/all_products.txt')
    #save_all_productsLink(FILE_ALL_PRODUCTS)
    print('DONE - 100% #\t', datetime.now(), '\n* Total produse:', len(set_all_products))


    # 6. Salvam comentariile produselor intr-un fisier
    print('\n\n...\n* Salvam comentariile produselor intr-un fisier')
    getProductsComments(FILE_ALL_PRODUCTS, FILE_ALL_COMMENTS)
    print('DONE - 100% #\t', datetime.now())

    # 7. Mutam informatiile obtinute in Output/all/all_comments.txt intr-un fisier .xml
    print('\n\n...\n* Mutam informatiile din .txt in format .xml')
    # dictionaryData = readData("Output\\all\\all_comments.txt")
    # generateXML(dictionaryData, "Output\\all\\all_comments.xml")
    # parseXML("Output\\all\\all_comments.xml")
    print('DONE - 100% #\t', datetime.now())

    # 8. Incepem analiza pe text
    print('\n\n...\n* Incepem analiza textului pe produsul dat...')
    nume_produs = "tbd"
    AnalizaText(FILE_ALL_COMMENTS_XML, nume_produs)
    print('DONE - 100% #\t', datetime.now())

