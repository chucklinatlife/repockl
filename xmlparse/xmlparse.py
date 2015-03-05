import xml.etree.ElementTree as ET
import os
import pprint

pp = pprint.PrettyPrinter(indent = 4)



if __name__ == "__main__":

    os.chdir('/Users/cklam/Desktop')
    pp.pprint(os.getcwd())
    xmltest = 'xmltest.xml'
    tree = ET.parse(xmltest)
    #tree = ET.parse('xmltest.xml')
    root = tree.getroot()
    #root = ET.fromstring(xmltest_as_string)

    program_list = []
    xml_user_dict = {}
    for item in root:
        xml_user_dict = {}
        for child in item:
            print child.tag, child.attrib["name"]
            xml_user_dict[child.tag] = child.attrib["name"]
        program_list.append(xml_user_dict)

    pp.pprint(program_list)
