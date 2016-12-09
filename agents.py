import random
import copy
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

    def done(self):
        return False

    def act(self, companies, candidates, compensation_data, time):
        return Offer()

    @staticmethod
    def valuation(avg_valuation, std_dev):
        std_dev_divisor = config.CANDIDATE_VALUATION_STD_DEV_DIVISOR
        if std_dev_divisor is None:
            std_dev_divisor = 5
        valuation = avg_valuation
        valuation.salary += std_dev*avg_valuation.salary/std_dev_divisor
        valuation.retirement += std_dev*avg_valuation.retirement/std_dev_divisor
        valuation.benefits += std_dev*avg_valuation.benefits/std_dev_divisor
        valuation.other += std_dev*avg_valuation.other/std_dev_divisor
        return valuation

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
        self.candidate_valuations = []

    def done(self):
        return len(self.candidates_hired) == self.candidates_to_hire

    def act(self, companies, candidates, compensation_data, time):
        if self.done():
            return None
        my_offers = []
        return my_offers
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

    def decide_valuations(self, compensation_data, candidates):
        for candidate in candidates:
            std_dev = random.normalvariate(0, 1)
            valuation = Agent.valuation(compensation_data[candidate.job_type], std_dev)
            self.candidate_valuations.append((std_dev, valuation))
        return


class Candidate(Agent):

    def __init__(self):
        super(Candidate, self).__init__()
        self.job_type = ''
        self.std_dev = 0.0  # Where candidate places themselves above or below average
        self.valuation = Negotiable()
        self.avg_valuation = Negotiable()
        self.accepted_with = -1  # id of company accepted with
        self.previous_rejected = []  # used for reject first accept second strategy, ids of rejected

    def done(self):
        return self.accepted_with != -1

    def has_rejected(self, company_idx):
        return company_idx in self.previous_rejected

    def is_satisified(self, offer):
        return offer.total() >= self.valuation.total()

    def negotiate(self, offer):
        return offer.increase_by_pct(config.CANDIDATE_NEGOTIATION_PCT)

    def act(self, companies, candidates, compensation_data, time):
        if self.done():
            return None
        my_offers = []

        for offer in sorted(self.inbox, reverse=True):
            if self.strategy == Strategy.accept_first:
                my_offers.append(offer.change_action(Action.accept))
                break
            elif self.strategy == Strategy.reject_first_accept_second:
                if self.has_rejected(offer.company):
                    my_offers.append(offer.change_action(Action.accept))
                    break
                else:
                    my_offers.append(offer.change_action(Action.reject))
                    self.previous_rejected.append(my_offer.company)
            elif self.strategy == Strategy.randomly_accept:
                die = random.randint(1, 100)
                if die >= config.CANDIDATE_RANDOM_STRATEGY_THRESHOLD:
                    my_offers.append(offer.change_action(Action.accept))
                    break
                else:
                    my_offers.append(offer.change_action(Action.reject))
            elif self.strategy == Strategy.negotiate_until_satisfied:
                if self.is_satisified(offer):
                    my_offers.append(offer.change_action(Action.accept))
                    break
                else:
                    my_offers.append(self.negotiate(offer.change_action(Action.propose)))
            elif self.strategy == Strategy.negotiate_once:
                if self.has_rejected(offer.company):
                    my_offers.append(offer.change_action(Action.accept))
                    break
                else:
                    my_offers.append(self.negotiate(offer.change_action(Action.propose)))
                    self.previous_rejected.append(offer.company)

        for my_offer in my_offers:
            my_offer.sender_is_company = False
            if my_offer.action == Action.accept:
                self.accepted_with = my_offer.company
        return my_offers

    def decide_valuation(self, avg_valuation):
        self.std_dev = random.normalvariate(0, 1)
        self.avg_valuation = avg_valuation
        self.valuation = Agent.valuation(avg_valuation, self.std_dev)
        return

