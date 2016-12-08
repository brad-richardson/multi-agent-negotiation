import operator
from classes import Negotiable


def negotiate():
    sfrawdata = []
    with open('data/sf-compensation.csv', 'r') as f:
        for idx, line in enumerate(f):
            if idx == 0 or line == "":
                continue
            sfrawdata.append(line.replace('\n', '').split(','))

    sfdata = {}
    for data in sfrawdata:
        title = data[0]
        valuation = Negotiable()
        valuation.salary = float(data[1])
        valuation.retirement = float(data[2])
        valuation.benefits = float(data[3])
        valuation.other = float(data[4])
        sfdata[title] = valuation

