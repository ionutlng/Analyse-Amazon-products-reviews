#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import subprocess
import xml.etree.ElementTree as et

from googletrans import Translator



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
                if line.startswith(' \\'):
                    line = line[2:]
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
        print(key)
        item = et.Element("item")
        root.append(item)

        link = et.SubElement(item, "link")
        link.text = key

        productName = key.split("amazon.com/")[1]
        productName = productName.split("/")[0]
        productName = productName.replace("-", " ")
        name = et.SubElement(item, "name")
        name.text = productName



        for value in myDict[key]:
            print(value)
            review = et.SubElement(item, "review")
            try:
                trans = Translator()
                review_translated = trans.translate(value, dest='ro').text
                review.text = review_translated
            except:
                continue

    tree = et.ElementTree(root)

    with open(writeIn, "wb") as files:
        tree.write(files, encoding='utf-8', xml_declaration=True)



#dictionaryData = readData("Output\\all\\all_comments.txt")
#generateXML(dictionaryData, "Output\\all\\all_comments.xml")



