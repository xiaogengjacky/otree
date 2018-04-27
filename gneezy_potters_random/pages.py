from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _
import random
from random import random
from random import randrange

def vars_for_all_templates(self):
    round_number = self.subsession.round_number
    within_id = self.player.id_in_group
    weight = round(Constants.weight[within_id - 1], 2)
    return{
        'group_size': Constants.players_per_group,
        'within_id': within_id,
        'weight': weight,
        'endowment': c(Constants.endowment[round_number - 1]),
        'probability': round(Constants.probability[round_number - 1], 2),
        'return': round(Constants.multiplier[round_number - 1] - 1, 2)
    }
# --------------------------------------------------------------------------------------------------------------------


class Instruction(Page):
    # Only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1
# --------------------------------------------------------------------------------------------------------------------


class Investment(Page):
    form_model = 'player'
    form_fields = ['investment']

    timeout_submission = {'investment': c(0)}

    def investment_max(self):
        return Constants.endowment[self.subsession.round_number - 1]

    def before_next_page(self):
        round_num = self.subsession.round_number
        self.player.set_participant_investment(round_num)

    # def vars_for_template(self):
    #     round_number = self.subsession.round_number
    #     return{
    #         'endowment': c(self.player.participant.vars['environment'][round_number - 1][1]),
    #         'probability': self.player.participant.vars['environment'][round_number - 1][2],
    #         'return': self.player.participant.vars['environment'][round_number - 1][3] - 1
    #     }

# --------------------------------------------------------------------------------------------------------------------


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return True

    def after_all_players_arrive(self):
        self.group.set_group_payoffs(self.subsession.round_number)

# --------------------------------------------------------------------------------------------------------------------
class Ceresults(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        rand_round = self.participant.vars['rand_round']
        choices = self.participant.vars['ce_environment'][rand_round - 1]
        endowment = choices[1]
        high = choices[2]
        low = choices[3]
        probability = choices[4]

        if self.participant.vars['ce_outcomes'][rand_round - 1][4] == 1:
            outcome = c(high)
        else:
            outcome = c(low)

        if self.participant.vars['ce_outcomes'][rand_round - 1][2] > \
                self.participant.vars['ce_outcomes'][rand_round - 1][0]:
            receive = "the sure amount"
        else:
            receive = "the lottery payout"

        if Constants.anonymous:
            return {
                'round_to_pay': rand_round,
                'id_self': self.participant.vars['result_info'][0],
                'id_other1': self.participant.vars['result_info'][1],
                'id_other2': self.participant.vars['result_info'][2],
                'ce_p': self.participant.vars['result_info'][3],
                'ce_p1': "unrevealed amount",
                'ce_p2': "unrevealed amount",
                'high': c(high),
                'low': c(low),
                'group_ce': self.participant.vars['ce_outcomes'][rand_round - 1][0],
                'chosen_endowment': c(endowment),
                'chosen_probability': format(probability, ",.0%"),
                'rnd_bdm': format(self.participant.vars['ce_outcomes'][rand_round - 1][2], ",.2f"),
                'group_payoff': c(round(self.participant.vars['result_info'][6], 0)),
                'outcome': outcome,
                'receive': receive,
                'payoff': self.participant.vars['ce_outcomes'][rand_round - 1][3],
                'final_payoff': self.participant.vars['ce_outcomes'][rand_round - 1][5],
                'selection': self.participant.vars['result_info'][7]
            }
        else:
            return {
                'round_to_pay': rand_round,
                'id_self': self.participant.vars['result_info'][0],
                'id_other1': self.participant.vars['result_info'][1],
                'id_other2': self.participant.vars['result_info'][2],
                'ce_p': self.participant.vars['result_info'][3],
                'ce_p1': self.participant.vars['result_info'][4],
                'ce_p2': self.participant.vars['result_info'][5],
                'high': c(high),
                'low': c(low),
                'group_ce': self.participant.vars['ce_outcomes'][rand_round - 1][0],
                'chosen_endowment': c(endowment),
                'chosen_probability': format(probability, ",.0%"),
                'rnd_bdm': format(self.participant.vars['ce_outcomes'][rand_round - 1][2], ",.2f"),
                'group_payoff': c(round(self.participant.vars['result_info'][6], 0)),
                'outcome': outcome,
                'receive': receive,
                'payoff': self.participant.vars['ce_outcomes'][rand_round - 1][3],
                'final_payoff': self.participant.vars['ce_outcomes'][rand_round - 1][5],
                'selection': self.participant.vars['result_info'][7]
            }
#     ----------------------------------------------------------------------------------------------------------------


class Results(Page):

    # skip results until last page
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    def vars_for_template(self):

        rand_num = self.player.subsession.random_round
        selection = self.player.group.selection
        id_self = self.player.id_in_group
        id_other1 = self.player.get_others_in_group()[0].id_in_group
        id_other2 = self.player.get_others_in_group()[1].id_in_group
        investment_p = self.player.participant.vars['investment'][rand_num - 1]
        investment_p1 = self.player.get_others_in_group()[0].participant.vars['investment'][rand_num - 1]
        investment_p2 = self.player.get_others_in_group()[1].participant.vars['investment'][rand_num - 1]
        # unzip <cem_choices> into list of lists
        choices = self.participant.vars['environment'][rand_num - 1]
        endowment = choices[1]
        probability = choices[2]
        return_rate = choices[3] - 1

        if self.player.group.winner == 1:
            outcome = "successful"
        else:
            outcome = "unsuccessful"

        if Constants.combined:
            self.participant.payoff = self.participant.vars['payoff'] + \
                                      self.participant.vars['ce_outcomes'][self.participant.vars['rand_round'] - 1][5]
        else:
            self.participant.payoff = self.participant.vars['payoff']

        if Constants.anonymous:
            return {
                'round_to_pay': rand_num,
                'id_self': id_self,
                'id_other1': id_other1,
                'id_other2': id_other2,
                'investment_p': investment_p,
                'investment_p1': "unrevealed amount",
                'investment_p2': "unrevealed amount",
                'group_investment': self.player.group.investment,
                'chosen_endowment': c(endowment),
                'chosen_probability': round(probability, 2),
                'chosen_return': round(return_rate, 2),
                'chosen_member': selection,
                'group_payoff': c(round(self.participant.vars['payoff'] * 3, 2)),
                'outcome': outcome,
                'payoff': self.participant.vars['payoff']
            }
        else:
            return {
                'round_to_pay': rand_num,
                'id_self': id_self,
                'id_other1': id_other1,
                'id_other2': id_other2,
                'investment_p': investment_p,
                'investment_p1': investment_p1,
                'investment_p2': investment_p2,
                'group_investment': self.player.group.investment,
                'chosen_endowment': c(endowment),
                'chosen_probability': round(probability, 2),
                'chosen_return': round(return_rate, 2),
                'chosen_member': selection,
                'group_payoff': c(round(self.participant.vars['payoff']*3, 2)),
                'outcome': outcome,
                'payoff': self.participant.vars['payoff']
            }


page_sequence = [Instruction,
                 Investment,
                 ResultsWaitPage,
                 Results]

# if Constants.instruction:
#     page_sequence.insert(0, Instruction)

if Constants.combined:
    page_sequence.insert(3, Ceresults)

# if Constants.results:
#     page_sequence.append(Results)
