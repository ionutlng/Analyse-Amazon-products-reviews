import codecs
import os
import xml.etree.ElementTree as ET
import subprocess

FILE_ALL_COMMENTS_XML = 'Output\\all\\all_comments.xml'
FILE_ALL_REVIEWS_XML = 'Output\\all\\final_reviews.xml'


def listToString(s):
    str1 = ""
    for ele in s:
        str1 = str1 + ", " + ele

    return str1[2:]


# Adjective_XML = os.getcwd() + "\\Output\\all\\translated_comments.xml"
def getLemmaFromAdj(xml_file):
    adj_list = list()
    with codecs.open(xml_file, encoding='utf-8') as file:
        xml_tree = ET.parse(file)
    root = xml_tree.getroot()
    for group in root.findall('S'):
        for att in group.findall('./W'):
            try:
                if att.attrib['POS'] == 'ADJECTIVE':
                    adj_list.append(att.attrib['LEMMA'])
            except:
                pass
    return adj_list


# calculeaza scorul pentru un review. Daca e Positiv/Negativ.
def valueOfSentence(list_to_be_processed):
    most_freq_adj = {"diferit": 1, "folosit": -1, "important":1, "mare":1, "disponibil":1, "popular":1,
    "in stare":1, "cunoscut":1, "variat":1, "dificil":-1, "vechi":-1, "similar":-1,"tradiţional":-1, "real":1,
    "de succes":1, "scump": -1, "inteligent":1, "interesant":1, "sărac":-1, "drăguţ":1, "util":1,
    "Recent":1, "Grozav":1, "minunat":1, "imposibil": -1, "serios":1, "imens":1,
    "rar":1, "exact":1, "capabil":1, "periculos": -1, "eficient":1, "puternic":1, "practic":1,
    "potrivit":1, "suficient":1, "neobișnuit":1, "nefericit":-1, "acceptabil":-1, "plictisitor":-1,
    "distinct":1, "logic":1, "rezonabil":-1, "strict":-1, "automat":1, "masiv":1, "impresionant":1,
    "placut":1,"incapabil":-1,"slab":-1,"decent":1,"remarcabil":1,"înalt":1,"minuscul":-1,"nou":1,
    "bun":1,"Cel mai bun":1,"mai bine":1,"simplu":1,"actual":1,"ultimul":1,
    "principal":1,"profesional":1,"internaţional":1,"inferior":-1,"in conformitate":1,"special":1,
    "întreg":1,"clar":1,"uşor":1,"pozitiv":1,"corect":1,"complex":1,"independent":1,"original":1,
    "frumos":1,"complet":1,"negativ":-1,"gresit":-1,"în urmă":-1,"rapid":1,"excelent":1,
    "unic":1,"clasic":1,"occidental":1,"familiar":1,"oficial":1,"perfect":1,"luminos":1,"confortabil":1,
    "bogat":1,"robust":1,"valoros":1,"încet":-1,"curat":1,"proaspăt":1,"normal":1,"ieftin":-1,"obiectiv":1,
    "sigur":1,"misto":1,"uimitor":1,"stare brută":-1,"ciudat":-1,"ilegal":-1,"comun":-1,"super":1,
    "superior":1,"murdar":-1,"Sclipitor":1,"dragă":1,"îngrijit":1,"ok":1,"prostesc":-1,"prost":-1}

    list_of_relevant_adj = []
    positive_adj_list = []
    negative_adj_list = []
    for adj in list_to_be_processed:
        if (adj in most_freq_adj) and (most_freq_adj[adj] == 1):
            positive_adj_list.append(adj)
        elif(adj in most_freq_adj) and (most_freq_adj[adj] == -1):
            negative_adj_list.append(adj)
    list_of_relevant_adj.append(positive_adj_list)
    list_of_relevant_adj.append(negative_adj_list)
    return list_of_relevant_adj

# cauta un produs in XML, face POS pe toate comentariile, si creaza un XML final, ce va fi folosit in UI
def AnalizaText(file, produs_cautat):
    tree = ET.parse(file)
    root = tree.getroot()
    root_newXML = ET.Element("amazon_item")
    total_reviews = 0

    # for each item
    for item in root.findall('item'):
        name_of_product = item.find('name')
        if name_of_product.text == produs_cautat:
            # adauga numele in XML
            name = ET.SubElement(root_newXML, "name")
            name.text = produs_cautat

            link = item.find('link')
            reviews = item.findall('review')

            for review in reviews:
                review_text = review.text
                if isinstance(review_text, str):
                    total_reviews = total_reviews + 1
                    if review_text.startswith('\\'):
                        review_text = review_text[1:]
                    review_text = review_text.replace('\n', '')
                    review_text = review_text.replace('\b', '')
                    review_text = review_text.replace('\r', '')

                    path = os.getcwd() + '\\bin_posro'
                    os.chdir(path)

                    # move review into a separate txt file
                    f = codecs.open("inputuri\\review.txt", 'w+', encoding='utf-8')
                    f.write(review_text)
                    f.close()

                    # run the tool to get POS
                    path = os.getcwd() + '\\posRO.bat'
                    subprocess.call([path])


                    # genereaza lista de adjective
                    list_of_adjectives = getLemmaFromAdj("outputuri\\review.xml")

                    # calculeaza scorul pentru lista de adjective
                    positive_negative = valueOfSentence(list_of_adjectives)
                    positive = positive_negative[0]
                    negative = positive_negative[1]

                    # adauga review-ul + scorul in XML
                    review_xml = ET.SubElement(root_newXML, "review", attrib={"id": str(total_reviews), "positive": listToString(positive), "negative": listToString(negative)})

                    os.chdir("..")
            break

    newTree = ET.ElementTree(root_newXML)
    with open(FILE_ALL_REVIEWS_XML, "wb") as files:
        newTree.write(files, encoding='utf-8', xml_declaration=True)



#AnalizaText(FILE_ALL_COMMENTS_XML, 'Ultimate Bundle Lightning Cable White')