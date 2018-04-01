# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
# </imports>


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #


class Constants(BaseConstants):
    name_in_url = 'gneezy_potters_random'
    players_per_group = 3
    endowment = (100, 100, 100, 100, 100)
    probability = (1/20, 1/3, 1/2, 2/3, 19/20)
    multiplier = (40, 6, 4, 3, 40/19)
    weight = (1/3, 1/3, 1/3)
    cum_weight = (0, 1/3, 2/3, 1)
    num_rounds = len(probability)
    instruction = True
    results = True

