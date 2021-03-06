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
    endowment = (300, 300, 300, 300, 300)
    # probability of success
    probability = (1 / 20, 1 / 4, 1 / 2, 3 / 4, 19 / 20)
    # multiplier = return rate + 1
    multiplier = (30, 6, 3, 2, 30 / 19)
    # the number of total rounds
    num_rounds = len(probability)
    # num_rounds = 2
    # whether GP game is used after the CE task
    combined = True
    # Toggle for anonymity
    anonymity = True
