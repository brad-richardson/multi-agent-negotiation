import random
import time
import config
from const import JOB_TYPES
from agents import Candidate, Company
from classes import Negotiable

random.seed(0)

compensation_data = {}
companies = []
candidates = []
offer_history = []
global_file = open('out/all.txt', 'w')
curr_file = None

global_company_strat_results = {}
global_candidate_strat_results = {}

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


def generate_candidates(count):
    global strat_index, candidates
    strat_index = 0
    candidates = []
    for i in range(count):
        candidate = Candidate()
        candidate.id = i
        candidate.strategy = next_strategy(is_company=False)
        candidate.job_type = random.choice(JOB_TYPES)
        candidate.decide_valuation(compensation_data[candidate.job_type])
        candidates.append(candidate)


# Must be called after generate_candidates
def generate_companies(count):
    global strat_index, companies
    strat_index = 0
    companies = []
    for i in range(count):
        company = Company()
        company.id = i
        company.strategy = next_strategy(is_company=True)
        company.candidates_to_hire = config.company_candidates_to_hire(count, len(candidates))
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
            global_company_strat_results[strat] = [happiness]
        else:
            companies_results[strat] += happiness
            companies_strategy_count[strat] += 1
            companies_done[strat] += done
            global_company_strat_results[strat].append(happiness)
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
            global_candidate_strat_results[strat] = [happiness]
        else:
            candidates_results[strat] += happiness
            candidates_strategy_count[strat] += 1
            candidates_done[strat] += done
            global_candidate_strat_results[strat].append(happiness)
        # if strat == Strategy.negotiate_until_satisfied:
            # print(happiness)

    # print(candidates_committed)
    # print(companies_committed)
    companies_avg = companies_total/len(companies)
    candidates_avg = candidates_total/len(candidates)

    output("===============================")
    output("== COMPANIES ==")
    output("Average happiness: ${:.2f}".format(companies_avg))
    for key, value in companies_results.items():
        count = companies_strategy_count[key]
        output("{} avg: ${:.2f}".format(key, value/count))  # (done: {}/{}) companies_done[key], count

    output("===============================")
    output("== CANDIDATES ==")
    output("Average happiness: ${:.2f}".format(candidates_avg))
    for key, value in candidates_results.items():
        count = candidates_strategy_count[key]
        output("{} avg: ${:.2f}".format(key, value/count))  # candidates_done[key], count

    output("===============================")
    output("== TOTAL ==")
    output("Average happiness: ${:.2f}".format((companies_total + candidates_total)/len(companies+candidates)))
    for key in companies_results.keys():
        total = companies_results[key]
        count = companies_strategy_count[key]
        if key in candidates_results.keys():
            total += candidates_results[key]
            count += candidates_strategy_count[key]
        output("{} avg: ${:.2f}".format(key, total/count))


def output(output_str):
    curr_file.write(output_str + "\n")
    global_file.write(output_str + "\n")


def run_iteration(max_time, company_count, candidate_count):
    global curr_file

    t = time.time()
    print("Generating agents...")
    generate_candidates(company_count)
    generate_companies(candidate_count)

    with open("out/{}-{}-{}.txt".format(max_time, company_count, candidate_count), 'w') as curr_file:
        done_companies = 0
        done_candidates = 0
        curr_time = 0
        output_str = "Running negotiations with {} companies and {} candidates (max steps: {}):" \
            .format(company_count, candidate_count, max_time)
        print(output_str)
        output(output_str)
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
                intervals = round(max_time / 10)
            if curr_time % intervals == 0:
                print("At step: {}".format(curr_time))
        output("Finished after {} steps".format(curr_time))
        output_results()
        output_str = "Ran for: {:.2f} seconds".format(time.time() - t)
        print(output_str)
        output(output_str)


def output_final_results():
    for key in global_candidate_strat_results.keys():
        print(key)
        global_file.write(str(key) + "\n")
        comp = global_company_strat_results[key]
        cand = global_candidate_strat_results[key]
        global_file.write(", ".join(str(c) for c in sorted(comp)) + "\n")
        global_file.write(", ".join(str(c) for c in sorted(cand)) + "\n")

        overall = comp + cand
        output_str = "Average for companies: ${:.2f}\nAverage for candidates: ${:.2f}\nAverage overall: ${:.2f}"\
            .format(sum(comp)/len(comp), sum(cand)/len(cand), sum(overall)/len(overall))
        print(output_str)
        global_file.write(output_str + "\n")


def start():
    global curr_file
    print("Reading data...")
    read_data()

    step_options = config.STEP_COUNTS  # [5, 10, 50, 100]
    company_options = config.COMPANY_COUNTS  # [1, 5, 10, 50, 100, 500, 1000]
    candidate_options = config.CANDIDATE_COUNTS  # [1, 5, 10, 50, 100, 500, 1000]

    for max_time in step_options:
        for company_count in company_options:
            for candidate_count in candidate_options:
                run_iteration(max_time, company_count, candidate_count)

    output_final_results()
    global_file.close()
