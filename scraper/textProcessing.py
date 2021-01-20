import codecs
import os
import xml.etree.ElementTree as ET


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