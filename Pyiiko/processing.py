import lxml
import json
import os
'''ф-я обработки департаментов'''

#with open('1.json', encoding='utf-8') as json_data:
#    d = json.load(json_data)

def dep_edit(xml):
    file = lxml.etree.fromstring(xml)
    events = file.xpath(
        r'//corporateItemDto/type[text() = "DEPARTMENT"]/..')
    departments = {}

    for event in events:
        result = ''.join(event.xpath(r'./id/text()'))
        name = ''.join(event.xpath(r'./name/text()'))
        departments[name] = result

    return departments


def emp_edit(id_user, xml):

    file = lxml.etree.fromstring(xml)
    user = file.xpath(r'.//id[text() = "{id}"]'r'/../name/text()'.format(id=id_user))

    return user


def courier_one(file):
    couriers = []
    for i in file['users']:

        couriers.append(i['id'])

    return couriers


