# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
# </imports>


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #


class Constants(BaseConstants):
    name_in_url = 'gneezy_potters_group'
    players_per_group = 3
    endowment = (100, 100, 100, 100,100)
    probability = (1/20, 1/3, 1/2, 2/3, 19/20)
    multiplier = (40, 6, 4, 3, 40/19)
    num_rounds = len(probability)
    instruction = True
    results = True