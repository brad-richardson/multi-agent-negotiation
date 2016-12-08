
import random

random.seed(0)


# All values should be in $ amounts for simplicity
class Negotiable:
    salary = 0.0
    retirement = 0.0
    benefits = 0.0
    pto = 0.0
    stock_options = 0.0
    signing_bonus = 0.0
    other = 0.0

    # Get all variables as a list for comparison
    def vars_list(self):
        return [self.salary, self.retirement, self.benefits, self.pto, self.stock_options, self.signing_bonus,
                self.other]

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
