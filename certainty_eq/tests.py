from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (pages.Instruction)
        yield (pages.Decision, {'ce': 30})
        if self.subsession.round_number == Constants.num_rounds:
            if Constants.results:
                yield (pages.Results)
            else:
                yield (pages.Pausepage)

