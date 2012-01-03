#!/usr/bin/python

from xml.etree import ElementTree

NAMESPACES = {
    'w':"http://schemas.microsoft.com/office/word/2003/wordml",
    'v':"urn:schemas-microsoft-com:vml",
    'w10':"urn:schemas-microsoft-com:office:word",
    'sl':"http://schemas.microsoft.com/schemaLibrary/2003/core",
    'aml':"http://schemas.microsoft.com/aml/2001/core",
    'wx':"http://schemas.microsoft.com/office/word/2003/auxHint",
    'o':"urn:schemas-microsoft-com:office:office",
    'dt':"uuid:C2F41010-65B3-11d1-A29F-00AA00C14882",
    'wsp':"http://schemas.microsoft.com/office/word/2003/wordml/sp2",
    'ns0':"GD_AssessmentReportManager.xsl",
}

ElementTree.register_namespace('o', 'urn:schemas-microsoft-com:office:office')

fp = open('print.xml')
parser = ElementTree.parse(fp)

#for elem in parser.find('.//w:body//ns0:ActionDateFormat//w:t',
#                  namespaces=NAMESPACES):
#    print elem.text

elems = parser.findall('.//w:body//ns0:AchievementMngList//ns0:Description//w:t',
                      namespaces=NAMESPACES)
for elem in elems:
    print elem.text
    print ' ---- '


#for item in parser.iter():
#    print item.tag