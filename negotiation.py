import random
import math
import config
from const import JOB_TYPES, Action, Strategy
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
        company.candidates_to_hire = config.COMPANY_CANDIDATES_TO_HIRE
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
    companies_total = 0
    companies_strategy_count = {}
    companies_results = {}
    companies_done = {}
    candidates_total = 0
    candidates_results = {}
    candidates_strategy_count = {}
    candidates_done = {}

    # used for debugging
    candidates_committed = len(candidates)*[0]
    companies_committed = len(companies)*[0]

    for company in companies:
        happiness = company.happiness()
        companies_total += happiness
        strat = company.strategy
        done = int(company.done())
        accepted = [o.candidate for o in company.accepted_offers]
        for candidate in accepted:
            candidates_committed[candidate] += 1
        if strat not in companies_results:
            companies_results[strat] = happiness
            companies_strategy_count[strat] = 1
            companies_done[strat] = done
        else:
            companies_results[strat] += happiness
            companies_strategy_count[strat] += 1
            companies_done[strat] += done
    for candidate in candidates:
        happiness = candidate.happiness()
        candidates_total += happiness
        strat = candidate.strategy
        done = int(candidate.done())
        if len(candidate.accepted_offers) > 0:
            companies_committed[candidate.accepted_offers[0].company] += 1
        if strat not in candidates_results:
            candidates_results[strat] = happiness
            candidates_strategy_count[strat] = 1
            candidates_done[strat] = done
        else:
            candidates_results[strat] += happiness
            candidates_strategy_count[strat] += 1
            candidates_done[strat] += done
        # if strat == Strategy.negotiate_until_satisfied:
            # print(happiness)

    print(candidates_committed)
    print(companies_committed)
    companies_avg = companies_total/len(companies)
    candidates_avg = candidates_total/len(candidates)

    print("===============================")
    print("== COMPANIES ==")
    print("Average happiness: ${:.2f}".format(companies_avg))
    for key, value in companies_results.items():
        count = companies_strategy_count[key]
        print("{} avg: ${:.2f}".format(key, value/count)) # (done: {}/{}) companies_done[key], count

    print("===============================")
    print("== CANDIDATES ==")
    print("Average happiness: ${:.2f}".format(candidates_avg))
    for key, value in candidates_results.items():
        count = candidates_strategy_count[key]
        print("{} avg: ${:.2f}".format(key, value/count)) # candidates_done[key], count

    print("===============================")
    print("== TOTAL ==")
    print("Average happiness: ${:.2f}".format((companies_total + candidates_total)/len(companies+candidates)))
    for key in companies_results.keys():
        sum = companies_results[key] + candidates_results[key]
        count = companies_strategy_count[key] + candidates_strategy_count[key]
        print("{} avg: ${:.2f}".format(key, sum/count))


def start():
    print("Reading data...")
    read_data()
    print("Generating agents...")
    generate_candidates()
    generate_companies()

    done_companies = 0
    done_candidates = 0
    curr_time = 0
    max_time = config.MAX_STEPS
    print("Running negotiations with {} companies and {} candidates (max steps: {}):"
          .format(config.COMPANY_COUNT, config.CANDIDATE_COUNT, max_time))
    while (done_companies < len(companies) or done_candidates < len(candidates)) and curr_time < max_time:
        curr_offers = []
        done_companies = 0
        done_candidates = 0
        for agent in companies:
            if agent.done():
                done_companies += 1
            offers = agent.act(companies, candidates, compensation_data, curr_time)
            curr_offers.extend(offers)
        for agent in candidates:
            if agent.done():
                done_candidates += 1
                continue
            offers = agent.act(companies, candidates, compensation_data, curr_time)
            curr_offers.extend(offers)
        for offer in curr_offers:
            if offer.sender_is_company:
                candidates[offer.candidate].give(offer)
            else:
                companies[offer.company].give(offer)
            offer_history.append(offer)

        curr_time += 1

        intervals = 1
        if max_time > 10:
            intervals = round(max_time/10)
        if curr_time % intervals == 0:
            print("At step: {}".format(curr_time))
    print("Finished after {} steps".format(curr_time))

    output_results()
