import random
import const
import config
from classes import Negotiable, Offer, Decision


class Agent:
    id = 0
    strategy = const.Strategy
    incoming_offers = [Offer]
    pending_accept_reply = False  # sent out accept reply, awaiting response
    previous_rejected = []  # used for reject first accept second strategy, ids of rejected

    def done(self):
        return False

    def decide(self, companies, candidates):
        return Decision()

    def __repr__(self):
        return 'Id: {}, Strategy: {}'.format(self.id, self.strategy)


class Company(Agent):
    candidates_to_hire = 0
    candidates_hired = []

    def done(self):
        return len(self.candidates_hired) == self.candidates_to_hire

    def decide(self, companies, candidates):
        print('decide')
        return Decision()
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
    job_type = ''
    std_dev = 0.0  # Where candidate places themselves above or below average
    valuation = Negotiable
    accepted_with = -1  # id of company accepted with

    def done(self):
        return self.accepted_with != -1

    def decide(self, companies, candidates):
        print('decide')
        return Decision()
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
