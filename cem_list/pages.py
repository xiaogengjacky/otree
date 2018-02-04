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
    return {
        'lottery_lo':  c(Constants.lottery_lo[round_number-1]),
        'lottery_hi':  c(Constants.lottery_hi[round_number-1]),
        'probability': "{0:.1f}".format(Constants.probability[round_number-1]) + "%"
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

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
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices_part1'][round_number-1])][1]

        return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # specify info for progress bar
        total = Constants.num_rounds
        round_number = self.subsession.round_number
        progress = round_number / total * 100


        return {
                'choices':   self.player.participant.vars['cem_choices_part1'][round_number-1]
            }

    # set payoff, determine consistency, and set switching row
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):

        # unzip indices and form fields from <cem_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices_part1'][round_number-1])][1]
        indices = [list(t) for t in zip(*self.participant.vars['cem_choices_part1'][round_number-1])][0]
        # index = indices[round_number - 1]



        # if choices are displayed in tabular format
        # ------------------------------------------------------------------------------------------------------------

        # replace choices in <choices_made>
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(self.player, choice)
            self.participant.vars['cem_choices_made_part1'][round_number-1][j - 1] = choice_i

        # set payoff
        self.player.set_payoffs(round_number)
        # determine consistency
        self.player.set_consistency(round_number)
        # set switching row
        self.player.set_switching_row(round_number)

        # if the result page is not displayed and it is in the last round, need to calculate payoff info.

        if not Constants.results and round_number == Constants.num_rounds:
            rand_num = randrange(1, Constants.num_rounds + 1)
            # unzip <cem_choices> into list of lists
            choices = [list(t) for t in zip(*self.participant.vars['cem_choices_part1'][rand_num - 1])]
            indices = choices[0]

            # payoff information
            index_to_pay = self.player.participant.vars['cem_index_to_pay_part1'][rand_num - 1]
            row_to_pay = indices.index(index_to_pay) + 1
            choice_to_pay = self.participant.vars['cem_choices_part1'][rand_num - 1][row_to_pay - 1]

            # pass to the next app
            self.participant.vars['cem_random_list_part1p'] = rand_num
            self.participant.vars['cem_choice_part1p'] = [choice_to_pay]
            self.participant.vars['option_to_pay_part1p'] = self.participant.vars['option_to_pay'][rand_num - 1]
            self.participant.vars['cem_payoff_part1p'] = self.participant.vars['cem_payoff_part1'][rand_num - 1]
            # pass to the webpage
            self.participant.payoff = self.participant.vars['cem_payoff_part1'][rand_num - 1]

# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # round_num = self.subsession.round_number
        rand_num = randrange(1, Constants.num_rounds + 1)
        # unzip <cem_choices> into list of lists
        choices = [list(t) for t in zip(*self.participant.vars['cem_choices_part1'][rand_num-1])]
        indices = choices[0]

        # payoff information
        index_to_pay = self.player.participant.vars['cem_index_to_pay_part1'][rand_num-1]
        row_to_pay = indices.index(index_to_pay) + 1
        choice_to_pay = self.participant.vars['cem_choices_part1'][rand_num-1][row_to_pay - 1]

        # pass to the next app
        self.participant.vars['cem_random_list_part1p'] = rand_num
        self.participant.vars['cem_choice_part1p'] = [choice_to_pay]
        self.participant.vars['option_to_pay_part1p'] = self.participant.vars['option_to_pay'][rand_num - 1]
        self.participant.vars['cem_payoff_part1p'] = self.participant.vars['cem_payoff_part1'][rand_num - 1]
        # pass to the webpage
        self.participant.payoff = self.participant.vars['cem_payoff_part1'][rand_num - 1]
        return {
            'list_to_pay':    rand_num,
            'choice_to_pay':  [choice_to_pay],
            'option_to_pay':  self.participant.vars['option_to_pay'][rand_num - 1],
            'payoff':         self.participant.vars['cem_payoff_part1'][rand_num - 1],
        }




# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
