import random
import const

random.seed(0)

# For random values on these values, set to 'None'
COMPANY_COUNT = 1
CANDIDATE_COUNT = 1

# Strategies to choose from (distributed uniformly, in order)
COMPANY_STRATEGY_ASSIGNMENT = [const.Strategy.accept_first] # list(const.Strategy)
CANDIDATE_STRATEGY_ASSIGNMENT = [const.Strategy.negotiate_once] # list(const.Strategy)

# Used for determining value of offers and for deciding personal valuation
# Ex: Avg $ = 100,000, CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5
#  Will generate valuation using normal distribution with 100000 as mu and 20000 as sigma (100000/5)
CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5

if COMPANY_COUNT is None:
    COMPANY_COUNT = random.randint(1, 100)
if CANDIDATE_COUNT is None:
    CANDIDATE_COUNT = random.randint(1, 100)
