# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
# </imports>


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #


class Constants(BaseConstants):
    name_in_url = 'certainty_eq'
    # group size
    players_per_group = None
    # CE part individual endowment
    endowment = (100, 100, 100, 100, 100, 100, 100, 100, 100, 100)
    # lottery payoff with specified probability
    lottery_hi = (100, 100, 100, 100, 100, -100, -100, -100, -100, -100)
    # lottery payoff with the rest probability
    lottery_lo = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # probability of gain or loss
    probability = (0.05, 0.25, 0.50, 0.75, 0.95, 0.05, 0.25, 0.50, 0.75, 0.95)
    # multiplier = return rate + 1
    # num_rounds = len(probability)
    num_rounds = 3
    # toggle for results
    results = False