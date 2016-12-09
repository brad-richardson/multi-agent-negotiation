import random
import const

random.seed(0)

COMPANY_COUNT = 1000
CANDIDATE_COUNT = 1000

# Strategies to choose from (distributed uniformly, in order)
COMPANY_STRATEGY_ASSIGNMENT = list(const.Strategy)
CANDIDATE_STRATEGY_ASSIGNMENT = list(const.Strategy)

# Used for determining value of offers and for deciding personal valuation
# Ex: Avg $ = 100,000, CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5
#  Will generate valuation using normal distribution with 100000 as mu and 20000 as sigma (100000/5)
CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5

# Random number 1-100 rolled. If above this, offer is accepted
COMPANY_RANDOM_STRATEGY_THRESHOLD = 90
CANDIDATE_RANDOM_STRATEGY_THRESHOLD = 90

# How high above/below willing to accept
ACCEPTANCE_RADIUS_PCT = .1


# How far up or down to increase/decrease on negotiation
def negotiation_pct():
    return random.uniform(.01, .1)