#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import subprocess
import xml.etree.ElementTree as et

from googletrans import Translator

from scraper.WebScaper import translateSequence


def readData(filename):
    my_dictionary = dict()
    key = ""
    review = ""
    new_review = False

    with codecs.open(filename, encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(0, len(lines)):
        line = lines[i]
        if new_review == False:
            if line[0:22] == 'https://www.amazon.com':
                key = line
                key = key.replace('\r', '')
                key = key.replace('\n', '')

                new_review = True
                review = ""
                continue

        else:
            #while new_review == True and i < len(lines):
            if line[0:22] == 'https://www.amazon.com':
                new_review = False
                my_dictionary[key] = review
            else:
                #i = i + 1
                #line = lines[i]
                if line.startswith('\\'):
                    line = line[1:]
                line = line.replace('\n', '')
                line = line.replace('\r', '')
                line = line.replace('\b', '')
                line = line.replace('[', '')
                line = line.replace(']', '')

                review = review + line

    dict_to_return = dict()
    for key in my_dictionary.keys():
        values = my_dictionary[key].split('\',')
        if ' ' in values:
            values.remove(' ')
        if ", " in values:
            values.remove(", ")

        dict_to_return[key] = values

    return dict_to_return





def generateXML(myDict, writeIn):
    root = et.Element("amazon_items")

    for key in myDict.keys():
        item = et.Element("item")
        root.append(item)

        name = et.SubElement(item, "link")
        name.text = key

        trans = Translator()

        for value in myDict[key]:
            review = et.SubElement(item, "review")
            try:
                review.text = trans.translate(value, dest='ro').text
            except:
                pass



    tree = et.ElementTree(root)

    with open(writeIn, "wb") as files:
        tree.write(files, encoding='utf-8', xml_declaration=True)

def parseXML(file):
    tree = et.parse(file)
    root = tree.getroot()

    # for each item
    for item in root.findall('item'):
        #name = item.name('name')
        #if name == 'xyz':
        link = item.find('link')
        reviews = item.findall('review')
        for review in reviews:
            #print(link.text, review.text)
            review_text = review.text
            if isinstance(review_text, str):
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
                break


#dictionaryData = readData("Output\\all\\all_comments.txt")
#generateXML(dictionaryData, "Output\\all\\all_comments.xml")
parseXML("Output\\all\\all_comments.xml")


