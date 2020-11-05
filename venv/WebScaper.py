from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.emag.ro'

#opening connection, save the page
uClient = uReq(my_url)
html_page = uClient.read()
uClient.close()

#parse html file
html_parsed = soup(html_page, "html.parser")

print(html_parsed)
