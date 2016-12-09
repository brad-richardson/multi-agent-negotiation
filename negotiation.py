import random
import math
import config
from const import JOB_TYPES, Action
from agents import Candidate, Company
from classes import Negotiable

random.seed(0)

compensation_data = {}
companies = []
candidates = []
offer_history = []

strat_index = 0


def next_strategy(is_company):
    global strat_index
    if is_company:
        if strat_index >= len(config.COMPANY_STRATEGY_ASSIGNMENT):
            strat_index = 0
        strategy = config.COMPANY_STRATEGY_ASSIGNMENT[strat_index]
    else:
        if strat_index >= len(config.CANDIDATE_STRATEGY_ASSIGNMENT):
            strat_index = 0
        strategy = config.CANDIDATE_STRATEGY_ASSIGNMENT[strat_index]
    strat_index += 1
    return strategy


def generate_candidates():
    global strat_index
    strat_index = 0
    for i in range(config.CANDIDATE_COUNT):
        candidate = Candidate()
        candidate.id = i
        candidate.strategy = next_strategy(is_company=False)
        candidate.job_type = random.choice(JOB_TYPES)
        candidate.decide_valuation(compensation_data[candidate.job_type])
        candidates.append(candidate)


# Must be called after generate_candidates
def generate_companies():
    global strat_index
    strat_index = 0
    for i in range(config.COMPANY_COUNT):
        company = Company()
        company.id = i
        company.strategy = next_strategy(is_company=True)
        company.candidates_to_hire = random.randint(1, math.ceil(len(candidates)/2))
        company.decide_valuations(compensation_data, candidates)
        companies.append(company)


def read_data():
    sfrawdata = []
    with open('data/sf-compensation.csv', 'r') as f:
        for idx, line in enumerate(f):
            if idx == 0 or line == "":
                continue
            sfrawdata.append(line.replace('\n', '').split(','))

    for data in sfrawdata:
        title = data[0]
        valuation = Negotiable()
        valuation.salary = float(data[1])
        valuation.retirement = float(data[2])
        valuation.benefits = float(data[3])
        valuation.other = float(data[4])
        compensation_data[title] = valuation


def output_results():
    for company in companies:
        print(company.happiness())
    for candidate in candidates:
        print(candidate.happiness())


def start():
    read_data()
    generate_candidates()
    generate_companies()

    total_agents = len(companies) + len(candidates)
    done_agents = 0
    curr_time = 0
    max_time = 1000
    print("Running negotiations with {} companies and {} candidates (max steps: {}):"
          .format(config.COMPANY_COUNT, config.CANDIDATE_COUNT, max_time))
    while done_agents < total_agents and curr_time < max_time:
        curr_offers = []
        done_agents = 0
        for agent in companies + candidates:
            if agent.done():
                done_agents += 1
                continue
            offers = agent.act(companies, candidates, compensation_data, curr_time)
            curr_offers.extend(offers)
        for offer in curr_offers:
            if offer.action == Action.nothing:
                continue
            else:
                if offer.sender_is_company:
                    candidates[offer.candidate].give(offer)
                else:
                    companies[offer.company].give(offer)
                offer_history.append(offer)

        curr_time += 1
        if curr_time % 10 == 0:
            print("At step: {}".format(curr_time))
    print("Finished after {} steps".format(curr_time))

    output_results()
