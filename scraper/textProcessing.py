import codecs
import xml.etree.ElementTree as ET


def get_adjective(xml_file):
    adj_list = list()
    with codecs.open(xml_file, encoding='utf-8') as file:
        xml_tree = ET.parse(file)
    root = xml_tree.getroot()
    for group in root.findall('S'):
        for att in group.findall('./W'):
            try:
                if att.attrib['POS'] == 'ADJECTIVE':
                    adj_list.append(att.text)
            except:
                pass
    return adj_list
