import random
import const
import config
from classes import Negotiable


class Agent:
    id = 0
    strategy = const.Strategy.accept_first

    def done(self):
        return False

    def __repr__(self):
        return 'Id: {}, Strategy: {}'.format(self.id, self.strategy)


class Company(Agent):
    candidates_to_hire = 0
    candidates_hired = []

    def done(self):
        return len(self.candidates_hired) == self.candidates_to_hire


class Candidate(Agent):
    job_type = ''
    std_dev = 0.0  # Where candidate places themselves above or below average
    valuation = Negotiable()
    accepted_with = -1 # id of company accepted with

    def done(self):
        return self.accepted_with != -1

    def decide_valuation(self, avg_valuation):
        self.std_dev = random.normalvariate(0, 1)
        std_dev_divisor = config.CANDIDATE_VALUATION_STD_DEV_DIVISOR
        if std_dev_divisor is None:
            std_dev_divisor = 5
        self.valuation = avg_valuation
        self.valuation.salary += self.std_dev*avg_valuation.salary/std_dev_divisor
        self.valuation.retirement += self.std_dev*avg_valuation.retirement/std_dev_divisor
        self.valuation.benefits += self.std_dev*avg_valuation.benefits/std_dev_divisor
        self.valuation.other += self.std_dev*avg_valuation.other/std_dev_divisor
