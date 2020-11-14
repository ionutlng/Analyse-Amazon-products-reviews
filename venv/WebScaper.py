import os
import re
from bs4 import BeautifulSoup
import requests

URL = "https://www.amazon.com"
HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
out_file = "amazom.txt"

# list with links for all categories
links_categories = list()
links_products = list()
set_all_products = set()


# returneaza codul HTML al unei pagini web
def getHTML(my_url, my_header):
    webpage = requests.get(my_url, headers=my_header)
    soup = BeautifulSoup(webpage.content, "lxml")
    return soup


# returneaza o lista cu LINK-urile pentru fiecare categorie de pe pagina amazon.com
def getCategoriesLink(soup):
    links = list()
    regex = re.compile('.*a-link-normal see-more.*')
    for a in soup.find_all('a', {"class": regex}):
        links.append("https://www.amazon.com" + a['href'])
    return links


# returneaza o lista cu LINK-urile PRODUSELOD
def getProductsLink(link):
    soup = getHTML(link, HEADERS)
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
        soup = getHTML(new_link, HEADERS)
        for a in soup.find_all("a", {"class": regex}):
            href = a['href']
            if not href.startswith("https://www.amazon.com"):
                href = "https://www.amazon.com" + href
            links.append(href)
        print(link, "page ", str(page), "- parsed")

    return links


# salveaza continutul unei liste, intr-un fisier
def save_list_to_file(my_file, my_list):
    file = open(my_file, "w+")
    for item in my_list:
        line_to_write = item + '\n'
        file.write(line_to_write)

    file.close()


# 1. citim continutul paginii https://www.amazon.com
amazon_html = getHTML(URL, HEADERS)

# 2. parsam link-urile pentru fiecare categorie, de pe pagina principala
links_categories = getCategoriesLink(amazon_html)


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
                link = content.read()
                set_all_products.add(link)


readAllLinks_removeDuplicates




# 5. accesam link-urile produselor(set_all_products), citim comentariile, si le punem intr-un dataframe
