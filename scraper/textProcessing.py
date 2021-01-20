import codecs
import os
import xml.etree.ElementTree as ET
import subprocess

FILE_ALL_COMMENTS_XML = 'Output\\all\\all_comments.xml'
FILE_ALL_REVIEWS_XML = 'Output\\all\\final_reviews.xml'


def listToString(s):
    str1 = s[0]
    for ele in s[1:]:
        str1 = str1 + ", " + ele

    return str1


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
def calculateScore(asd):
    return "TDB"


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
                    review_score = calculateScore(list_of_adjectives)

                    # adauga review-ul + scorul in XML
                    review_xml = ET.SubElement(root_newXML, "review", attrib={"id": str(total_reviews), "score": review_score})
                    review_xml.text = listToString(list_of_adjectives)

                    os.chdir("..")
            break

    newTree = ET.ElementTree(root_newXML)
    with open(FILE_ALL_REVIEWS_XML, "wb") as files:
        newTree.write(files, encoding='utf-8', xml_declaration=True)



AnalizaText(FILE_ALL_COMMENTS_XML, 'iPhone 15 PRO smecher 12GB de inch')