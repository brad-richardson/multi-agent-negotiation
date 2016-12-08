
import random
import config
import const
from classes import Negotiable, Company, Candidate

random.seed(0)

compensation_data = {}
companies = []
candidates = []


def random_strategy():
    return random.choice(list(const.Strategy))


def generate_companies():
    count = config.COMPANY_COUNT
    if count is None:
        count = random.randint(1,100)
    for i in range(count):
        company = Company()
        company.id = i
        if config.COMPANY_STRATEGY_ASSIGNMENT is None:
            company.strategy = random_strategy()
        else:
            company.strategy = config.COMPANY_STRATEGY_ASSIGNMENT
        if config.CANDIDATE_COUNT is None:
            company.candidates_to_hire = random.randint(1, 20)
        else:
            company.candidates_to_hire = random.randint(1, config.CANDIDATE_COUNT)
        companies.append(company)


def candidate_valuation(job_type):
    return Negotiable()


def generate_candidates():
    count = config.CANDIDATE_COUNT
    if count is None:
        count = random.randint(1, 100)
    for i in range(count):
        candidate = Candidate()
        candidate.id = i
        if config.CANDIDATE_STRATEGY_ASSIGNMENT is None:
            candidate.strategy = random_strategy()
        else:
            candidate.strategy = config.CANDIDATE_STRATEGY_ASSIGNMENT
        candidate.job_type = random.choice(const.JOB_TYPES)
        candidate.valuation = candidate_valuation(candidate.job_type)
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


def negotiate():
    read_data()
    generate_companies()
    generate_candidates()

    print(companies)
    print(candidates)

