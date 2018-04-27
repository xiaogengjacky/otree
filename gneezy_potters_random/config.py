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
    endowment = (300, 300, 300, 300, 300)
    # probability of success
    probability = (1 / 20, 1 / 4, 1 / 2, 3 / 4, 19 / 20)
    multiplier = (30, 6, 3, 2, 30 / 19)
    weight = (1/3, 1/3, 1/3)
    cum_weight = (0, 1/3, 2/3, 1)
    # the number of total rounds
    num_rounds = len(probability)
    # whether GP game is used after the CE task
    combined = True
    # toggle anonymity
    anonymous = True


