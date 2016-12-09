import const

COMPANY_COUNT = 1
CANDIDATE_COUNT = 1

# Strategies to choose from (distributed uniformly, in order)
COMPANY_STRATEGY_ASSIGNMENT = [const.Strategy.accept_first]  # list(const.Strategy)
CANDIDATE_STRATEGY_ASSIGNMENT = [const.Strategy.negotiate_once]  # list(const.Strategy)

# Used for determining value of offers and for deciding personal valuation
# Ex: Avg $ = 100,000, CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5
#  Will generate valuation using normal distribution with 100000 as mu and 20000 as sigma (100000/5)
CANDIDATE_VALUATION_STD_DEV_DIVISOR = 5

# Random number 1-100 rolled. If above this, offer is accepted
COMPANY_RANDOM_STRATEGY_THRESHOLD = 90
CANDIDATE_RANDOM_STRATEGY_THRESHOLD = 90

# When <= this many incoming, send new offer
COMPANY_PROPOSE_THRESHOLD = 0
CANDIDATE_PROPOSE_THRESHOLD = 0

# How far up or down to negotiate
COMPANY_NEGOTIATION_PCT = .05
CANDIDATE_NEGOTIATION_PCT = .05