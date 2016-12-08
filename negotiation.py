
import random
import config
from const import JOB_TYPES
from agents import Candidate, Company
from classes import Negotiable

random.seed(0)

compensation_data = {}
companies = []
candidates = []
decision_history = []

strat_index = 0


def next_strategy(is_company):
    global strat_index
    strategy = None
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


def generate_companies():
    global strat_index
    strat_index = 0
    for i in range(config.COMPANY_COUNT):
        company = Company()
        company.id = i
        company.strategy = next_strategy(is_company=True)
        company.candidates_to_hire = random.randint(1, config.CANDIDATE_COUNT/2)
        companies.append(company)


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


def start():
    global offer_matrix
    read_data()
    generate_companies()
    generate_candidates()
    offer_matrix = len(companies)*[len(candidates)*[[]]]

    total_agents = len(companies) + len(candidates)
    done_agents = 0
    curr_time = 0
    max_time = 1000
    while done_agents < total_agents and curr_time < max_time:
        done_agents = 0
        for agent in companies + candidates:
            if agent.done():
                done_agents += 1
                continue
            decision = agent.decide(companies, candidates)
            decision_history.append(decision)
        curr_time += 1

