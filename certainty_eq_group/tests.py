from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (pages.Instruction)
        yield (pages.Decision, {'ce': (5 - self.subsession.round_number)*30 + self.player.id_in_group*10})
        if self.subsession.round_number == Constants.num_rounds:
            if Constants.results:
                yield (pages.Results)
            else:
                yield (pages.Pausepage)
