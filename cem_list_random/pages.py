from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _
import random
from random import randrange

# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    round_number = self.subsession.round_number
    player_id = self.player.id_in_group
    return {
        'endowment': c(Constants.endowment),
        'lottery_lo':  c(Constants.lottery_lo[round_number-1]),
        'lottery_hi':  c(Constants.lottery_hi[round_number-1]),
        'probability': "{0:.1f}".format(Constants.probability[round_number-1]) + "%",
        'weight':   "{0:.1f}".format(Constants.weights[player_id - 1]*100) + "%"
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # pass the values of weights to template
    # ----------------------------------------------------------------------------------------------------------------
    # def vars_for_template(self):
    #     weight = Constants.weights[self.player.id_in_group - 1]
    #     return weight
    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form model
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    def get_form_fields(self):
        round_number = self.subsession.round_number
        # unzip list of form_fields from <cem_choices> list
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices'][round_number-1])][1]

        # provide form field associated with pagination or full list
        # if Constants.one_choice_per_page:
        #     page = self.subsession.round_number
        #     return [form_fields[page - 1]]
        # else:
        return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # specify info for progress bar
        total = Constants.num_rounds
        round_number = self.subsession.round_number
        progress = round_number / total * 100

        # if Constants.one_choice_per_page:
        #     return {
        #         'page':      page,
        #         'total':     total,
        #         'progress':  progress,
        #         'choices':   [self.player.participant.vars['cem_choices'][page-1]]
        #     }
        # else:
        return {
                'choices':   self.player.participant.vars['cem_choices'][round_number-1]
            }

    # set payoff, determine consistency, and set switching row
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):

        # unzip indices and form fields from <cem_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices'][round_number-1])][1]
        indices = [list(t) for t in zip(*self.participant.vars['cem_choices'][round_number-1])][0]
        # index = indices[round_number - 1]


        #-------------------------------------------------------------------------------------------------

        # replace choices in <choices_made>
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(self.player, choice)
            self.participant.vars['cem_choices_made'][round_number-1][j - 1] = choice_i

        # set payoff
        # self.player.set_payoffs(round_number)
        # determine consistency
        self.player.set_consistency(round_number)
        # set switching row
        self.player.set_switching_row(round_number)


# ******************************************************************************************************************** #
# *** PAGE WAIT *** #
# ******************************************************************************************************************** #


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_group_payoffs()

# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #


class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # display results after the final round
        return self.subsession.round_number == Constants.num_rounds

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # retrieve random selected list number from group class
        rand_num = self.player.group.random_list
        id_self = self.player.id_in_group
        id_other1 = self.player.get_others_in_group()[0].id_in_group
        id_other2 = self.player.get_others_in_group()[1].id_in_group

        # payoff information

        row_to_pay = self.player.group.choice_to_pay
        choice_to_pay = self.participant.vars['cem_choices'][rand_num - 1][row_to_pay - 1]
        option_to_pay_p = self.participant.vars['cem_choices_made'][rand_num - 1][row_to_pay - 1]
        option_to_pay_p1 = self.player.get_others_in_group()[0].participant.vars['cem_choices_made'][rand_num - 1][row_to_pay - 1]
        option_to_pay_p2 = self.player.get_others_in_group()[1].participant.vars['cem_choices_made'][rand_num - 1][row_to_pay - 1]
        if Constants.combined_use:
            self.participant.payoff = self.participant.vars['cem_payoff_part1p'] + self.participant.vars['cem_payoff']
            return {
                'list_to_pay_part1': self.participant.vars['cem_random_list_part1p'],
                'choice_to_pay_part1': self.participant.vars['cem_choice_part1p'],
                'option_to_pay_part1': self.participant.vars['option_to_pay_part1p'],
                'list_to_pay': rand_num,
                'choice_to_pay': [choice_to_pay],
                'option_to_pay': self.player.group.option_to_pay,
                'option_to_pay_p': option_to_pay_p,
                # 'payoff':         self.player.payoff
                'payoff_part1': self.participant.vars['cem_payoff_part1p'],
                'payoff_part2': self.participant.vars['cem_payoff'],
                'payoff': self.participant.payoff
            }
        else:
            self.participant.payoff = self.participant.vars['cem_payoff']
            return {
                'list_to_pay': rand_num,
                'choice_to_pay': [choice_to_pay],
                'option_to_pay': self.player.group.option_to_pay,
                'id_self': id_self,
                'id_other1': id_other1,
                'id_other2': id_other2,
                'option_to_pay_p': option_to_pay_p,
                'option_to_pay_p1': option_to_pay_p1,
                'option_to_pay_p2': option_to_pay_p2,
                # 'payoff':         self.player.payoff
                'group_payoff': c(round((self.participant.vars['cem_payoff'] - Constants.endowment) * 3, 0)),
                'payoff_part2': self.participant.vars['cem_payoff'],
                'payoff': self.participant.payoff
            }





# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision,
                 ResultsWaitPage]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
