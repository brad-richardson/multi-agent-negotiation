
import random
import config
import const
from agents import Candidate, Company
from classes import Negotiable

random.seed(0)

compensation_data = {}
companies = []
candidates = []
offer_matrix = [[[]]]  # idx1 - company, idx2 - candidate, idx3 - offer number
offer_history = []


def random_strategy():
    return random.choice(list(const.Strategy))


def generate_companies():
    for i in range(config.COMPANY_COUNT):
        company = Company()
        company.id = i
        company.strategy = config.COMPANY_STRATEGY_ASSIGNMENT
        company.candidates_to_hire = random.randint(1, config.CANDIDATE_COUNT/2)
        companies.append(company)


def generate_candidates():
    for i in range(config.CANDIDATE_COUNT):
        candidate = Candidate()
        candidate.id = i
        candidate.strategy = config.CANDIDATE_STRATEGY_ASSIGNMENT
        candidate.job_type = random.choice(const.JOB_TYPES)
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


def store_new_offer(company_id, candidate_id, offer):
    offer_history.append(offer)
    offer_matrix[company_id][candidate_id].append(offer)


def negotiate():
    global offer_matrix
    read_data()
    generate_companies()
    generate_candidates()
    offer_matrix = len(companies)*[len(candidates)*[[]]]

    total_agents = len(companies) + len(candidates)
    done_agents = 0
    while done_agents < total_agents:
        done_agents = 0
        for agent in companies + candidates:
            if agent.done():
                done_agents += 1



