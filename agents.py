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
        self.previous_rejected = []  # used for reject first accept second strategy, ids of rejected

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

    def has_rejected(self, candidate_idx):
        return candidate_idx in self.previous_rejected

    # if <= valuation of candidate, satisfied with offer
    def is_satisfied(self, offer):
        return offer.total() <= self.candidate_valuations[offer.candidate][1].total()

    def negotiate(self, offer):
        return offer.increase_by_pct(-1*config.COMPANY_NEGOTIATION_PCT)

    def act(self, companies, candidates, compensation_data, time):
        if self.done():
            return None
        my_offers = []
        pending = 0

        for offer in sorted(self.inbox):
            # Reached limit, reject offers
            if len(self.candidates_hired) + pending >= self.candidates_to_hire:
                my_offers.append(offer.change_action(Action.reject))
                break

            # Acknowledge acceptance
            if offer.action == Action.accept:
                self.candidates_hired.append(offer.candidate)
                continue

            # Handle incoming offers
            if offer.action == Action.propose:
                if self.strategy == Strategy.accept_first:
                    my_offers.append(offer.change_action(Action.accept))
                elif self.strategy == Strategy.reject_first_accept_second:
                    if self.has_rejected(offer.candidate):
                        my_offers.append(offer.change_action(Action.accept))
                    else:
                        my_offers.append(self.negotiate(offer.change_action(Action.propose)))
                elif self.strategy == Strategy.randomly_accept:
                    die = random.randint(1, 100)
                    if die >= config.COMPANY_RANDOM_STRATEGY_THRESHOLD:
                        my_offers.append(offer.change_action(Action.accept))
                    else:
                        my_offers.append(self.negotiate(offer.change_action(Action.propose)))
                elif self.strategy == Strategy.negotiate_until_satisfied:
                    if self.is_satisfied(offer):
                        my_offers.append(offer.change_action(Action.accept))
                    else:
                        my_offers.append(self.negotiate(offer.change_action(Action.propose)))
                elif self.strategy == Strategy.negotiate_once:
                    if self.has_rejected(offer.candidate):
                        my_offers.append(offer.change_action(Action.accept))
                    else:
                        my_offers.append(self.negotiate(offer.change_action(Action.propose)))
            pending += 1

        for my_offer in my_offers:
            my_offer.sender_is_company = True
            if my_offer.action == Action.accept:
                self.candidates_hired.append(my_offer.candidate)
            elif my_offer.action == Action.reject:
                self.previous_rejected.append(my_offer.candidate)
        return my_offers

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

    def done(self):
        return self.accepted_with != -1

    def has_rejected(self, company_idx):
        return company_idx in self.previous_rejected

    def is_satisfied(self, offer):
        return offer.total() >= self.valuation.total()

    def negotiate(self, offer, sign=1):
        return offer.increase_by_pct(sign*config.CANDIDATE_NEGOTIATION_PCT)

    def act(self, companies, candidates, compensation_data, time):
        if self.done():
            return None
        my_offers = []

        for offer in sorted(self.inbox, reverse=True):
            if offer.action == Action.accept:
                my_offers.clear()
                self.accepted_with = offer.company
                break

            if offer.action == Action.propose:
                if self.strategy == Strategy.accept_first:
                    my_offers.append(offer.change_action(Action.accept))
                    break
                elif self.strategy == Strategy.reject_first_accept_second:
                    if self.has_rejected(offer.company):
                        my_offers.append(offer.change_action(Action.accept))
                        break
                    else:
                        my_offers.append(self.negotiate(offer.change_action(Action.reject)))
                elif self.strategy == Strategy.randomly_accept:
                    die = random.randint(1, 100)
                    if die >= config.CANDIDATE_RANDOM_STRATEGY_THRESHOLD:
                        my_offers.append(offer.change_action(Action.accept))
                        break
                    else:
                        my_offers.append(self.negotiate(offer.change_action(Action.propose)))
                elif self.strategy == Strategy.negotiate_until_satisfied:
                    if self.is_satisfied(offer):
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

        for my_offer in my_offers:
            my_offer.sender_is_company = False
            if my_offer.action == Action.accept:
                self.accepted_with = my_offer.company
            elif my_offer.action == Action.reject:
                self.previous_rejected.append(my_offer.company)
        return my_offers

    def decide_valuation(self, avg_valuation):
        self.std_dev = random.normalvariate(0, 1)
        self.avg_valuation = avg_valuation
        self.valuation = Agent.valuation(avg_valuation, self.std_dev)
        return

