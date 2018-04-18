# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
# </imports>


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #


class Constants(BaseConstants):
    name_in_url = 'gneezy_potters'
    # group size
    players_per_group = None
    # endowment amount for each different round
    endowment = (100, 100, 100, 100, 100)
    # probability of success
    probability = (1/20, 1/4, 1/2, 3/4, 19/20)
    # multiplier = return rate + 1
    multiplier = (30, 6, 3, 2, 30/19)
    # the number of total rounds
    num_rounds = len(probability)
    # whether GP game is used after the CE task
    combined = True

