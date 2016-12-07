# Brad Richardson
# Multi-Agent
# Final project: Job offer negotiation

from enum import Enum
import operator
import const

EMPLOYEE_COUNT = 20
EMPLOYER_COUNT = 1


# All values should be in $ amounts for simplicity
class Negotiable:
    salary = 0.0
    retirement = 0.0
    benefits = 0.0
    pto = 0.0
    stock_options = 0.0
    signing_bonus = 0.0
    other = 0.0

    def vars_list(self):
        return [self.salary, self.retirement, self.benefits, self.pto, self.stock_options, self.signing_bonus, self.other]

    def total(self):
        return round(sum(self.vars_list()), 2)

    def __eq__(self, other):
        return self.vars_list() == other.vars_list()

    def __lt__(self, other):
        return self.total() < other.total()

    def __repr__(self):
        return 'Salary: {:.2f}, Pto: {:.2f}, Retirement: {:.2f}, Benefits: {:.2f}, Stock: {:.2f}, Signing: {:.2f}, ' \
               'Other: {:.2f}'.format(self.salary, self.pto, self.retirement, self.benefits, self.stock_options,
                                      self.signing_bonus, self.other)

    def __str__(self):
        return self.__repr__()


class Offer(Negotiable):
    is_counter = False
    creator = 0  # id of creator?

    def __init__(self):
        print("Offer")


class Strategy(Enum):
    accept_first = 1
    reject_first_accept_second = 2
    randomly_accept = 3
    negotiate_until_all_met = 4
    negotiate_until_only_important_met = 5
    negotiate_once = 6


def main():
    sfrawdata = []
    with open('data/sf-compensation.csv', 'r') as f:
        for idx, line in enumerate(f):
            if idx == 0 or line == "":
                continue
            sfrawdata.append(line.replace('\n', '').split(','))

    print(sfrawdata)

    sfdata = {}
    for data in sfrawdata:
        title = data[0]
        valuation = Negotiable()
        valuation.salary = float(data[1])
        valuation.retirement = float(data[2])
        valuation.benefits = float(data[3])
        valuation.other = float(data[4])
        sfdata[title] = valuation
        print(valuation.total())

    sorteddata = sorted(sfdata.items(), key=operator.itemgetter(1), reverse=True)
    print(sorteddata)


if __name__ == '__main__':
    main()
