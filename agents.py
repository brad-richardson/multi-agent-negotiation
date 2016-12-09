import random
from const import Action, Strategy
import config
from classes import Negotiable, Offer

random.seed(0)


class Agent:

    def __init__(self):
        self.id = 0
        self.strategy = Strategy
        self.pending_accept_reply = False  # sent out accept reply, awaiting responseself.
        self.inbox = []
        self.previous_rejected = []  # used for reject first accept second strategy, ids of rejected

    def done(self):
        return False

    def decide(self, companies, candidates, compensation_data):
        return Offer()

    def give(self, decision):
        self.inbox.append(decision)

    def __repr__(self):
        return '<{} #{}, {}, offers: {}, done? {}>'.format(type(self).__name__, self.id, self.strategy, len(self.inbox),
                                                           self.done())


class Company(Agent):

    def __init__(self):
        super(Company, self).__init__()
        self.candidates_to_hire = 0
        self.candidates_hired = []

    def done(self):
        return len(self.candidates_hired) == self.candidates_to_hire

    def decide(self, companies, candidates, compensation_data):
        sorted_offers = sorted(self.inbox)
        print(sorted_offers)

        offer = Offer()
        offer.sender_is_company = True

        return offer
        # Process:
        # 1. Look at pending offers
        # 2. Sort to find best offers
        # 3. Determine what to do based on strategy and pending offers



        # # Do these action inside agents?
        # if action == Action.propose:
        #     print("propose")
        # elif action == Action.nothing:
        #     print("nothing")
        # elif action == Action.reject:
        #     print("reject")
        # elif action == Action.accept:
        #     print("accept")
        # # Need to send data along
        # if action != action.nothing:
        #     print("do stuff")


class Candidate(Agent):

    def __init__(self):
        super(Candidate, self).__init__()
        self.job_type = ''
        self.std_dev = 0.0  # Where candidate places themselves above or below average
        self.valuation = Negotiable
        self.accepted_with = -1  # id of company accepted with

    def done(self):
        return self.accepted_with != -1

    def decide(self, companies, candidates, compensation_data):
        offer = Offer()
        offer.sender_is_company = False
        offer.action = Action.nothing
        return offer

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
