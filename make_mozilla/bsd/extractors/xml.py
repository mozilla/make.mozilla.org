from lxml import etree

def constituent_email(xml):
    doc = etree.fromstring(xml)
    return doc.xpath('/api/cons/cons_email/email')[0].text
