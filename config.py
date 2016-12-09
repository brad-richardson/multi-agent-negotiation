import random
import const

random.seed(0)

MAX_STEPS = 100

COMPANY_COUNT = 1000
CANDIDATE_COUNT = 1000
COMPANY_CANDIDATES_TO_HIRE = 20

# Strategies to choose from (distributed uniformly, in order)
COMPANY_STRATEGY_ASSIGNMENT = list(const.Strategy)
CANDIDATE_STRATEGY_ASSIGNMENT = list(const.Strategy)

# Used for determining value of offers and for deciding personal valuation
# Ex: Avg $ = 100,000, CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5
#  Will generate valuation using normal distribution with 100000 as mu and 20000 as sigma (100000/5)
CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5

# Random number 1-100 rolled. If above this, offer is accepted
COMPANY_RANDOM_STRATEGY_THRESHOLD = 50
CANDIDATE_RANDOM_STRATEGY_THRESHOLD = 50

# How high above/below willing to accept
ACCEPTANCE_RADIUS_PCT = .05

# How much value is lost when a company doesn't hire all the employees they want
COMPANY_LOST_HAPPINESS_MISSING_EMPLOYEES = 0


# How far up or down to increase/decrease on negotiation
def negotiation_pct():
    return random.uniform(.02, .05)


def offer_expire_time():
    return random.randint(2, 3)
