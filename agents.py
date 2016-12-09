import random
import math
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
        self.accepted_offers = []
        self.previous_rejected = []  # used for reject first accept second strategy, ids of rejected

    def done(self):
        return False

    def act(self, companies, candidates, compensation_data, time):
        return Offer()

    # Called after found a job
    def happiness(self):
        return 0

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

    @staticmethod
    def negotiate_down(offer):
        return offer.increase_by_pct(-1*config.negotiation_pct())

    @staticmethod
    def negotiate_up(offer):
        return offer.increase_by_pct(config.negotiation_pct())

    def has_rejected(self, idx):
        return idx in self.previous_rejected

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
        self.pending_offers = {}

    def done(self):
        return len(self.candidates_hired) == self.candidates_to_hire

    # if <= valuation of candidate, satisfied with offer
    def is_satisfied(self, offer):
        valuation_total = self.candidate_valuations[offer.candidate][1].total()
        radius = config.ACCEPTANCE_RADIUS_PCT*valuation_total
        return (offer.total() - valuation_total) <= radius

    # Called after found a job
    def happiness(self):
        happiness = 0.0
        for offer in self.accepted_offers:
            valuation = self.candidate_valuations[offer.candidate][1]
            happiness += valuation.total() - offer.total()
        return happiness

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
                self.accepted_offers.append(offer)
                continue

            # Handle incoming offers
            if offer.action == Action.propose:
                if self.strategy == Strategy.accept_first:
                    my_offers.append(offer.change_action(offer, Action.accept))
                elif self.strategy == Strategy.reject_first_accept_second:
                    if self.has_rejected(offer.candidate):
                        my_offers.append(offer.change_action(offer, Action.accept))
                    else:
                        my_offers.append(self.negotiate_down(offer.change_action(offer, Action.propose)))
                        self.previous_rejected.append(offer.candidate)
                elif self.strategy == Strategy.randomly_accept:
                    die = random.randint(1, 100)
                    if die >= config.COMPANY_RANDOM_STRATEGY_THRESHOLD:
                        my_offers.append(offer.change_action(offer, Action.accept))
                    else:
                        my_offers.append(self.negotiate_down(offer.change_action(offer, Action.propose)))
                elif self.strategy == Strategy.negotiate_until_satisfied:
                    if self.is_satisfied(offer):
                        my_offers.append(offer.change_action(offer, Action.accept))
                    else:
                        my_offers.append(self.negotiate_down(offer.change_action(offer, Action.propose)))
                elif self.strategy == Strategy.negotiate_once:
                    if self.has_rejected(offer.candidate):
                        my_offers.append(offer.change_action(offer, Action.accept))
                    else:
                        my_offers.append(self.negotiate_down(offer.change_action(offer, Action.propose)))
                        self.previous_rejected.append(offer.candidate)
            pending += 1
        self.inbox.clear()

        # If need to fill spots still, send new offers
        all_candidates = set([c.id for c in candidates])
        hired_candidates = set(self.candidates_hired)
        pending_candidates = set([o.candidate for o in my_offers] + list(self.pending_offers.keys()))
        potential_candidates = list(all_candidates ^ hired_candidates ^ pending_candidates)
        offers_to_send = math.ceil(min(self.candidates_to_hire - len(hired_candidates) - len(pending_candidates),
                                       len(potential_candidates))/2)
        for i in range(offers_to_send):
            curr = random.choice(potential_candidates)
            potential_candidates.remove(curr)
            valuation = self.candidate_valuations[curr][1]
            new_offer = Offer()
            new_offer.salary = valuation.salary
            new_offer.retirement = valuation.retirement
            new_offer.benefits = valuation.benefits
            new_offer.other = valuation.other
            new_offer.increase_by_pct(-1*config.negotiation_pct())
            new_offer.action = Action.propose
            new_offer.candidate = curr
            new_offer.company = self.id
            my_offers.append(new_offer)

        for my_offer in my_offers:
            my_offer.sender_is_company = True
            self.pending_offers[my_offer.candidate] = my_offer
            if my_offer.action == Action.accept:
                self.candidates_hired.append(my_offer.candidate)
                self.accepted_offers.append(my_offer)
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

    def done(self):
        return len(self.accepted_offers) > 0

    # if >= valuation of candidate, satisfied with offer
    def is_satisfied(self, offer):
        radius = config.ACCEPTANCE_RADIUS_PCT*self.valuation.total()
        return (self.valuation.total() - offer.total()) <= radius

    # Called after found a job
    def happiness(self):
        return self.valuation.total() - self.accepted_offers[0].total()

    def act(self, companies, candidates, compensation_data, time):
        if self.done():
            return None
        my_offers = []

        for offer in sorted(self.inbox, reverse=True):
            if offer.action == Action.accept:
                my_offers.clear()
                self.accepted_offers.append(offer)
                break

            if offer.action == Action.propose:
                if self.strategy == Strategy.accept_first:
                    my_offers.append(offer.change_action(offer, Action.accept))
                    break
                elif self.strategy == Strategy.reject_first_accept_second:
                    if self.has_rejected(offer.company):
                        my_offers.append(offer.change_action(offer, Action.accept))
                        break
                    else:
                        my_offers.append(self.negotiate_up(offer.change_action(offer, Action.propose)))
                        self.previous_rejected.append(offer.company)
                elif self.strategy == Strategy.randomly_accept:
                    die = random.randint(1, 100)
                    if die >= config.CANDIDATE_RANDOM_STRATEGY_THRESHOLD:
                        my_offers.append(offer.change_action(offer, Action.accept))
                        break
                    else:
                        my_offers.append(self.negotiate_up(offer.change_action(offer, Action.propose)))
                elif self.strategy == Strategy.negotiate_until_satisfied:
                    if self.is_satisfied(offer):
                        my_offers.append(offer.change_action(offer, Action.accept))
                        break
                    else:
                        my_offers.append(self.negotiate_up(offer.change_action(offer, Action.propose)))
                elif self.strategy == Strategy.negotiate_once:
                    if self.has_rejected(offer.company):
                        my_offers.append(offer.change_action(offer, Action.accept))
                        break
                    else:
                        my_offers.append(self.negotiate_up(Offer.change_action(offer, Action.propose)))
                        self.previous_rejected.append(offer.company)
        self.inbox.clear()

        for my_offer in my_offers:
            my_offer.sender_is_company = False
            if my_offer.action == Action.accept:
                self.accepted_offers.append(my_offer)
        return my_offers

    def decide_valuation(self, avg_valuation):
        self.std_dev = random.normalvariate(0, 1)
        self.avg_valuation = avg_valuation
        self.valuation = Agent.valuation(avg_valuation, self.std_dev)
        return
